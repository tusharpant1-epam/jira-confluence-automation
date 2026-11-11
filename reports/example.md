# Project Status Report — Illustrative Example

> This is a fictional example to demonstrate the format. Replace all project details with verified information before using it.

## Report details

- **Project:** Jira Sprint Dashboard (sample project)
- **Reporting period:** 2026-11-03 to 2026-11-10
- **Report date:** 2026-11-10
- **Owner:** Delivery lead (sample)
- **Overall status:** Amber

## Summary

The team has clarified the first-release scope for a read-only dashboard focused on the active Jira sprint. Progress is in requirements definition; implementation and access setup are not represented as complete in this example. The board identity and approved credential approach are still open, so the project remains Amber until those dependencies are resolved.

## Progress this period

- Documented the first-release audience, active-sprint scope, and read-only access expectations.
- Defined the issue fields and initial risk signal, including blocked issues and unestimated story points.
- Recorded open setup questions for the board, Jira authentication, and story-point field.

## Plans for next period

- Confirm the Scrum board and how blocked issues are identified — delivery lead — target date to be agreed.
- Agree an approved local credential-storage approach — project owner — target date to be agreed.
- Validate the story-point field and required Jira permissions — implementation owner — target date to be agreed.

## Risks and blockers

| Risk or blocker | Impact | Response / next step | Owner | Due date |
|---|---|---|---|---|
| Board and blocked-issue workflow are not yet confirmed | Dashboard scope and issue queries may need rework | Confirm the board and workflow with the Jira owner before implementation | Delivery lead | To be agreed |
| Authentication and credential storage are undecided | Data access cannot be safely configured | Select an approved identity and local credential-storage approach; do not put credentials in source code | Project owner | To be agreed |

## Decisions or help needed

- Jira owner: confirm the Scrum board and the workflow signal used to identify blocked issues.
- Project owner: approve the authentication and credential-storage approach.

## Milestones

| Milestone | Target date | Status |
|---|---|---|
| Confirm first-release requirements | 2026-11-10 | Complete (sample) |
| Confirm board and access setup | To be agreed | At risk |
| Begin implementation | To be agreed | Not started |
