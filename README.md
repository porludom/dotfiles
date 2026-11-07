# riZZZhik's dotfiles

## Installation

```bash
# Install git and other xcode tools
xcode-select --install

# Clone dotfiles repo
git clone https://github.com/riZZZhik/dotfiles.git $HOME/.dotfiles

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
