- **Input format:** Use a feature request or acceptance criteria naming the browser screens and expected behavior. Inspect the existing UI, local API, database schema, and tests to discover the actual framework, routes, data shapes, and conventions before changing code.
  + Treat the requested register, project detail, review queue, dashboard, alert, and report screens as the integration scope unless the request narrows it.
  + If an API operation or data contract is missing, identify the gap and follow existing project patterns; ask only when a consequential behavior cannot be determined safely.
- **Processing steps:**
  + Trace each screen's current data source and actions to the corresponding API operations and persisted entities; keep database access in the local API, not browser code.
  + Reuse existing request, response, validation, and error-handling patterns. Implement or update API operations and migrations only when the screen cannot be correctly wired to existing contracts.
  + Connect the register and project detail to persisted records, search/filter state, accepted updates, milestones, source references, related proposals, and audit history where supported.
  + Connect the review queue to persisted proposals and their project/source/validation details. Preserve unresolved or ambiguous matches; require an explicit review decision before a proposal changes authoritative project data.
  + Connect the dashboard to persisted portfolio data and supported drill-downs. Show exceptions only when their evidence exists.
  + Connect alerts to persisted alert records and navigate to the related project and supporting record/source. Use configured rules; do not invent numeric thresholds.
  + Generate report previews from authoritative, reviewed data. Show the reporting period, generation time, and data freshness; keep preview corrections separate from source records and use the existing download flow.
  + Give every screen distinct loading, successful-empty, validation, and API/persistence error states. Preserve form input on validation or request failure, explain errors clearly, and provide retry where appropriate.
  + Add or update focused tests for API integration, persistence, screen behavior, and relevant loading, empty, validation, and failure states.
- **Output format:** Deliver the integrated UI and any necessary API, persistence, and test changes. In the completion response, summarize the screens wired, important data-flow decisions, and tests run; call out any unresolved contract or policy decisions.
- **Constraints:**
  + Use the existing local stack and persisted data; do not substitute mock, hard-coded, or success-shaped fallback data for API results.
  + Do not silently discard, overwrite, or mark data saved after failed validation or persistence. Keep proposal review, source attribution, and audit behavior intact.
  + Do not add cloud dependencies, expose the local API beyond the existing local-only boundary, or hard-code unapproved business thresholds.
  + Preserve existing UX and API contracts unless a required integration gap justifies a compatible, tested change.
