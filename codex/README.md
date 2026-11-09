# Codex

Setup copies `config.toml` to `~/.codex/config.toml` only when missing.
The local file owns effective settings, machine paths, project trust and app state.
Tracked defaults are a starting template; later changes must be applied explicitly
on each Mac. Setup preserves existing config and needs no `/etc/codex` link.
Restart Codex after changing startup settings.

Portable guidance is linked as `~/.codex/AGENTS.md`. Start a fresh chat after
installation to check instruction discovery. Runtime state stays local.
The former `dev-flow` skill is retired; remove its old symlink at
`~/.agents/skills/dev-flow` if present. No replacement skill is required.

## Maintaining instructions

Keep `AGENTS.md` a compact set of decisions that improve everyday judgment.
This note is maintenance guidance, not another instruction file to load each task.

- Revise or replace an existing rule before adding one. Fix the underlying decision
  failure rather than appending a rule for each incident.
- Keep global preferences in `AGENTS.md`; put repository facts, commands and
  operating procedures in their owning project. Do not copy system/tool instructions or
  maintain a parallel development workflow in a skill.
- Before expanding guidance, name the recurring failure, explain why existing rules
  did not cover it and remove overlap. A single awkward task rarely needs a global
  rule. Reconsider the structure if the file grows beyond roughly 800 words.
- Evaluate changes against realistic cases: a trivial fix proceeds directly; a
  nontrivial refactor waits for design agreement; a simplification reduces concepts;
  a language change covers visible buttons; failed Mac emulation triggers a cheaper
  alternative discussion; approved integration preserves another chat's work.
- Text review, links and formatting establish instruction consistency only. Claims
  of fewer corrections or faster completion require observed behavior in comparable
  tasks. Keep evaluation evidence in chat unless a durable artifact is requested.
