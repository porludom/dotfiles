---
name: dev-flow
description: "Scoped development, risk-based reviews and verification permissions."
---

# Development flow

Apply only when explicitly invoked, including continuations. Inherit global
`~/.codex/AGENTS.md`; this skill grants no access or Git permissions. Resume current
state without replaying completed phases. Read only the applicable guidance below.

## Approvals

Reuse approval within its scope; silence or urgency is not approval. Reopen
consequential amendments. Delivery approval binds the reviewed diff/revision;
relevant edits invalidate only affected approval. Waivers name scope/skipped phases.

## Reviews and checks

- For consequential shared-contract/runtime decisions, new-project planning or a
  requested plan/delivery review, read [review boundaries](references/reviews.md).
- Unit, lint/type and brief health/startup smoke checks need no separate approval
  unless restricted. For integration/end-to-end/load/performance/GPU tests or a
  standing offline permission, read [check permissions](references/checks.md).
- Shared API checks cover public callers/implementations. Markdown needs diff,
  link and whitespace checks, not app tests. For workflow/guidance changes only,
  use [evaluation cases](references/evaluation.md) and state proof limits.

## Documentation and handoffs

Keep durable quickstart, non-obvious contracts/rationale, operating/recovery and
check instructions where useful. Prefer existing files; prescribe no directory
structure or copied chat history. Before compaction retain decisions, approval
conditions, evidence gaps and next action in chat.

When delegating, prefer built-in roles; custom profiles need recurring benefit.
Give workers outcome, exclusive boundary, dependencies, checks/resource limits
and done condition in chat with minimal context. They return changes/evidence/blockers and
do not delegate unless assigned. Route approval questions/delays through the
coordinator; reuse workers and avoid unchanged polling or waiting on inactive ones.
If required delegation is unavailable/prohibited, obtain a fallback.

## Worktrees and delivery

Include task worktree path, base, target branch, owner and scope in the handoff.
Carry only owned changes; never reset/stash another owner's work. Use a worktree's
own environment/outputs, sharing download caches, not editable virtualenvs or live
installations. Review committed, uncommitted and untracked work against its base;
open that folder in VS Code for Changes. Use Codex for managed worktrees, Git for
others; global policy owns integration and cleanup.

Review the staged diff and report inseparable changes. Prefer one task commit with
an imperative `type(scope): outcome`; no WIP/planning commits. PR creation and remote
deletion need authorization. Deliver outcome, proof limits and commit disposition;
stop at acceptance without selecting another batch.
