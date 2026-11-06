# Helpers

_exists() {
  if command -v -- "$1" >/dev/null 2>&1; then
    return 0
  else
    echo "Command not found: $1" >&2
    return 1
  fi
}

_source() {
  if [[ -f $1 ]]; then
    source $1
  else
    echo "File not found: $1"
  fi
}

_extend_path() {
  [[ -d "$1" ]] || return
  export PATH="$1:$PATH"
}

# Environment

# User settings
export EDITOR=nvim

# Locale
export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US.UTF-8

_extend_path "$HOME/.local/bin"
if [ "$(uname)" = "Darwin" ]; then
  _extend_path "/opt/homebrew/sbin"
  _extend_path "/opt/homebrew/bin"
  _extend_path "$HOME/go/bin"
  _extend_path "$(brew --prefix)/opt/python@3.12/libexec/bin"
fi

# Load the default config first, followed by YAML paths from ~/.kube.
# _kube_yaml_files=("$HOME/.kube/config" "$HOME"/.kube/*.(yaml|yml)(N-.))
# export KUBECONFIG="${(j.:.)_kube_yaml_files}"
# unset _kube_yaml_files

# History
HISTSIZE=50000
SAVEHIST=50000
HISTFILE="$HOME/.zsh_history"
setopt HIST_IGNORE_DUPS
setopt HIST_IGNORE_SPACE  # don't save commands starting with space
setopt SHARE_HISTORY  # share history across terminals

# Completions
autoload -Uz compinit
zmodload -i zsh/complist
compinit -C

# Plugins
export ZSH="$HOME/.local/share/sheldon/repos/github.com/ohmyzsh/ohmyzsh"
plugins=(
  macos          # https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/macos
  git            # https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/git
  brew           # https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/brew
  docker         # https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/docker
  docker-compose # https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/docker-compose
  sudo           # https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/sudo

  colored-man-pages # https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/colored-man-pages

  ssh-agent
  #   gpg-agent
)

# The ssh-agent plugin reads these settings while loading.
if [[ "$OSTYPE" == "darwin"* ]]; then
  zstyle :omz:plugins:ssh-agent ssh-add-args --apple-use-keychain
  # An explicit identity list replaces the plugin's defaults; retain those keys.
  zstyle :omz:plugins:ssh-agent identities \
    id_rsa id_dsa id_ecdsa id_ed25519 id_ed25519_sk identity id_ed25519_rizzzhik
fi

eval "$(sheldon source)"

# Shell integrations

# Fuzzy finder - https://github.com/junegunn/fzf
if _exists fzf; then
  source <(fzf --zsh)
fi

# Modern cd - https://github.com/ajeetdsouza/zoxide
if _exists zoxide; then
  eval "$(zoxide init zsh)"
fi

# Enable iTerm shell integration
if [ "$(uname)" = "Darwin" ]; then
  _source ~/.iterm2_shell_integration.zsh
fi

# Load personal command overrides after plugins and integrations.
_source ~/.aliases.zsh

# Private settings
if [ -f ~/.zshrc.private.zsh ]; then
  source ~/.zshrc.private.zsh
fi
