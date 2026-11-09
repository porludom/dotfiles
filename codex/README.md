# Codex

Setup copies `config.toml` to `~/.codex/config.toml` only when missing.
The local file owns effective settings, machine paths, project trust and app state.
Tracked defaults are a starting template; later changes must be applied explicitly
on each Mac. Setup preserves existing config and needs no `/etc/codex` link.
Restart Codex after changing startup settings.

Portable guidance is linked as `~/.codex/AGENTS.md` and
`~/.agents/skills/dev-flow`. Invoke `$dev-flow` explicitly; open a fresh chat after
installation to verify discovery. Runtime state stays local.
