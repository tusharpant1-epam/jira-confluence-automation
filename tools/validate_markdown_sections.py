#!/usr/bin/env python3
"""Validate Summary and Quiz sections in workspace Markdown files."""

from __future__ import annotations

import re
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RULES_FILE = ROOT / "validation-rules.md"
OUTPUT_FILE = ROOT / "validation-results.txt"
HEADING_RE = re.compile(r"^(#{1,6})[ \t]+(.*?)[ \t]*#*[ \t]*$")
PLACEHOLDER_RE = re.compile(
    r"^(?:[-*+]\s*)?\[(?:TODO|TBD|PLACEHOLDER|INSERT[^]]*)\]\s*\.?$",
    re.IGNORECASE,
)
REQUIRED_SECTIONS = ("summary", "quiz")


def markdown_files() -> list[Path]:
    paths: list[Path] = []
    for directory, subdirectories, filenames in os.walk(ROOT):
        subdirectories[:] = [name for name in subdirectories if name != ".git"]
        paths.extend(
            Path(directory) / filename
            for filename in filenames
            if filename.endswith(".md")
        )
    return sorted(path for path in paths if path != OUTPUT_FILE)


def headings_and_content(path: Path) -> tuple[list[tuple[int, int, str]], list[str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    headings: list[tuple[int, int, str]] = []
    in_fence = False
    fence_marker = ""

    for number, line in enumerate(lines, start=1):
        fence = re.match(r"^\s*(```+|~~~+)", line)
        if fence:
            marker = fence.group(1)[0]
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif marker == fence_marker:
                in_fence = False
            continue
        if in_fence:
            continue
        match = HEADING_RE.match(line)
        if match:
            title = re.sub(r"\s+#+\s*$", "", match.group(2)).strip()
            headings.append((number, len(match.group(1)), title.casefold()))

    return headings, lines


def findings_for(path: Path) -> list[str]:
    headings, lines = headings_and_content(path)
    findings: list[str] = []
    relative = path.relative_to(ROOT).as_posix()
    found = {
        section: [(number, level) for number, level, title in headings if title == section]
        for section in REQUIRED_SECTIONS
    }

    for section in REQUIRED_SECTIONS:
        occurrences = found[section]
        if not occurrences:
            findings.append(f"{relative}: missing {section.title()} section")
            continue

        for number, _ in occurrences[1:]:
            findings.append(
                f"{relative}:{number}: duplicate {section.title()} section"
            )

        for number, level in occurrences:
            end = len(lines)
            for next_number, next_level, _ in headings:
                if next_number > number and next_level <= level:
                    end = next_number - 1
                    break
            content = [
                line.strip()
                for line in lines[number:end]
                if line.strip()
                and not HEADING_RE.match(line)
                and not PLACEHOLDER_RE.match(line.strip())
            ]
            if not content:
                findings.append(
                    f"{relative}:{number}: empty or placeholder-only "
                    f"{section.title()} section"
                )

    return findings


def main() -> None:
    if not RULES_FILE.is_file():
        raise FileNotFoundError(f"Validation rules not found: {RULES_FILE}")

    files = markdown_files()
    all_findings = [finding for path in files for finding in findings_for(path)]

    report = [
        "Markdown section validation",
        f"Rules: {RULES_FILE.relative_to(ROOT).as_posix()}",
        f"Files checked: {len(files)}",
        "",
    ]
    report.extend(all_findings or ["No issues found."])
    OUTPUT_FILE.write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"Checked {len(files)} Markdown files.")
    print(f"Found {len(all_findings)} issue(s).")
    print(f"Results: {OUTPUT_FILE.relative_to(ROOT).as_posix()}")


if __name__ == "__main__":
    main()
