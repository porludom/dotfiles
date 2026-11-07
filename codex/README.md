# Codex

`config.toml` links to `/etc/codex/config.toml` as shared defaults.
Keep local overrides (models, machine paths, project trust and app state)
in `~/.codex/config.toml`.

Setup uses `sudo` once per Mac to make `/etc/codex` writable by your user,
preserving existing config files or other links. Restart Codex to reload.

Portable guidance lives here, linked as `~/.codex/AGENTS.md` and
`~/.agents/skills/dev-flow`. Runtime state stays local. Invoke `$dev-flow`
explicitly; after installing or moving the link, open a fresh chat to verify discovery.
