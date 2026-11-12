# Specification Implementation Checklist

**Reviewed**: 2026-11-12
**Specification**: [specification.md](./specification.md)
**Implementation reviewed**: [work/payments-portfolio/](../work/payments-portfolio/)

## Review method and overall result

The implementation root contains only empty placeholder files and `.gitkeep`
markers. The root and app `package.json` files, API `server.ts`, and shared
contracts `index.ts` are all zero bytes. No frontend implementation, test
suite, migrations, Docker Compose file, or executable app configuration was
found.

Consequently, no feature behavior could be run or proven to work. “Not
implemented” means no implementation was found in the reviewed project root;
“Not verifiable” means there is no executable behavior or test evidence to
confirm runtime behavior. Prohibitions are separately identified where the
absence of integrations means no violating behavior was observed, but there
is also no test enforcing the prohibition.

**Overall**: The specified dashboard is not implemented. No acceptance
criterion has been demonstrated to work. Automated tests/builds were not run:
there are no non-empty package manifests or test commands to execute. No live
Jira access was attempted.

## Functional requirements

| ID | Requirement summary | Implemented? | Does it work? / evidence |
|---|---|---|---|
| FR-001 | Browser dashboard for one configured Jira Cloud Scrum board | No | Not verifiable; no frontend or running application. |
| FR-002 | Show only the current active sprint | No | Not verifiable; no sprint selection or Jira data flow. |
| FR-003 | Sprint issue list is the primary view | No | Not verifiable; no UI exists. |
| FR-004 | Show issue key, summary, status, assignee, points, and blocker flag | No | Not verifiable; no issue model or UI exists. |
| FR-005 | Filter and sort by status and assignee | No | Not verifiable; no list or controls exist. |
| FR-006 | Treat Jira Done-category issues as completed | No | Not verifiable; no status mapping or metric logic exists. |
| FR-007 | Distinguish missing estimates from zero and identify unestimated issues | No | Not verifiable; no estimate handling exists. |
| FR-008 | Show sprint progress and remaining work with counts and available points | No | Not verifiable; no metric logic or UI exists. |
| FR-009 | Emphasize blocked issues as the primary risk signal | No | Not verifiable; no blocker mapping or UI exists. |
| FR-010 | Refresh on startup and every five minutes only while open; show last success | No | Not verifiable; no refresh scheduler or dashboard exists. |
| FR-011 | Report refresh errors/partial results; never present them as success | No | Not verifiable; no Jira integration or error states exist. |
| FR-012 | Enforce the current viewer's Jira permissions | No | Not verifiable; no authentication or Jira calls exist. |
| FR-013 | Use documented Jira interfaces; do not scrape or bypass access controls | No | No Jira integration was found, so no scraping/bypass behavior was observed; the requirement is not implemented or covered by tests. |
| FR-014 | Read-only dashboard; do not update Jira issues | No | No Jira integration was found, so no issue-write behavior was observed; the dashboard is absent and the prohibition is not test-enforced. |
| FR-015 | Delegated 3LO; secrets only in backend/macOS Keychain | No | Not verifiable; no OAuth flow, Keychain adapter, or credential handling exists. |
| FR-016 | Identify board and story-point/blocked configuration during setup | No | Not verifiable; no setup UI/API exists. |
| FR-017 | One local user; loopback-only; no LAN/team/mobile/production scope | No | Not verifiable; no app listeners or deployment configuration exist. |
| FR-018 | Distinguish unavailable/unknown values from zero or known values | No | Not verifiable; no data model or rendering exists. |
| FR-019 | No Confluence automation or content access in this feature | No | No Confluence integration was found, so none was observed; there is no test enforcing this exclusion. |
| FR-020 | Manual refresh, no overlap, 30-second request timeout, respect `Retry-After` | No | Not verifiable; no Jira transport or refresh controls exist. |
| FR-021 | Accept, validate, and persist one actual board ID; clear data on change | No | Not verifiable; no setup, persistence, or snapshot lifecycle exists. |
| FR-022 | Configure story-point field and deterministic blocked mapping | No | Not verifiable; no configuration or Jira metadata validation exists. |
| FR-023 | Jira REST API v3/Agile API, pagination, reject incomplete/invalid refreshes | No | Not verifiable; no Jira client or response validation exists. |
| FR-024 | Scope snapshots to active identity and clear them on specified events | No | Not verifiable; no identity or snapshot lifecycle exists. |
| FR-025 | Calculate full-sprint counts, points, coverage, unestimated count, and progress | No | Not verifiable; no metric code exists. |
| FR-026 | Include all Jira-returned sprint issues, including subtasks/types | No | Not verifiable; no issue fetching or filtering exists. |
| FR-027 | Combined status/assignee filters and defined stable sorting | No | Not verifiable; no list, filters, or sort logic exists. |
| FR-028 | Jira issue links, display names, explicit unassigned/unavailable labels | No | Not verifiable; no issue rows exist. |
| FR-029 | Textual blocked state, desktop browser support, WCAG 2.1 AA target | No | Not verifiable; no UI or accessibility/browser tests exist. |
| FR-030 | PostgreSQL 15 for approved metadata only; memory-only snapshots; loopback DB | No | Not verifiable; no database, schema, Docker configuration, or snapshot store exists. |
| FR-031 | Synthetic fixtures and credential-free CI with required edge-case coverage | No | Not verifiable; no tests, fixtures, or CI configuration were found. |
| FR-032 | Show active sprint name/dates and label unavailable dates | No | Not verifiable; no sprint data flow or UI exists. |
| FR-033 | Disconnect clears memory and tokens; reset removes client credentials | No | Not verifiable; no OAuth, Keychain, disconnect, or reset implementation exists. |

## Measurable success criteria

| ID | Success criterion | Passed? | Evidence / gap |
|---|---|---|---|
| SC-001 | Inspect authorized issues and available fields for a configured active sprint | No | No dashboard or Jira integration. |
| SC-002 | Counts match Done and non-Done status categories | No | No metric implementation or tests. |
| SC-003 | Point totals and unestimated issue labels are correct | No | No metric implementation or tests. |
| SC-004 | Status/assignee filters and sorting produce expected results | No | No UI behavior or tests. |
| SC-005 | Blocked issues are identified and emphasized | No | No blocker mapping, UI, or tests. |
| SC-006 | Startup/five-minute refreshes run only while open and do not overlap | No | No scheduler, lifecycle handling, or tests. |
| SC-007 | Unauthorized issues never appear in rows or totals | No | No delegated identity, Jira integration, or permission tests. |
| SC-008 | Failure/partial result clears issue data and reports non-success | No | No refresh implementation or failure tests. |
| SC-009 | No dashboard action writes to Jira or Confluence | No | No integrations or actions exist; the exclusion has not been tested. |
| SC-010 | Sequential synthetic identities remain isolated after cleanup | No | No identity/session implementation or tests. |
| SC-011 | Invalid board and zero/multiple active sprints are handled correctly | No | No setup, Jira metadata, or sprint handling. |
| SC-012 | Synthetic fixtures verify filters, sorting, labels, and blocked unknowns | No | No fixtures or automated tests. |

## User-story acceptance scenarios

| Story / scenario | Implemented? | Does it work? / evidence |
|---|---|---|
| Story 1.1 — Identify active sprint and list required issue fields | No | Not verifiable; no dashboard/data flow. |
| Story 1.2 — Count Done-category issues as completed | No | Not verifiable; no status logic. |
| Story 1.3 — Identify unestimated issues without treating them as zero | No | Not verifiable; no estimate logic. |
| Story 1.4 — Show no-active-sprint state without substituting another sprint | No | Not verifiable; no sprint handling. |
| Story 2.1 — Visually emphasize blocked issues | No | Not verifiable; no blocker mapping/UI. |
| Story 2.2 — Filter by status | No | Not verifiable; no list/filter UI. |
| Story 2.3 — Filter by assignee | No | Not verifiable; no list/filter UI. |
| Story 2.4 — Clear filters to restore full authorized list | No | Not verifiable; no list/filter UI. |
| Story 3.1 — Show completed and remaining issue counts | No | Not verifiable; no metric logic. |
| Story 3.2 — Show completed and remaining point totals | No | Not verifiable; no metric logic. |
| Story 3.3 — Show unestimated count and preserve missing-estimate meaning | No | Not verifiable; no metric logic. |
| Story 4.1 — Exclude issues unavailable to viewer | No | Not verifiable; no Jira identity or data flow. |
| Story 4.2 — Show last successful refresh time | No | Not verifiable; no refresh state/UI. |
| Story 4.3 — Report failed/partial refresh without marking success | No | Not verifiable; no refresh state/UI. |
| Story 4.4 — Refresh every five minutes while open without overlap | No | Not verifiable; no scheduler or lifecycle implementation. |
| Story 4.5 — Clear old rows/metrics after failure, retain last success time | No | Not verifiable; no snapshot or refresh implementation. |

## Edge-case coverage

| Edge case | Implemented? | Does it work? / evidence |
|---|---|---|
| Missing, invalid, inaccessible, or non-Scrum board | No | Not verifiable; no board setup/validation. |
| Zero or multiple active sprints | No | Not verifiable; no sprint handling. |
| Jira unavailable, rate-limited, timed out, or partial response | No | Not verifiable; no Jira transport or refresh handling. |
| Issue deleted, moved, or newly inaccessible | No | Not verifiable; no refresh implementation. |
| Unassigned issue and missing/unavailable fields | No | Not verifiable; no issue model/rendering. |
| Story-point field missing or inaccessible | No | Not verifiable; no field configuration or metrics. |
| Blocked mapping absent or unevaluable | No | Not verifiable; no mapping or unknown-state handling. |
| Refresh completes while filters change | No | Not verifiable; no UI or refresh flow. |
| Credentials expire or are revoked | No | Not verifiable; no OAuth/token lifecycle. |

## Verification summary

- **Source inspection**: Reviewed the project root's tracked file list and all
  non-placeholder files. The six present code/package files are zero bytes.
- **Build/tests**: Not run; no package scripts or test runner are defined.
- **Live Jira checks**: Not run; environment-specific board inputs and OAuth
  prerequisites are not available, and no integration exists.
- **Conclusion**: This repository is still at the project-skeleton stage. The
  specified product behavior remains unimplemented and none of it has been
  runtime-verified.
