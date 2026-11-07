#!/usr/bin/env bash

link_file() {
  local source="$1" destination="$2" policy="$3"
  [[ -e "$source" ]] || { fail "Link source is missing: $source"; return 1; }
  if [[ "$source" -ef "$destination" ]]; then
    return
  fi
  if [[ -e "$destination" || -L "$destination" ]]; then
    if [[ "$policy" == replace ]]; then
      rm -rf -- "$destination"
    elif [[ "$policy" == relink && -L "$destination" ]]; then
      rm -- "$destination"
    else
      fail "Refusing to replace existing path: $destination"
      return 1
    fi
  fi
  mkdir -p -- "$(dirname "$destination")"
  ln -s -- "$source" "$destination"
  log "Linked $destination"
}

clean_home_links() {
  local link target component resolved checkout
  local -a components
  checkout="$(cd -P "$ROOT" && pwd)"
  for link in "$HOME"/* "$HOME"/.[!.]* "$HOME"/..?*; do
    [[ -L "$link" && ! -e "$link" ]] || continue
    target="$(readlink "$link")"
    [[ "$target" == /* ]] || target="$HOME/$target"
    IFS=/ read -r -a components <<< "$target"
    resolved=""
    for component in "${components[@]}"; do
      case "$component" in
        ''|.) continue ;;
        ..) resolved="${resolved%/*}" ;;
        *) resolved="$resolved/$component" ;;
      esac
      # Resolve existing directory symlinks before checking checkout ownership.
      if [[ -d "$resolved" ]]; then
        resolved="$(cd -P "$resolved" && pwd)"
        [[ "$resolved" != / ]] || resolved=""
      fi
    done
    case "$resolved" in
      "$checkout"/*) rm -- "$link"; log "Removed broken link $link" ;;
    esac
  done
}

apply_links() {
  local source
  clean_home_links
  for source in "$ROOT"/home/.[!.]* "$ROOT"/home/..?*; do
    [[ -e "$source" || -L "$source" ]] || continue
    link_file "$source" "$HOME/${source##*/}" replace
  done
  link_file "$ROOT/codex/skills/dev-flow" "$HOME/.agents/skills/dev-flow" relink
  link_file "$ROOT/codex/AGENTS.md" "$HOME/.codex/AGENTS.md" relink
  link_file "$ROOT/codex/keybindings.json" "$HOME/.codex/keybindings.json" relink
  if [[ ! -w /etc/codex ]]; then
    sudo install -d -o "$(id -un)" /etc/codex
  fi
  link_file "$ROOT/codex/config.toml" /etc/codex/config.toml preserve
  mkdir -p -- "$HOME/dev"
}

sync_settings() {
  local formula prefix
  if [[ "$(uname -s)" == Darwin ]]; then
    formula="$(brew bundle list --formula --file="$ROOT/Brewfile" \
      | awk '/^python(@|$)/ && !selected { selected = $0 } END { print selected }')"
    prefix="$(brew --prefix "$formula")"
    "$prefix/libexec/bin/python3" "$ROOT/sync.py" "$@"
  fi
}
