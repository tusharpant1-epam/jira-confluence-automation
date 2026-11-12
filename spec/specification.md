# Feature Specification: Jira Active Sprint Dashboard

**Feature Branch**: `[001-jira-active-sprint-dashboard]`

**Created**: 2026-11-12

**Status**: Draft

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
   operating normally, **Then** it attempts to refresh Jira data at an interval
   between 5 and 10 minutes.

## Edge Cases

- The configured board identifier is missing, invalid, or the viewer cannot
  access the board.
- No active sprint exists, or Jira reports multiple active sprints for the
  configured board.
- The Jira API is unavailable, rate-limits the request, times out, or returns
  partial results.
- A sprint issue is deleted, moved, or becomes inaccessible between refreshes.
- An issue has no assignee, no story-point value, or an unknown status.
- The configured story-point field is absent, unavailable, or inconsistent
  across issues.
- The rules for identifying blocked issues are not configured or cannot be
  evaluated from the board's workflow.
- A refresh is in progress while the viewer changes filters or navigates the
  dashboard.
- Jira credentials expire or do not represent the viewer whose permissions
  must be enforced.

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
  normal operation and provide the last successful refresh time.
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
  client-side code. The authentication and local credential-storage approach
  MUST be decided before Jira integration is implemented.
- **FR-016**: The system MUST identify the configured board and the rule or
  field used to determine story points and blocked status during setup.
- **FR-017**: The first release MUST run as a local prototype. Network exposure,
  shared-user authentication, and internal deployment behavior MUST NOT be
  assumed until separately specified and reviewed.
- **FR-018**: The system MUST surface unavailable or unknown values distinctly
  from zero or a known value.
- **FR-019**: The system MUST NOT automate Confluence content creation,
  modification, publication, or deletion as part of this feature. Confluence
  behavior requires a separate approved specification.

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

### Open Questions / Needs Clarification

- **Board**: What is the Jira Scrum board name or URL to configure?
- **Authentication**: How should local prototype viewers authenticate to Jira,
  and how will the system preserve each viewer's Jira permissions? The
  requirements imply per-viewer access but do not specify the local identity
  flow.
- **Credential storage**: Which approved local credential or OS credential
  store should be used?
- **Story points**: Which Jira field is authoritative for story points on the
  configured board?
- **Blocked issues**: Which workflow statuses, fields, or other agreed rule
  defines a blocked issue?
- **Multiple active sprints**: If Jira reports more than one active sprint for
  the configured board, should setup fail or should a particular sprint be
  selected?
- **Refresh interpretation**: Is the 5-10 minute cadence measured from refresh
  start or successful completion, and what should viewers see when Jira is
  unavailable?
- **Deployment**: What internal hosting, network exposure, and shared-user
  authentication requirements apply before team-wide deployment?
- **Confluence**: Which Confluence sources, content, user journeys, and
  read/write actions are intended? No Confluence operation is included until
  those requirements are specified.
- **Success targets**: What project-level targets are required for dashboard
  load time, refresh completion, and usability beyond the functional
  acceptance criteria below?

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
- **SC-006**: Under normal operation, successive automatic refresh attempts
  occur no less frequently than every 10 minutes and no more frequently than
  every 5 minutes.
- **SC-007**: In permission tests, no issue unavailable to the viewer in Jira
  appears in the dashboard or its displayed totals.
- **SC-008**: In simulated refresh failure and partial-result tests, the
  dashboard identifies the outcome and does not report a complete successful
  refresh.
- **SC-009**: In first-release acceptance testing, no dashboard action creates,
  edits, or deletes Jira issues or Confluence content.

## Assumptions

- The initial product scope is the Jira active sprint dashboard described in
  `work/jira-dashboard-requirements.md`; broader Jira and Confluence automation
  requires additional feature specifications.
- The configured Jira board is a Scrum board and has at most one active sprint
  for the dashboard's expected operation; handling multiple active sprints
  remains an open decision.
- Jira remains the authoritative source for issue data and issue changes.
- The dashboard is read-only and the first release is a local prototype.
- A viewer must see only Jira issues permitted by that viewer's own Jira
  permissions. The mechanism for doing so must be clarified before integration
  work.
- Story points and blocked status depend on board-specific Jira configuration
  that has not yet been provided.
- No numerical service-level, usability, or performance targets are supplied;
  the measurable criteria above are feature acceptance checks, not production
  SLAs.
- React 18 with Vite, Node.js with Express, and PostgreSQL 15 via Docker are
  project-level technology constraints recorded in `spec/constitution.md`;
  implementation planning belongs in a separate plan artifact.
