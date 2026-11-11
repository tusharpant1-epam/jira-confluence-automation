- **Input format:** Accept an operator-selected `.csv` or `.xlsx` file, the source name or system, the dataset type (such as project register or planning data), and column mappings to supported fields. Use configured mappings when available; otherwise require the operator to map columns.
- **Processing steps:**
  + Parse the selected file using existing project dependencies and validate the file type, readable content, headers, and required fields before offering import.
  + Show a representative row preview and allow the operator to map source columns to supported fields; do not infer ambiguous mappings silently.
  + Validate mapped values and cross-record references using existing schema and business rules. Preserve distinctions between missing, zero, healthy, and not applicable values.
  + Follow `./instructions/validate-import-data.agent.md` for detailed row validation, duplicate/conflict handling, and safe application.
  + Report row-level validation errors and warnings, duplicate records, and likely repeated updates. Do not silently overwrite accepted data.
  + Present an acceptance summary with source, dataset type, total rows, valid rows, rejected rows, warnings, duplicates, and the changes that will be applied.
  + Apply changes only after explicit operator confirmation. Use a transaction or equivalent safe mechanism so invalid input or persistence errors cannot silently cause partial data loss.
  + Preserve source name, import time, source record identifiers when available, and import-job outcome, counts, and actionable errors.
  + Route imported update candidates through the existing review workflow; only approved proposals may change authoritative records. Keep unresolved or ambiguous project matches unresolved for review.
- **Output format:** Before confirmation, provide a preview, column mapping, row-level validation results, and an acceptance summary. After confirmation, report the persisted import outcome and counts, including failures; do not report success until persistence completes.
- **Constraints:**
  + Support only the existing CSV/XLSX import scope and supported fields; do not silently drop unsupported columns or rows.
  + Never auto-apply changes during preview, skip validation, guess ambiguous project matches, or overwrite accepted values without explicit review.
  + Make errors actionable and retain enough row/source context for correction without exposing unrelated data.
  + Keep the workflow user-triggered and local; do not add background imports, external connectors, or cloud dependencies unless separately requested and approved.
  + Test valid and invalid rows, mapping, duplicates, repeated imports, persistence failures, and preservation of existing accepted values.
