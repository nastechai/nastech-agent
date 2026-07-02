#!/usr/bin/env python3
"""Generates the PR body for the NasUpstream sync PR and writes it to /tmp/pr-body.txt."""
import os

sha   = os.environ.get("UPSTREAM_SHA", "unknown")
short = os.environ.get("UPSTREAM_SHORT", sha[:8])

body = (
    "## Upstream Sync - NasUpstream branch\n\n"
    "| | |\n"
    "|---|---|\n"
    f"| **Upstream SHA** | `{sha}` |\n"
    "| **Source** | https://github.com/NousResearch/hermes-agent |\n"
    "| **Branch** | `NasUpstream` |\n\n"
    "### What is included\n"
    "- All upstream commits rebranded (hermes->nastech, NousResearch->NastechaiResearch)\n"
    "- nastechai CI workflows, .npmrc, and scripts/release.py preserved\n"
    "- Brand validation must pass before merging\n\n"
    "### Do NOT auto-merge - manual review required\n"
    "- [ ] CI passes\n"
    "- [ ] Brand validation passes (no upstream string leakage)\n"
    "- [ ] nastechai customisations intact\n\n"
    "Auto-updated every 4 hours."
)

with open("/tmp/pr-body.txt", "w") as f:
    f.write(body)

print("PR body written to /tmp/pr-body.txt")
