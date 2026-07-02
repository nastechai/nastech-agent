#!/usr/bin/env python3
"""
Rebranding script: NousResearch/hermes-agent -> nastechai/nastech-agent

Apply all nastechai branding substitutions to a directory tree.
Handles file content, filenames, and directory names.

Usage:
    python3 rebrand.py <directory>
"""

import os
import sys
from pathlib import Path

# Text substitutions (ORDER MATTERS - most specific first)
TEXT_SUBS = [
    # Specific GitHub repo URL - must be first (before generic NousResearch)
    ("NousResearch/hermes-agent",       "nastechai/nastech-agent"),
    # npm scope
    ("@nousresearch/",                  "@nastechai-research/"),
    # Org name - two-word variant before one-word
    ("Nous Research",                   "Nastechai Research"),
    ("NousResearch",                    "NastechaiResearch"),
    ("nousresearch",                    "nastechai"),
    ("NOUSRESEARCH",                    "NASTECHAI"),
    # hermes-agent compound forms - before bare 'hermes'
    ("hermes-agent",                    "nastech-agent"),
    ("hermes_agent",                    "nastech_agent"),
    ("HERMES_AGENT",                    "NASTECH_AGENT"),
    ("Hermes Agent",                    "Nastech Agent"),
    ("hermes agent",                    "nastech agent"),
    # Env var prefix - more specific before generic HERMES_
    ("HERMES_HOME",                     "NASTECH_HOME"),
    ("HERMES_",                         "NASTECH_"),
    # Python module prefix
    ("hermes_",                         "nastech_"),
    ("_hermes",                         "_nastech"),
    # CLI entry points
    ("hermes-acp",                      "nastech-acp"),
    # Title / mixed case - before lowercase
    ("Hermes",                          "Nastech"),
    # All caps
    ("HERMES",                          "NASTECH"),
    # Bare lowercase - last
    ("hermes",                          "nastech"),
]

# Filename substitutions (applied to basename only, in order)
NAME_SUBS = [
    ("hermes_",      "nastech_"),    # hermes_constants.py -> nastech_constants.py
    ("hermes-",      "nastech-"),    # hermes-already-has-routines.md -> nastech-already-has-routines.md
    ("setup-hermes", "setup-nastech"),
    ("hermes",       "nastech"),     # hermes/ dir -> nastech/
]

# Skip these - do not modify content (binary / lockfiles)
SKIP_CONTENT_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".svg",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".mp4", ".webm", ".mov", ".avi",
    ".zip", ".gz", ".tar", ".tgz", ".bz2", ".7z", ".xz",
    ".pyc", ".pyo", ".so", ".dylib", ".dll", ".exe",
    ".db", ".sqlite", ".sqlite3",
    ".lock",
    ".bin",
}

SKIP_DIRS = {
    ".git", "node_modules", "__pycache__", ".venv", "venv",
    "dist", "build", ".mypy_cache", ".ruff_cache", ".pytest_cache",
    ".eggs",
}


def rebrand_text(text: str) -> str:
    for old, new in TEXT_SUBS:
        text = text.replace(old, new)
    return text


def rebrand_name(name: str) -> str:
    for old, new in NAME_SUBS:
        if old in name:
            return name.replace(old, new, 1)
    return name


def should_skip_dir(name: str) -> bool:
    return name in SKIP_DIRS or name.endswith(".egg-info")


def process_tree(root: Path) -> None:
    for dirpath, dirnames, filenames in os.walk(root, topdown=False):
        dp = Path(dirpath)

        # Skip any path that contains an excluded directory component
        try:
            rel_parts = dp.relative_to(root).parts
        except ValueError:
            continue
        if any(should_skip_dir(part) for part in rel_parts):
            dirnames.clear()
            continue

        # Process file contents and rename files
        for fname in filenames:
            fpath = dp / fname
            ext = fpath.suffix.lower()

            if ext not in SKIP_CONTENT_EXTENSIONS:
                try:
                    content = fpath.read_text(encoding="utf-8")
                    new_content = rebrand_text(content)
                    if new_content != content:
                        fpath.write_text(new_content, encoding="utf-8")
                except (UnicodeDecodeError, PermissionError, OSError):
                    pass

            new_fname = rebrand_name(fname)
            if new_fname != fname:
                try:
                    fpath.rename(dp / new_fname)
                except OSError:
                    pass

        # Rename the directory itself (skip root)
        if dp != root:
            new_dname = rebrand_name(dp.name)
            if new_dname != dp.name:
                try:
                    dp.rename(dp.parent / new_dname)
                except OSError:
                    pass


if __name__ == "__main__":
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    if not root.exists():
        print(f"ERROR: {root} does not exist", file=sys.stderr)
        sys.exit(1)
    process_tree(root)
    print(f"Rebranding complete: {root}")
