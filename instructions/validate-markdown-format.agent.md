---
description: Validate project-authored Markdown files for consistent basic formatting.
---

Validate all project-authored `.md` files, including hidden project folders, while excluding `.git`, virtual environments, `node_modules`, and the generated validation report.

- Use `python3 tools/validate_markdown_format.py` to process each Markdown file independently and write `reports/markdown-format-validation.md`.
- Apply these checks to each file:
  + Require UTF-8 text without a byte-order mark.
  + Require LF line endings and exactly one final newline.
  + Flag trailing spaces or tabs on any line.
  + Require blank lines immediately before and after ATX headings, except at file boundaries.
  + Require fenced code blocks to close with a matching fence character and a fence at least as long as the opening fence.
- Report each issue with a relative path, line number when available, and concise explanation. Do not edit source files automatically.
- Review the report for false positives and exceptions before changing any documents; preserve intentional Markdown structure and code examples.
