#!/usr/bin/env python3
"""
hermes_sync.py — Automated Hermes → Nastech parity sync bot.

Pulls commits from NousResearch/hermes-agent that are not yet in
nastechai/nastech-agent, applies Nastech branding to every touched file and
the commit message, then pushes a branch and opens a GitHub PR.

Usage
-----
    # Sync everything since the saved state (or all commits on first run)
    python scripts/hermes_sync.py

    # Force-start from a specific hermes SHA (exclusive lower bound)
    python scripts/hermes_sync.py --since abc123

    # Full tree sync: brand entire hermes tree and commit as one squash
    python scripts/hermes_sync.py --full

    # Preview without writing anything
    python scripts/hermes_sync.py --dry-run

    # Custom PR branch
    python scripts/hermes_sync.py --branch hermes-sync-2026-07

Environment
-----------
    GITHUB_PERSONAL_ACCESS_TOKEN   GitHub PAT with repo + PR permissions
    GITHUB_TOKEN                   Fallback (GitHub Actions default token)
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

# ── Insert scripts/ on sys.path so `import brand` works regardless of cwd ──
_SCRIPTS_DIR = Path(__file__).resolve().parent
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from brand import (  # noqa: E402
    apply_branding,
    brand_commit_message,
    brand_file_content,
    brand_path,
)

# ── Constants ─────────────────────────────────────────────────────────────────
HERMES_REMOTE_NAME = "_hermes_upstream"
HERMES_REMOTE_URL  = "https://github.com/NousResearch/hermes-agent.git"
NASTECH_REPO       = "nastechai/nastech-agent"
SYNC_STATE_FILE    = ".hermes-sync-state"
DEFAULT_BRANCH     = "hermes-sync-auto"
MAX_COMMITS_PER_PR = 200   # hard cap to keep PRs reviewable


# ── Git helpers ───────────────────────────────────────────────────────────────

def run(cmd: list[str], capture: bool = True, check: bool = True, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=capture, text=True, check=check, **kw)


def git(*args: str, check: bool = True, capture: bool = True) -> str:
    result = run(["git", *args], check=check, capture=capture)
    return result.stdout.strip()


def git_ok(*args: str) -> bool:
    """Return True if the git command exits 0."""
    return run(["git", *args], check=False).returncode == 0


# ── GitHub API ────────────────────────────────────────────────────────────────

def _token() -> str:
    t = (os.environ.get("GITHUB_PERSONAL_ACCESS_TOKEN") or
         os.environ.get("GITHUB_TOKEN") or "")
    if not t:
        sys.exit("ERROR: set GITHUB_PERSONAL_ACCESS_TOKEN or GITHUB_TOKEN")
    return t


def gh_api(method: str, path: str, data: dict | None = None) -> dict:
    token = _token()
    url = f"https://api.github.com{path}"
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(
        url, data=body, method=method,
        headers={
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as exc:
        body_text = exc.read().decode()
        raise RuntimeError(f"GitHub API {method} {path} → {exc.code}: {body_text}") from exc


# ── Remote management ─────────────────────────────────────────────────────────

def ensure_hermes_remote() -> None:
    try:
        git("remote", "get-url", HERMES_REMOTE_NAME)
    except subprocess.CalledProcessError:
        git("remote", "add", HERMES_REMOTE_NAME, HERMES_REMOTE_URL)
    print(f"  Fetching {HERMES_REMOTE_URL} …")
    git("fetch", HERMES_REMOTE_NAME, "--no-tags", "--quiet")


# ── State file ────────────────────────────────────────────────────────────────

def read_state() -> dict:
    p = Path(SYNC_STATE_FILE)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text())
    except Exception:
        # Legacy plain-text SHA format
        sha = p.read_text().strip()
        return {"last_hermes_sha": sha} if sha else {}


def write_state(sha: str) -> None:
    state = {
        "last_hermes_sha": sha,
        "synced_at": datetime.datetime.utcnow().isoformat() + "Z",
    }
    Path(SYNC_STATE_FILE).write_text(json.dumps(state, indent=2) + "\n")


# ── Commit enumeration ────────────────────────────────────────────────────────

def list_new_commits(since_sha: str | None) -> list[tuple[str, str]]:
    """Return [(sha, subject), …] for hermes commits after *since_sha* (oldest first)."""
    if since_sha:
        log = git("log", "--oneline", "--reverse", "--format=%H %s",
                  f"{since_sha}..{HERMES_REMOTE_NAME}/main")
    else:
        log = git("log", "--oneline", "--reverse", "--format=%H %s",
                  f"{HERMES_REMOTE_NAME}/main")
    if not log:
        return []
    result = []
    for line in log.splitlines():
        sha, _, subj = line.partition(" ")
        result.append((sha, subj))
    return result


# ── File-level application ────────────────────────────────────────────────────

def _hermes_file_bytes(sha: str, hermes_path: str) -> bytes | None:
    """Return raw bytes of *hermes_path* at commit *sha*, or None on error."""
    result = run(["git", "cat-file", "blob", f"{sha}:{hermes_path}"], check=False)
    if result.returncode != 0:
        return None
    return result.stdout.encode("utf-8", errors="surrogateescape")


def _apply_file(sha: str, hermes_path: str) -> str:
    """
    Brand *hermes_path* from commit *sha* and write it to the working tree.

    Returns the nastech path that was written (for staging).
    """
    raw = _hermes_file_bytes(sha, hermes_path)
    if raw is None:
        return ""
    nastech_path = brand_path(hermes_path)
    out = Path(nastech_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    branded = brand_file_content(out, raw)
    out.write_bytes(branded)
    return nastech_path


def _delete_file(hermes_path: str) -> str:
    """Delete the nastech equivalent of *hermes_path* from the working tree."""
    nastech_path = brand_path(hermes_path)
    p = Path(nastech_path)
    if p.exists():
        p.unlink()
    return nastech_path


def apply_hermes_commit(sha: str) -> tuple[list[str], list[str]]:
    """
    Apply a single hermes commit to the working tree with branding.

    Returns (added_or_modified_paths, deleted_paths) — both as nastech paths.
    """
    diff = git("diff-tree", "--no-commit-id", "-r", "--name-status", "-z", sha)
    # -z separates fields with NUL and records with NUL
    # Format per record: STATUS\0path  (for simple) or STATUS score\0old\0new (rename/copy)
    tokens = diff.split("\0") if diff else []

    added: list[str] = []
    deleted: list[str] = []

    i = 0
    while i < len(tokens):
        tok = tokens[i].strip()
        if not tok:
            i += 1
            continue

        status = tok[0]  # A M D R C T

        if status in ("A", "M", "T"):  # added / modified / type-changed
            hermes_path = tokens[i + 1] if i + 1 < len(tokens) else ""
            i += 2
            if hermes_path:
                p = _apply_file(sha, hermes_path)
                if p:
                    added.append(p)

        elif status == "D":  # deleted
            hermes_path = tokens[i + 1] if i + 1 < len(tokens) else ""
            i += 2
            if hermes_path:
                p = _delete_file(hermes_path)
                deleted.append(p)

        elif status in ("R", "C"):  # renamed / copied
            old_path = tokens[i + 1] if i + 1 < len(tokens) else ""
            new_path = tokens[i + 2] if i + 2 < len(tokens) else ""
            i += 3
            if status == "R" and old_path:
                _delete_file(old_path)
                deleted.append(brand_path(old_path))
            if new_path:
                p = _apply_file(sha, new_path)
                if p:
                    added.append(p)

        else:
            i += 1

    return added, deleted


# ── Full-tree sync ────────────────────────────────────────────────────────────

def full_tree_sync(dry_run: bool = False) -> int:
    """
    Brand the ENTIRE hermes/main tree and apply it to the working tree.

    This is used for the initial catch-up run.  It produces a single squash
    commit titled "chore: full Hermes→Nastech tree sync".

    Returns the number of files touched.
    """
    print("  Running full-tree sync from hermes/main …")
    ls = git("ls-tree", "-r", "--name-only", f"{HERMES_REMOTE_NAME}/main")
    files = [f for f in ls.splitlines() if f]

    touched = 0
    for hermes_path in files:
        nastech_path = brand_path(hermes_path)
        raw = _hermes_file_bytes(f"{HERMES_REMOTE_NAME}/main", hermes_path)
        if raw is None:
            continue
        out = Path(nastech_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        branded = brand_file_content(out, raw)
        if not dry_run:
            out.write_bytes(branded)
        touched += 1

    return touched


# ── Per-commit sync loop ──────────────────────────────────────────────────────

def sync_commits(
    commits: list[tuple[str, str]],
    dry_run: bool = False,
) -> tuple[list[str], list[str]]:
    """
    Apply each commit in *commits* to the working tree with branding.

    Returns (synced_shas, skipped_shas).
    """
    synced: list[str] = []
    skipped: list[str] = []

    for sha, subj in commits:
        print(f"  [{sha[:9]}] {subj[:72]}")
        try:
            added, deleted = apply_hermes_commit(sha)
        except Exception as exc:
            print(f"    ⚠ error applying {sha[:9]}: {exc}")
            skipped.append(sha)
            continue

        if not added and not deleted:
            # Empty commit — still record it so state advances
            synced.append(sha)
            continue

        if dry_run:
            synced.append(sha)
            continue

        # Stage
        if added:
            run(["git", "add", "--"] + added, check=False)
        if deleted:
            for p in deleted:
                git_ok("rm", "--ignore-unmatch", "--quiet", "--", p)

        # Commit
        branded_msg = brand_commit_message(f"{subj}\n\n(cherry-picked from hermes {sha[:12]})")
        try:
            git("commit", "--allow-empty", "-m", branded_msg)
            synced.append(sha)
        except subprocess.CalledProcessError as exc:
            print(f"    ⚠ commit failed for {sha[:9]}: {exc.stderr}")
            # Reset staging area and continue
            git_ok("reset", "HEAD", "--quiet")
            skipped.append(sha)

    return synced, skipped


# ── PR creation ───────────────────────────────────────────────────────────────

def create_pr(branch: str, base: str, synced: list[str], skipped: list[str], full: bool) -> str:
    count = len(synced)
    title = f"chore(sync): Hermes → Nastech — {count} commit(s)"
    if full:
        title = "chore(sync): full Hermes → Nastech tree parity"

    lines = [
        "## Hermes → Nastech automated sync",
        "",
        f"Synced **{count}** commit(s) from "
        f"[NousResearch/hermes-agent](https://github.com/NousResearch/hermes-agent) "
        f"with Nastechai branding applied.",
        "",
    ]
    if full:
        lines += [
            "### Mode: full tree sync",
            "All files from `hermes/main` were branded and written as a single squash commit.",
            "",
        ]
    if synced:
        lines += ["### Synced commits", "```"]
        for s in synced[:40]:
            lines.append(s[:12])
        if len(synced) > 40:
            lines.append(f"… and {len(synced) - 40} more")
        lines += ["```", ""]
    if skipped:
        lines += [
            f"### ⚠️ {len(skipped)} commit(s) skipped (apply errors — manual review needed)",
            "```",
        ]
        for s in skipped[:20]:
            lines.append(s[:12])
        lines += ["```", ""]
    lines += [
        "---",
        "*Generated by `scripts/hermes_sync.py`.*",
    ]

    body = "\n".join(lines)
    result = gh_api("POST", f"/repos/{NASTECH_REPO}/pulls", {
        "title": title,
        "body": body,
        "head": branch,
        "base": base,
    })
    return result["html_url"]


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--since",    metavar="SHA",
                    help="Hermes SHA to start from (exclusive). Overrides saved state.")
    ap.add_argument("--full",     action="store_true",
                    help="Full-tree sync: brand the entire hermes/main tree as one commit.")
    ap.add_argument("--dry-run",  action="store_true",
                    help="Show what would happen without writing anything.")
    ap.add_argument("--branch",   default=DEFAULT_BRANCH,
                    help=f"Branch to push (default: {DEFAULT_BRANCH})")
    ap.add_argument("--base",     default="main",
                    help="PR target branch (default: main)")
    ap.add_argument("--no-pr",    action="store_true",
                    help="Push but do not open a PR.")
    ap.add_argument("--max",      type=int, default=MAX_COMMITS_PER_PR,
                    help=f"Max commits per run (default: {MAX_COMMITS_PER_PR})")
    args = ap.parse_args()

    # ── Setup git identity & auth ──────────────────────────────────────────────
    token = _token()
    git("config", "user.email", "bot@nastechai.com")
    git("config", "user.name", "Nastech Sync Bot")
    remote_url = f"https://x-access-token:{token}@github.com/{NASTECH_REPO}.git"
    git("remote", "set-url", "origin", remote_url)

    # ── Fetch hermes ───────────────────────────────────────────────────────────
    ensure_hermes_remote()

    hermes_head = git("rev-parse", f"{HERMES_REMOTE_NAME}/main")
    print(f"  hermes/main HEAD: {hermes_head[:12]}")

    # ── Create / reset sync branch ─────────────────────────────────────────────
    git("checkout", "-B", args.branch)

    synced_shas: list[str] = []
    skipped_shas: list[str] = []

    if args.full:
        # ── Full-tree mode ─────────────────────────────────────────────────────
        touched = full_tree_sync(dry_run=args.dry_run)
        print(f"  Touched {touched} files.")
        if not args.dry_run:
            git("add", "-A")
            git("commit", "--allow-empty",
                "-m", "chore(sync): full Hermes→Nastech tree parity\n\n"
                      f"Branded {touched} files from {HERMES_REMOTE_URL}\n"
                      f"hermes HEAD: {hermes_head[:12]}")
            synced_shas = [hermes_head]
    else:
        # ── Incremental commit-by-commit mode ──────────────────────────────────
        state = read_state()
        since = args.since or state.get("last_hermes_sha")
        print(f"  Syncing from: {since[:12] if since else '(beginning)'}")

        commits = list_new_commits(since)
        if not commits:
            print("  Nothing new to sync. Exiting.")
            # Restore remote URL to public (no token)
            git("remote", "set-url", "origin",
                f"https://github.com/{NASTECH_REPO}.git")
            return

        if len(commits) > args.max:
            print(f"  Capping at {args.max} commits (of {len(commits)} available).")
            commits = commits[:args.max]

        print(f"  Applying {len(commits)} commit(s) …")
        synced_shas, skipped_shas = sync_commits(commits, dry_run=args.dry_run)

    if not synced_shas:
        print("  No commits successfully synced. Nothing to push.")
        git("remote", "set-url", "origin", f"https://github.com/{NASTECH_REPO}.git")
        return

    # ── Update state file & commit it ─────────────────────────────────────────
    if not args.dry_run:
        write_state(hermes_head)
        git("add", SYNC_STATE_FILE)
        git("commit", "--allow-empty",
            "-m", f"chore(sync): update hermes sync state → {hermes_head[:12]}")

        # ── Push ──────────────────────────────────────────────────────────────
        print(f"\n  Pushing branch {args.branch!r} …")
        git("push", "-f", "origin", f"{args.branch}:{args.branch}")

        # ── Open PR ───────────────────────────────────────────────────────────
        if not args.no_pr:
            try:
                url = create_pr(args.branch, args.base, synced_shas, skipped_shas, args.full)
                print(f"\n  ✅  PR: {url}")
            except RuntimeError as exc:
                err = str(exc)
                if "already exists" in err.lower() or "A pull request already exists" in err:
                    print("  ℹ  PR already exists for this branch.")
                else:
                    print(f"  ⚠  PR creation failed: {exc}")
    else:
        print(f"\n  Dry-run complete. Would push {len(synced_shas)} commit(s).")

    # ── Restore public remote URL (strip token) ────────────────────────────────
    git("remote", "set-url", "origin", f"https://github.com/{NASTECH_REPO}.git")

    print(f"\n  synced={len(synced_shas)}  skipped={len(skipped_shas)}")


if __name__ == "__main__":
    main()
