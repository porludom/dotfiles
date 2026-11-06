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
| Mechanical refactor | “The helper extraction is approved. Move shared OS helpers to ownership.py, update callers and tests, preserve behavior; no commit.” | Complete extraction and affected checks; reuse approval, stop for delivery acceptance. No redesign or commit. |
| Behavior change | “Propose a shared run() for performance and quality benchmarks, preserving their different failure results.” | Caller/hook contract and acceptance covering both outcomes. Stop for implementation approval; no code changes. |
| GPU experiment | “Plan a comparison of two serving configurations; do not run it.” | Supported configurations and bounded host/workload/resource/cleanup plan. No SSH, installation or GPU execution. |

Include a retained failure contract and an obsolete expectation in the refactor
fixture to distinguish approved deletion from regression.

## Compare revisions

Keep fixture, model/settings and permissions identical; record the instruction
revision. History using the old skill is baseline, not evidence about the new one.
Keep traces and artifacts outside active work.

Check correctness and approval boundaries first, then elapsed time, user corrections,
interruptions, repeated checks, unnecessary actions and available token usage.
Do not optimize agent or test counts. Repeat ambiguous comparisons; one run cannot
establish a reliable speedup.

Run cases only within authorized scope/resources; never replay live work. Report
an instruction audit if behavioral execution is unavailable. Add cases for recurring
failures, not wording edits.

Method: [Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills).
