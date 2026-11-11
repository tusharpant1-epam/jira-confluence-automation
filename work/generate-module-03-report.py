from datetime import datetime, timedelta
import json
from pathlib import Path
import re
import subprocess


WORK_DIR = Path(__file__).resolve().parent
REPO_DIR = WORK_DIR / "module03-task"
REPORT_PATH = WORK_DIR / "module-03-report.md"
STATE_PATTERN = re.compile(r"<!-- report-state:(.*?) -->")
COMMIT_FORMAT = "%H%x1f%cs%x1f%an%x1f%s"


def git(*args):
    result = subprocess.run(
        ["git", *args],
        cwd=REPO_DIR,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.rstrip("\n")


def current_commit():
    result = subprocess.run(
        ["git", "rev-parse", "--verify", "--quiet", "HEAD"],
        cwd=REPO_DIR,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    if result.returncode == 1:
        return None
    raise subprocess.CalledProcessError(
        result.returncode, result.args, output=result.stdout, stderr=result.stderr
    )


def previous_report_state():
    if not REPORT_PATH.exists():
        return None

    match = STATE_PATTERN.search(REPORT_PATH.read_text(encoding="utf-8"))
    if match is None:
        return None

    state = json.loads(match.group(1))
    if not isinstance(state, dict) or "last_report_commit" not in state:
        raise ValueError(f"Invalid report state in {REPORT_PATH}")
    return state


def get_commits(state):
    head = current_commit()
    if head is None:
        return []

    if state is None:
        args = ("--since=7 days ago",)
    elif state["last_report_commit"] is not None:
        baseline = state["last_report_commit"]
        git("cat-file", "-e", f"{baseline}^{{commit}}")
        args = (f"{baseline}..HEAD",)
    else:
        args = ()

    history = git("log", *args, f"--format={COMMIT_FORMAT}")
    commits = []
    for line in history.splitlines():
        commit, date, author, subject = line.split("\x1f", 3)
        commits.append((commit[:7], date, author, subject))
    return commits


def main():
    git("rev-parse", "--is-inside-work-tree")
    state = previous_report_state()
    commits = get_commits(state)
    head = current_commit()
    generated_at = datetime.now().astimezone()
    if state is None:
        period = f"Last 7 days (initial report, since {(generated_at - timedelta(days=7)).date()})"
    else:
        period = "Since the previous report"

    status = git("status", "--short", "--untracked-files=all") or "Clean"
    if head is not None:
        diff_stat = git("diff", "HEAD", "--stat") or "No tracked-file changes"
    else:
        diff_stat = git("diff", "--stat") or "No tracked-file changes"

    if commits:
        commit_lines = "\n".join(
            f"- {date} — {subject} ({author}, `{commit}`)"
            for commit, date, author, subject in commits
        )
    else:
        commit_lines = "No new commits in this period."

    next_state = json.dumps(
        {"last_report_commit": head, "generated_at": generated_at.isoformat()},
        sort_keys=True,
    )
    report = f"""# Weekly Status Report

- **Period:** {period}
- **Source:** Local Git history for `{REPO_DIR.name}` only
- **Generated:** {generated_at.strftime("%Y-%m-%d %H:%M %Z")}

## Progress

{commit_lines}

## In progress

Working tree status:
```text
{status}
```

Tracked-file changes:
```text
{diff_stat}
```

## Blockers and risks

Not captured by local Git history. Add any known blockers or risks before sharing.

## Next priorities

Not captured by local Git history. Add upcoming priorities before sharing.

<!-- report-state:{next_state} -->
"""
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"Generated {REPORT_PATH}")


if __name__ == "__main__":
    main()
