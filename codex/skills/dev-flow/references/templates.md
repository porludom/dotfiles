# Documents and records

Process: [SKILL.md](../SKILL.md). Common rules: [global AGENTS.md](../../../AGENTS.md).
Use relevant sections; adapt headings/order.
Preserve existing plans, approvals and concurrent entries.

## Document map

| File | Owns |
| --- | --- |
| README.md | Quickstart/prerequisites |
| docs/README.md | Document links |
| docs/requirements.md | Lasting behavior/UX/constraints |
| docs/design.md | Architecture, protocols and rationale |
| docs/operations.md | Deployment, updates and recovery |
| docs/status.md | Concurrent owners, dependencies, shared constraints and coordination |
| docs/backlog.md | Ordered task links/queue; Completed last |
| docs/backlog/<ID>.md | Scope, state/progress, acceptance, decisions, approvals and evidence |
| tests/README.md | Check commands, environments and proof limits |

Selection is not approval. One outcome has one task, including code/tests/docs. Review notes hold
findings, not copied approvals. Status/backlog link tasks rather than copying their state/progress.

## Task record

```markdown
# PROJ-017: Outcome

Type: bug. State: Clarify.
Approval: plan=pending; delivery=pending.
Progress: Input selection unresolved; next: clarify requirements.

## Overview

[Problem, outcome and scope.]

## Tasks

- [ ] [Observable behavior and requested API/ownership structure, if changed.]

Verification: [Risks, permitted checks and limits.]

## Evidence

[Checked boundary/revision, results/references and gaps.]
```

Capture needs title/ID, Type/State, Approval and Overview. Full records add acceptance, Verification
and Evidence. Optional Details hold decisions/contracts/dependencies and caller examples; Overview
and checklist must read independently. Approval owns gates (pending/approved/waived), conditions
and reviewed diff/revision; do not duplicate them in Evidence.

Types: feature, bug, improvement, refactor, research, docs, maintenance, task.
States: Backlog (captured/queued), Clarify (questions), To Do (scoped), In Progress (authorized work),
Review (awaiting plan/delivery approval), Done (accepted), Cancelled (abandoned).

Use Review when only waiting; ongoing authorized work stays In Progress with its pending gate named.
Add no review-specific states. Record blockers/unblock conditions. Postponement returns to Backlog
with a reason; retain cancellation reasons and Done records. Done requires accepted scope/resolved gates.

Progress: `milestone; next gate/blocker`. Optional percentages estimate selected work, not checkboxes
or fixed state values; label phase-only estimates. Deferred required checks remain incomplete;
unapproved optional work does not reduce progress. Revise estimates on scope change, retain them
while blocked and name the blocker. 100% means Done, without strengthening proof limits.

## Status

```markdown
# Current work

Maturity: pre-production.
Baseline: [Revision/evidence.]
Shared limits: [Constraints; link tasks.]

| Task | Owner/chat | Checkout / write boundary | Dependency/resource | Coordination |
| --- | --- | --- | --- | --- |
| [PROJ-017](backlog/PROJ-017.md) | chat-a | checkout A: src/feature/ | Shared host | Wait for PROJ-016 to release it |
```

## Backlog

```markdown
# Backlog

Next new ID: PROJ-018.

## Open

| ID | Task |
| --- | --- |
| [PROJ-017](backlog/PROJ-017.md) | Outcome |

## Cancelled

[Optional; same columns.]

## Completed

[Accepted task links; same columns.]
```

Reserve IDs by exclusive creation; retry collisions, never overwrite/reuse. Serialize index writes
or re-read/merge/retry, preserving concurrent rows and the highest counter.

## Worker handoffs

Assign phase, outcome/contracts, exclusive boundary, dependencies, done condition, permitted checks/
budget and escalation conditions. Return outcome, changed files, decisions, evidence and blockers.
