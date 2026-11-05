# Document templates

Use applicable sections only. Keep facts in their owning document; link instead of repeating.
[SKILL.md](../SKILL.md) owns workflow policy. These examples define content, not heading order.

## README.md

```markdown
# [Project]

[Purpose and prerequisites.]

[Working quickstart and expected result.]

[Documentation](docs/README.md)
```

## docs/README.md

```markdown
# Documentation

| Document                        | Purpose                 |
| ------------------------------- | ----------------------- |
| [Quickstart](../README.md)      | Setup and use           |
| [Requirements](requirements.md) | Behavior and UX         |
| [Design](design.md)             | Architecture            |
| [Operations](operations.md)     | Deployment and recovery |
| [Status](status.md)             | Active work             |
| [Backlog](backlog.md)           | Task index              |
| [Testing](../tests/README.md)   | Checks and environments |
```

## docs/requirements.md

```markdown
# Requirements

## Purpose
[Actors, outcome and scope.]

## UX and contracts
[Supported flows, failures/cancellation, interfaces/configuration and defaults.]

## Constraints
[Lasting project policies. Link pending changes; omit task plans/progress.]
```

## docs/design.md

```markdown
# Design

## Boundaries
[Components, stack and dependency direction.]

## Contracts
[Data flow, protocols, ownership and lifecycle invariants.]

## Decisions
[Material rationale only; link approved requirements and task details.]
```

## docs/operations.md

```markdown
# Operations

## Access
[Prerequisites and permissions.]

## Deploy and update
[Usable commands and observable success.]

## Recover
[Backup/recovery procedures and limits.]
```

## docs/status.md

```markdown
# Current work

Maturity: pre-production.
Baseline: [delivered revision/evidence].
Scope: [active selection and shared limits; link task approvals/evidence].

| Task                            | Phase          | Owner    | Waiting on    | Next                   |
| ------------------------------- | -------------- | -------- | ------------- | ---------------------- |
| [PROJ-017](backlog/PROJ-017.md) | Planning       | worker-a | Plan approval | User reviews proposal  |
| [PROJ-018](backlog/PROJ-018.md) | Implementation | worker-b | —             | Complete owned changes |

Next step: [main's coordination action; retain every ongoing task].
```

Batch evidence/last delivery may be a short link when useful. Task records own approvals,
checklists and detailed evidence; status owns selection, scheduling and shared constraints.

## docs/backlog.md

```markdown
# Backlog

Next new ID: PROJ-019.

## Open

| ID                              | Task                            | State   |
| ------------------------------- | ------------------------------- | ------- |
| [PROJ-017](backlog/PROJ-017.md) | Preserve details during refresh | Clarify |

## Cancelled
[Optional rows with task links; reasons stay in the task.]

## Completed
[Done rows using the same columns; always the final section.]
```

## docs/backlog/<ID>.md

```markdown
# PROJ-017: Preserve details during refresh

Type: bug. State: Clarify.
Approval: plan=pending; delivery=pending.

## Overview

[Problem, why it matters, intended outcome and boundaries. Link useful details below.]

## Tasks

- [ ] [Keep the selected run stable during refresh](#selection-rules).

Verification: [affected risks, checks/permissions, owner and limits].

## Details

### Selection rules

[Only additional decisions, constraints, owners/dependencies or links to existing contracts.]

## Evidence

[Delivered revision, check results/references, review findings and remaining gaps.]
```

Keep Overview and task items readable on their own. Details are optional; omit them and their
links when they add no useful information. Each task item describes an observable result.
Approval owns both gates, conditions/waivers and the reviewed delivery revision.
Values are pending, approved or waived; do not repeat approval in Evidence.
Capture needs title/ID, Type/State, Approval and Overview. Full records also need Tasks with
an acceptance checklist, Verification and Evidence. Section order is flexible; add detail only
where needed. Existing linked plans remain authoritative.

## tests/README.md

```markdown
# Testing

## Local checks
[Relevant unit/smoke commands and prerequisites.]

## Broader checks
[Commands, environments, expected duration and required approval.]

## Limits
[What each check proves and remaining runtime/manual evidence.]
```

## Handoffs

Approval: outcome/decisions; task link; scope/owners; acceptance/test limits; precise gate requested.

Worker: assigned phase/authorization, outcome/contracts; exclusive boundary/dependencies;
done condition; permitted checks/budget;
escalation conditions. Return short outcome/files, decisions needed, evidence references and blockers.

Delivery: outcome/files and delivered diff/revision; verification limits; pending approval/commit; **Next:** exact action/input.
