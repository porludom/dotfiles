#!/usr/bin/env bash

initialize_submodules() {
  git -C "$ROOT" submodule sync --recursive
  git -C "$ROOT" submodule update --init --recursive
}

apply_links() {
  if [[ ! -f "$ROOT/dotbot/bin/dotbot" ]]; then
    fail "Dotbot is missing; run make install."
    return 1
  fi
  if [[ ! -w /etc/codex ]]; then
    sudo install -d -o "$(id -un)" /etc/codex
  fi
  "$ROOT/dotbot/bin/dotbot" -d "$ROOT" -c "$ROOT/install.conf.yaml"
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
