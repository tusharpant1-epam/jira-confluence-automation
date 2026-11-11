# Jira Sprint Dashboard Requirements

## Overview

Build a read-only browser dashboard that helps the team understand progress and risks in its active Jira sprint. The first release is a local prototype, with a path to internal deployment so the whole team can use it.

## Users and access

- **Primary audience:** The whole team.
- **Initial access:** Local prototype.
- **Intended next step:** Internal team deployment.
- **Jira deployment:** Jira Cloud.
- **Permissions:** Each viewer should see data according to their own Jira permissions; the dashboard must not expose issues a viewer cannot access in Jira.
- **Issue updates:** The dashboard is read-only. Changes to issues are made in Jira.

## Scope and sprint rules

- Track one Scrum board; identify the board during setup because its name or URL is not yet known.
- Show the currently active sprint only in the first release.
- Treat issues in Jira's **Done** status category as completed.
- Show story points when available, alongside issue counts.
- Do not treat missing story-point estimates as zero; clearly flag unestimated issues.

## Dashboard experience

- Make the issue list the primary view.
- Include these issue fields:
  - Issue key
  - Summary
  - Status
  - Assignee
  - Story points, when present
  - Blocker flag
- Support sorting and filtering by status and assignee.
- Emphasize blocked issues as the primary risk signal.
- Show overall sprint health using progress and remaining-work information, with both points and issue counts where applicable.
- Refresh Jira data every 5–10 minutes.

## Not in the first release

- Selecting or comparing past and future sprints.
- Updating Jira issues from the dashboard.
- Other risk signals beyond the agreed initial focus on blocked issues.

## Open setup details

- Scrum board name or URL.
- Jira Cloud authentication and local credential-storage approach. Credentials must not be stored in source code.
- The board's story-point field and any details needed to identify blocked issues in its workflow.
- Internal hosting and deployment details for the later team-wide version.
