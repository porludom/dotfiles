#!/usr/bin/env bash
set -euo pipefail
export PATH="$PATH:/opt/homebrew/bin:/usr/local/bin"

homebrew() (
  if ! command -v brew >/dev/null; then
    script=$(mktemp)
    trap 'rm -f "$script"' EXIT
    curl --fail --location https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh -o "$script"
    bash "$script"
  fi
)

fork() (
  if ! command -v gh >/dev/null; then
    echo 'Skipping fork setup: install the CLI tools stage for GitHub CLI.'
    exit 0
  fi
  if [[ $# -gt 0 ]]; then
    answer=$1
  else
    read -r -p 'Create a GitHub fork and use it as origin? [y/N]: ' answer
  fi
  [[ "$answer" == [yY] || "$answer" == [yY][eE][sS] ]] || exit 0
  gh auth status >/dev/null 2>&1 || gh auth login

  repo=$(gh repo view --json name --jq .name)
  login=$(gh api user --jq .login)
  gh repo fork --clone=false --remote=false
  git remote set-url origin "https://github.com/$login/$repo.git"
  printf 'Fork ready: https://github.com/%s/%s\n' "$login" "$repo"
)

packages() (
  action=$1
  shift
  case "$action" in
    plugins)
      if [[ "$1" == update ]]; then
        sheldon lock --update
      else
        sheldon lock
      fi
      exit 0
      ;;
    cleanup)
      brew cleanup
      exit 0
      ;;
  esac
  manifest=$1
  shift
  [[ $# -gt 0 ]] || exit 0
  homebrew
  export HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_CLEANUP=1
  export MAS_NO_AUTO_INDEX=1
  mas_ids=()
  if [[ "$action" == update ]]; then
    brew update
    while [[ $# -gt 0 ]]; do
      kind=$1
      name=$2
      shift 2
      if [[ "$kind" == mas ]]; then
        mas_ids+=("$name")
        continue
      fi
      flag=--formula
      [[ "$kind" != cask ]] || flag=--cask
      if brew list "$flag" "$name" >/dev/null 2>&1; then
        brew upgrade "$flag" "$name"
      fi
    done
  fi
  brew bundle install --no-upgrade "--file=$manifest"
  if [[ ${#mas_ids[@]} -gt 0 ]]; then
    mas upgrade "${mas_ids[@]}"
  fi
)

touch_id() (
  config=$1
  source=$config
  [[ -f "$source" ]] || source=$2
  entry='^auth[[:space:]]+sufficient[[:space:]]+pam_tid\.so([[:space:]]|$)'
  if [[ -f "$config" ]] && grep -Eq "$entry" "$config"; then
    exit 0
  fi
  file=$(mktemp)
  trap 'rm -f "$file"' EXIT
  sed -E 's/^#(auth[[:space:]]+sufficient[[:space:]]+pam_tid\.so)/\1/' "$source" > "$file"
  if ! grep -Eq "$entry" "$file"; then
    echo 'No Touch ID entry found in the system sudo template.' >&2
    exit 1
  fi
  sudo install -o root -g wheel -m 0444 "$file" "$config"
)

update() (
  cd "$1"
  git -c merge.autoStash=false pull --ff-only --no-rebase
  export DOTFILES_AFTER_PULL=1
  exec bash "$PWD/install" update
)

case "${1:-}" in
  --fork)
    shift
    fork "$@"
    exit
    ;;
  --packages)
    shift
    packages "$@"
    exit
    ;;
  --touch-id)
    shift
    touch_id "$@"
    exit
    ;;
  --update)
    shift
    update "$@"
    exit
    ;;
esac
