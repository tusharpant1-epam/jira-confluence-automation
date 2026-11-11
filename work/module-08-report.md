# Module 08 Completion Report

## Tracked Files
.gitignore
README.md
calculator.py
main.py
project_spec.md

## Spec Commit History
7c65f5b Add project specification document outlining application purpose, goals, user access model, and functional requirements

## project_spec.md Contents
# Automated Payments Program Workbook

## 1. Purpose

Define a local web application that gives delivery leadership a consolidated,
reviewable view of customer Payments projects across approximately 20 programs.
The application will bring operational data and important updates together,
surface exceptions, and prepare a weekly executive summary.

The initial operating model is a single-user application on one local machine.
Delivery leads are the intended business users, but simultaneous access by
multiple leads is not part of the initial deployment.

## 2. Goals and outcomes

- Maintain a portfolio register of programs and customer projects.
- Collect key updates from Jira, spreadsheets/planning data, Outlook, Teams,
  and calendars as source access is approved.
- Track decisions, risks, issues, milestones, blockers, scope changes,
  dependencies, staffing, and actions.
- Surface project health and exceptions in a dashboard.
- Require a delivery lead to review proposed updates before they change
  authoritative workbook records.
- Prepare a weekly executive summary focused on portfolio health and exceptions.

Success means less manual status collation, more complete and traceable project
updates, earlier visibility of delivery risks, and a useful weekly summary.
Baseline measures and numeric targets are to be agreed during rollout.

## 3. Users and access model

### Initial user

- One local operator, expected to be a delivery lead or Director of Delivery.
- The operator can view the portfolio, import/refresh source data, review
  proposed updates, edit project records, and generate reports.

### Later users

Other delivery leads are intended stakeholders. A shared, multi-user deployment
would require authentication, role-based access, concurrency controls, and
deployment/security approval; it is explicitly outside the local single-user
MVP.

### Authorization

- The local application binds to the loopback interface and is not exposed to
  the network by default.
- External integrations use approved, least-privilege, read-only access where
  possible.
- Never store credentials in source code or plain-text application settings.
  Use the operating system credential store or the approved identity provider.

## 4. Scope

### In scope

- Approximately 20 programs and their customer projects.
- Project identification by project code.
- Project-to-program relationship and delivery-manager ownership.
- Project status, RAG health, dates, phase, budget, staffing, last update, and
  next milestone.
- Operational update types: decisions, RAID items, milestones, blockers, scope
  changes, dependencies, staffing changes, and actions.
- Manual refresh/import, a review queue, dashboard alerts, and a weekly report.
- Source attribution and change history for accepted updates.

### Out of scope for the initial local release

- Multi-user collaboration or remote/network access.
- Automatic writes back to Jira, Microsoft 365, or planning systems.
- Unreviewed extraction directly changing authoritative records.
- Automatically emailing reports or alerts.
- External AI processing of project content without a separately approved
  provider, data-handling review, and explicit implementation decision.

## 5. Functional requirements

### FR-1: Program and project register

- Create, view, edit, and archive programs and projects.
- Require a unique project code and project name; associate each project with a
  customer and a program.
- Capture project lifecycle/status, RAG health, start/end dates, phase, budget,
  staffing, last update, and next milestone.
- Allow filtering and sorting by program, customer, delivery manager, status,
  health, and next milestone.
- Keep project-level ownership explicit. The recommended default is one
  accountable delivery manager, with optional additional contributors.

### FR-2: Source refresh and import

- Provide a user-triggered **Refresh / Import** workflow; no background refresh
  is required for the initial release.
- Support structured CSV/XLSX imports for project registers and planning data,
  with a preview, field mapping, validation errors, and a summary before data
  is accepted.
- Preserve the source name, import time, and source record identifier where
  available.
- Detect duplicate records and likely repeated updates; do not silently
  overwrite accepted data.
- Design source adapters so Jira and Microsoft 365 connectors can be added
  without changing the core update/review workflow.

### FR-3: Source capture and proposed updates

- Target sources are Jira, spreadsheets/planning tools, Outlook, Teams, and
  calendars.
- Present extracted or imported information as proposed updates associated with
  a project code and source reference.
- Support the update types listed in Scope.
- A delivery lead must be able to review, edit, approve, or reject each
  proposed update. Only approved updates become authoritative workbook records.
- Retain source attribution (source/system, source ID or link when available,
  capture time) with each accepted update.
- If project association or extraction confidence is low, leave the item
  unresolved in the review queue; do not guess or silently discard it.

### FR-4: Update and audit history

- Show the latest accepted status and update for each project.
- Record who/what made each change, when it occurred, the prior and new values,
  and the source or review action that caused it.
- Permit corrections without erasing the original audit history.
- Allow operators to inspect and resolve duplicate or conflicting proposals.

### FR-5: Dashboard and alerts

- Provide a portfolio overview across programs, with drill-down to project
  details and underlying updates.
- Show counts and lists of projects by RAG/status, overdue or slipping
  milestones, aging blockers, open RAID items, resource/budget variance where
  source data exists, and client escalations.
- Surface alerts in the dashboard and link each alert to its project and
  supporting record/source.
- Make alert thresholds configurable. Numeric thresholds are not yet supplied;
  do not hard-code business thresholds. Begin with explicit project health,
  overdue dates, and configured thresholds once approved.
- Clearly distinguish missing data from zero, healthy, or not applicable.

### FR-6: Weekly executive summary

- Generate a weekly summary covering overall portfolio health, material
  changes, at-risk projects, key milestones, blockers/escalations, and
  decisions/actions needing attention.
- Include the reporting period, generation time, and source/update freshness.
- Allow the operator to preview and correct the report before distribution.
- Initial delivery is an in-app preview and downloadable report. Email drafting
  or sending requires a later Microsoft 365 integration and approval.

## 6. Recommended delivery phases

### Phase 0: Access and data discovery

- Confirm project-code conventions, program/project inventory, and delivery
  manager ownership.
- Inspect sample Jira, spreadsheet, and planning exports and map their fields.
- Confirm Microsoft 365/Jira products, tenant policies, API permissions, and
  whether message/calendar content may be stored locally.
- Agree alert thresholds, reporting week/time zone, retention, and success
  measures.

### Phase 1: Local MVP

- Local-only web app with program/project register and portfolio dashboard.
- CSV/XLSX import with preview and validation.
- Manual update entry plus a review queue for imported/proposed updates.
- Track RAID, milestones, blockers, decisions, scope changes, dependencies,
  staffing, and actions with source references and history.
- Dashboard exceptions and configurable alert rules.
- Weekly summary preview and downloadable report.
- Use a small, representative data set for acceptance testing.

### Phase 2: Approved source connectors

- Add Jira and Microsoft 365 connectors after API access, scopes, and data
  retention have been approved.
- Begin with user-initiated refresh and read-only access.
- Convert relevant source records into review-queue proposals; preserve the
  approval gate.
- Add Outlook report drafting only if requested and approved.

### Phase 3: Shared deployment (optional)

- Reassess hosting, identity, role-based access, audit, backup, concurrency,
  and client-data separation before enabling multiple users.

## 7. Recommended technical design

### Application shape

- A local web application accessed in a browser on the operator's machine.
- Recommended initial stack: Python with FastAPI for the local API and
  background/import orchestration; a lightweight browser UI; SQLite for local
  structured data.
- Keep source-specific connectors behind adapters and keep the workbook
  records/review workflow independent of any single vendor.
- Bind to localhost only. Do not expose a port on the LAN by default.
- Avoid requiring a cloud service for core register, import, review, dashboard,
  or report functionality.

### Data storage

- Store the database and any permitted local source material in an
  application-data directory, not in the source-code repository.
- Prefer retaining extracted/approved update text and source references over
  copying entire email, chat, or calendar contents. Full-content retention
  requires explicit policy approval.
- Protect local files using operating-system account permissions and
  device-level disk encryption. Provide a documented backup/export and
  deletion procedure.
- Keep secrets in the OS credential store. Do not log credentials or
  unnecessary message content.

### Proposed core entities

- **Program**: ID, name/code, customer or portfolio grouping, status.
- **Project**: project code, name, program, customer, lifecycle/status, RAG,
  dates, phase, budget, staffing, last update, next milestone.
- **Project assignment**: project, accountable delivery manager, optional
  contributors.
- **Update**: project, type, title/summary, detail, owner, status, due date,
  severity, created/updated timestamps.
- **Source reference**: source system, source record ID/link, capture time,
  import/refresh job.
- **Update proposal**: extracted/imported candidate, project match, confidence
  or validation state, reviewer decision, and decision time.
- **Audit event**: entity, prior/new values, actor or process, timestamp, and
  reason/source.
- **Alert rule/alert**: metric/condition, configured threshold, scope,
  lifecycle state, and linked project/update.
- **Import/refresh job**: source, start/end time, result, record counts, and
  actionable errors.

### Integration boundaries

- Use documented Jira and Microsoft Graph APIs only after organization
  approval; do not scrape web interfaces.
- Request the minimum read permissions required. Keep authentication
  user-delegated unless IT approves another model.
- Make refreshes idempotent where source IDs allow it and report partial
  failures; do not present a failed refresh as successful.
- The extraction implementation (rules, local model, or approved enterprise
  service) remains a decision. Any extraction must produce reviewable
  proposals, not direct writes.

## 8. Non-functional requirements

- **Privacy:** Do not transmit project communications to an external AI or
  service by default. Any exception requires approval.
- **Security:** Localhost-only default, OS-protected storage, no embedded
  secrets, and least-privilege connector scopes.
- **Traceability:** Every accepted update and generated report can be traced to
  its source and review/change history.
- **Reliability:** Validate imports before applying them; provide clear errors
  and avoid partial, silent data loss.
- **Usability:** A delivery lead can identify exceptions, inspect supporting
  information, and approve or correct proposals from the main workflow.
- **Performance:** Dashboard and project search should remain responsive for
  the agreed portfolio size. Confirm an explicit project-count and response
  time target using the actual project inventory before release.
- **Portability:** Core local operation should not depend on network access;
  source refresh and email features may require network access.

## 9. Acceptance criteria

1. The operator can create/import programs and projects and identify each
   project unambiguously by project code.
2. The dashboard can filter projects by program, delivery manager, status,
   health, and milestone, and drill down to project updates.
3. Supported update types can be created or imported as proposals and are not
   authoritative until a lead approves them.
4. Approving, editing, rejecting, and correcting updates leaves traceable
   history and source attribution.
5. Invalid imports show row-level errors and do not silently overwrite valid
   existing records.
6. Alerts link to their underlying project and explain the triggering
   condition; unconfigured numeric thresholds are not treated as agreed policy.
7. The weekly summary can be previewed, corrected, and downloaded, and
   identifies its reporting period and data freshness.
8. The local app is not reachable by another machine on the network by
   default; credentials are not stored in source code or plain text.
9. Refresh/import errors are visible, and the dashboard indicates when data was
   last refreshed.

## 10. Open decisions and dependencies

1. What are the authoritative program names/codes, project codes, and
   customer/project inventory?
2. Does each project have one accountable delivery manager, multiple
   co-owners, or an assignment to every DM? The recommended model is one
   accountable DM with optional contributors.
3. Which planning/resource/budget systems and spreadsheet formats are
   authoritative?
4. Is Jira Cloud or Data Center in use, and which projects/fields/statuses
   represent milestones, blockers, estimates, and client escalations?
5. Are Outlook, Teams, and calendar APIs permitted, and which data types may be
   read and stored locally?
6. What constitutes a material milestone slip, an aging blocker, a red RAID
   item, and budget/resource variance? Who owns threshold approval?
7. What reporting week, time zone, recipients, and report format are required?
8. Is automated extraction expected to use approved enterprise AI, a local
   model, or deterministic/rule-based processing?
9. What local retention period, backup location, and deletion policy apply to
   source content and generated reports?
10. Which operating systems must the local app support, and what project volume
    and dashboard response-time target should be validated?

## 11. Assumptions recorded from the interview

- The portfolio has roughly 20 customer programs and includes Payments
  projects managed in Jira.
- Projects are identified by project code and associated with delivery
  manager(s).
- The product is a local-machine web app with one initial user and manual,
  user-triggered refresh.
- Delivery leads are intended to review the dashboard and update critical
  points.
- Updates from source content must go through a review queue before becoming
  authoritative.
- The initial critical update types are decisions, risks/issues, milestones,
  blockers, scope changes, dependencies, staffing, and actions.
- Required dashboard signals include milestone slippage, aging blockers, RAID
  status, budget/resource variance, and client escalations.
- The requested recurring report is a weekly executive summary.
- The organization has not yet specified source API permissions, numerical
  alert thresholds, report recipients, or content-retention policy.
