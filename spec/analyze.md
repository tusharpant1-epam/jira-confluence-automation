# Spec / Plan / Tasks Analysis

**Reviewed**: [specification](./specification.md), [plan](./plan.md),
[tasks](./tasks.md), and [constitution](./constitution.md)
**Review date**: 2026-11-12

## Executive assessment

The plan and task list generally preserve the prototype's most important
boundaries: Jira is read-only, Jira requests are delegated to the connected
identity, issue snapshots are memory-only, and the application is
loopback-only. The 30 tasks are phased, have acceptance criteria, and include
the plan's milestones.

The plan is **not yet fully implementation-ready**. Resolve the high-priority
items below before or during foundation work:

1. Research and verify that Jira OAuth 2.0 (3LO), administrator-approved
   scopes, a local callback, and macOS Keychain can be used together for this
   prototype. Do not treat OAuth implementation as a routine task until this
   gate passes.
2. Define how the backend detects that the dashboard is open so it can stop
   scheduled refreshes when no dashboard is open.
3. Define the local browser session, cookie/CSRF protections, OAuth callback
   protections, and loopback request-origin policy. Loopback-only binding by
   itself does not define browser request security.
4. Define exactly which Jira errors are a failed refresh versus a field-level
   unavailable value, and define the estimate-coverage formula and `Retry-After`
   behavior for manual refresh.
5. Add the missing design artifacts needed to make implementation contracts
   testable: API contract, data model/migration design, OAuth/API research
   decisions, and local setup/quickstart.

These are specification/plan refinements, not reasons to expand the prototype
scope. In particular, keep Confluence, Jira writes, team deployment, and
persistent issue snapshots out of scope.

## Prioritized execution review

The review's ordering principle is to do **small, low-risk, high-leverage
alignment first**, continue independent fixture-only foundation work in
parallel, and keep external/security-sensitive Jira integration behind explicit
gates.

### Completed low-risk, high-gain alignment

- **Canonical implementation root**: Resolved to the existing
  `work/payments-portfolio/` skeleton. The plan's structure and T004 now
  populate that root instead of proposing a duplicate project.
- **Decision timing**: The plan now selects the test runner in Phase 0/T003,
  before Phase 1 configures its scripts.
- **Execution batches**: `tasks.md` now recommends T003 first, T004 and T005
  in parallel, then their dependent setup, while external T001/T002 discovery
  can proceed independently.
- **OAuth stop/go gate**: T002 now includes callback and browser-session
  feasibility/security review before T010 implementation.
- **Node runtime reproducibility**: The plan now pins Node.js 26 LTS at an
  exact patch version rather than using a floating “current LTS” reference.

These are documentation and sequencing changes only; no OAuth credentials,
external Jira calls, or destructive environment operations were performed.

### Recommended next execution order

1. **Parallel discovery, no production data access**: Gather board metadata and
   field mapping inputs (T001), request OAuth approval/security feasibility
   (T002), and finalize tooling (T003). Keep live access disabled.
2. **Cheap local foundation in parallel**: After T003, populate the existing
   frontend/backend skeleton (T004) and add the loopback-only PostgreSQL
   runtime (T005). This delivers runnable structure without waiting on Jira.
3. **Foundation dependents**: Add schema/migrations after T005 (T006), API
   runtime and proxy after T004 (T007), and credential-free CI after T004
   (T008). These paths remain fixture-only.
4. **Gate credential handling**: Proceed with Keychain/OAuth tasks (T009/T010)
   only after T002 documents a viable callback/session/security design.
   Administrator approval may remain pending; if so, continue fixtures without
   enabling live OAuth/API access.
5. **Integrate by dependency**: Complete setup and identity boundaries
   (T011–T013), Jira transport and sprint loading (T014–T016), refresh and
   snapshot lifecycle (T017–T018), and API contract (T019) before frontend
   integration.
6. **Build and verify user value**: Metrics (T020), dashboard shell/list and
   controls (T021–T025), then accessibility/browser verification (T026).
7. **Close release evidence**: Automated acceptance, security/data-boundary
   checks, setup documentation, and acceptance review (T027–T030).

Do not parallelize tasks across a dependency boundary merely to increase
throughput. In particular, OAuth coding, live Jira access, and UI/API
integration carry higher risk than foundation and synthetic-test work.

## Task-by-task complexity, dependencies, and risks

Complexity estimates indicate relative implementation effort and uncertainty,
not elapsed time. Dependencies below summarize the task list; the final column
calls out material risk or a dependency that should be made more explicit.

| Task | Complexity | Dependencies | Risks / assessment |
|---|---|---|---|
| T001 — Confirm Jira board and field configuration | Medium | External input; metadata discovery independent; identity access check after T010 | Board ID, story-point field, and blocker mapping are separate inputs and may be owned by different administrators. Board metadata may be gathered independently; verify access only with the approved OAuth identity. |
| T002 — Obtain Jira OAuth app approval | High | External administrator approval; none listed | Potential schedule blocker. T002 now includes local callback/browser-session feasibility and a security stop/go decision. Keep all live API calls disabled if approval/flow cannot be validated. |
| T003 — Select and record project tooling | Medium | Independent of T001/T002 | Several choices affect every package (Node version, package manager, DB driver, migration tooling, tests, Keychain). Test-runner selection is now in Phase 0/T003; Phase 1 configures the selected runner. |
| T004 — Populate the existing typed web/API workspace | Medium | T003 | Root mismatch is resolved: the plan and task now use the committed `work/payments-portfolio/` skeleton. Confirm implementation continues in this root and does not create another project. |
| T005 — Add loopback-only PostgreSQL 15 runtime | Medium | T003 | Docker volume/reset behavior can delete data unexpectedly. Specify an explicit service/volume-scoped reset; do not use broad Docker prune operations. Validate actual published-port binding. |
| T006 — Add minimal configuration schema and migrations | Medium | T005 | The precise fields, uniqueness, refresh metadata retention, and schema rollback strategy are not modeled in a data artifact. “No issue snapshot tables” should be checked in migration and integration tests. |
| T007 — Add local API runtime and development proxy | Low | T004 | Loopback binding is appropriate, but browser/API origin, CORS/proxy, CSRF, and Host-header/DNS-rebinding policy are not specified. Health endpoint should not reveal configuration or secrets. |
| T008 — Establish credential-free CI checks | Medium | T004 | Keychain integration is macOS-specific; CI runner OS and whether Keychain calls are mocked are unspecified. Ensure CI tests the adapter contract without accessing a developer's real Keychain. |
| T009 — Implement the Keychain credential adapter | High | T002, T003 | Platform permissions, user prompts, item access groups, reset behavior, and error conditions are security-sensitive. OAuth client credentials in Keychain are mandated by the spec, but initial provisioning/reset and local development workflow need a secret-safe procedure. T002's feasibility/security stop-go decision must pass first. |
| T010 — Implement delegated Jira OAuth flow | High | T007, T009, T002 | Highest-risk implementation task. T002 now requires a feasibility/security decision, but its outcome is still pending. Before coding, resolve callback-origin/state lifetime, PKCE, cookie/session/CSRF policy, token refresh/revocation handling, and safe callback failure behavior. |
| T011 — Implement disconnect and credential cleanup | Medium | T009, T010 | Disconnect must clear memory, credentials, timers, and any active request; reset must not delete unrelated Keychain entries or Docker resources. Remote grant revocation is explicitly user-managed, so present that limitation clearly. |
| T012 — Implement board setup and validation | High | T006, T010, T001 | Combines UI, persistence, authorization, Jira metadata, and field mapping validation. Define whether missing optional story points are allowed and validate Boolean-field type/status names before saving. |
| T013 — Verify loopback and identity boundaries | High | T007, T010, T011 | Acceptance criteria cover listener/auth behavior but omit browser-origin and CSRF attacks, cookie flags, callback replay, and local malicious-web requests. Test sequential identity switching (consistent with one identity at a time), not concurrent user sessions. |
| T014 — Implement Jira API transport | High | T003 | API transport needs centralized timeout, pagination, rate-limit and error policy. The 30-second limit is specified per request, but total refresh duration across many pages is not bounded. Ensure redirects cannot forward authorization to an untrusted host. |
| T015 — Load board, active sprint, and sprint metadata | Medium | T012, T014 | Must distinguish board validation errors from Jira transient/API failures. Multiple active sprint behavior is clear; setup and API error response shapes are not. |
| T016 — Fetch and validate complete sprint issue snapshots | High | T014, T015, T001 | Correct pagination, duplicate detection, field-level unavailable values, and snapshot atomicity are central. The spec says missing fields should not drop issues, while schema-invalid responses reject the full refresh; define required versus optional fields precisely. |
| T017 — Implement refresh orchestration | High | T016, T006 | The backend needs a defined signal for dashboard-open/closed state; browser close, tab close, sleep, and lost connection behavior are unspecified. `Retry-After` conflicts with immediate manual retry unless the UI/API reject or defer refresh until the delay expires. |
| T018 — Add identity-scoped in-memory snapshot lifecycle | High | T011, T016, T017 | Single-user identity scope is simpler than multi-tenant but still requires ordering/race rules for identity change during an in-flight request. Shutdown cleanup cannot be relied on after abrupt termination; process memory should naturally disappear and should never be swapped/dumped if that is a required guarantee. |
| T019 — Expose typed read-only dashboard API | High | T015, T016, T017, T018 | No API contract artifact defines routes, payload schemas, error codes, or refresh states. Create one before parallel frontend/backend work. Ensure no unauthorized refresh/status endpoint leaks issue counts. |
| T020 — Implement sprint metric calculations | Medium | T016 | “Estimate coverage” has no numerator/denominator definition. Numeric-but-negative or invalid values are not addressed. Specify whether zero is a valid estimate and define metric behavior for all-unestimated and partially unavailable fields. |
| T021 — Build dashboard shell and state views | Medium | T004, T019 | UI states are well enumerated but copy and transitions are not; spec requires failed refresh clear issue data while preserving last successful timestamp. The task now names a failed-refresh state and explicitly forbids issue details or metrics there. |
| T022 — Build sprint issue list | Medium | T021, T019 | Visual emphasis and row behavior for unknown blocked state, unavailable summary/status, long content, and link safety are not detailed. Ensure Jira links use Jira-provided/validated site URLs, not arbitrary issue data. |
| T023 — Add status/assignee filters and sorting | Medium | T022 | “Single-select status and assignee filters” may mean one value in each simultaneously; task covers this. Define status/assignee ordering/collation and behavior when a refresh removes the selected value. |
| T024 — Add sprint progress and estimate coverage | Medium | T020, T021 | Depends on unresolved estimate coverage definition and field-level availability semantics. Verify labels differentiate estimated totals from complete sprint totals. |
| T025 — Add refresh controls and status | Medium | T021, T019 | Manual refresh under `Retry-After` needs a specified response: disable until allowed, queue, or return a rate-limit state. Ensure refresh-in-progress and failure status are announced to assistive technology. |
| T026 — Verify accessibility and browser support | Medium | T021–T025 | “Current stable” browser versions move over time; define verification date/version capture. WCAG 2.1 AA is a target, but no automated/manual audit method or evidence format is named. |
| T027 — Complete automated acceptance coverage | High | T008, T013–T026 | Acceptance criterion requires SC-001–SC-012 mapping, but no traceability matrix exists. SC-010 now specifies sequential identities; ensure tests disconnect and clean up between identities and assert no residual data. |
| T028 — Verify security and data boundaries | High | T009–T019, T027 | “Inspect filesystem writes” and prove no snapshot persistence need concrete instrumentation/tests. Runtime process arguments should not carry secrets. Security checks should include browser storage, logs, database contents, network bind addresses, and write-call absence. |
| T029 — Document local setup and operation | Low | T004–T028 | Dependency on every implementation task is sensible for final documentation but prevents useful early documentation. Plan needs an explicit README/quickstart artifact and environment-specific setup ownership. |
| T030 — Perform final prototype acceptance review | Medium | T027–T029 | “No unresolved prototype behavior” conflicts with external setup prerequisites if these remain unavailable. Define acceptance as fixture-complete with live integration explicitly gated, not as requiring inaccessible administrator inputs. |

## Dependency and sequencing review

### Strong dependencies represented correctly

- T004 precedes API/UI setup; T005 precedes T006 migrations.
- OAuth approval and Keychain work precede live OAuth (T010).
- Board setup and API transport precede sprint retrieval (T015), which precedes
  complete issue snapshots (T016).
- Snapshot and refresh lifecycle precede the read-only dashboard API (T019).
- Metrics depend on normalized issue data (T020), and UI features depend on
  the dashboard shell/API (T021–T025).
- Final acceptance/security/documentation tasks are downstream of testable
  implementation work.

### Dependencies or gates to make explicit

1. **T001 ↔ T002**: Initial board metadata collection proceeds independently;
   identity-specific access validation is gated on T010, which depends on T002.
2. **T012/T015 versus external prerequisites**: T012 names T001 but not T002;
   its body correctly gates live validation on both. Make the dependency
   machine-readable as `T001, T002, T010` for live setup, while keeping mocked
   setup tests unblocked.
3. **T017 dashboard lifecycle**: T017 has no task that supplies the
   backend with dashboard-open/closed state. Add a task or explicitly revise
   the runtime semantics (for example, refresh only while an authenticated
   dashboard session is actively connected).
4. **T018 and T019 lifecycle API**: Disconnect is in T011, but cancellation of
   in-flight requests and clearing the API response/client state are not
   explicit acceptance criteria. Add them to T011/T018/T019.
5. **T027 traceability**: Add a requirement-to-test matrix mapping every FR and
   SC to task/test evidence; the current acceptance criterion only says every
   SC maps to a check.
6. **T030 release gate**: Separate “fixture prototype accepted” from “live
   Jira integration ready”; T002/T001 may remain pending without invalidating
   fixture-only completion.

## Gaps, contradictions, and missing artifacts across documents

### High priority

- **Implementation root mismatch — resolved**: The plan and T004 now name the
  committed `work/payments-portfolio/` skeleton as canonical and populate it
  rather than creating a duplicate.
- **OAuth feasibility/security design is not closed**: The spec mandates
  delegated Jira 3LO, backend-held client secret, macOS Keychain, and local
  callback but does not define redirect URI feasibility, token lifecycle,
  session cookies, CSRF/state lifetime, callback replay protection, local
  browser origin policy, or how the backend learns the dashboard is open.
  Phase 0 research and a security decision artifact are needed before T010.
- **No API contract artifact**: T019 promises typed routes/contracts, but
  neither the spec nor plan defines endpoints, response/error schemas, or
  auth/session behavior. Add `spec/contracts/` (or an equivalent document)
  before frontend and backend integration.
- **No data-model artifact**: PostgreSQL entities are described only in prose.
  Specify configuration and refresh metadata fields, constraints, retention,
  migrations, and reset semantics before T006. Explicitly exclude issue
  snapshot and credential tables.
- **Refresh cadence/open-state ambiguity**: The spec says refresh every five
  minutes only while the dashboard is open, but the backend scheduler has no
  definition of “open” or behavior on tab close, sleep, network loss, or
  multiple tabs. Define a session/heartbeat or choose a simpler and different
  documented cadence.

### Medium priority

- **Spec and plan test-tool timing — resolved**: Phase 0/T003 selects the
  runner; Phase 1 configures its scripts.
- **Estimate coverage is not mathematically defined**: Specify
  `estimated issue count / authorized sprint issue count` (or the approved
  alternative), treatment of unavailable field values, and whether coverage
  is count- or point-based. Also define handling of negative/non-numeric Jira
  values.
- **Rate-limit manual refresh semantics**: Respecting `Retry-After` is required,
  but immediate manual refresh behavior during that window is not. Specify a
  visible cooldown/rejection/queue policy and test it.
- **Per-request timeout versus whole refresh**: A 30-second request timeout
  applies to each paginated request; there is no whole-refresh deadline or
  maximum page count. Clarify whether the total may exceed 30 seconds and how
  a prolonged refresh affects the next schedule.
- **Errors versus unavailable fields**: FR-023 rejects schema-invalid
  responses, while FR-028 permits field-level unavailable values and does not
  drop issues. Define which response fields are required for an issue to be
  valid and which can be unavailable.
- **Refresh metadata retention**: PostgreSQL stores refresh metadata, but
  retention, maximum history, and whether raw error details are persisted are
  unspecified. Store only sanitized status/timestamps unless more is approved.
- **Node runtime and package configuration — partially resolved**: Plan/tasks
  now require Node.js 26 LTS pinned to an exact patch and a reproducible
  lockfile. T003 still needs to record the selected patch and package manager.
- **Docker reset and CI platforms**: Specify the safe scoped volume reset and
  CI runner OS. Keychain behavior should be tested via a mock/adapter in
  credential-free CI, with real Keychain verification on macOS.
- **Constitution consistency — resolved**: The constitution now narrows the
  prototype cadence to five minutes while the dashboard is open.
- **Acceptance criteria wording — resolved**: SC-010 now specifies sequential
  identity connections with disconnect/cleanup between them.

### Missing or useful artifacts

The current set has constitution, feature specification, clarification,
plan, and tasks. The following artifacts would close execution gaps:

1. **Research/decision record** — Jira OAuth 3LO with a local callback,
   administrator scope set, macOS Keychain library/operations, and browser
   session/security decisions.
2. **Data model** — PostgreSQL configuration/refresh metadata schema,
   constraints, sanitized error fields, migration/reset/retention rules, and
   explicit non-persistence of issue data and credentials.
3. **API contract** — Auth/session behavior, routes, request/response
   schemas, error codes, refresh states, and no-cache/security headers.
4. **Quickstart/setup guide** — local prerequisites, Docker commands, OAuth
   app registration inputs, board setup, run/test/reset, and feature gates.
5. **Requirement-to-test traceability matrix** — mapping FR-001–FR-033 and
   SC-001–SC-012 to unit, contract, integration, accessibility, and browser
   checks.

These can be included as separate `spec/` artifacts or explicitly scheduled
outputs of the plan. They should not duplicate the feature specification.
The implementation-root, test-runner timing, and initial execution-order
findings above have been addressed in the plan/tasks; the remaining artifact
and security-design gaps still need resolution.

## Recommended actions before implementation

1. Finish T002's OAuth callback/session security feasibility decision and
   explicitly keep live access gated.
2. Define dashboard-open detection, browser session/CSRF/origin protections,
   and lifecycle behavior before T017.
3. Add API contract, data model, research decisions, quickstart, and
   requirement-to-test traceability artifacts before their dependent tasks.
4. Clarify estimate coverage, field validation, `Retry-After` manual behavior,
   total refresh duration, and metadata retention.
5. Separate fixture-only milestone acceptance from live Jira readiness so
   administrator approval does not block fixture-backed prototype completion.
