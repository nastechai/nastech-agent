#!/usr/bin/env python3
"""
Mirror open upstream PRs (NousResearch/hermes-agent) into isolated
upstream-pr-{NUMBER} branches on nastechai/nastech-agent.

Called by upstream-pr-mirror.yml workflow.
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GH_TOKEN = os.environ["GH_TOKEN"]
UPSTREAM = "NousResearch/hermes-agent"
ORIGIN   = "nastechai/nastech-agent"
SCRIPT_DIR = Path(__file__).parent


def gh(*args):
    env = {**os.environ, "GH_TOKEN": GH_TOKEN}
    r = subprocess.run(["gh"] + list(args), capture_output=True, text=True, env=env)
    return r.stdout.strip(), r.returncode


def run(*args, **kw):
    r = subprocess.run(list(args), capture_output=True, text=True, **kw)
    return r.stdout.strip(), r.returncode


def get_open_upstream_prs():
    out, rc = gh(
        "api", f"repos/{UPSTREAM}/pulls",
        "--paginate",
        "--jq", "[.[] | {number:.number, title:.title, sha:.head.sha, body:.body}]",
    )
    if rc != 0:
        print(f"Could not fetch upstream PRs: {out}")
        return []
    return json.loads(out or "[]")


def get_mirrored_branch_numbers():
    out, _ = run("git", "ls-remote", "--heads", "origin", "upstream-pr-*")
    mirrored = set()
    for line in out.splitlines():
        ref = line.split("\t")[-1].replace("refs/heads/", "")
        if ref.startswith("upstream-pr-"):
            try:
                mirrored.add(int(ref.replace("upstream-pr-", "")))
            except ValueError:
                pass
    return mirrored


def archive_sha(sha):
    """Try to git-archive a SHA; fetch the PR ref if not locally available."""
    r = subprocess.run(["git", "archive", sha], capture_output=True)
    if r.returncode == 0:
        return r.stdout
    # Try fetching the PR ref
    run("git", "fetch", "upstream", f"pull/{sha}/head:tmp-fetch-{sha[:8]}")
    r = subprocess.run(["git", "archive", sha], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def mirror_pr(pr):
    num   = pr["number"]
    title = pr["title"]
    sha   = pr["sha"]
    body  = pr.get("body") or ""
    branch = f"upstream-pr-{num}"

    print(f"\n-> Mirroring upstream PR #{num}: {title[:70]}")

    work = tempfile.mkdtemp()
    try:
        # Try fetching the specific PR ref
        run("git", "fetch", "upstream", f"pull/{num}/head:{branch}-tmp")
        local_sha, rc = run("git", "rev-parse", f"{branch}-tmp")
        if rc == 0:
            sha = local_sha

        tar_data = archive_sha(sha)
        if tar_data is None:
            print(f"  Could not archive SHA {sha[:8]} — skipping")
            return False

        tar_path = Path(work) / "tree.tar"
        tar_path.write_bytes(tar_data)
        subprocess.run(["tar", "-x", "-C", work, "-f", str(tar_path)], check=True)
        tar_path.unlink()

        # Apply nastechai rebranding
        rebrand = SCRIPT_DIR / "rebrand.py"
        subprocess.run([sys.executable, str(rebrand), work], check=True, capture_output=True)

        # Create isolated branch from origin/main
        run("git", "fetch", "origin", "main")
        run("git", "branch", "-D", branch)
        _, rc_b = run("git", "checkout", "-b", branch, "origin/main")
        if rc_b != 0:
            print(f"  Could not create branch {branch} — skipping")
            return False

        # Replace tree with rebranded upstream PR content
        subprocess.run(
            "git ls-files -z | xargs -0 -r git rm -f --quiet",
            shell=True, capture_output=True,
        )
        for item in Path(work).iterdir():
            dest = Path(".") / item.name
            if dest.exists():
                shutil.rmtree(dest) if dest.is_dir() else dest.unlink()
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

        # Restore nastechai-specific overrides
        protected = [
            ".github/workflows/ci.yml",
            ".github/workflows/typecheck.yml",
            ".github/workflows/upload_to_pypi.yml",
            ".github/workflows/contributor-check.yml",
            ".github/workflows/upstream-sync.yml",
            ".github/workflows/upstream-pr-mirror.yml",
            ".github/workflows/brand-validation.yml",
            ".github/workflows/bot-health-check.yml",
            ".github/scripts/rebrand.py",
            ".github/scripts/mirror_prs.py",
            ".github/scripts/close_stale_mirrors.py",
            ".github/scripts/brand_validate.py",
            ".npmrc",
            "scripts/release.py",
        ]
        for f in protected:
            content, rc3 = run("git", "show", f"origin/main:{f}")
            if rc3 == 0:
                p = Path(f)
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(content)

        run("git", "add", "-A")
        short = sha[:8]
        msg = (
            f"mirror: upstream hermes-agent PR #{num} @ {short}\n\n"
            f"Upstream PR: https://github.com/{UPSTREAM}/pull/{num}\n"
            f"Title: {title}\n"
            f"SHA: {sha}\n\n"
            f"nastechai rebranding applied.\n"
            f"Do NOT merge without review.\n"
            f"Auto-generated by upstream-pr-mirror workflow."
        )
        run("git", "commit", "-m", msg)

        _, rc_push = run("git", "push", "origin", branch, "--force")
        if rc_push != 0:
            print(f"  Push failed for {branch}")
            run("git", "checkout", "main")
            return False

        pr_body = (
            f"## Mirror of upstream PR #{num}\n\n"
            f"> **Do NOT merge without review.** "
            f"This is an isolated mirror — never auto-merged.\n\n"
            f"| | |\n|---|---|\n"
            f"| **Upstream PR** | https://github.com/{UPSTREAM}/pull/{num} |\n"
            f"| **Title** | {title} |\n"
            f"| **SHA** | `{sha}` |\n\n"
            f"### Review checklist\n"
            f"- [ ] CI passes on this branch\n"
            f"- [ ] Brand validation passes (no hermes/NousResearch leakage)\n"
            f"- [ ] Change is desirable for nastechai\n\n"
            f"---\n\n"
            f"{body[:3000]}\n\n"
            f"---\n"
            f"> Auto-mirrored by upstream-pr-mirror workflow with nastechai rebranding applied."
        )
        _, rc_pr = gh(
            "pr", "create",
            "--repo", ORIGIN,
            "--head", branch,
            "--base", "main",
            "--title", f"[upstream-pr-{num}] {title}",
            "--body", pr_body,
        )
        if rc_pr == 0:
            print(f"  Created branch {branch} and opened PR")
        else:
            print(f"  Branch {branch} pushed. PR creation may have failed (duplicate or permission).")
        return True

    except Exception as e:
        print(f"  Error mirroring PR #{num}: {e}")
        return False
    finally:
        shutil.rmtree(work, ignore_errors=True)
        run("git", "checkout", "main")


def main():
    upstream_prs = get_open_upstream_prs()
    print(f"Open upstream PRs: {len(upstream_prs)}")

    mirrored = get_mirrored_branch_numbers()
    print(f"Already mirrored: {sorted(mirrored)}")

    new_count = 0
    for pr in upstream_prs:
        if pr["number"] not in mirrored:
            if mirror_pr(pr):
                new_count += 1

    print(f"\nDone. New upstream PRs mirrored: {new_count}")


if __name__ == "__main__":
    main()
