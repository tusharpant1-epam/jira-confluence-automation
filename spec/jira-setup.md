# Jira Environment Setup Inputs

This file records non-secret, environment-specific values for the local
prototype. Do not put passwords, OAuth tokens, client secrets, or other
credentials here. Do not guess missing values.

## Board configuration

| Input | Value | Status |
|---|---|---|
| Jira Cloud site URL | Not provided | Pending |
| Scrum board ID | Not provided | Pending |
| Story-point field ID | Not provided; confirm whether estimates are unused | Pending |
| Blocked mapping | Not provided; supply a Boolean field ID or exact status name(s) | Pending |
| Board type and metadata validation | Not verified; requires board ID and an authorized metadata source | Pending |
| Access validation for the prototype identity | Not verified; gated on approved OAuth setup and T010 | Pending |

## Readiness

T001 is **blocked pending operator input**. Live Jira setup and board-specific
metrics remain disabled until the required values are supplied and validated.
No board, field, or status values have been inferred.

Update this file with the supplied values and verification evidence when
available. Keep OAuth approval and credentials out of this record.
