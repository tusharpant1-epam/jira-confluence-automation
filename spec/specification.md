# Feature Specification: Jira Active Sprint Dashboard

**Feature Branch**: `[001-jira-active-sprint-dashboard]`

**Created**: 2026-11-12

**Status**: Clarified prototype scope

**Input**: User description: Build a read-only local browser dashboard for the team's active Jira Cloud sprint, with a path to internal deployment. Source requirements: `work/jira-dashboard-requirements.md`.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Inspect active sprint work (Priority: P1)

As a team member, I want to see the issues in the configured board's currently
active sprint in one place, so I can quickly understand what the team is
working on.

**Why this priority**: The issue list is the primary dashboard view and the
minimum useful outcome of the feature.

**Independent Test**: Configure a Scrum board with an active sprint and verify
that a viewer can inspect its authorized sprint issues and the required issue
details without using any other dashboard feature.

**Acceptance Scenarios**:

1. **Given** a configured Scrum board has an active sprint, **When** an
   authorized viewer opens the dashboard, **Then** the dashboard identifies
   that sprint and lists its issues with issue key, summary, status, assignee,
   available story points, and blocker flag.
2. **Given** an issue is in Jira's Done status category, **When** the sprint
   issue list is shown, **Then** the issue is counted as completed.
3. **Given** an issue has no story-point estimate, **When** the issue and
   sprint totals are displayed, **Then** the issue is identified as
   unestimated and is not counted as having zero points.
4. **Given** the configured board has no active sprint, **When** a viewer
   opens the dashboard, **Then** the dashboard clearly reports that no active
   sprint is available and does not present a past or future sprint as active.

### User Story 2 - Find blocked and relevant issues (Priority: P1)

As a team member, I want to identify blocked issues and narrow the issue list
by status or assignee, so I can focus on work that needs attention.

**Why this priority**: Blocked issues are the agreed primary risk signal, and
basic filtering makes the primary list useful to the whole team.

**Independent Test**: Load sprint issues with varied statuses, assignees, and
blocker flags; verify blocker emphasis and each filter independently.

**Acceptance Scenarios**:

1. **Given** the sprint contains blocked and unblocked issues, **When** the
   dashboard is displayed, **Then** blocked issues are visually emphasized as
   the primary risk signal.
2. **Given** the issue list contains multiple statuses, **When** a viewer
   filters by a status, **Then** only issues matching that status remain
   visible.
3. **Given** the issue list contains multiple assignees, **When** a viewer
   filters by an assignee, **Then** only issues assigned to that person remain
   visible.
4. **Given** a filter is active, **When** the viewer clears it, **Then** the
   full authorized sprint issue list is restored.

### User Story 3 - Understand sprint progress (Priority: P2)

As a team member, I want a concise view of completed and remaining work, so I
can assess sprint progress using both issue counts and estimates where
available.

**Why this priority**: Progress context complements the issue list and blocked
issue signal, but depends on correctly interpreting the sprint's issue data.

**Independent Test**: Provide a sprint fixture containing completed,
incomplete, estimated, and unestimated issues; verify counts, point totals,
and missing-estimate handling.

**Acceptance Scenarios**:

1. **Given** a sprint contains issues in Done and non-Done status categories,
   **When** progress is shown, **Then** completed and remaining issue counts
   are reported using those status categories.
2. **Given** some sprint issues have story points, **When** progress is shown,
   **Then** completed and remaining point totals are shown for available
   estimates.
3. **Given** one or more issues lack story-point estimates, **When** progress
   is shown, **Then** the number of unestimated issues is visible and missing
   estimates are not represented as zero-point estimates.

### User Story 4 - Trust refreshed and permission-scoped data (Priority: P1)

As a viewer, I want to know whether the displayed Jira data is current and
limited to issues I can access, so I can rely on the dashboard without
receiving unauthorized information.

**Why this priority**: The dashboard must preserve Jira access boundaries and
must not disguise failed or stale data as current.

**Independent Test**: Use two Jira permission contexts with different issue
visibility and simulate successful, delayed, and failed refreshes; verify
visible data and refresh status for each case.

**Acceptance Scenarios**:

1. **Given** an issue is not visible to the current viewer in Jira, **When**
   the dashboard loads, **Then** that issue and its details are not disclosed.
2. **Given** a refresh succeeds, **When** the dashboard presents the data,
   **Then** it shows when the data was last refreshed.
3. **Given** a refresh fails or returns only partial data, **When** the viewer
   checks the dashboard, **Then** the failure or partial result is clearly
   indicated and is not presented as a fully successful refresh.
4. **Given** the dashboard is configured for periodic refresh, **When** it is
   open and operating normally, **Then** it begins a refresh every five
   minutes without overlapping an earlier refresh.
5. **Given** a refresh fails, **When** the result is shown, **Then** issue
   details and metrics from an earlier refresh are cleared and the failure is
   shown with the last successful refresh time.

## Edge Cases

- The configured board ID is missing, invalid, inaccessible, or not a Scrum
  board; setup stays incomplete and no issue data is shown.
- No active sprint exists; show an empty state and do not substitute a past or
  future sprint. If more than one active sprint is returned, show a
  configuration error and no sprint data rather than selecting implicitly.
- The Jira API is unavailable, rate-limits the request, times out, or returns
  partial results; clear issue details and metrics, retain only the last
  successful refresh timestamp, and display an actionable error.
- A sprint issue is deleted, moved, or becomes inaccessible; omit it on the
  next complete successful refresh and never use partial responses.
- An issue has no assignee; show “Unassigned”. Missing or unavailable values
  are shown as such, never as zero or as a known value.
- The story-point field is missing or inaccessible; show issue counts and
  mark point totals unavailable. Identify unestimated issues wherever the
  configured field can be read.
- A blocked-issue mapping is absent or cannot be evaluated; show the blocked
  state as “Unknown”, not “Not blocked”, and identify the setup issue.
- If refresh completes while the viewer changes filters, apply the current
  filters to the new complete result.
- Jira credentials expire or are revoked; clear issue data, stop presenting
  the dashboard as current, and require the viewer to reconnect.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a browser dashboard for one configured
  Jira Cloud Scrum board.
- **FR-002**: The system MUST show only the currently active sprint in the
  first release; selecting or comparing past and future sprints is out of
  scope.
- **FR-003**: The system MUST make the sprint issue list the primary dashboard
  view.
- **FR-004**: The system MUST show each available issue's key, summary,
  status, assignee, story points when present, and blocker flag.
- **FR-005**: The system MUST support filtering and sorting the issue list by
  status and assignee.
- **FR-006**: The system MUST treat issues in Jira's Done status category as
  completed.
- **FR-007**: The system MUST distinguish missing story-point estimates from
  zero and identify unestimated issues.
- **FR-008**: The system MUST show sprint progress and remaining work using
  issue counts and story-point totals where estimates are available.
- **FR-009**: The system MUST emphasize blocked issues as the primary risk
  signal. Other risk signals are outside the first-release scope.
- **FR-010**: The system MUST refresh Jira data every 5 to 10 minutes during
  normal operation and provide the last successful refresh time. For the
  prototype, refresh MUST begin on dashboard startup and every five minutes
  while the dashboard is open. It MUST NOT run while the dashboard is closed.
- **FR-011**: The system MUST visibly report refresh errors and partial
  results, and MUST NOT label incomplete or failed data as a successful
  complete refresh.
- **FR-012**: The system MUST enforce the current viewer's Jira issue
  permissions and MUST NOT disclose issues the viewer cannot access in Jira.
- **FR-013**: The system MUST use documented Jira Cloud interfaces and MUST
  NOT scrape Jira's web interface or bypass its access controls.
- **FR-014**: The dashboard MUST be read-only. Issue changes MUST be made in
  Jira; the dashboard MUST NOT update Jira issues in the first release.
- **FR-015**: The system MUST keep Jira credentials out of source code and
  client-side code. The prototype MUST use viewer-delegated Jira Cloud OAuth
  2.0 (3LO) authorization with approved read-only scopes. Tokens MUST be held
  by the backend and stored in macOS Keychain; OAuth client secrets MUST also
  be stored there. Credentials MUST NOT be stored in PostgreSQL, browser
  storage, or application configuration. A viewer MUST reconnect after
  credentials expire or are revoked.
- **FR-016**: The system MUST identify the configured board and the rule or
  field used to determine story points and blocked status during setup.
- **FR-017**: The prototype MUST run for one local OS user and bind only to
  loopback. LAN access, multi-user access, internal/team deployment, mobile
  support, and production hosting MUST be out of scope and separately
  specified and reviewed before implementation.
- **FR-018**: The system MUST surface unavailable or unknown values distinctly
  from zero or a known value.
- **FR-019**: The system MUST NOT automate Confluence content creation,
  modification, publication, or deletion as part of this feature. Confluence
  integration and all Confluence behavior are out of scope for this prototype
  and require a separate approved specification.
- **FR-020**: The system MUST provide a manual refresh action and MUST NOT
  start overlapping refreshes. Jira requests MUST time out after 30 seconds.
  For rate limiting, the system MUST respect Jira's `Retry-After` response
  and MUST NOT label the result successful. Failed refreshes MUST NOT be
  retried automatically; the next attempt is the next scheduled refresh or a
  user-triggered refresh, subject to `Retry-After`.
- **FR-021**: The prototype MUST accept one Jira Scrum board ID during local
  setup, validate that the current viewer can access it, and persist the
  non-secret board configuration locally. The local operator MAY replace the
  configured board through setup; changing it MUST clear the in-memory issue
  result. The actual board ID is an environment-specific setup input and MUST
  NOT be guessed or hard-coded.
- **FR-022**: Setup MUST accept a board-specific story-point field ID when
  available and require a deterministic blocked-issue mapping. The blocked
  mapping MUST be either an explicitly selected Jira Boolean field or a
  configured list of exact Jira status names. If a mapping is unavailable,
  the affected value MUST be shown as “Unknown” or “Unavailable”; the system
  MUST NOT infer that an issue is unblocked.
- **FR-023**: The system MUST use the documented Jira Cloud REST API v3 and
  Jira Software Agile REST API for issue, board, and sprint data. It MUST
  paginate responses and MUST reject an incomplete or schema-invalid refresh
  rather than displaying partial data as a complete sprint.
- **FR-024**: Issue data and metrics MUST be scoped to the currently connected
  Jira identity. The system MUST NOT share issue data or derived aggregates
  between identities. A successful refresh MUST replace the previous
  in-memory issue result; logout, identity change, refresh failure, or process
  shutdown MUST clear that result.
- **FR-025**: The system MUST calculate issue counts over all authorized
  issues in the active sprint, regardless of UI filters. Done-category issues
  are completed; every other returned status category is remaining. Point
  totals MUST sum only available numeric estimates and MUST show estimate
  coverage and the number of unestimated issues. If total estimated points are
  greater than zero, point progress MUST be completed estimated points
  divided by total estimated points; otherwise it MUST be “Unavailable”.
  Missing estimates MUST NOT be treated as zero.
- **FR-026**: The system MUST include all issues Jira returns as members of the
  active sprint; it MUST NOT silently exclude subtasks or issue types.
- **FR-027**: The system MUST support combined single-select status and
  assignee filters, including an explicit “Unassigned” option. It MUST support
  ascending and descending sorting by status or assignee, one sort key at a
  time, with issue key ascending as the default and stable tie-breaker.
  Unassigned values MUST sort last.
- **FR-028**: Each issue row MUST show its key as a link to the corresponding
  Jira issue when a valid URL is available. Assignees MUST use Jira's display
  name; unassigned and unavailable values MUST be explicitly labeled. Missing
  or unreadable fields MUST NOT cause an otherwise authorized issue to be
  omitted; label each unavailable field distinctly.
- **FR-029**: Blocked state MUST be represented by text and not color alone.
  The desktop prototype MUST support current stable Chrome, Firefox, and
  Safari on macOS and target WCAG 2.1 AA for implemented dashboard flows.
  Mobile layout and formal performance SLAs or usability studies are out of
  scope for this prototype.
- **FR-030**: PostgreSQL 15 MUST store only non-secret board setup, field
  mappings, and refresh metadata for the single local user. Jira issue
  snapshots MUST remain in process memory only and MUST NOT be persisted or
  backed up. Credentials MUST remain in macOS Keychain. Clearing local
  application data MUST remove the stored setup and refresh metadata. The
  Docker database port MUST be bound to loopback only.
- **FR-031**: Automated acceptance tests MUST use synthetic Jira fixtures and
  mocked API responses; CI MUST NOT require Jira credentials or real project
  data. Fixtures MUST cover permissions, no/one/multiple active sprints,
  missing estimates, unassigned issues, unknown blocked state, pagination,
  rate limits, and partial failures. A manual live smoke test MAY use a
  user-authorized test board and read-only access.
- **FR-032**: The dashboard MUST identify the active sprint by name and show
  its start/end dates when Jira provides them. Missing dates MUST be labeled
  unavailable.
- **FR-033**: The dashboard MUST provide a disconnect action that clears
  in-memory issue data and removes the viewer's OAuth tokens from Keychain.
  Resetting the local application MUST also remove its stored OAuth client
  credentials. Revoking the app's grant at Atlassian is managed by the user
  through Atlassian account settings.

### Key Entities *(include if feature involves data)*

- **Board**: The configured Scrum board that defines which active sprint and
  issues are in scope.
- **Sprint**: The currently active sprint for the configured board, including
  its identity and active date range when Jira provides them.
- **Issue**: A Jira work item with its key, summary, status category, status,
  assignee, optional story-point estimate, and blocker state.
- **Viewer permission context**: The Jira identity or authorization context
  whose access rules determine which issues may be shown.
- **Refresh result**: The outcome and time of a Jira data refresh, including
  success, partial completion, or failure and any actionable error details.
- **Board configuration**: The non-secret local board ID, configured
  story-point field ID, and blocked-issue mapping required to interpret Jira
  data.

### Prototype Decisions

- Configure one board by its actual Jira board ID; setup validates access and
  Scrum type. No active sprint produces an empty state; multiple active
  sprints produce an error and no issue data.
- Use delegated Jira Cloud OAuth 2.0 (3LO) with administrator-approved
  read-only scopes. The local operator is the only viewer; tokens are kept in
  macOS Keychain and never shared between identities.
- The operator supplies the board's story-point field ID and an explicit
  blocked mapping (a Boolean field or exact status names). Missing mappings
  produce “Unavailable” or “Unknown”, never an inferred zero or unblocked
  state.
- Refresh at startup and every five minutes while the dashboard is open;
  provide manual refresh, prohibit overlap, use a 30-second request timeout,
  and respect `Retry-After`. A failed or partial refresh clears issue details
  and metrics while retaining the last successful timestamp.
- Compute counts over the full authorized sprint, unaffected by filters.
  Done-category issues are complete; other returned statuses are remaining.
  Sum only available numeric estimates, report estimate coverage, and mark
  point progress unavailable when no positive estimated total exists.
- Store only non-secret setup and refresh metadata in local PostgreSQL.
  Issue snapshots are memory-only; no backups or historical issue records are
  part of the prototype.
- Support combined single-value status and assignee filters, sorting by
  either field, issue-key ascending by default, and explicit unassigned and
  unavailable labels. Link issue keys to Jira when a valid URL exists.
- Use synthetic fixtures for automated tests; live Jira smoke testing is
  optional and must use user-authorized read-only access.
- Confluence, team/network deployment, mobile support, backup/recovery,
  audit-history features, formal performance SLAs, and usability studies are
  out of scope. The prototype targets current stable desktop Chrome, Firefox,
  and Safari on macOS and WCAG 2.1 AA for implemented dashboard flows.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For a configured board with one active sprint, a viewer can
  inspect the authorized sprint issue list and all available required fields
  in the dashboard.
- **SC-002**: For test data containing Done and non-Done issues, displayed
  completed and remaining issue counts match Jira's status categories.
- **SC-003**: For test data containing estimated and unestimated issues, point
  totals include only available estimates, and every unestimated issue is
  identifiable without being counted as zero points.
- **SC-004**: For test issues with varied statuses and assignees, each status
  and assignee filter and sort produces the expected matching or ordered
  results.
- **SC-005**: For test data containing blocked and unblocked issues, all
  blocked issues are identified and visually emphasized.
- **SC-006**: While the dashboard is open and Jira is available, a refresh
  begins on initial load and every five minutes thereafter; refreshes do not
  overlap.
- **SC-007**: In permission tests, no issue unavailable to the viewer in Jira
  appears in the dashboard or its displayed totals.
- **SC-008**: In simulated refresh failure and partial-result tests, the
  dashboard identifies the outcome, clears issue details and metrics, and
  does not report a complete successful refresh.
- **SC-009**: In first-release acceptance testing, no dashboard action creates,
  edits, or deletes Jira issues or Confluence content.
- **SC-010**: Tests using synthetic Jira identities with disjoint issue
  permissions confirm that issue rows and all derived metrics are isolated to
  the active identity.
- **SC-011**: Setup rejects an inaccessible/non-Scrum board and does not
  display sprint data when zero or multiple active sprints are returned.
- **SC-012**: Synthetic fixtures verify combined filters, sorting, missing
  estimates, unassigned values, and blocked-state unknowns against the
  specified labels, counts, and ordering.

## Assumptions

- The initial product scope is the Jira active sprint dashboard described in
  `work/jira-dashboard-requirements.md`; broader Jira automation requires
  additional feature specifications.
- The prototype has one local OS user and one connected Jira OAuth identity at
  a time; it binds to loopback only.
- The configured board ID, story-point field (if applicable), and blocked
  mapping are supplied as setup inputs and validated rather than inferred.
- If Jira returns zero active sprints, the UI shows an empty state; if Jira
  returns more than one, the UI shows a configuration error and no sprint
  data.
- Jira remains the authoritative source for issue data and issue changes.
- Each Jira API request uses the currently connected viewer's delegated
  authorization; no shared Jira service credential is used.
- Failed or partial refreshes do not leave earlier issue data visible. No
  issue snapshot is persisted between requests or identities.
- The prototype runs on macOS, uses the OS Keychain for credentials, and
  stores only non-secret setup and refresh metadata in local PostgreSQL.
- Confluence, team/network deployment, mobile layout, backups, audit history,
  performance SLAs, and formal usability studies are out of scope.
- Automated integration tests use synthetic fixtures; live Jira access is an
  optional user-authorized smoke test.
- React 18 with Vite, Node.js with Express, and PostgreSQL 15 via Docker are
  project-level technology constraints recorded in `spec/constitution.md`;
  implementation planning belongs in a separate plan artifact.
