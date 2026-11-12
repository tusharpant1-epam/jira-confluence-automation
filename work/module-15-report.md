# Module 15 Completion Report

## Script Metadata

- Filename: `tools/validate_markdown_format.py`
- Language: Python
- Purpose: Processes project-authored Markdown files and checks UTF-8 encoding, line endings, final newlines, trailing whitespace, blank lines around headings, and matching fenced code blocks. It writes findings to `reports/markdown-format-validation.md` without modifying source files.

## Script Contents

```python
#!/usr/bin/env python3
"""Check project-authored Markdown files against the formatting instruction."""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES_FILE = ROOT / "instructions/validate-markdown-format.agent.md"
OUTPUT_FILE = ROOT / "reports/markdown-format-validation.md"
EXCLUDED_DIRECTORIES = {".git", ".venv", "venv", "virtualenv", "node_modules"}
FENCE_RE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
HEADING_RE = re.compile(r"^ {0,3}#{1,6}(?:[ \t]+|$)")


def markdown_files() -> list[Path]:
    files: list[Path] = []
    for directory, subdirectories, filenames in os.walk(ROOT):
        subdirectories[:] = [
            name for name in subdirectories if name not in EXCLUDED_DIRECTORIES
        ]
        files.extend(
            Path(directory) / filename
            for filename in filenames
            if filename.endswith(".md")
        )
    return sorted(path for path in files if path != OUTPUT_FILE)


def selected_files(arguments: list[str]) -> list[Path]:
    if not arguments:
        return markdown_files()

    files: list[Path] = []
    for argument in arguments:
        path = Path(argument)
        if not path.is_absolute():
            path = ROOT / path
        path = path.resolve()
        if not path.is_relative_to(ROOT):
            raise ValueError(f"File is outside the workspace: {argument}")
        if not path.is_file():
            raise FileNotFoundError(f"Markdown file not found: {argument}")
        if path.suffix != ".md":
            raise ValueError(f"Expected a .md file: {argument}")
        if path != OUTPUT_FILE and path not in files:
            files.append(path)
    return sorted(files)


def line_for_offset(content: bytes, offset: int) -> int:
    return content[:offset].count(b"\n") + 1


def check_file(path: Path) -> list[str]:
    rules = RULES_FILE.read_text(encoding="utf-8")
    if not rules.strip():
        raise ValueError(f"Validation instruction is empty: {RULES_FILE}")

    relative = path.relative_to(ROOT).as_posix()
    findings: list[str] = []
    content = path.read_bytes()

    if content.startswith(b"\xef\xbb\xbf"):
        findings.append(f"{relative}:1: remove the UTF-8 byte-order mark")
    try:
        text = content.decode("utf-8-sig")
    except UnicodeDecodeError as error:
        line = line_for_offset(content, error.start)
        findings.append(f"{relative}:{line}: file is not valid UTF-8")
        return findings

    for match in re.finditer(b"\r\n|\r", content):
        line = line_for_offset(content, match.start())
        kind = "CRLF" if match.group() == b"\r\n" else "CR"
        findings.append(f"{relative}:{line}: use LF line endings, found {kind}")

    if not content.endswith(b"\n"):
        findings.append(f"{relative}: missing final newline")
    elif content.endswith(b"\n\n"):
        findings.append(f"{relative}: more than one newline at end of file")

    lines = text.splitlines()
    for number, line in enumerate(lines, start=1):
        if line.endswith((" ", "\t")):
            findings.append(f"{relative}:{number}: trailing whitespace")

    open_fence: tuple[str, int, int] | None = None
    for index, line in enumerate(lines):
        number = index + 1
        fence_match = FENCE_RE.match(line)
        if open_fence:
            marker, minimum_length, opening_line = open_fence
            if fence_match:
                token = fence_match.group(1)
                closing_info = fence_match.group(2)
                if (
                    token[0] == marker
                    and len(token) >= minimum_length
                    and not closing_info.strip()
                ):
                    open_fence = None
            continue

        if fence_match:
            token = fence_match.group(1)
            open_fence = (token[0], len(token), number)
            continue

        if HEADING_RE.match(line):
            if index > 0 and lines[index - 1].strip():
                findings.append(
                    f"{relative}:{number}: add a blank line before the heading"
                )
            if index + 1 < len(lines) and lines[index + 1].strip():
                findings.append(
                    f"{relative}:{number}: add a blank line after the heading"
                )

    if open_fence:
        _, _, opening_line = open_fence
        findings.append(f"{relative}:{opening_line}: fenced code block is not closed")

    return findings


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate Markdown formatting across the workspace or selected files."
    )
    parser.add_argument(
        "files",
        nargs="*",
        help="Optional Markdown paths relative to the workspace root (default: scan workspace).",
    )
    args = parser.parse_args()

    if not RULES_FILE.is_file():
        raise FileNotFoundError(f"Validation instruction not found: {RULES_FILE}")

    files = selected_files(args.files)
    findings = [issue for path in files for issue in check_file(path)]
    passed = len(files) - len({issue.split(":", 1)[0] for issue in findings})

    report = [
        "# Markdown Formatting Validation",
        "",
        f"- **Scope:** Project-authored Markdown files; excluded `.git`, virtual environments, `node_modules`, and this report.",
        f"- **Rules:** [{RULES_FILE.relative_to(ROOT).as_posix()}](../instructions/validate-markdown-format.agent.md)",
        f"- **Files checked:** {len(files)}",
        f"- **Files with findings:** {len(files) - passed}",
        f"- **Total findings:** {len(findings)}",
        "",
        "## Findings",
        "",
    ]
    report.extend(f"- {finding}" for finding in findings)
    if not findings:
        report.append("- No issues found.")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(
        f"Checked {len(files)} files: {len(findings)} finding(s) "
        f"across {len(files) - passed} file(s)."
    )
    print(f"Report: {OUTPUT_FILE.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `files` (positional, optional; repeatable) | Markdown paths relative to the workspace root; when supplied, validates only those files. | Scan all project-authored Markdown files |

## Test Run Output

Command:
```text
python3 tools/validate_markdown_format.py work/module-13-report.md work/module03-task/report_template.md
```

Output:
```text
Checked 2 files: 6 finding(s) across 2 file(s).
Report: reports/markdown-format-validation.md
```
