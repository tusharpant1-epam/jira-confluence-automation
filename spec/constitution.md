# Project Constitution

## Purpose

This constitution establishes the principles and constraints for the Jira and
Confluence automation project. Feature specifications and implementation plans
must comply with these principles. Where a feature needs an exception, document
and approve it before implementation.

## Principles

### 1. Respect source-system permissions

- Jira and Confluence access must use documented APIs and the minimum
  permissions required for the approved feature.
- Jira data shown to a viewer must not exceed the issues that viewer is
  authorized to see in Jira. Enforce access checks in the backend; the frontend
  is not an authorization boundary.
- Do not scrape web interfaces or bypass source-system access controls.

### 2. Read-only by default; require approval for writes

- The initial Jira dashboard is read-only. Jira remains authoritative for issue
  changes.
- No feature may create, edit, publish, or delete Jira issues or Confluence
  content unless a separate specification explicitly authorizes those actions,
  defines the permitted operations, and includes appropriate confirmation and
  audit requirements.
- Automation must not silently apply changes to either source system.

### 3. Protect credentials and project data

- Never commit credentials, tokens, or secrets to source control or expose them
  in client-side code, logs, error messages, or reports.
- Use an approved secret or credential-storage mechanism; the specific
  mechanism must be decided before integration work begins.
- Collect, retain, and transmit only data needed for an approved feature.
- Do not send project data to external services unless the data handling and
  service have been explicitly approved.

### 4. Preserve data meaning and traceability

- Clearly distinguish missing, unknown, and unavailable data from zero or a
  positive/negative result.
- Preserve source identifiers and links where available, and show when data
  was last refreshed.
- Surface API, refresh, validation, and partial-failure errors clearly. Never
  present an incomplete or failed refresh as successful.
- Keep derived metrics explainable and consistent with Jira's source fields
  and status semantics.

### 5. Keep the application maintainable and testable

- Keep UI, API, integration, and persistence responsibilities separated.
- Validate inputs at API boundaries and handle expected external-service
  failures explicitly.
- Add or update automated tests for behavior, permissions, data interpretation,
  and error paths affected by each feature.
- Keep changes focused and update relevant documentation when behavior or
  setup changes.

## Technology constraints

- Frontend: React 18 with Vite.
- Backend: Node.js with Express.
- Database: PostgreSQL 15, run locally through Docker for development.
- Do not introduce a different primary framework, database, or database
  version without documenting the reason and obtaining approval.

## Delivery and deployment constraints

- The first release is a local prototype, with a possible later internal
  team-wide deployment.
- Do not assume local-prototype network exposure, shared-user authentication,
  or production hosting requirements. Define and review those before enabling
  team-wide access.
- The Jira dashboard initially covers one configured Scrum board and its
  currently active sprint. Refresh data every 5–10 minutes as specified by the
  requirements.
- Confluence automation behavior and scope must be specified per feature;
  mentioning Confluence does not authorize content changes.

## Decision rule

When requirements conflict with this constitution or leave security,
permissions, data retention, or source-system write behavior ambiguous, pause
the affected work and resolve the decision in the feature specification before
implementation.
