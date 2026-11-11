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
