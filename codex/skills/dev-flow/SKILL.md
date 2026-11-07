---
name: dev-flow
description: "Scoped development, risk-based reviews and verification budgets."
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
separate approval. Agree local integration checks in the request, a plan or
standing repository permission: commands, time budget, scope and external resource
limits. Reuse that permission; ask again only to extend its limits.

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

## Documentation

Keep only durable documentation that helps someone use, operate or change the
project: quickstart, non-obvious contracts/design decisions, operations/recovery
and check entrypoints. Use existing files; create separate docs only when their
content warrants it. Do not prescribe a directory structure or copy chat history.
Preserve decisions, approval conditions, evidence gaps and next action in chat
before compaction.

## Delegation

When delegating, prefer built-in roles; custom profiles need recurring benefit.
If required delegation is unavailable/prohibited, report it and obtain a fallback.

Give workers outcome, exclusive boundary, dependencies, permitted checks/budget
and done condition in chat with minimal context, not full-chat forks. Workers
return changes, evidence and blockers; they do not delegate unless assigned. Route approval
questions and delays through the coordinator. Reuse workers for coherent assignments;
bound logs and avoid unchanged-status polling or waiting on inactive workers.

## Worktrees and review

Reuse a suitable task-owned worktree before creating one. Include its path,
starting commit, target branch, owner and assigned scope in the chat handoff.
Carry dirty changes only when in scope; never reset or stash another owner's work.

Verify in the worktree with its own environment and outputs. Share download
caches, not editable virtualenvs; preserve shared-resource ownership. Worktree
preparation must not alter live installations.

For review, give the worktree path and recorded base, covering committed,
uncommitted and untracked changes. Open that folder in VS Code for Changes;
compare committed work against the base. The target checkout's owner integrates
through one agreed route and verifies affected behavior. Follow global cleanup
policy; use Codex for managed worktrees and Git for other worktrees.

## Delivery

Follow global Git authorization; pushing, PR creation, history rewrites and remote
deletion need authorization beyond local integration. Review the staged diff and
report inseparable changes. Prefer one task commit with an imperative
`type(scope): outcome` message; no WIP/planning commits.

Deliver outcome, proof limits and commit disposition. Stop at acceptance;
do not select another batch. For workflow changes, use the
[evaluation cases](references/evaluation.md) and report verification limits.
