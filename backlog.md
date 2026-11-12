# Automated Payments Program Workbook — Implementation Backlog

Priorities: **P0** = required for the local MVP or a release gate; **P1** = important MVP capability; **P2** = follow-up or optional improvement. Complete the Setup decisions before locking configuration-dependent behavior. Deliver the local, single-user MVP before considering vendor connectors or shared deployment.

Classification: **custom skill** marks workbook-specific work that is not provided by an existing MCP server; it does not replace the required local application code. No current task is marked **MCP** because the Jira/Confluence connector is deferred pending approval, and those servers do not implement the workbook's local workflows. If connector work is approved, add it as a separate MCP task.

Batch approach: **Approach 1** = a single request for a deliberately bounded set of up to 3–5 files/items; **Approach 2** = iterative rereading for a quality-critical set of 10–15 files/items when automation is not appropriate; **Approach 3** = Script Automation for repeatable or larger batch processing. Use Approach 3 for batch imports, validation, report generation, and repeatable batch tests. Approach 2 is reserved for cases that cannot safely or usefully be automated; no current backlog task meets that condition.

## Setup

- [ ] **[P0] Confirm the project inventory and identifiers:** collect authoritative program names/codes, customer and project inventory, unique project-code conventions, and representative examples. (custom skill; GitHub issue #1)
- [ ] **[P0] Confirm project ownership rules:** agree on one accountable delivery manager per project and whether optional contributors are needed. (custom skill; GitHub issues #2, #19)
- [ ] **[P0] Inspect representative source files:** review up to 3–5 sample project-register and planning/resource/budget CSV/XLSX exports; identify authoritative sources, formats, columns, identifiers, and update frequency. (custom skill; GitHub issue #3; Approach 1: Single Request)
- [ ] **[P0] Define MVP acceptance data:** select a small, curated dataset covering multiple programs, project statuses/RAG values, missing fields, milestones, staffing, and budget data where available. (custom skill; GitHub issues #4, #18; Approach 1: Single Request)
- [ ] **[P0] Agree on local operating constraints:** identify supported operating systems, local application-data location, project-volume target, and dashboard/search response-time target. (custom skill; GitHub issues #5, #17)
- [ ] **[P0] Agree on policy-dependent settings:** assign owners and capture decisions for alert thresholds, reporting week/time zone, retention, backup location, deletion procedure, and success measures; mark undecided values as pending rather than inventing defaults. (custom skill; GitHub issues #6, #16)
- [ ] **[P0] Record integration and privacy boundaries:** confirm that the MVP uses no external AI or network-dependent core workflow, and document that Jira/Microsoft 365 access requires separate approval before connector work begins. (custom skill; GitHub issues #7, #15)
- [ ] **[P1] Establish the project skeleton:** create the local web application structure, configuration approach, development commands, and dependency management for the approved implementation stack. (custom skill; GitHub issues #8, #14)
- [ ] **[P0] Define safe local defaults:** bind the application to loopback only; store application data outside the source repository; prohibit embedded credentials and plain-text secret settings. (custom skill; GitHub issues #9, #11, #13)
- [ ] **[P1] Define data and API contracts:** agree on field names, identifier rules, timestamps/time zone handling, validation-error shape, and API responses for programs, projects, updates, proposals, alerts, and import jobs. (custom skill; GitHub issues #10, #12)

## Core Features

- [ ] **[P0] Implement the local persistence layer:** create and version the SQLite schema for programs, projects, assignments, updates, source references, update proposals, audit events, alert rules/alerts, and import/refresh jobs. (custom skill)
- [ ] **[P0] Enforce register integrity:** require unique project codes and project names, valid program/customer associations, and explicit project ownership; distinguish missing values from zero, healthy, or not applicable. (custom skill)
- [ ] **[P0] Implement program and project management:** support creating, viewing, editing, and archiving programs and projects, including lifecycle/status, RAG, dates, phase, budget, staffing, last update, and next milestone. (custom skill)
- [ ] **[P0] Implement project assignment management:** assign one accountable delivery manager and support contributors if confirmed in Setup. (custom skill)
- [ ] **[P0] Implement project search and filtering:** filter and sort projects by program, customer, delivery manager, status, health, and next milestone. (custom skill)
- [ ] **[P0] Implement project detail views:** show register fields, current accepted updates, linked source references, related proposals, milestones, and audit history. (custom skill)
- [ ] **[P0] Implement update creation:** support decisions, risks, issues, milestones, blockers, scope changes, dependencies, staffing changes, and actions, with appropriate owner, status, dates, severity, title/summary, and detail fields. (custom skill)
- [ ] **[P0] Implement the review queue:** list proposed updates with project association or unresolved match, source details, validation/confidence state where applicable, and duplicate/conflict indicators. (custom skill)
- [ ] **[P0] Implement proposal review actions:** allow the operator to inspect, edit, approve, or reject a proposal; only an approved proposal may create or change an authoritative update. (custom skill)
- [ ] **[P0] Preserve attribution and decisions:** record source system/name, source record ID/link when available, capture/import time, reviewer action, and decision time for accepted or rejected proposals. (custom skill)
- [ ] **[P0] Implement correction and conflict handling:** allow corrections without erasing the original accepted record or audit event; let the operator inspect and resolve duplicate or conflicting proposals. (custom skill)
- [ ] **[P0] Implement audit history:** record actor/process, timestamp, entity, prior and new values, and the source or review action that caused each change. (custom skill)
- [ ] **[P0] Implement portfolio dashboard:** show portfolio health and counts/lists by RAG and status, with drill-down from program and project summaries to underlying updates and sources. (custom skill)
- [ ] **[P0] Implement actionable exception views:** surface overdue/slipping milestones, aging blockers, open RAID items, client escalations, and resource/budget variance only when supporting data exists. (custom skill)
- [ ] **[P0] Implement alert records and navigation:** link every alert to its project and supporting record/source and explain the condition that triggered it. (custom skill)
- [ ] **[P1] Implement configurable alert rules:** support explicit project health, overdue dates, and approved/configured thresholds; do not hard-code unapproved numeric business thresholds. (custom skill)
- [ ] **[P0] Implement the weekly executive summary:** generate an in-app preview covering portfolio health, material changes, at-risk projects, key milestones, blockers/escalations, and decisions/actions needing attention. (custom skill; Approach 3: Script Automation for assembling and validating report inputs)
- [ ] **[P0] Support report review and download:** show reporting period, generation time, and source/update freshness; let the operator correct the preview and download the report. (custom skill; Approach 3: Script Automation for report generation; operator reviews the result)
- [ ] **[P1] Make refresh/import state visible:** show the most recent refresh/import time and job outcome on the dashboard, including actionable failure details. (custom skill)

## Integration

- [ ] **[P0] Connect the browser UI to the local API and database:** wire register, project detail, review queue, dashboard, alert, and report screens to persisted data and handle loading, empty, validation, and error states. (custom skill)
- [ ] **[P0] Implement the user-triggered import workflow:** let the operator select a CSV/XLSX file, identify its source, preview rows, map columns, validate values, and review an acceptance summary before applying changes. (custom skill; Approach 3: Script Automation for batch parsing, preview, and validation; operator confirms application)
- [ ] **[P0] Implement import validation and safe application:** report row-level errors, detect duplicate records and likely repeated updates, prevent silent overwrite of accepted data, and ensure invalid rows cannot cause partial or silent data loss. (custom skill; Approach 3: Script Automation)
- [ ] **[P0] Persist import job details:** record source, start/end time, result, record counts, and actionable errors; make partial failures visible and never display a failed job as successful. (custom skill; Approach 3: Script Automation)
- [ ] **[P0] Convert imported candidates into proposals:** associate import records with project codes and source identifiers where available; leave unresolved or ambiguous project matches in the review queue without guessing or discarding them. (custom skill; Approach 3: Script Automation for batch association; uncertain matches remain for operator review)
- [ ] **[P0] Integrate manual update entry with review and audit flows:** ensure updates created through the UI follow the agreed authoritative-record and traceability rules. (custom skill)
- [ ] **[P0] Integrate dashboard alerts with their evidence:** verify that alert lists, project details, and supporting updates/source references navigate consistently. (custom skill)
- [ ] **[P0] Integrate report generation with reviewed data:** base summaries on authoritative accepted updates, include current data freshness, and ensure corrections to the preview do not silently alter source records. (custom skill; Approach 3: Script Automation)

## Testing

- [ ] **[P0] Test register validation and integrity:** cover unique project codes, required fields, valid program relationships, ownership, archive behavior, and missing-versus-zero handling. (custom skill)
- [ ] **[P0] Test CSV/XLSX import end to end:** cover preview, field mapping, valid and invalid rows, duplicate detection, repeated imports, row-level errors, and preservation of existing accepted values. (custom skill; Approach 3: Script Automation)
- [ ] **[P0] Test proposal approval gates:** verify that imported/proposed information remains non-authoritative until approved, and that edit, reject, unresolved association, and conflict-resolution paths behave correctly. (custom skill)
- [ ] **[P0] Test audit and source traceability:** verify that approvals, edits, rejections, and corrections retain actor/action, timestamp, prior/new values, and source attribution without erasing history. (custom skill)
- [ ] **[P0] Test filters and dashboard drill-down:** verify all required filter fields and that exception counts/lists navigate to the correct project and supporting record. (custom skill)
- [ ] **[P0] Test alert behavior:** verify links and explanations, missing-data behavior, and that unconfigured numeric thresholds do not trigger as if approved. (custom skill)
- [ ] **[P0] Test executive summary output:** verify required sections, reporting period, generation time, freshness, preview corrections, and downloadable output. (custom skill; Approach 3: Script Automation)
- [ ] **[P0] Test import/refresh failures:** verify actionable failure details, partial-failure reporting, and accurate dashboard last-refreshed state. (custom skill; Approach 3: Script Automation)
- [ ] **[P0] Test local-only security defaults:** verify the server binds to loopback, is not reachable from another machine by default, and contains no embedded or plain-text credentials. (custom skill)
- [ ] **[P1] Run acceptance scenarios against the representative dataset:** demonstrate each acceptance criterion with realistic multi-program data, including missing fields and exceptions. (custom skill; Approach 3: Script Automation for repeatable dataset-driven scenarios)
- [ ] **[P1] Validate performance against agreed targets:** measure dashboard and project search using the agreed project volume and record results. (custom skill; Approach 3: Script Automation for repeatable benchmarks)
- [ ] **[P1] Test backup and deletion procedures:** verify the documented approach for backing up and deleting permitted local data and generated reports. (custom skill; Approach 3: Script Automation for repeatable file-operation checks)

## Documentation

- [ ] **[P0] Write local setup and run instructions:** document supported prerequisites, installation, configuration, startup, loopback access, and troubleshooting. (custom skill)
- [ ] **[P0] Document register and import workflows:** explain project-code and ownership rules, supported file formats, column mapping, validation errors, duplicates, and safe import acceptance. (custom skill)
- [ ] **[P0] Document proposal review and audit behavior:** explain approval/rejection, unresolved associations, corrections, conflicts, source attribution, and how to inspect change history. (custom skill)
- [ ] **[P0] Document dashboard, alerts, and reporting:** define displayed signals, configurable-threshold behavior, weekly report period/freshness, preview correction, and download steps. (custom skill)
- [ ] **[P0] Document privacy and local data handling:** state what is stored, where it is stored, what is not transmitted, credential handling, retention decisions, backup, and deletion steps. (custom skill)
- [ ] **[P1] Document known limitations and deferred scope:** explicitly note that automatic source writes, unreviewed authoritative updates, email sending, external AI processing, approved vendor connectors, and shared/network deployment are not part of the local MVP. (custom skill)
- [ ] **[P1] Record release acceptance results:** capture tested acceptance criteria, project-volume/performance results, unresolved policy decisions, and operational handoff items. (custom skill)
