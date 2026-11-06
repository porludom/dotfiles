# Codex

`config.toml` links to `/etc/codex/config.toml` as shared defaults.
Keep local overrides (models, machine paths, project trust and app state)
in `~/.codex/config.toml`.

Dotbot uses `sudo` once per Mac to make `/etc/codex` writable by your user,
preserving existing config files or other links. Restart Codex to reload.
