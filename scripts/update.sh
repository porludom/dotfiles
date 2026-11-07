#!/usr/bin/env bash

set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=lib/common.sh
source "$ROOT/scripts/lib/common.sh"
# shellcheck source=packages.sh
source "$ROOT/scripts/packages.sh"
# shellcheck source=links.sh
source "$ROOT/scripts/links.sh"
trap 'report_error "$?" "$BASH_COMMAND"' ERR
export PATH="$HOME/.local/bin:$PATH"

update_repository() {
  local status
  status="$(git -C "$ROOT" status --porcelain)"
  if [[ -n "$status" ]]; then
    fail "Commit or stash local changes before make update."
    return 1
  fi
  git -C "$ROOT" pull --ff-only
  initialize_submodules
}

if [[ $# -gt 1 ]]; then
  printf 'Usage: %s [update|cleanup]\n' "$0" >&2
  exit 2
fi

case "${1:-update}" in
  update)
    load_repository_url
    step "Update dotfiles repository" update_repository
    step "Update packages and applications" update_packages
    step "Apply links" apply_links
    step "Update shell plugins" sheldon lock --update
    step "Apply configured application settings" sync_settings
    log "Update complete."
    ;;
  cleanup)
    load_repository_url
    step "Clean package caches" cleanup_packages
    log "Cleanup complete."
    ;;
  *)
    printf 'Usage: %s [update|cleanup]\n' "$0" >&2
    exit 2
    ;;
esac
