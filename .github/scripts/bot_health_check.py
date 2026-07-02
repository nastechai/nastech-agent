#!/usr/bin/env python3
"""
Bot Health Check Script
=======================
Queries GitHub Actions workflow runs to verify all nastechai automation
bots are healthy. Writes a report and sets GITHUB_OUTPUT.

Called by bot-health-check.yml workflow.
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

GH_TOKEN = os.environ.get("GH_TOKEN", "")
REPO = "nastechai/nastech-agent"

# Max age in hours before a bot is considered overdue
MAX_AGE_HOURS = {
    "upstream-sync.yml":       6,    # scheduled every 4h
    "upstream-pr-mirror.yml":  4,    # scheduled every 2h
    "brand-validation.yml":    48,   # triggered on push / PR
    "bot-health-check.yml":    26,   # scheduled daily
}


def gh_api(path):
    env = {**os.environ, "GH_TOKEN": GH_TOKEN}
    r = subprocess.run(
        ["gh", "api", f"repos/{REPO}/{path}", "--paginate"],
        capture_output=True, text=True, env=env,
    )
    try:
        return json.loads(r.stdout or "{}")
    except json.JSONDecodeError:
        return {}


def main():
    now = datetime.now(timezone.utc)
    all_ok = True
    report_lines = []
    alert_lines = []

    for workflow_file, max_age in MAX_AGE_HOURS.items():
        data = gh_api(f"actions/workflows/{workflow_file}/runs?per_page=1")
        runs = data.get("workflow_runs", []) if isinstance(data, dict) else []

        if not runs:
            symbol = "NEVER_RUN"
            conclusion = "never"
            age_str = "n/a"
            all_ok = False
            alert_lines.append(f"- {workflow_file}: has never run")
        else:
            r = runs[0]
            updated = r.get("updated_at", "")
            conclusion = r.get("conclusion") or r.get("status", "unknown")

            try:
                ts = datetime.fromisoformat(updated.replace("Z", "+00:00"))
                age_h = (now - ts).total_seconds() / 3600
                age_str = f"{age_h:.1f}h ago"
            except Exception:
                age_h = 0.0
                age_str = "unknown"

            if conclusion == "success":
                symbol = "OK"
            elif conclusion in ("skipped", "neutral"):
                symbol = "SKIP"
            else:
                symbol = "FAIL"
                all_ok = False
                alert_lines.append(
                    f"- {workflow_file}: last run was '{conclusion}' ({age_str})"
                )

            if age_h > max_age:
                symbol = "OVERDUE"
                all_ok = False
                alert_lines.append(
                    f"- {workflow_file}: overdue (last ran {age_str}, limit {max_age}h)"
                )

        report_lines.append(f"{workflow_file:<36}  {symbol:<10}  {conclusion:<12}  {age_str}")

    report = "\n".join(report_lines)
    print(report)

    summary = "All bots healthy" if all_ok else f"{len(alert_lines)} alert(s)"

    report_path = "/tmp/health-report.txt"
    with open(report_path, "w") as f:
        f.write(f"Bot Health Check - {now.strftime('%Y-%m-%d %H:%M UTC')}\n\n")
        f.write(report)
        if alert_lines:
            f.write("\n\nALERTS:\n" + "\n".join(alert_lines))

    # Write issue body to file (avoids inline multi-line shell strings)
    issue_body_path = "/tmp/health-issue-body.txt"
    with open(issue_body_path, "w") as f:
        f.write("## Bot Health Check Alert\n\n")
        f.write("```\n")
        f.write(report)
        f.write("\n```\n\n")
        if alert_lines:
            f.write("**Alerts:**\n")
            for a in alert_lines:
                f.write(f"{a}\n")
        f.write("\nTriggered by scheduled health check. Check the Actions tab for details.\n\n")
        f.write("cc: @nastechai")

    # Set GITHUB_OUTPUT
    github_output = os.environ.get("GITHUB_OUTPUT", "")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"all_ok={'true' if all_ok else 'false'}\n")
            f.write(f"summary={summary}\n")

    print(f"\nHealth: {summary}")
    if alert_lines:
        print("ALERTS:")
        for a in alert_lines:
            print(a)

    sys.exit(0)


if __name__ == "__main__":
    main()
