# porludom's dotfiles

## Installation

```bash
# Install git and other xcode tools
xcode-select --install

# Clone dotfiles repo
git clone https://github.com/porludom/dotfiles.git $HOME/.dotfiles

# Go to the dotfiles directory
cd $HOME/.dotfiles

# Install dotfiles
make install
```

## Commands

| Command | Action |
| --- | --- |
| `make install` | Install missing prerequisites and packages, link dotfiles, apply macOS preferences, and configure application settings sync. |
| `make apply` | Reapply links and application settings using the selected sync modes. |
| `make update` | Fast-forward the clean checkout, update packages and shell plugins, then reapply links and settings. |
| `make cleanup` | Clean package caches without upgrading software. |
| `make help` | Show available commands. |

`./install` remains an alias for full installation. Installation uses Homebrew's
no-upgrade mode. Homebrew owns Python and uv on macOS; automation resolves the
Python interpreter from the Brewfile instead of pinning a version in scripts. Linux
uses distribution Python and user-installed uv; an older pip-managed uv must be
migrated to its standalone installer before using its self-update command.
Linux installs a minimal CLI set through apt-get, dnf, or pacman; other tools in
`Brewfile` are optional there.

Application settings remain managed by `sync.py`. Apply and update reuse existing
choices without prompting. Update requires a clean Git working tree. Error links
derive from the checkout's origin remote. Links are managed directly by
`scripts/links.sh`.

## Terminal workflow

Use `lg` to review changes, stage hunks, manage branches, and resolve conflicts in
Lazygit. It replaces forgit; ordinary Git aliases, `git-open`, and `gud` remain
available.

Python environments switch automatically when entering a project with an existing
`.venv`, including its subdirectories. Leaving deactivates the environment. Run
`uv sync` explicitly to create or update dependencies; directory changes do not
install them. No `.envrc` is needed for activation. Each worktree uses its own
`.venv`. Direnv remains available for approved project-specific variables; avoid
also activating Python environments there.

Open a new shell after updating; existing shells retain previously loaded plugins.
