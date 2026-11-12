# Specification Clarification Outcomes

**Reviewed documents**: [constitution](./constitution.md) and
[Jira active sprint dashboard specification](./specification.md)  
**Source requirements**: [Jira dashboard requirements](../work/jira-dashboard-requirements.md)  
**Review date**: 2026-11-12

The questions from the senior review are resolved below for the local
prototype. Decisions and functional behavior are recorded in
[specification.md](./specification.md). Environment-specific values that the
requirements do not provide remain explicit setup prerequisites; they are not
guessed. Items marked out of scope are deferred to a separately specified
release.

| ID | Topic | Resolution |
|---|---|---|
| C-01 | Viewer model and Jira authorization | One local OS user and one connected Jira identity at a time. Use that viewer's delegated OAuth authorization for Jira requests; no shared Jira credential or cross-identity cache. Backend enforces the returned Jira permissions. See FR-015, FR-024. |
| C-02 | Local boundary and team access | Bind to loopback only. LAN access, multiple local viewers, and team-wide deployment are out of scope for this prototype. See FR-017. |
| C-03 | Authentication and credential storage | Use Jira Cloud OAuth 2.0 (3LO) with administrator-approved, least-privilege read-only scopes. The local operator must reconnect after expiry/revocation; disconnect clears local user tokens, and resetting the app removes its OAuth client credentials. Remote grant revocation is managed by the user in Atlassian account settings. Store credentials in macOS Keychain only; admin app registration is a prerequisite. See FR-015, FR-033, and Prototype Setup Dependencies. |
| C-04 | Board setup | Operator enters one actual Jira Scrum board ID during local setup. Validate board type and current-user access. The local operator may replace the configured board through setup, which clears in-memory issue data. Missing/invalid/inaccessible configuration blocks issue display. The actual board ID remains an environment-specific prerequisite. See FR-021. |
| C-05 | Active sprint behavior | Use the active sprint returned for the configured board. Zero active sprints shows an empty state; multiple active sprints show a configuration error and no sprint data. Display sprint name and dates when available. Include all issues returned as sprint members; do not silently exclude issue types. See Edge Cases, FR-026, FR-032. |
| C-06 | Story points | Configure the board's story-point field ID when available; do not assume a universal field. Sum only readable numeric estimates, separately report unestimated count/coverage, and show point metrics as unavailable when the field cannot be read. Point progress is completed estimated points divided by total estimated points only when the total is positive. See FR-022, FR-025. |
| C-07 | Blocked definition | During setup, operator selects either an explicit Boolean Jira field or exact status names as the board's blocked mapping. A missing/unreadable mapping is “Unknown” or “Unavailable”, never “Not blocked”. The actual mapping is a setup prerequisite. See FR-022. |
| C-08 | Progress and scope | Counts use all authorized issues in the active sprint and are independent of list filters. Jira Done-category issues are complete; every other returned status is remaining. Point totals include only available estimates; missing estimates are not zero. See FR-025, FR-026. |
| C-09 | Unavailable fields and issue links | Show explicit “Unassigned”, “Unknown”, or “Unavailable” labels as applicable; do not drop an otherwise visible issue solely because a field is unavailable. Link issue keys to Jira when a valid URL exists, and use Jira display names for assignees. See FR-028 and FR-018. |
| C-10 | Filters and sorting | Combine single-select status and assignee filters; include “Unassigned”. Sort by one of status or assignee, ascending or descending. Default to issue key ascending, use issue key as the stable tie-breaker, and sort unassigned values last. Metrics remain for the full authorized sprint. See FR-025, FR-027. |
| C-11 | Refresh lifecycle | Refresh at startup and every five minutes only while the dashboard is open; also provide manual refresh. Do not overlap refreshes. Each Jira request times out after 30 seconds; respect `Retry-After` on rate limiting and report failure rather than success. Do not retry failed requests automatically beyond the next scheduled or manual refresh. See FR-010, FR-020. |
| C-12 | Stale and partial data | Never render partial results. On failure, clear issue details and metrics, retain only the last successful refresh time, and show an actionable error. Reconnect after expired/revoked credentials. See FR-011 and Edge Cases. |
| C-13 | Persistence and retention | PostgreSQL holds only non-secret board/field configuration and refresh metadata; its Docker port binds to loopback. Issue snapshots are process-memory-only and are cleared on logout, identity change, failed refresh, board change, or shutdown. Tokens are in Keychain. Backup/recovery is out of scope; clearing local app data removes configuration and metadata. See FR-024, FR-030. |
| C-14 | Jira APIs and operational failures | Use documented Jira Cloud REST API v3 and Jira Software Agile REST API; paginate fully. A timeout, rate limit, or incomplete response cannot produce a successful complete snapshot. Issues removed or no longer accessible disappear on the next complete successful refresh. See FR-020, FR-023. |
| C-15 | UX and quality targets | Support current stable desktop Chrome, Firefox, and Safari on macOS; target WCAG 2.1 AA for implemented dashboard flows and identify blocked work with text, not color alone. Mobile support, formal performance SLAs, and usability studies are out of scope. See FR-029. |
| C-16 | Confluence | Confluence integration and all Confluence reads/writes are out of scope for this prototype. A separate specification is required. See FR-019. |
| C-17 | Internal deployment | This specification covers only the single-user, loopback-only prototype. Network/team deployment, shared identity, hosting, concurrency, backup operations, and deployment security review are out of scope and require a separate specification. See FR-017, FR-030. |
| C-18 | Test environment | Automated acceptance tests use synthetic Jira fixtures and mocked API responses for permissions, sprint cardinality, missing estimates, unassigned issues, unknown blocked state, pagination, rate limits, and partial failures. CI requires no Jira credentials or real project content. A live smoke test is optional and must use user-authorized read-only access. See FR-031. |

## Remaining external prerequisites

These are not unanswered product behavior choices; they are values or
approvals that must be supplied before live Jira setup can complete:

1. The actual Jira Cloud Scrum board ID.
2. The board's story-point field ID, if estimates are used.
3. The board's explicit blocked field or exact blocked status names.
4. Jira site-administrator approval and registration of the delegated OAuth
   integration with its least-privilege read-only scopes.

Until these prerequisites are provided and validated, the affected live
integration or metrics remain unavailable. The prototype must not guess
configuration or substitute synthetic data in the live dashboard.

## Explicit prototype exclusions

- Confluence automation and content access.
- More than one local viewer, LAN access, and internal/team deployment.
- Selecting or comparing past/future sprints, and automatic selection among
  multiple active sprints.
- Jira issue writes or automated Jira updates.
- Mobile layout, backup/recovery, audit-history features, and production
  operations.
- Formal performance SLAs and usability studies.
- Real project content or Jira credentials in automated tests or CI.
