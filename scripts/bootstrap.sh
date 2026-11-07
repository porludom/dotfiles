#!/usr/bin/env bash

set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=lib/common.sh
source "$ROOT/scripts/lib/common.sh"
# shellcheck source=packages.sh
source "$ROOT/scripts/packages.sh"
# shellcheck source=links.sh
source "$ROOT/scripts/links.sh"
# shellcheck source=macos.sh
source "$ROOT/scripts/macos.sh"
trap 'report_error "$?" "$BASH_COMMAND"' ERR
export PATH="$HOME/.local/bin:$PATH"

if [[ $# -gt 1 ]]; then
  printf 'Usage: %s [install|apply]\n' "$0" >&2
  exit 2
fi

case "${1:-install}" in
  install)
    step "Install prerequisites" install_prerequisites
    load_repository_url
    step "Install missing packages" install_packages
    load_repository_url
    step "Initialize pinned dependencies" initialize_submodules
    step "Apply links" apply_links
    step "Install shell plugins" sheldon lock
    step "Apply macOS preferences" apply_macos_preferences
    step "Configure application settings synchronization" sync_settings --setup
    log "Installation complete."
    ;;
  apply)
    load_repository_url
    if [[ "$(uname -s)" == Darwin ]]; then
      configure_brew || { fail "Homebrew is missing; run make install."; exit 1; }
    fi
    step "Apply links" apply_links
    step "Apply configured application settings" sync_settings
    log "Dotfiles applied."
    ;;
  *)
    printf 'Usage: %s [install|apply]\n' "$0" >&2
    exit 2
    ;;
esac
