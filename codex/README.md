`config.toml` contains shared defaults. The main Dotbot config links it to
`/etc/codex/config.toml`; Codex loads it natively.

`~/.codex/config.toml` stays local and overrides shared defaults. Model changes,
machine paths, project trust and app state belong there.

The installer uses `sudo` once per Mac to make `/etc/codex` writable by your user.
Existing files or different links at `/etc/codex/config.toml` are left untouched.
Restart Codex after changing the configuration.
