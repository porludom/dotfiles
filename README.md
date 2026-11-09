# riZZZhik's dotfiles

Personal macOS setup.

## Clone

```sh
git clone https://github.com/riZZZhik/dotfiles.git ~/.dotfiles
cd ~/.dotfiles
```

## Customize

Review these files **before installing**:

| File                            | What to customize                                                             |
| ------------------------------- | ----------------------------------------------------------------------------- |
| `config/install.yaml`           | Apps, macOS preferences and entire `setup-*` stages.                          |
| `pyproject.toml`                | Personal Python libraries in `global`. Keep `installer` intact.               |
| `.python-version`               | Default Python version, managed by uv.                                        |
| `home/`                         | Always linked into `~/`; review every file. Existing conflicts are backed up. |
| `config/{vscode,iterm2,codex}/` | Settings for the app stages you keep.                                         |

For example, remove `spotify` from `setup-desktop.cask` to skip Spotify,
or add `requests` to the `global` Python group. Remove a whole `setup-*` block to skip that stage.
Removing entries does not uninstall existing software.

## Install

```sh
./install
```

All remaining stages run without a confirmation menu. If Command Line Tools setup
opens, finish it and rerun. App backups go to `.private/backups/`.
Review local changes, then commit and push them yourself.

## Maintain

- `./install apply` — relink files and reapply app settings.
- `./install update` — pull changes and update configured software.
- `./install cleanup` — clear package caches.
- `./install fork` — create a GitHub fork and switch `origin`, without pushing.

Only installation and updates reconcile Python and shared libraries. Other commands
use the installed runtime; `./install --help` performs no setup.
