# Documents and records

Use relevant sections; adapt headings/order. Process: [SKILL.md](../SKILL.md).

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
| tests/README.md | Check entrypoint usage, environments and proof limits |

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

Verification: [Risks, selected commands, time budget, external resource limits
and whether plan approval includes these checks.]

## Evidence

[Checked boundary/revision, results/references and gaps.]
```

Capture requires title/ID, Type/State, Approval and Overview; full records add
acceptance, Verification and Evidence. Optional Details hold contracts, decisions
and caller examples. Overview and acceptance must stand alone.

Approval owns gate state (pending/approved/waived), conditions and reviewed revision;
Evidence owns verification. Keep the approved target, implemented boundary, pending
amendments and applicable evidence near the top. Retain superseded decisions and
approvals below as history.

Types: feature, bug, refactor, research, docs, maintenance. Use maintenance for
otherwise unclassified work; leave historical types unchanged.
States: Backlog, Clarify, To Do, In Progress, Review, Done, Cancelled.
Use Review only when awaiting plan/delivery approval; otherwise name the blocker
under the current state with its unblock condition. Authorized work stays In Progress
until only approval remains; add no review-specific states. Postponed work returns
to Backlog with a reason.
Done requires accepted scope and resolved gates. Retain cancellation reasons and
Done records. Progress states milestone and next gate/blocker; any percentage is
an estimate of named scope. Required unverified checks remain incomplete;
unapproved optional work does not reduce progress. 100% means Done.

## Status

```markdown
# Current work

Maturity: pre-production.
Baseline: [Revision/evidence.]
Shared limits: [Constraints; link tasks.]
Integration/index owner: [One chat/agent for this checkout.]

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
