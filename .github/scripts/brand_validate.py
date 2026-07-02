#!/usr/bin/env python3
"""
Brand Validation Script
=======================
Two modes:

1. Default scan (--strict / no flag):
   Walks the current working directory (the repo checkout) and reports any
   upstream strings that rebrand.py should have replaced.  Exits non-zero
   if violations are found and --strict is passed.

2. Ruleset completeness check (--check-ruleset --upstream-ref <ref>):
   Archives the upstream ref, runs rebrand.py against it, then scans the
   result to verify NO upstream strings remain.  Also checks whether any
   new upstream strings appear that rebrand.py does not yet handle.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# -----------------------------------------------------------------------
# Source of truth: the exact strings we must NEVER allow in nastechai code.
# These mirror TEXT_SUBS in rebrand.py (old values only).
# -----------------------------------------------------------------------
FORBIDDEN = [
    # Most specific first (same ordering discipline as rebrand.py)
    "NousResearch/hermes-agent",
    "@nousresearch/",
    "Nous Research",
    "NousResearch",
    "nousresearch",
    "NOUSRESEARCH",
    "hermes-agent",
    "hermes_agent",
    "HERMES_AGENT",
    "Hermes Agent",
    "hermes agent",
    "HERMES_HOME",
    "HERMES_",
    "hermes_",
    "_hermes",
    "hermes-acp",
    "Hermes",
    "HERMES",
    "hermes",
]

# Files / directories to skip entirely during scans
SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    "dist", "build", ".mypy_cache", ".ruff_cache", ".pytest_cache",
    ".eggs",
}
SKIP_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".mp4", ".webm", ".mov", ".avi",
    ".zip", ".gz", ".tar", ".tgz", ".bz2", ".7z", ".xz",
    ".pyc", ".pyo", ".so", ".dylib", ".dll", ".exe",
    ".db", ".sqlite", ".sqlite3",
    ".lock",
    ".bin",
}

# These files are allowed to contain upstream strings because they
# intentionally reference upstream (e.g., the sync workflows themselves).
ALLOWLIST_PATHS = {
    ".github/workflows/upstream-sync.yml",
    ".github/workflows/upstream-pr-mirror.yml",
    ".github/workflows/brand-validation.yml",
    ".github/workflows/bot-health-check.yml",
    ".github/scripts/rebrand.py",
    ".github/scripts/brand_validate.py",
    ".github/scripts/mirror_prs.py",
    ".github/scripts/close_stale_mirrors.py",
}


def should_skip_path(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    parts = rel.parts
    if any(p in SKIP_DIRS or p.endswith(".egg-info") for p in parts):
        return True
    if str(rel) in ALLOWLIST_PATHS:
        return True
    return False


def scan_for_violations(root: Path, strict: bool, report_path: str | None) -> int:
    """Scan root for forbidden upstream strings. Returns violation count."""
    violations = []

    for filepath in root.rglob("*"):
        if not filepath.is_file():
            continue
        if should_skip_path(filepath, root):
            continue
        if filepath.suffix.lower() in SKIP_EXTENSIONS:
            continue

        try:
            text = filepath.read_text(encoding="utf-8", errors="replace")
        except (OSError, PermissionError):
            continue

        rel = str(filepath.relative_to(root))
        for pattern in FORBIDDEN:
            # Case-sensitive match
            idx = 0
            while True:
                pos = text.find(pattern, idx)
                if pos == -1:
                    break
                # Get the line number
                line_no = text[:pos].count("\n") + 1
                # Get the surrounding line for context
                line_start = text.rfind("\n", 0, pos) + 1
                line_end   = text.find("\n", pos)
                line_content = text[line_start:line_end if line_end != -1 else None].strip()
                violations.append({
                    "file": rel,
                    "line": line_no,
                    "pattern": pattern,
                    "context": line_content[:120],
                })
                idx = pos + len(pattern)

        # Also scan filename itself
        for pattern in FORBIDDEN:
            if pattern in filepath.name:
                violations.append({
                    "file": rel,
                    "line": 0,
                    "pattern": pattern,
                    "context": f"[FILENAME] {filepath.name}",
                })

    # Deduplicate by (file, line, pattern)
    seen = set()
    unique = []
    for v in violations:
        key = (v["file"], v["line"], v["pattern"])
        if key not in seen:
            seen.add(key)
            unique.append(v)

    unique.sort(key=lambda x: (x["file"], x["line"]))

    lines = []
    if unique:
        lines.append(f"BRAND VIOLATIONS FOUND: {len(unique)}")
        lines.append("=" * 60)
        for v in unique:
            loc = f"{v['file']}:{v['line']}" if v["line"] else v["file"]
            lines.append(f"  [{v['pattern']}]  {loc}")
            lines.append(f"    {v['context']}")
        lines.append("=" * 60)
        lines.append("Run .github/scripts/rebrand.py to fix these.")
    else:
        lines.append("Brand validation PASSED — no upstream strings found.")

    report_text = "\n".join(lines)
    print(report_text)

    if report_path:
        Path(report_path).write_text(report_text)

    if strict and unique:
        return len(unique)
    return 0


def check_ruleset_completeness(upstream_ref: str, report_path: str | None) -> int:
    """
    Archive upstream_ref, apply rebrand.py, check for residual upstream strings.
    Also checks whether upstream introduces new strings not in FORBIDDEN list.
    """
    rebrand_py = Path(__file__).parent / "rebrand.py"
    work = tempfile.mkdtemp()
    issues = []

    try:
        print(f"Archiving upstream ref: {upstream_ref}")
        r = subprocess.run(
            ["git", "archive", upstream_ref],
            capture_output=True,
        )
        if r.returncode != 0:
            print(f"Could not archive {upstream_ref}: {r.stderr.decode()[:200]}")
            return 1

        # Extract to work dir
        tar_path = Path(work) / "tree.tar"
        tar_path.write_bytes(r.stdout)
        subprocess.run(["tar", "-x", "-C", work, "-f", str(tar_path)], check=True)
        tar_path.unlink()

        root = Path(work)

        # --- Pass 1: scan BEFORE rebranding to find all upstream strings ---
        upstream_strings_found = set()
        for filepath in root.rglob("*"):
            if not filepath.is_file():
                continue
            if filepath.suffix.lower() in SKIP_EXTENSIONS:
                continue
            try:
                text = filepath.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for pattern in FORBIDDEN:
                if pattern in text:
                    upstream_strings_found.add(pattern)

        # Check for strings in upstream that are NOT in our FORBIDDEN list
        all_upstream_words = []
        for filepath in root.rglob("*"):
            if not filepath.is_file():
                continue
            if filepath.suffix.lower() in SKIP_EXTENSIONS:
                continue
            try:
                text = filepath.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            # Look for NousResearch / hermes / Hermes / HERMES in any form
            for match in re.finditer(
                r'\b(NousResearch|nousresearch|hermes|Hermes|HERMES|nous[_\-]?research)\b',
                text
            ):
                word = match.group(0)
                if word not in FORBIDDEN and word not in upstream_strings_found:
                    all_upstream_words.append(word)

        uncovered = sorted(set(all_upstream_words))
        if uncovered:
            issues.append(
                f"WARNING: Upstream contains strings not covered by rebrand.py FORBIDDEN list: "
                f"{uncovered[:20]}"
            )

        # --- Pass 2: apply rebrand.py ---
        print("Applying rebrand.py...")
        result = subprocess.run(
            [sys.executable, str(rebrand_py), str(root)],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            issues.append(f"rebrand.py exited with error: {result.stderr[:300]}")
            return 1

        # --- Pass 3: scan AFTER rebranding for residual upstream strings ---
        residual = []
        for filepath in root.rglob("*"):
            if not filepath.is_file():
                continue
            if filepath.suffix.lower() in SKIP_EXTENSIONS:
                continue
            try:
                text = filepath.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            rel = str(filepath.relative_to(root))
            for pattern in FORBIDDEN:
                if pattern in text:
                    line_no = text[:text.find(pattern)].count("\n") + 1
                    line_start = text.rfind("\n", 0, text.find(pattern)) + 1
                    line_end   = text.find("\n", text.find(pattern))
                    ctx = text[line_start:line_end if line_end != -1 else None].strip()[:100]
                    residual.append(f"  [{pattern}] {rel}:{line_no}  {ctx}")

            if pattern in filepath.name:
                residual.append(f"  [{pattern}] FILENAME: {rel}")

        lines = []
        lines.append(f"Ruleset completeness check — upstream: {upstream_ref}")
        lines.append(f"Upstream strings found before rebranding: {sorted(upstream_strings_found)}")
        lines.append("")

        if uncovered:
            lines.append(f"POSSIBLE GAPS in rebrand.py ({len(uncovered)} new patterns):")
            for u in uncovered[:30]:
                lines.append(f"  - {u!r}")
            lines.append("")

        if residual:
            lines.append(f"RESIDUAL UPSTREAM STRINGS after rebrand.py ({len(residual)}):")
            lines.extend(residual[:50])
            lines.append("")
            lines.append("ACTION: Update TEXT_SUBS or NAME_SUBS in rebrand.py to cover these.")
            issues.append(f"{len(residual)} residual strings after rebranding")
        else:
            lines.append("Rebranding is COMPLETE — no residual upstream strings found.")

        if issues:
            lines.append("\nISSUES DETECTED:")
            for issue in issues:
                lines.append(f"  - {issue}")

        report_text = "\n".join(lines)
        print(report_text)

        if report_path:
            Path(report_path).write_text(report_text)

        return 1 if (residual or uncovered) else 0

    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(description="Brand validation for nastechai/nastech-agent")
    parser.add_argument("--strict", action="store_true",
                        help="Exit non-zero on any violation (default for CI)")
    parser.add_argument("--report", metavar="FILE",
                        help="Write report to this file")
    parser.add_argument("--check-ruleset", action="store_true",
                        help="Check rebrand.py ruleset completeness vs upstream")
    parser.add_argument("--upstream-ref", default="upstream/main",
                        help="Git ref for upstream content (used with --check-ruleset)")
    args = parser.parse_args()

    if args.check_ruleset:
        rc = check_ruleset_completeness(args.upstream_ref, args.report)
    else:
        root = Path.cwd()
        rc = scan_for_violations(root, args.strict, args.report)

    sys.exit(rc)


if __name__ == "__main__":
    main()
