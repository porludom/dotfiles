# Working agreements

Apply sections by intent: an action request phrased as a question is still an action.

## General

- Use English unless explicitly asked otherwise.
- Keep responses, docs and code concise and precise; omit repetition and boilerplate.
- Respect project instructions, permissions, scope and approvals. Preserve unrelated
  work and other tasks' state and owners unless explicitly changed.
- Challenge unnecessary proposals, including the user's; consider runtime, tokens
  and maintenance.
- Check tool and device feasibility early; choose the cheapest experiment that
  answers the question. Report setup friction before expanding the test setup;
  do not add plans, records or approval gates solely for this rule.
- Promptly report overruns/stalls: elapsed/expected time, blocker, next action and
  useful user help.
- In operational updates, distinguish implemented, committed, prepared, deployed
  and verified states; name the revision and host when relevant. Report only
  relevant states and verification limits, without a boilerplate checklist.

## Questions and analysis

- Answer explanations, advice and research directly. Investigate read-only as
  needed; clarify consequential gaps and distinguish facts from assumptions or
  uncertainty.
- Mentioning code does not itself call for implementation, tests or task tracking.
- Keep task progress, approvals and handoffs in chat; do not create or maintain
  backlog, status or task-tracking documents unless explicitly requested.

## Code changes

- Follow the applicable [Google style guide](https://google.github.io/styleguide/).
- For Python quality checks, use repository entrypoints; otherwise use
  `uvx ruff check` and `uvx mypy` with repository configuration.
- Reuse repository check entrypoints. Consolidate repeatedly reconstructed commands;
  keep costly and remote checks explicit.
- Comment only non-obvious rationale, constraints or pitfalls.
- Before nontrivial implementation, assess responsibilities, reuse, alternatives
  and failure costs.
- Before nontrivial changes, define observable acceptance criteria and critical
  invariants, then verify those exact behavior paths. Keep small fixes direct;
  do not add plans, records or approval gates solely for this rule.
- Before significant UI layout or navigation changes, show a representative mockup
  with realistic content and agree on the direction before implementation. Reuse
  an already approved design or honor an explicit waiver. Handle minor copy and
  button fixes directly when they do not materially change layout or navigation.
- For substantial architecture changes, show a representative caller, responsibility
  owners, concrete deletions and retained failure guarantees before implementation.
- Put concrete shared behavior/contracts in base classes; avoid speculative
  abstractions. Propose useful structural changes; obtain approval for substantial
  changes and update affected requirements/design.
- Validate only selected-path inputs, once at their owning boundary. Leave prompt,
  harmless argument failures to dependencies; guard concrete dangerous or costly
  failures.
- Separate readiness/liveness from functional diagnostics. Add stronger checks
  only for required guarantees worth their operational cost.
- Test behavior and explicitly required structure. For approved removals, update
  obsolete expectations against the accepted contract; do not restore removed
  behavior or weaken remaining acceptance to satisfy tests.
- The implementation owner verifies affected behavior. Reviewers reuse evidence
  and add only named missing coverage. Rerun only for relevant changes, failures or
  uncovered risks; agree before reducing acceptance.
- Final checks need a stable source boundary: suspend relevant writes or use an
  isolated snapshot. Relevant changes invalidate affected evidence; unrelated
  changes do not. Report verification limits; mocks/static checks do not prove
  runtime behavior.
- Unless instructed otherwise, finish completed code work by integrating owned
  changes into `main` and making a local commit after required verification.
  This is standing authorization for local commits and integration, not pushing
  or deployment. Respect the checkout's integration owner and unrelated changes.
- After integration, remove completed task worktrees and prune stale worktree
  records. Record the integration commit and any worktree retention reason in the
  chat handoff; add no separate tracking process. Compare content and history
  before treating dirty worktrees as unfinished. Verify their
  changes are in `main`; preserve uncommitted work, ignored data, evidence and
  running previews. Keep a worktree while an active owner or runtime needs it.

## Delegation and shared work

- When delegation is authorized, use it when expected benefit exceeds coordination
  cost or independent review is required. Size, file/caller count and concurrency
  alone do not require workers.
- One owner delivers code, tests and docs; reassign boundaries only after the
  previous owner stops.
- Before implementation, check active chats, ownership and worktrees. When
  another implementation task is active in the repository, default to a separate
  task worktree before editing: reuse a suitable one owned by this task or create
  one without asking. A lone task may reuse the current checkout. If concurrency
  begins later, isolate owned edits before further writes; preserve others' work.
- Ownership applies across chats and agents. State owners and write boundaries
  in chat. Allow one writer per overlapping boundary and one integration/index
  owner per checkout. Serialize integration into `main`
  and shared host mutations, including across worktrees. In a shared checkout,
  other writers hand off without staging or committing; never commit the whole
  checkout while another writer is active. Wait or isolate work when ownership
  overlaps; continue independent and read-only work.
