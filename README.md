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
| `config/setup.yaml`           | Apps, macOS preferences and entire `setup-*` stages.                          |
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

## Restore VS Code layout on a new machine

Before its first sync, VS Code setup stops if a saved `config/vscode/ui-state.code-profile`
exists. In VS Code, run **Profiles: Import Profile**, select that file, change the
profile name to **Default**, and confirm **Replace**. This file contains only UI
state; dotfiles manages settings, keybindings and extensions separately. Reload
the Default profile and check the layout, then run:

```sh
./install apply --vscode-ui-restored
```

The acknowledgement also works with `./install sync`. It allows the first sync to
establish the normal local extension baseline; subsequent syncs export layout
changes normally. Machines with an existing baseline need no acknowledgement.
If that local baseline was removed, repeat the explicit restoration/check before
acknowledging. Import into Default: a separate “Dotfiles UI” profile is outside
this sync adapter's scope.

## Maintain

- `./install apply` — relink files and reapply app settings.
- `./install update` — pull changes and update configured software.
- `./install cleanup` — clear package caches.
- `./install fork` — create a GitHub fork and switch `origin`, without pushing.

Only installation and updates reconcile Python and shared libraries. Other commands
use the installed runtime; `./install --help` performs no setup.
