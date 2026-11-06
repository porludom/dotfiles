# Working agreements

Apply sections by intent: an action request phrased as a question is still an action.

## General

- Use English unless explicitly asked otherwise.
- Keep responses, docs and code concise and precise; omit repetition and boilerplate.
- Respect project instructions, permissions, scope and approvals. Preserve unrelated
  work and other tasks' state and owners unless explicitly changed.
- Challenge unnecessary proposals, including the user's; consider runtime, tokens
  and maintenance.
- Promptly report overruns/stalls: elapsed/expected time, blocker, next action and
  useful user help.

## Questions and analysis

- Answer explanations, advice and research directly. Investigate read-only as
  needed; clarify consequential gaps and distinguish facts from assumptions or
  uncertainty.
- Mentioning code does not itself call for implementation, tests or task tracking.

## Code changes

- Follow the applicable [Google style guide](https://google.github.io/styleguide/).
- For Python quality checks, use `uvx ruff check` and `uvx mypy` with repository
  configuration.
- Reuse repository check entrypoints. Consolidate repeatedly reconstructed commands;
  keep costly and remote checks explicit.
- Comment only non-obvious rationale, constraints or pitfalls.
- Before nontrivial implementation, assess responsibilities, reuse, alternatives
  and failure costs.
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

## Delegation and shared work

- When delegation is authorized, use it when expected benefit exceeds coordination
  cost or independent review is required. Size, file/caller count and concurrency
  alone do not require workers.
- One owner delivers code, tests and docs; reassign boundaries only after the
  previous owner stops.
- Ownership applies across chats and agents. In a shared checkout, identify owners
  and write boundaries in the existing coordination view. Allow one writer per
  overlapping boundary, including the Git index; serialize conflicts or use
  separate worktrees. Continue independent work; read-only work may run in
  parallel. Serialize shared host mutations.
