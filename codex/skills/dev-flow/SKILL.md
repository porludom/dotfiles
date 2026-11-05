---
name: dev-flow
description: "Explicit team workflow: main orchestrates parallel workers, plan/delivery approvals, proportionate checks and concise repository documentation."
---

# Development Flow

Apply only when invoked, including continuations. Preserve project instructions, execution limits,
uncommitted work and existing approvals. Read status and relevant contracts; resume current work
without replaying completed phases. This skill grants no access or external-action permission.
General output preferences belong in global AGENTS.md; this skill defines workflow rules.

## Repository guidance

On first use, ensure the repository's active AGENTS.md/AGENTS.override.md contains a short,
conditional reference to dev-flow. Preserve other instructions and reuse existing guidance.
During read-only work, report missing guidance without creating or changing files.
Keep portable sources in ~/.dotfiles/codex/ and link individual files into ~/.codex; runtime
state stays local.

## Team and scope

Main only orchestrates: scope outcomes, assign owners, resolve decisions, maintain coordination
records, judge evidence and handle Git. Subagents perform investigation, planning, implementation,
verification and review. Parallelize independent work at every phase, including different tasks
in different phases; dependencies still determine order. If delegation is unavailable/prohibited,
report the limitation and obtain an explicit fallback instead of silently taking over execution.
Prefer suitable built-in roles; custom profiles need a demonstrated recurring benefit. Avoid
redundant agents. Delegated workers execute the assigned phase within handoff authorization,
not the whole workflow: no renewed approval requests, commits, shared tracking edits or further
delegation unless assigned. Escalate decisions to main.

Give each worker an outcome, relevant contracts, exclusive boundary, dependencies, done condition,
check permissions/budget and escalation conditions. One owner delivers code, affected tests and
doc changes. Serialize shared files and host mutations. Reassign a write boundary only after
confirming its previous owner stopped writing or completed the handoff. Workers stop at completion; main resolves
engineering choices and asks the user only about consequential unknowns or insufficient authority.

An incoming task does not replace, pause or change other tasks unless explicitly requested.
Preserve each task's scope, approvals, owners and state; queue conflicting boundaries/resources
and continue independent work. Reuse workers only within coherent assignments; avoid nested
agents without a justified assignment. Use fresh minimal context, not whole-chat forks.

Workers return outcome, changed files, decisions needed, evidence links and blockers. Keep logs
and detailed investigation outside main chat. Main reports decisions, meaningful changes and
results. Supervise long processes with bounded logs and sensible polling, not repeated analysis
of unchanged status. Route worker delay reports through main. Before handoff/compaction,
update the short coordination view.

## Planning and approvals

Default: **plan → user approval → implement/verify → user approval → commit**.
For a new project, agree requirements/UX before architecture. Existing work normally has one
concise plan covering behavior/design, owners/dependencies, acceptance and execution limits.
A worker other than the author reviews substantial plans/change batches for omissions, complexity
and contract risks, reusing existing test evidence. Resolve findings before user review. Implementation approval never grants delivery
approval. Reuse authorization only for its stated scope; reopen consequential amendments.
Freeze writes to the delivered boundary before user review; identify its diff/revision in the
approval record. Relevant subsequent edits invalidate delivery approval and affected check
evidence. Unrelated tasks may continue.

A separate planning phase may be skipped only for a localized, known correction to an approved
contract, with no unresolved decisions or contract changes. Briefly state correction/acceptance;
both user approval gates remain. No size-based exception for refactors, features or config changes.

Both approvals may be skipped only for mechanical documentation/comment edits with no meaning
or behavior change and no external mutation, deployment, deletion or migration. The diff must be
fully inspectable; explicit review requirements override this exception. Tiny edits need no task
record. Any other shortcut requires a user waiver naming its scope and skipped phases.

Match reasoning to uncertainty/impact. Do not invent design exercises, audits or edge cases for
clear work. For refactors, state preserved behavior and intended removals; approve user-visible
losses. Resolve only concrete findings, then stop when acceptance is met. Queue unrelated ideas.
Never weaken acceptance or treat silence/urgency as approval. Commit only when delivery approval
is satisfied or validly waived; a review-pending task is not done.

## Verification

Choose checks from affected behavior/boundaries. Unit and smoke tests need no separate test
approval. **All other tests require explicit user approval before execution**, including
integration, end-to-end and performance/load tests. Smoke means a brief basic health/startup
check, not a relabelled full workflow. Test permission does not grant external access/resources.

Propose non-unit/non-smoke checks together for ready tasks: purpose, expected duration, scope,
limits and why cheaper proof is insufficient. Reuse an existing explicit approval within its
scope; ask before material extensions. Feasibility, if needed, starts with a shared 15-minute
budget, scaled explicitly; it does not waive test approval.

One verification owner reuses worker evidence and adds missing coverage. Record checked
revision/boundary, outcome/reference and relevant later edits once in task evidence. Rerun only
for relevant changes, failures or a named uncovered risk; no reassurance reruns or unrelated
suites. Static/mocked checks do not establish runtime proof. Report remaining gaps and obtain
agreement before reducing acceptance. Markdown changes need relevant reading/link/whitespace
checks, not application tests. Explain what failures were ruled out, not just counts.

## Documentation and tracking

Read only the relevant [template](references/templates.md). Preserve approved linked plans and audited UX; do not
migrate unrelated documents when updating this skill. One authority per fact; link details.

| File | Owns |
| --- | --- |
| README.md | Usable quickstart/prerequisites |
| docs/README.md | Document index |
| docs/requirements.md | Lasting behavior/UX |
| docs/design.md | Stack, architecture/protocols |
| docs/operations.md | Usable deployment, updates/recovery |
| docs/status.md | Active tasks/batches, approvals, owners/order, blockers, evidence limits, next action |
| docs/backlog.md | Concise task index; Completed last |
| docs/backlog/<ID>.md | Scope/checklist, acceptance, decisions, approvals/evidence |
| tests/README.md | Commands, environments/proof boundaries |

Task records use Overview, a short Tasks checklist, optional linked Details and Evidence.
Task owns scope, approvals, acceptance and evidence; status owns concurrent selection/scheduling
and shared constraints. Backlog is a linked ID/title/state index. Review notes contain findings,
not duplicate approval records. Distinguish approved targets from delivered/tested behavior.
Update states when transitions happen, without rewriting plans for every message. At existing
approval/delivery boundaries, briefly review scope, approvals, acceptance and evidence.
No extra plan/progress/handoff files without approval.

/side Capture records only a short task/index entry: outcome, essential constraints/questions
and approval state. Do not select work, implement, change status/contracts or commit. Main
explicitly incorporates side decisions. Return ID/link and stop.

Reserve sequential IDs through exclusive creation; retry collisions without overwriting. Serialize
index edits or re-read/merge/retry, preserving concurrent rows/highest counter. Never reuse IDs.
Split independent outcomes, not code/tests/docs for one outcome. Selection and approval differ.

Types: feature, bug, improvement, refactor, research, docs, maintenance, task.
States: Backlog (captured), Clarify (questions), To Do (scoped/queued), In Progress (authorized
work), Review (plan or delivery awaiting approval), Done (accepted), Cancelled (abandoned).
Task owns state; index mirrors it. Track phase/blockers separately with reasons/unblock conditions.
Postponement returns to Backlog with a reason; preserve cancellation reasons. Done requires
acceptance and resolved approvals. Keep Done rows in final Completed and retain task records.
Compact status only after preserving decisions, conditions, waivers, evidence and unresolved
gaps in task records.

## Maturity, Git and delivery

Default to pre-production until explicit promotion. Preserve the checkout and unrelated work.
Pre-production uses main/existing default branch, no task branches/PRs and no compatibility
unless requested. Update consumers/remove obsolete shims; preserve resource safety/evidence.
Production follows project policy; otherwise one branch per batch and PR/MR when authorized.
Push/create, merge, history rewrite/force-push and remote deletion need applicable authorization.

After the approval rules above are satisfied, make one local task commit unless prohibited;
no routine WIP/planning commits. Do not commit changes that depend on another task’s work awaiting
delivery approval; wait or review the dependent changes together. Main stages only owned hunks, checks the
staged diff and excludes
secrets/generated artifacts. Report inseparable changes. Use a short imperative
`type(scope): outcome`; include task IDs/material limits and approved breaking changes as needed.

Deliver outcome/files, verification limits and pending review/commit disposition. End with
**Next:** and the exact action/input, or finished; do not automatically select another batch.
After every skill refactor, verify every supplied requirement across the skill, supporting files
and global AGENTS.md; report omissions/conflicts. Judge real workflow improvements by time, available token usage,
interruptions, repeated checks and delivered defects, not agent or test counts alone.
