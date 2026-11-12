# Implementation Tasks: Jira Active Sprint Dashboard

**Plan**: [plan.md](./plan.md)  
**Specification**: [specification.md](./specification.md)  
**Constitution**: [constitution.md](./constitution.md)

Tasks are grouped by the implementation phases and milestones in the plan.
Complete dependencies before starting dependent tasks. `[P]` marks work that
can proceed in parallel once its listed dependencies are complete. A task is
done only when all acceptance criteria are verified.

## Recommended execution order

1. **Low-risk, high-gain alignment**: confirm the implementation root is the
   existing `work/payments-portfolio/` skeleton; complete T003 tooling
   decisions; and run T001/T002 external discovery in parallel without
   enabling live Jira access.
2. **Foundation in parallel**: after T003, populate the web/API skeleton (T004)
   and establish the loopback database runtime (T005) in parallel. Then run
   T006 after T005 and T007/T008 after T004.
3. **Security gate before credentials**: finish the OAuth/browser security
   feasibility decision and Keychain integration selection before T009/T010.
   If the local OAuth design does not pass, stop live-integration work and
   continue only with fixture-backed functionality.
4. **Build in dependency order**: T009/T010/T011 and validated setup precede
   Jira access; T014/T015 precede snapshots and refresh; T019 precedes
   frontend integration; metrics and UI follow typed data/API contracts.
5. **Acceptance and handoff**: finish synthetic tests and security boundary
   checks before final documentation and acceptance.

## Phase 0 — Prerequisites and technical decisions

### T001 — Confirm Jira board and field configuration

**Depends on**: None; external operator input.

**Status**: Blocked pending operator input. See
[jira-setup.md](./jira-setup.md).

- [ ] Record and validate the target Jira Cloud Scrum board ID.
- [ ] Record the board's story-point field ID, if used.
- [ ] Record the blocked Boolean field or exact blocked status names.

**Acceptance criteria**

- The values are documented as environment-specific setup inputs and are not
  hard-coded into source code.
- Board metadata is verified as Scrum where an authorized metadata source is
  available. Access verification for the prototype identity is gated on T010.
- If an input cannot be obtained, live setup remains disabled and the missing
  value is reported; no value is guessed.

### T002 — Obtain Jira OAuth app approval

**Depends on**: None; Jira site-administrator approval.

- [ ] Register the Jira Cloud OAuth 2.0 (3LO) integration.
- [ ] Obtain approval for least-privilege read-only scopes.
- [ ] Document the approved redirect URI and local setup procedure without
  recording secrets.
- [ ] Research and record a stop/go decision for local callback feasibility,
  OAuth state/replay protection, callback error handling, browser session and
  cookie protections, CSRF/origin policy, and dashboard-open refresh signals.

**Acceptance criteria**

- The approval, scopes, and redirect URI are documented.
- No Jira write scope is requested.
- The callback/browser security decision is documented and reviewed before
  T010 begins.
- If approval is pending, live Jira access stays disabled and fixture-based
  development can continue.

### T003 — Select and record project tooling

**Depends on**: None; may proceed in parallel with T001–T002.

- [ ] Select the package manager and pin Node.js 26 LTS to an exact patch
  version.
- [ ] Select PostgreSQL driver, migration tool, test runner, and macOS Keychain
  integration.
- [ ] Record versions and rationale in project setup documentation.

**Acceptance criteria**

- All choices are compatible with React 18/Vite, Node.js/Express, PostgreSQL
  15, and macOS Keychain.
- Tool versions can be reproduced from repository configuration.
- Node.js 26 LTS and package-manager versions are pinned with repository
  configuration and a lockfile.
- No choice requires storing OAuth credentials or Jira issue snapshots in the
  repository or database.

**Milestone M0**: T001–T003 are complete, or live Jira integration is explicitly
held behind missing external prerequisites or a failed OAuth feasibility gate.
T004/T005 foundation work may proceed independently after T003.

## Phase 1 — Application foundation and local runtime

### T004 — Populate the existing typed web/API workspace

**Depends on**: T003.

- [ ] Use the existing `work/payments-portfolio/` project root and create root
  workspace scripts for separate `apps/web` and `apps/api` packages.
- [ ] Configure React 18/Vite and Node.js/Express with TypeScript.
- [ ] Add development, build, type-check, and test scripts.

**Acceptance criteria**

- A clean install followed by the documented build and type-check commands
  succeeds.
- Work is added to the existing skeleton; no duplicate project root is
  created.
- Web and API packages remain independently buildable.
- No credentials or real Jira data are present in source or example
  configuration.

### T005 — Add loopback-only PostgreSQL 15 runtime

**Depends on**: T003.

- [ ] Add Docker Compose configuration for PostgreSQL 15.
- [ ] Publish the database port on loopback only.
- [ ] Document start, stop, and local data-reset commands.

**Acceptance criteria**

- PostgreSQL 15 starts using the documented command.
- The published database port is bound only to `127.0.0.1`.
- Reset removes local prototype data without touching other Docker resources.

### T006 — Add minimal configuration schema and migrations

**Depends on**: T005.

- [ ] Create migrations for one board configuration, field mappings, and
  refresh metadata.
- [ ] Add migration up/down or the repository-standard rollback procedure.
- [ ] Exclude OAuth tokens, client secrets, and issue/sprint snapshots.

**Acceptance criteria**

- Migrations apply to a clean PostgreSQL 15 instance and can be verified as
  applied.
- Schema stores only approved non-secret configuration and refresh metadata.
- A schema review/test confirms there are no issue snapshot or credential
  tables.

### T007 — Add local API runtime and development proxy

**Depends on**: T004.

- [ ] Add validated API configuration and an Express health endpoint.
- [ ] Bind the API explicitly to loopback.
- [ ] Configure the Vite development proxy to reach the local API.

**Acceptance criteria**

- Health endpoint returns a success response when the API is ready.
- API listener binds to loopback, not a wildcard/LAN interface.
- The frontend can call the health endpoint through its development proxy.

### T008 — Establish credential-free CI checks

**Depends on**: T004.

- [ ] Configure CI for install, lint, type-check, build, and test commands.
- [ ] Ensure CI uses mocks/fixtures and does not require Jira credentials or
  real project content.
- [ ] Run adapter contract tests with a mocked Keychain implementation; run
  real Keychain checks only in the macOS verification path.

**Acceptance criteria**

- CI completes successfully from a clean checkout without Jira or Keychain
  credentials.
- Failure in lint, type-check, build, or tests fails the CI job.
- No job publishes or logs secrets.
- The CI runner and OS-specific Keychain test strategy are documented.

**Milestone M1**: T004–T008 complete; local application and database start
reproducibly with loopback-only listeners and an empty passing test suite.

## Phase 2 — Jira authorization and board setup

### T009 — Implement the Keychain credential adapter

**Depends on**: T002, T003.

- [ ] Implement backend-only read, write, and delete operations for OAuth
  credentials using the selected macOS Keychain integration.
- [ ] Store OAuth client credentials and user tokens in Keychain.
- [ ] Redact secrets from errors and logs.

**Acceptance criteria**

- Unit tests cover successful storage/retrieval, missing item, update, and
  deletion.
- Tokens and client secrets do not appear in PostgreSQL, application config,
  browser storage, logs, or API responses.
- Keychain errors are reported explicitly without leaking secret values.

### T010 — Implement delegated Jira OAuth flow

**Depends on**: T007, T009, T002.

- [ ] Add backend-owned OAuth 2.0 (3LO) start and callback routes.
- [ ] Validate OAuth state and callback inputs.
- [ ] Exchange and retain credentials through the Keychain adapter; expose
  only connection state to the frontend.

**Acceptance criteria**

- Tests cover callback success, denial, invalid state, token exchange failure,
  and expired/revoked credentials.
- No access or refresh token is returned to the browser.
- OAuth requests use only the administrator-approved read-only scopes.
- Live OAuth is disabled if T002 is not approved.

### T011 — Implement disconnect and credential cleanup

**Depends on**: T009, T010.

- [ ] Add a disconnect action and backend endpoint.
- [ ] Clear in-memory issue data on disconnect and identity change.
- [ ] Add a documented local reset that also removes stored OAuth client
  credentials and application setup.

**Acceptance criteria**

- Disconnect deletes user tokens from Keychain and clears issue data.
- Reset removes local setup, refresh metadata, and OAuth client credentials.
- Tests confirm repeated disconnect/reset is safe and does not disclose
  credentials.

### T012 — Implement board setup and validation

**Depends on**: T006, T010, T001.

- [ ] Add setup UI/API for one Jira board ID, story-point field ID, and
  blocked mapping.
- [ ] Validate board accessibility and Scrum type using the connected
  identity.
- [ ] Allow the local operator to replace the board and clear in-memory
  issue data on change.

**Acceptance criteria**

- Valid setup persists only non-secret configuration in PostgreSQL.
- Missing, inaccessible, invalid, and non-Scrum board configurations do not
  expose sprint issue data.
- Board changes clear the previous issue result before using the new board.
- Live validation is gated on T001 and T002; mocked tests work without them.

### T013 — Verify loopback and identity boundaries

**Depends on**: T007, T010, T011.

- [ ] Add automated tests for local listener binding, authenticated route
  behavior, and identity change cleanup.
- [ ] Verify OAuth callback/session data cannot be used to retrieve another
  identity's snapshot.

**Acceptance criteria**

- Tests fail if the API binds to a wildcard/LAN address.
- Unauthorized requests receive an explicit authentication response and no
  Jira data.
- Identity change clears the old identity's in-memory data before new data is
  accepted.

**Milestone M2**: T009–T013 complete; secure local identity and validated board
configuration work with mocks, with live integration still approval-gated.

## Phase 3 — Jira data adapter and refresh lifecycle

### T014 — Implement Jira API transport

**Depends on**: T003.

- [ ] Implement a backend-only Jira Cloud REST API v3 and Jira Software Agile
  API client.
- [ ] Add request timeout, pagination primitives, `Retry-After` handling,
  response validation, and safe error mapping.

**Acceptance criteria**

- Tests cover success, non-success HTTP responses, timeout, malformed
  response, pagination continuation, and rate-limit headers.
- Requests use the active delegated identity and approved read-only scopes.
- Error messages omit credentials and sensitive response content.

### T015 — Load board, active sprint, and sprint metadata

**Depends on**: T012, T014.

- [ ] Fetch board metadata and verify Scrum type/access.
- [ ] Fetch active sprint state for the configured board.
- [ ] Implement zero-sprint empty state and multiple-sprint configuration
  error.

**Acceptance criteria**

- Fixtures cover inaccessible/non-Scrum board and zero, one, and multiple
  active sprint results.
- No past/future sprint is substituted and no sprint is implicitly selected
  when multiple active sprints are returned.
- Sprint name and dates are included when available; missing dates are
  explicitly unavailable.

### T016 — Fetch and validate complete sprint issue snapshots

**Depends on**: T014, T015, T001.

- [ ] Fetch all Jira-returned sprint issues and required fields with complete
  pagination.
- [ ] Map Jira issue data into a typed in-memory snapshot, including
  unavailable values.
- [ ] Reject partial, duplicate-page, or schema-invalid results.

**Acceptance criteria**

- Fixtures verify issue keys, summaries, status category, status, assignee,
  configured story points, blocked state, and issue URL mapping.
- Tests include subtasks/varied issue types and prove no type is silently
  filtered out.
- Any failed page or invalid required response rejects the entire snapshot.
- Issue content is not persisted to PostgreSQL or disk.

### T017 — Implement refresh orchestration

**Depends on**: T016, T006.

- [ ] Implement refresh at startup and every five minutes while the dashboard
  is open, plus manual refresh.
- [ ] Prevent overlapping refreshes and persist refresh metadata only.
- [ ] On failure/partial result, clear issue data and metrics but retain the
  last successful timestamp.

**Acceptance criteria**

- Fake-clock tests verify startup and five-minute scheduling and ensure no
  scheduled refresh while the dashboard is closed.
- Concurrent manual/scheduled requests do not overlap.
- Timeout is 30 seconds; rate limiting honors `Retry-After`; failed requests
  do not retry before the next scheduled/manual attempt.
- Failure states clear all issue rows and derived metrics and are not marked
  successful.

### T018 — Add identity-scoped in-memory snapshot lifecycle

**Depends on**: T011, T016, T017.

- [ ] Scope the current snapshot to the connected OAuth identity.
- [ ] Clear snapshots on logout, identity/board change, failed refresh, and
  process shutdown.

**Acceptance criteria**

- Two synthetic identities with disjoint issue sets are connected
  sequentially, with disconnect/cleanup between them, and never observe each
  other's rows or aggregates.
- Lifecycle tests prove data is cleared on every specified event.
- No cross-identity or persistent snapshot cache exists.

### T019 — Expose typed read-only dashboard API

**Depends on**: T015, T016, T017, T018.

- [ ] Add endpoints for connection state, setup, active sprint data, refresh
  status, manual refresh, and disconnect.
- [ ] Define typed request/response contracts and explicit error responses.
- [ ] Ensure dashboard endpoints perform no Jira write operations.

**Acceptance criteria**

- Contract tests cover success, unauthorized, invalid configuration, no
  active sprint, multiple active sprints, refresh in progress, and refresh
  failure.
- Responses contain only fields authorized and returned for the connected
  identity.
- Tests or code inspection confirm no create/update/delete Jira calls exist.

**Milestone M3**: T014–T019 complete; a full, permission-scoped sprint snapshot
is produced atomically, or a clear non-success state is returned.

## Phase 4 — Metrics and dashboard experience

### T020 — Implement sprint metric calculations

**Depends on**: T016.

- [ ] Implement pure calculation functions for Done/remaining issue counts,
  point totals, estimate coverage, unestimated count, and point progress.
- [ ] Keep calculations independent of UI filters.

**Acceptance criteria**

- Unit fixtures verify Done-category completion and non-Done remaining counts.
- Numeric estimates are summed; missing estimates are counted as unestimated
  and never converted to zero.
- Point progress is unavailable when total estimated points are not positive.
- Metrics always reflect the full authorized sprint regardless of list
  filters.

### T021 — Build dashboard shell and state views

**Depends on**: T004, T019.

- [ ] Build the React application shell and route/page for the sprint
  dashboard.
- [ ] Add connection, setup-required, loading, empty-sprint,
  multiple-sprint-error, failed-refresh, and disconnected states.

**Acceptance criteria**

- Each backend state has a distinct, understandable UI representation.
- Failed or partial refresh state contains no issue details or metrics.
- Loading and errors are keyboard reachable and announced accessibly.

### T022 — Build sprint issue list

**Depends on**: T021, T019.

- [ ] Render issue key, summary, status, assignee, story points, and blocked
  state.
- [ ] Show sprint name and dates when available.
- [ ] Link issue keys to Jira when a valid URL is present.

**Acceptance criteria**

- Fixtures show all authorized returned issues, including unassigned and
  unavailable fields, without silently dropping rows.
- Missing, unknown, and unavailable values are distinct; “Unassigned” is
  explicit.
- Blocked state is readable text, not color alone.

### T023 — Add status/assignee filters and sorting

**Depends on**: T022.

- [ ] Add combined single-select status and assignee filters, including
  “Unassigned”.
- [ ] Add ascending/descending sort by status or assignee with issue-key
  ascending default and tie-breaker.

**Acceptance criteria**

- Tests cover each filter individually, both filters combined, clearing
  filters, and values changing after refresh.
- Sorting by either supported field works in both directions and is stable.
- Unassigned values sort last; aggregate metrics remain unchanged by filters.

### T024 — Add sprint progress and estimate coverage

**Depends on**: T020, T021.

- [ ] Render complete/remaining issue counts and estimated point totals.
- [ ] Show estimate coverage and unestimated issue count.
- [ ] Show point progress only when the specification's denominator rule is
  met.

**Acceptance criteria**

- UI totals match the pure metric function for synthetic fixtures.
- Missing or inaccessible estimates never appear as zero.
- Totals are labeled as full-sprint totals, not filtered-list totals.

### T025 — Add refresh controls and status

**Depends on**: T021, T019.

- [ ] Add manual refresh control, refresh-in-progress state, last successful
  refresh time, and actionable error text.
- [ ] Reflect backend non-overlap and rate-limit behavior.

**Acceptance criteria**

- Manual refresh starts one request and disables/rejects overlapping
  refreshes.
- Success updates the last-success time; failure preserves that timestamp and
  clears issue data/metrics.
- Errors do not expose tokens or sensitive Jira response content.

### T026 — Verify accessibility and browser support

**Depends on**: T021–T025.

- [ ] Verify keyboard navigation, focus handling, text alternatives, and
  screen-reader announcements for implemented flows.
- [ ] Run dashboard acceptance checks in current stable Chrome, Firefox, and
  Safari on macOS.

**Acceptance criteria**

- Implemented dashboard flows target WCAG 2.1 AA; blocked state is not
  conveyed by color alone.
- No critical keyboard-only or screen-reader blocker remains in connection,
  setup, filtering, refresh, and error flows.
- Browser smoke checks pass in all three supported desktop browsers.

**Milestone M4**: T020–T026 complete; dashboard behavior matches the
specification for authorized fixture data, all relevant empty/error states,
and supported desktop browsers.

## Phase 5 — Hardening and prototype handoff

### T027 — Complete automated acceptance coverage

**Depends on**: T008, T013–T026.

- [ ] Add integration and end-to-end synthetic tests for specification
  acceptance scenarios and edge cases.
- [ ] Cover permission isolation, active sprint cardinality, pagination,
  estimates, blocked state, filters, metrics, and refresh failures.

**Acceptance criteria**

- SC-001 through SC-012 each map to at least one automated test or an
  explicitly approved manual check.
- CI runs the tests without Jira credentials or real project content.
- Sequential identity-switch tests fail when unauthorized issue rows or
  derived metrics leak across identities.

### T028 — Verify security and data boundaries

**Depends on**: T009–T019, T027.

- [ ] Inspect browser bundles/storage, logs, PostgreSQL schema/data, and
  filesystem writes for secrets or issue snapshots.
- [ ] Verify loopback-only web/API/database listeners and read-only Jira
  integration behavior.

**Acceptance criteria**

- No tokens/client secrets appear in source, bundles, browser storage, logs,
  PostgreSQL, or process arguments.
- No Jira issue snapshot is written to disk or database.
- Disconnect/reset cleanup and loopback binding tests pass.
- No Jira or Confluence write request is sent.

### T029 — Document local setup and operation

**Depends on**: T004–T028.

- [ ] Document prerequisites, Docker/PostgreSQL startup, OAuth/Keychain
  configuration, board setup, run/test commands, refresh/error behavior, and
  reset/teardown.
- [ ] Document out-of-scope capabilities and external Jira setup dependencies.

**Acceptance criteria**

- A developer can follow the documentation from a clean checkout to run the
  fixture-driven prototype.
- Documentation does not include credentials or real project data.
- Missing board/OAuth prerequisites are explicit and live access is described
  as gated.

### T030 — Perform final prototype acceptance review

**Depends on**: T027–T029.

- [ ] Review each FR and SC against implementation and test evidence.
- [ ] Record any unmet external prerequisite and keep live Jira access
  disabled until it is satisfied.
- [ ] Confirm constitution compliance and explicit prototype scope.

**Acceptance criteria**

- SC-001 through SC-012 pass or have a documented approved manual verification.
- No unresolved prototype behavior or constitution violation remains.
- Confluence, Jira writes, LAN/team access, and other excluded features are
  absent.

**Milestone M5**: T027–T030 complete; the local prototype is verified and
documented, with live Jira access enabled only after all external gates pass.
