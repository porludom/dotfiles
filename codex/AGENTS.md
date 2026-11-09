# Working agreements

Apply sections by intent: an action request phrased as a question is still an action.

## General

- Use English unless asked otherwise. Keep responses, docs and code concise;
  distinguish facts, assumptions and verification limits.
- Respect scope, permissions, approvals and ownership; preserve unrelated work.
  Challenge unnecessary work, considering runtime, tokens and maintenance.
- Read only task-relevant guidance: architecture for boundary changes, operations
  for deployment/recovery, check instructions for verification. Load skills and
  supporting references only when their workflow applies, not every linked file.
- Check tool/device feasibility early; choose the cheapest useful experiment and
  report setup friction before expanding it. Report stalls with elapsed/expected
  time, blocker, next action and useful user help.
- Operational updates distinguish implemented, committed, prepared, deployed and
  verified; name revision/host when relevant, without a boilerplate checklist.
- Answer explanations/research read-only as needed; clarify consequential gaps.
  Mentioning code alone does not authorize implementation or tests. Keep progress,
  approvals and handoffs in chat; no tracking documents unless requested.

## Changes and verification

- Follow the applicable [Google style guide](https://google.github.io/styleguide/).
  Comment only non-obvious rationale, constraints or pitfalls.
- Format changed files with the repository/editor-configured formatter, including
  JSON/JSONC, shell, YAML and similar formats. Use readily available tools; avoid
  costly setup just for formatting, and report any files left unformatted.
- Reuse repository check entrypoints and consolidate repeated commands. For Python,
  otherwise use `uvx ruff check` and `uvx mypy` with repository configuration.
  Keep costly/remote checks explicit.
- Before nontrivial changes, assess responsibilities, reuse, alternatives and
  failure costs; define observable acceptance and critical invariants, then verify
  those exact paths. Small fixes need no extra plans, records or approval gates.
- Before significant UI layout/navigation changes, show a realistic mockup and agree
  direction; reuse approved designs or explicit waivers. Minor copy/button fixes
  stay direct when layout/navigation do not materially change.
- For substantial architecture changes, show a caller, owners, concrete deletions
  and retained failure guarantees before implementation; obtain approval and update
  affected requirements/design. Put concrete shared behavior/contracts in base
  classes; avoid speculative abstractions.
- Validate selected-path inputs once at their owning boundary. Leave harmless,
  prompt argument errors to dependencies; guard concrete dangerous/costly failures.
- Separate readiness/liveness from functional diagnostics; stronger checks must
  justify their operational cost. Test behavior and required structure. Approved
  removals retire obsolete expectations without restoring behavior or weakening
  remaining acceptance.
- The implementation owner verifies affected behavior; reviewers reuse evidence
  and name missing coverage. Rerun only for relevant edits, failures or uncovered
  risks; agree before reducing acceptance. Final checks use stable source or an
  isolated snapshot. Invalidate only affected evidence; mocks/static checks do not
  prove runtime behavior.

## Git and delivery

- Unless instructed otherwise, verify and commit owned work on a task branch.
  Integrating into `main` requires explicit user approval for the selected changes;
  permission to implement, test, commit or rebase does not grant it. Present the
  concrete diff/commit and verification before asking; reuse approval within its
  stated scope. Pushing and deployment require separate authorization. Respect
  the checkout's integration owner and unrelated changes.
- Keep `main` linear with rebase/fast-forward or squash, not merge commits. Use
  descriptive commits for coherent implementation steps; fold related fixups,
  wording iterations and verification-only notes into their owning change before
  integration. Keep unrelated tasks separate. Rewriting existing `main` or another
  owner's commits requires explicit authorization.
- After integration, remove completed task worktrees/local task branches and prune
  stale records. Verify integration by content/history; dirty does not mean
  unfinished. Preserve uncommitted work, ignored data, evidence and previews. Retain
  worktrees/branches needed by an owner/runtime or with unproven integration; report
  the integration commit and retention reason in chat.

## Shared work

- When delegation is authorized, use it when its benefit exceeds coordination cost
  or independent review is required; size/concurrency alone does not require workers.
  One owner delivers code/tests/docs; transfer boundaries only after the previous
  owner stops.
- Before implementation, check active chats, ownership and worktrees. Concurrent
  implementation defaults to a separate task-owned worktree: reuse or create one
  without asking. A lone task may use the current checkout; if concurrency starts
  later, isolate owned edits before further writes without moving others' work.
- State owners/boundaries in chat. Allow one writer per overlapping boundary and
  one integration/index owner per checkout. Serialize main integration and shared
  host mutations across worktrees. Other shared-checkout writers hand off without
  staging/committing. Never commit the whole checkout with another writer active;
  wait or isolate overlaps while continuing independent/read-only work.
