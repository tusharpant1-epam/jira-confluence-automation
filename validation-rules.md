# Markdown Validation Rules

Apply these checks to each Markdown file in the requested scope:

1. **Check only the specified files.** Use `.md` files within the requested directory or workspace; do not include this rules file unless explicitly requested.
2. **Recognize real headings only.** A section counts when `Summary` or `Quiz` appears as a Markdown ATX heading (`#` through `######`), case-insensitively. Ignore mentions in prose, links, and fenced code blocks.
3. **Require both sections.** Flag a file if it has no `Summary` heading, no `Quiz` heading, or both are missing. Report each missing section by name.
4. **Flag duplicate sections.** Each required heading should appear once; report repeated `Summary` or `Quiz` headings with their line numbers.
5. **Require section content.** Each required heading must have non-placeholder content before the next heading of the same or higher level, or the end of the file. Flag empty sections and sections containing only placeholders such as `[TODO]`.
6. **Report findings precisely.** Give the relative file path, issue type, section name, and line number when available. List only files with a finding; do not modify the files being reviewed.
