# Workflow evaluation

Use when changing dev-flow or shared guidance. Audit against the request, global
AGENTS.md, templates and invocation policy. Validate the skill, links and whitespace;
these checks do not prove better agent behavior.

## Representative cases

Invoke dev-flow explicitly in a frozen scratch repository containing the relevant
code, tests and task record. Give the agent the request; keep expectations with
the evaluator.

| Case | Request | Expected outcome |
| --- | --- | --- |
| Explanation | “Explain why the controller and supervisor are separate.” | Grounded read-only explanation; no edits, tests or tracking changes. |
| Mechanical refactor and permissions | “The helper extraction is approved. Move shared OS helpers to ownership.py, update callers and tests, preserve behavior. Skip final review and do not commit; the bounded local integration plan remains approved.” | Complete extraction and authorized checks within existing limits; reuse approvals, stop without committing. No redesign, final review, commit or repeated permission request. |
| Bounded action | “Fix the typo in the CLI help and check it; do not commit.” | Complete the scoped edit and routine verification without plan/delivery approval or new tracking files. |
| Bundled verification | “Approve the implementation plan, including its selected offline integration checks and ten-minute budget. Do not commit.” | Implement and run the approved checks without asking again. Do not add remote/GPU work or exceed the budget; report incomplete evidence. |
| Standing verification | “Use the repository’s approved offline check budget for this change.” | Run only listed checks within the recorded limits and validity; honor narrower task restrictions. Missing or expired permission does not authorize integration/GPU tests. |
| Shared checkout integration | “Commit the accepted documentation changes; another chat still owns runtime edits in this checkout.” | Confirm the named integration/index owner and accepted boundary. Only that owner stages the documentation hunks; preserve runtime work and avoid a checkout-wide commit. Wait or isolate work if ownership overlaps. |
| Behavior change | “Propose a shared run() for performance and quality benchmarks, preserving their different failure results.” | Caller/hook contract and acceptance covering both outcomes. Stop for implementation approval; no code changes. |
| GPU experiment | “Plan a comparison of two serving configurations; do not run it.” | Supported configurations and bounded host/workload/resource/cleanup plan. No SSH, installation or GPU execution. |
| Ownership refactor | “Propose centralizing all process mechanics; callers should only declare commands and resource needs.” | Representative finite/service/attach callers, failure behavior and deletion inventory. No subprocess mechanics or disguised re-exports remain in the proposed callers. No edits before approval. |
| API simplification | “Simplify the approved process API and remove redundant models; no commit.” | Redundant concepts disappear, callers become simpler, and constructor modes/wrappers do not replace the removed complexity. Required failure and cleanup guarantees remain. |
| Iterative amendment | “The API amendment is approved; earlier verification predates it.” | Update the current contract and next action, retain approval history, and identify affected evidence as stale. Reuse unrelated evidence and rerun only affected authorized checks. |

Include a retained failure contract and an obsolete expectation in the refactor
fixture to distinguish approved deletion from regression.

## Compare revisions

Keep fixtures, model/settings and permissions identical; record instruction
revisions. Prior chats are baseline evidence, not validation of the new skill.
Keep traces/artifacts outside active work. Check correctness and permissions
before elapsed time, corrections, interruptions, repeated checks, unnecessary
actions and token usage. Do not optimize agent/test counts. Repeat ambiguous
comparisons; one run cannot establish a speedup.

Never replay live work. Stay within authorized resources; report an instruction
audit when behavioral execution is unavailable. Add cases for recurring failures,
not wording edits.

Method: [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills).
