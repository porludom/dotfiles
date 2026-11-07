---
name: dev-flow
description: "Scoped development, risk-based reviews, verification budgets and task tracking."
---

# Development flow

Apply only when invoked, including continuations. Global `~/.codex/AGENTS.md`
owns common policy, including ownership, verification evidence, local integration,
commits and worktree cleanup. This skill adds the workflow below; it grants no
access permissions. Resume current task state without replaying completed phases.

## Approvals

Ask for a plan decision only when consequential choices remain unresolved or the
user requests a plan first. Agree new-project requirements/UX before architecture.
Plans state behavior, owners/dependencies, acceptance and verification limits.
Require design review for consequential shared-contract decisions and independent
implementation review for consequential runtime risks. Resolve findings before delivery.

Reuse approval within its scope/time limits; never infer it from silence or
urgency. Reopen consequential amendments. When delivery approval is requested,
identify its diff/revision; relevant edits invalidate only the affected approval.
Waivers name scope and skipped phases.

## Verification

Unless restricted, unit, lint/type and brief health/startup smoke checks need no
separate approval. Include selected local integration checks in the plan with
purpose/commands, time budget, scope and external resource limits. Plan approval
includes that package unless excluded; ask again only to extend its limits.

Reuse explicitly approved standing offline budgets within their listed commands,
time/resource limits and validity; past runs do not establish permission.
Task-specific restrictions prevail.

Other integration, end-to-end and load/performance tests need explicit approval;
propose them together and explain why cheaper proof is insufficient. Keep separate
GPU-experiment and deployment gates. Do not relabel tests as smoke or treat test
approval as external access. After 15 minutes of elapsed investigation, report
findings and propose further work unless a larger budget is approved. This is
not a task limit or test authorization.

Shared API checks cover public callers and affected implementations. For Markdown,
read the diff and check links/whitespace; do not run app tests.

## Records

Use the [document map/templates](references/templates.md) when recording work.
Keep each fact with its owner. Bounded work may use a concise task entry;
tiny edits need none. Create extra plan/progress/handoff files only when requested
or necessary; prefer existing records.
Preserve decisions, approval conditions, evidence gaps and next action before compaction.

`/side Capture` creates only a task/index entry with outcome, constraints/questions
and approval state. Return its ID/link and stop; do not select work, implement,
change existing status/contracts or commit. Main incorporates side decisions.

## Delegation

When delegating, prefer built-in roles; custom profiles need recurring benefit.
If required delegation is unavailable/prohibited, report it and obtain a fallback.

Use scoped [handoffs](references/templates.md#worker-handoffs) with minimal context,
not full-chat forks. Workers stop after assigned phases and return decisions/blockers;
they do not edit shared tracking or delegate unless assigned. Route approval
questions and delays through the coordinator. Reuse workers for coherent assignments;
bound logs and avoid unchanged-status polling or waiting on inactive workers.

## Delivery

Follow global Git authorization; pushing, PR creation, history rewrites and remote
deletion need authorization beyond local integration. Review the staged diff and
report inseparable changes. Prefer one task commit with an imperative
`type(scope): outcome` message; no WIP/planning commits.

Deliver outcome, proof limits and commit disposition. Stop at acceptance;
do not select another batch. For workflow changes, use the
[evaluation cases](references/evaluation.md) and report verification limits.
