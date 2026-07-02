#!/usr/bin/env python3
"""
Close mirrored PRs in nastechai/nastech-agent whose corresponding upstream PR
(NousResearch/hermes-agent) is no longer open.

Called by upstream-pr-mirror.yml workflow.
"""

import json
import os
import subprocess

GH_TOKEN = os.environ["GH_TOKEN"]
UPSTREAM = "NousResearch/hermes-agent"
ORIGIN   = "nastechai/nastech-agent"


def gh(*args):
    env = {**os.environ, "GH_TOKEN": GH_TOKEN}
    r = subprocess.run(["gh"] + list(args), capture_output=True, text=True, env=env)
    return r.stdout.strip(), r.returncode


def run(*args):
    r = subprocess.run(list(args), capture_output=True, text=True)
    return r.stdout.strip(), r.returncode


def get_open_upstream_numbers():
    out, _ = gh("api", f"repos/{UPSTREAM}/pulls", "--jq", "[.[].number]")
    return set(json.loads(out or "[]"))


def main():
    open_upstream = get_open_upstream_numbers()
    print(f"Open upstream PRs: {sorted(open_upstream)}")

    out, _ = run("git", "ls-remote", "--heads", "origin", "upstream-pr-*")
    closed = 0
    for line in out.splitlines():
        ref = line.split("\t")[-1].replace("refs/heads/", "")
        if not ref.startswith("upstream-pr-"):
            continue
        try:
            upstream_num = int(ref.replace("upstream-pr-", ""))
        except ValueError:
            continue

        if upstream_num not in open_upstream:
            out3, _ = gh(
                "pr", "list", "--repo", ORIGIN,
                "--head", ref, "--state", "open",
                "--json", "number", "--jq", ".[0].number",
            )
            if out3:
                print(f"Closing PR for {ref} (upstream #{upstream_num} is no longer open)")
                gh(
                    "pr", "close", out3, "--repo", ORIGIN,
                    "--comment",
                    f"Closing: upstream PR #{upstream_num} is no longer open "
                    f"on NousResearch/hermes-agent.",
                )
                closed += 1

    print(f"Stale mirror PRs closed: {closed}")


if __name__ == "__main__":
    main()
