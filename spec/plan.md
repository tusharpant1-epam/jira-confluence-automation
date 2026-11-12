# Implementation Plan: Jira Active Sprint Dashboard

**Branch**: `[001-jira-active-sprint-dashboard]` | **Date**: 2026-11-12 | **Spec**: [specification.md](./specification.md)

**Input**: Clarified feature specification and project constitution in `spec/`.

## Summary

Deliver a read-only, single-user macOS prototype showing the currently active
sprint for one configured Jira Cloud Scrum board. Implement the React 18/Vite
dashboard, Node.js/Express API, PostgreSQL 15 local configuration store, and
Docker development setup. Use viewer-delegated Jira OAuth 2.0 (3LO), store
credentials in macOS Keychain, fetch Jira data through documented REST APIs,
and keep issue snapshots in backend memory only. Build and verify the feature
with synthetic fixtures before any optional live Jira smoke test.

The work is gated on board-specific setup values and Jira administrator
approval. No Jira issue writes, Confluence integration, LAN access, or
team-wide deployment are part of this plan.

## Technical Context

**Language/Version**: TypeScript on Node.js (current project Node.js LTS; pin a supported version in project configuration)

**Primary Dependencies**: React 18, Vite, Express; PostgreSQL driver and macOS Keychain integration to be selected during foundation work

**Storage**: PostgreSQL 15 in Docker for non-secret board configuration, field mappings, and refresh metadata; process memory for the current authorized issue snapshot; macOS Keychain for OAuth credentials

**Testing**: Unit tests for mapping/metrics and validation; API/integration tests with mocked Jira responses; React component/accessibility tests; end-to-end acceptance tests against synthetic fixtures. Test runner selection is a Phase 1 decision.

**Target Platform**: Local macOS prototype; loopback-only browser and API access; Docker-based PostgreSQL 15

**Project Type**: Local web application with separate frontend and backend

**Performance Goals**: No numerical load-time or refresh-completion SLA is defined for the prototype. Jira request timeout is 30 seconds; automatic refresh starts at startup and every five minutes while the dashboard is open, with no overlapping refreshes.

**Constraints**: Jira Cloud REST API v3 and Jira Software Agile REST API; least-privilege delegated read-only access; never show issues beyond the connected viewer's Jira permissions; reject incomplete refreshes; clear issue data on failed refresh, disconnect, identity/board change, and shutdown; no credentials or issue snapshots in PostgreSQL; bind app and database ports to loopback.

**Scale/Scope**: One local OS user, one OAuth identity at a time, one configured Scrum board, its current active sprint, all Jira-returned sprint issues, and no historical sprint selection.

## Constitution Check

| Gate | Plan |
|---|---|
| Source-system permissions | Use the connected user's delegated Jira authorization on backend requests. Do not use shared credentials, scrape Jira, or rely on frontend filtering for authorization. |
| Read-only behavior | Jira calls are read-only. Dashboard actions cannot create, edit, or delete Jira issues. Confluence is excluded. |
| Credential and data protection | Store OAuth credentials/client secrets in macOS Keychain; never expose them to the browser or persist them in PostgreSQL. Do not persist issue snapshots. |
| Traceability and failure handling | Keep last successful refresh time and refresh metadata; explicitly report errors and partial results, clear issue data on failure, and never represent incomplete results as successful. |
| Maintainability and testing | Separate UI, API, Jira adapter, persistence, and metric calculation. Use synthetic fixtures and test permission, mapping, refresh, and failure paths. |
| Technology | React 18/Vite, Node.js/Express, PostgreSQL 15 via Docker. No alternate primary stack is proposed. |
| Local boundary | Bind web/API and Docker-published database port to loopback. Do not implement LAN or team access. |

**Gate result**: Pass, subject to Phase 0 verification of the OAuth app and
Keychain integration requirements. No constitution exception is requested.

## Implementation Phases and Milestones

Phases are ordered; each milestone has an explicit exit check. Do not enable
live Jira integration until the external prerequisites below are satisfied.

### Phase 0 — Prerequisites and technical decisions

**Work**

- Confirm the actual Jira Cloud Scrum board ID, story-point field ID (if used),
  and explicit blocked mapping (Boolean field or exact status names).
- Obtain Jira administrator approval and register the OAuth 2.0 (3LO)
  integration with approved read-only scopes.
- Verify the local OAuth redirect/callback approach and the mechanism for
  reading/writing credentials in macOS Keychain without exposing secrets in
  source, browser code, logs, or process arguments.
- Confirm Node.js version pinning, package manager, test runner, PostgreSQL
  driver, and Keychain library/OS integration approach; record choices in
  project setup documentation.

**Milestone M0 — Integration prerequisites ready**

- Required board and field/mapping values are available and verified against
  the target board.
- OAuth app registration/scopes are approved, or Jira integration remains
  disabled while the fixture-driven prototype proceeds.
- Keychain and redirect design is validated before credentials are handled.

### Phase 1 — Application foundation and local runtime

**Work**

- Create the web/API workspace and project scripts with pinned React 18,
  Vite, Node.js/Express, and TypeScript configuration.
- Add Docker Compose configuration for PostgreSQL 15, publishing its port
  only on loopback.
- Add the initial schema/migrations for non-secret board configuration,
  field mappings, and refresh metadata; do not create issue snapshot tables.
- Add an Express health endpoint, validated configuration loading, explicit
  loopback binding, and a Vite development proxy to the API.
- Establish unit, API, and UI test commands and CI checks that require no Jira
  credentials.

**Milestone M1 — Local foundation runs**

- A developer can start PostgreSQL and both application processes using
  documented commands.
- Health checks pass; web/API/database ports bind only to loopback.
- Empty application build and test suites pass; migrations contain no
  credential or issue-content storage.

### Phase 2 — Jira authorization and board setup

**Work**

- Implement backend-owned OAuth 2.0 (3LO) connect/callback/disconnect flow.
- Store tokens and OAuth client credentials through the Keychain adapter;
  keep browser state free of tokens and clear in-memory issue data on
  disconnect or identity change.
- Implement board setup and validation for Jira Cloud, including Scrum board
  type and current-user access.
- Persist only the board ID and non-secret story-point/blocked mappings.
- Implement explicit setup, authorization, expiry, and invalid-configuration
  states.

**Milestone M2 — Secure configuration and identity**

- A synthetic OAuth test flow exercises success, denial, expiry, disconnect,
  and credential cleanup without exposing credentials to the frontend.
- Board validation rejects inaccessible and non-Scrum boards.
- No production Jira API access is enabled unless M0 approval is complete.

### Phase 3 — Jira data adapter and refresh lifecycle

**Work**

- Implement isolated Jira API clients for board, active sprint, and sprint
  issues using the documented REST API v3 and Jira Software Agile API.
- Add pagination, 30-second request timeouts, `Retry-After` handling, response
  validation, and explicit errors.
- Detect no active sprint and multiple active sprints with the specified empty
  state/error behavior.
- Build complete sprint snapshots in backend memory, scoped to the connected
  identity; publish only after every required page is successfully fetched
  and validated.
- Implement startup refresh, five-minute refresh while the dashboard is open,
  manual refresh, and non-overlap protection. Clear issue data and metrics on
  failed/partial refresh, disconnect, board/identity change, and shutdown.
- Persist refresh status/timestamps only, never issue content.

**Milestone M3 — Complete permission-scoped sprint data**

- Synthetic API fixtures prove pagination and reject partial, malformed,
  timed-out, rate-limited, or unauthorized results without presenting a
  successful snapshot.
- Tests prove issue snapshots and totals are scoped to the active identity
  and cleared on the specified events.
- A live read-only smoke test is optional after M0 approval.

### Phase 4 — Metrics and dashboard experience

**Work**

- Implement status-category counts and estimate-aware point totals over the
  full authorized sprint, independent of UI filters.
- Apply configured blocked mapping; represent missing mappings/values as
  “Unknown” or “Unavailable”, never as not blocked.
- Build the primary issue list with required fields, sprint name/date,
  explicit missing/unassigned labels, and Jira issue links where valid.
- Add combined single-select status/assignee filters, sorting rules, manual
  refresh control, refresh timestamp, and clear error/empty/configuration
  states.
- Ensure blocked state is conveyed in text and verify keyboard and screen
  reader operation against WCAG 2.1 AA for implemented flows.

**Milestone M4 — Functional dashboard complete**

- Acceptance fixtures cover complete, incomplete, unestimated, unassigned,
  blocked, and unknown-field cases; displayed counts, estimates, coverage,
  sorting, and filtering match the specification.
- No active sprint, multiple active sprints, and failed/partial refresh states
  have the specified UI behavior.
- Dashboard works in current stable desktop Chrome, Firefox, and Safari on
  macOS.

### Phase 5 — Hardening and prototype handoff

**Work**

- Run the full synthetic acceptance suite, security-oriented configuration
  checks, and dependency/build checks.
- Verify no OAuth secrets/tokens in repository files, browser bundles,
  browser storage, logs, or PostgreSQL; verify no issue snapshots are written
  to disk.
- Verify disconnect/reset cleanup, loopback-only listeners, and no Jira or
  Confluence write calls.
- Document local setup, Keychain/OAuth prerequisites, board configuration,
  test commands, refresh behavior, known limits, and teardown/reset.
- Review every acceptance criterion against test evidence and the final
  prototype.

**Milestone M5 — Prototype acceptance**

- SC-001 through SC-012 are verified by automated tests or the approved
  manual smoke test, as applicable.
- Constitution checks pass; no unresolved prototype behavior remains.
- External prerequisites not yet supplied are clearly called out, and live
  integration stays disabled until they are met.

## Dependencies and Release Gates

- **External gate**: Board ID, story-point field ID if applicable, blocked
  mapping, and Jira administrator OAuth approval are needed for live setup.
  Until then, continue with fixtures and do not invent values.
- **Security gate**: Validate that delegated Jira permissions are retained by
  the OAuth/API approach. Any inability to enforce viewer permissions blocks
  live integration.
- **Local platform gate**: This plan targets macOS Keychain. Other operating
  systems are not supported by this prototype.
- **Release gate**: Do not enable LAN access, multiple users, Confluence, Jira
  writes, persistent issue snapshots, or production hosting under this plan.
  Each requires a separate specification and review.

## Proposed Project Structure

```text
project-root/
├── package.json
├── docker-compose.yml
├── apps/
│   ├── web/
│   │   └── src/
│   │       ├── app/
│   │       ├── components/
│   │       ├── features/sprint-dashboard/
│   │       └── api/
│   └── api/
│       └── src/
│           ├── config/
│           ├── routes/
│           ├── auth/
│           ├── jira/
│           ├── sprint/
│           ├── persistence/
│           └── server.ts
├── db/
│   └── migrations/
├── tests/
│   ├── fixtures/jira/
│   ├── api/
│   └── e2e/
└── docs/
```

**Structure Decision**: Use a small web monorepo with distinct frontend and
backend packages. Keep Jira API and OAuth logic in the backend; isolate
Keychain and PostgreSQL access behind adapters; keep issue snapshots in
backend memory. Shared contracts may be added only if needed to keep API
payloads type-safe.

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| OAuth app registration or scopes are not approved | Build against synthetic fixtures; keep live Jira access gated on M0. |
| Jira permissions are not preserved by the selected authorization flow | Validate identity-scoped API access before live integration; stop rather than substituting a shared credential. |
| Board fields/statuses differ from assumptions | Require explicit board setup values and validate them; show unknown/unavailable states rather than guessing. |
| Rate limits or incomplete pagination produce misleading totals | Paginate and validate the full response; reject partial snapshots and clear issue metrics. |
| Credentials or issue data leak to browser/disk/logs | Backend-only tokens, Keychain adapter, memory-only snapshots, loopback binds, and automated secret/data-boundary tests. |
| Database becomes an unintended issue-data cache | Schema review and tests prohibit issue snapshot persistence; store only approved configuration and refresh metadata. |

## Out of Scope

- Confluence access or automation.
- Jira issue updates, writes, or comments.
- Past/future sprint selection or comparison.
- Multi-user, LAN, internal/team, or production deployment.
- Mobile layout, backup/recovery, audit-history features, and formal SLAs.
- Real project content or Jira credentials in automated tests or CI.
