# Module 10 Completion Report

## Instruction Files
```text
instructions/connect-browser-ui-to-local-api.agent.md
instructions/create-status-report.agent.md
instructions/creating-instructions.agent.md
instructions/import-csv-xlsx-data.agent.md
instructions/main.agent.md
instructions/validate-import-data.agent.md
```

## main.agent.md Contents
```markdown
# Instruction Catalog

Each entry below is an instruction file with a one-line description.

---

- [`./instructions/creating-instructions.agent.md`](./creating-instructions.agent.md) — Create, update, and connect portable project instructions.
  + Keywords: create instruction, update instruction, instruction setup, prompt wrappers
- [`./instructions/create-status-report.agent.md`](./create-status-report.agent.md) — Create a concise weekly status report in Markdown.
  + Keywords: weekly status report, status report, weekly update
- [`./instructions/connect-browser-ui-to-local-api.agent.md`](./connect-browser-ui-to-local-api.agent.md) — Connect portfolio browser screens to the local API and persisted data.
  + Keywords: browser UI, local API, database integration, register, project detail, review queue, dashboard, alerts, reports
  + Target: `work/**`
- [`./instructions/import-csv-xlsx-data.agent.md`](./import-csv-xlsx-data.agent.md) — Import CSV/XLSX data through preview, mapping, validation, and confirmed application.
  + Keywords: import CSV, import XLSX, file import, column mapping, import preview, import validation
  + Target: `work/**`
- [`./instructions/validate-import-data.agent.md`](./validate-import-data.agent.md) — Validate imported rows, identify duplicates and conflicts, and apply accepted data safely.
  + Keywords: import validation, row-level errors, duplicate detection, repeated updates, safe import, rollback
  + Target: `work/**`
```

## Sample Instruction
- File: validate-import-data.agent.md
- Contents:
```markdown
- **Input format:** Accept parsed import rows with stable source row numbers, source/dataset identifiers, mapped fields, and the current persisted records needed for integrity, duplicate, and conflict checks. Use the existing import schema and validation-error shape.
- **Processing steps:**
  + Validate each row against required fields, field types, allowed values, relationships, and business rules; retain row and field context for every error.
  + Distinguish invalid data from warnings and missing optional values. Preserve meaningful differences such as missing, zero, healthy, and not applicable.
  + Detect duplicate rows within the file, records already present in storage, and likely repeated updates using stable source IDs and existing matching rules. Mark uncertain matches for operator review instead of guessing.
  + Compare proposed values with accepted records. Report conflicts and require explicit review for changes; never silently overwrite accepted data.
  + Produce a deterministic validation summary with total, valid, invalid, warning, duplicate, and conflicting row counts, plus actionable row-level findings.
  + Block application when the import cannot meet integrity requirements. If partial acceptance is supported, make excluded rows explicit and ensure only the operator-confirmed valid set is applied.
  + Apply the confirmed set atomically using a database transaction or equivalent. On failure, roll back the import changes, surface the error, and persist an accurate failed/partial job outcome without claiming success.
  + Preserve source attribution, accepted values, and audit history. Route imported update candidates through proposal review rather than directly changing authoritative records.
  + Add tests for invalid rows, intra-file and persisted duplicates, repeated imports, conflicting updates, atomic rollback, and unchanged accepted data after failure.
- **Output format:** Return a validation result containing row-level errors/warnings with row and field identifiers, duplicate/conflict classifications, and aggregate counts. After application, return the persisted job status and applied/rejected counts; clearly distinguish validation failure, application failure, and success.
- **Constraints:**
  + Never discard invalid or unsupported rows silently, report success before persistence completes, or hide partial failures.
  + Do not overwrite accepted data, treat duplicate candidates as new authoritative updates, or bypass required review/approval.
  + Reuse established schemas, matching rules, persistence patterns, and API error contracts; do not invent business rules or thresholds.
  + Keep validation deterministic and local; do not introduce external services or dependencies for import processing.
```
