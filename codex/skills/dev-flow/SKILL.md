---
name: dev-flow
description: "Explicit plan/delivery approvals, test permissions and task tracking for development work."
---

# Development Flow

Apply only when invoked, including continuations. Follow [global
AGENTS.md](../../AGENTS.md) for common rules; this skill adds process, not
access permissions. Resume assigned tasks/contracts and concurrent status
without replaying completed phases.

## Repository guidance

On first use, ensure active AGENTS.md/AGENTS.override.md conditionally
references dev-flow, preserving other guidance. During read-only work, report
missing guidance without editing it. Keep portable sources in
~/.dotfiles/codex/, linked into ~/.codex; runtime state stays local.

## Team and scope

Main owns workflow coordination and Git. Prefer built-in roles; custom profiles
need recurring benefit. Report the limitation and obtain a fallback if required
delegation is unavailable/prohibited.

Use scoped [handoffs](references/templates.md#worker-handoffs) and minimal
context, not full-chat forks. Workers perform assigned phases, escalate
decisions and stop when finished. They cannot repeat approval requests, commit,
edit shared tracking or delegate unless assigned.

Reuse workers for coherent assignments; reactivate completed workers before
waiting. Bound logs, keep details outside chat and avoid polling unchanged
status. Route worker delays through main; update coordination before
handoff/compaction.

## Planning and approvals

Default: **plan → user approval → implement/verify → user approval → commit**.
Agree new-project requirements/UX before architecture. Plans cover behavior,
owners/dependencies, acceptance and limits; keep clear plans brief. Add design
investigation only for consequential open decisions. Independently review
material design/behavior changes, costly failure risks and explicit requests for
independent review; clear mechanical/type changes need no separate plan review.
Review cohesive batches and resolve findings before user review.

Reuse scoped approvals; implementation approval never grants delivery approval.
Reopen consequential amendments. Freeze each delivered diff/revision for
approval; later edits invalidate its approval without stopping unrelated work.
Never infer approval from silence/urgency. Only meaning-preserving
documentation/comment edits with an inspectable diff and no external mutation,
deployment, deletion or migration may skip both gates. Explicit review
requirements prevail; other shortcuts need a waiver naming scope and skipped
phases.

For refactors, agree behavior, removals and contract changes. For a changed
shared API, include a short caller example and identify where shared behavior
belongs. Acceptance must prove the requested API/ownership structure as well as
output behavior. Honor deletion-before-restructuring requests; moves, wrappers
and extra modes do not satisfy removals. Report net production LOC for
substantial reductions, including replacements; it is evidence, not a quota.
Update affected requirements/design together.

## Verification

Unit and brief health/startup smoke checks need no separate test approval. **All
other tests require explicit approval**, including integration, end-to-end and
load/performance. Do not relabel workflows as smoke. Test permission grants no
external access/resources.

Propose broader checks together: purpose, duration, scope/limits and why cheaper
proof is insufficient. Reuse scoped permission; ask before extending it.
Feasibility starts with a shared 15-minute budget unless explicitly scaled; this
does not waive test approval.

Record the checked revision/diff, result/reference and relevant later edits once
in task evidence. For changed shared APIs, exercise the public caller path and
affected implementations. Markdown needs reading/link/whitespace checks, not
application tests.

## Documentation and tracking

Use the [document map/templates](references/templates.md); do not migrate
unrelated docs. Keep facts with their owner and update only when they change.
Preserve approval history and distinguish approved targets from delivered/tested
behavior. Bounded work may reuse a concise task entry; tiny edits need no
record. Check scope, approvals, acceptance and evidence at gates. Extra
plan/progress/handoff files require approval.

Before compacting status, preserve decisions, conditions, waivers, evidence and
gaps in task records. `/side Capture` creates only a short task/index entry:
outcome, constraints/questions and approval state. Do not select work,
implement, change status/contracts or commit; return ID/link and stop. Main
incorporates side decisions.

## Maturity, Git and delivery

Default to pre-production until explicitly promoted: reuse the default
branch/checkout; no task branches/PRs or compatibility unless requested. Update
consumers/remove obsolete shims; retain resource safety and evidence. Production
follows project policy; otherwise use a branch per batch and PR/MR when
authorized. Push/PR creation, merge, history rewrite and remote deletion need
authorization.

After delivery approval/valid waiver, make one local task commit unless
prohibited; no WIP/planning commits. Do not commit dependencies on unaccepted
work: wait or review together. Main stages owned hunks, checks the staged diff,
excludes secrets/generated artifacts and reports inseparable changes. Use an
imperative `type(scope): outcome`; add task IDs, limits or approved breaking
changes as useful.

Stop at acceptance; queue unrelated ideas. Deliver outcome/files, proof limits
and approval/commit disposition. End with **Next:** exact input/action or
finished; do not select another batch. Validate skill edits against supplied
requirements, supporting files and global AGENTS.md; report conflicts/omissions.
Judge improvements by time, available token usage, interruptions, repeated
checks and defects, not agent/test counts.
