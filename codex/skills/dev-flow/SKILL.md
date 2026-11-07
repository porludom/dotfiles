---
name: dev-flow
description: "Scoped development, risk-based reviews, verification budgets and task tracking."
---

# Development flow

Apply only when invoked, including continuations. Inherit common rules from
`~/.codex/AGENTS.md`; this skill grants no access permissions. Resume the assigned
task and current coordination state without replaying completed phases.

## Approvals

A bounded action request authorizes implementation and routine verification.
Ask for a plan decision only when consequential choices remain unresolved or the
user requests a plan first. Agree new-project requirements/UX before architecture.
Plans state behavior, owners/dependencies, acceptance and verification limits.
Require design review for consequential shared-contract decisions and independent
implementation review for consequential runtime risks; otherwise use owner
verification. Explicit review requests prevail. Resolve findings before delivery.

Reuse approval within its scope/time limits; never infer it from silence or
urgency. Reopen consequential amendments. Commit authorization remains explicit
and may be granted with implementation. When delivery approval is requested,
freeze its diff/revision; relevant edits invalidate only the affected approval.
Waivers name scope and skipped phases.

For refactors, agree behavior, removals and contract changes; use the proposal required
by global guidance. Define acceptance for caller paths and responsibility
boundaries; justify retained abstractions. Repeated ownership corrections require
a coherent design amendment before further implementation. Moves, wrappers and
extra modes do not satisfy deletions; honor deletion-before-restructuring requests.
For substantial reductions, report remaining caller responsibilities and net production LOC, including
replacements; LOC is evidence, not a quota.

## Verification

Unless restricted, unit, lint/type and brief health/startup smoke checks need no
separate approval. Include selected local integration checks in the plan with
purpose/commands, time budget, scope and external resource limits. Plan approval
includes that package unless excluded; ask again only to extend its limits.

Repositories may record an explicitly approved standing offline verification
budget in existing guidance: commands, per-task time/resource limits and expiry
or revocation conditions. Reuse it within scope; do not infer one from past runs.
Task-specific restrictions override standing permission.

Other integration, end-to-end and load/performance tests need explicit approval;
propose them together and explain why cheaper proof is insufficient. Keep separate
GPU-experiment and deployment gates. Do not relabel tests as smoke or treat test
approval as external access. After 15 minutes of elapsed investigation, report
findings and propose further work unless a larger budget is approved. This is
not a task limit or test authorization.

Record checked revision/diff, results/references and relevant later edits once in
task evidence. Shared API changes must exercise public callers and affected
implementations. Markdown needs reading/link/whitespace checks, not app tests.

## Records

Use the [document map/templates](references/templates.md), preserving unrelated
docs. Keep each fact with its owner. Bounded work may use a concise task entry;
tiny edits need none. Create extra plan/progress/handoff files only when requested
or necessary; prefer existing records.
Check scope, approvals, acceptance and evidence at gates; preserve decisions,
conditions, waivers and gaps before compaction.

`/side Capture` creates only a task/index entry with outcome, constraints/questions
and approval state. Return its ID/link and stop; do not select work, implement,
change existing status/contracts or commit. Main incorporates side decisions.

## Delegation

Main coordinates; the checkout's integration owner controls Git under global
ownership rules. Prefer built-in roles; custom profiles need recurring benefit.
If required delegation is unavailable/prohibited, report it and obtain a fallback.

Use scoped [handoffs](references/templates.md#worker-handoffs) with minimal context,
not full-chat forks. Workers stop after assigned phases and return decisions/blockers;
they cannot repeat approval requests, commit, edit shared tracking or delegate
unless assigned. Reuse workers for coherent assignments; route delays through
main. Bound logs, avoid unchanged-status polling and waiting on inactive workers;
update coordination before handoff/compaction.

## Git and delivery

Default to pre-production until promoted: reuse the default checkout/branch;
no task branches/PRs or compatibility unless requested. Update consumers and remove
obsolete shims, retaining resource safety and evidence. For production, follow
project policy; absent one, use a branch per batch and an authorized PR/MR.
Push, PR creation, merge, history rewrite and remote deletion need authorization.

Commit only when explicitly authorized, after required verification and any
requested delivery approval; make one local task commit unless prohibited;
no WIP/planning commits or dependencies on unaccepted work. Wait or review dependent
work together. The integration owner stages owned hunks, reviews the staged diff,
excludes secrets/generated artifacts and reports inseparable changes. Use an
imperative `type(scope): outcome`, adding task IDs/limits/breaking changes as useful.

Deliver outcome/files, proof limits and approval/commit disposition. Stop at
acceptance; queue unrelated ideas. End with **Next:** exact action/input or finished;
do not select another batch. For workflow changes, use the
[evaluation cases](references/evaluation.md) and report verification limits.
