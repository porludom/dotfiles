#!/usr/bin/env bash

log() {
  printf '==> %s\n' "$*"
}

fail() {
  printf 'Error: %s\n' "$*" >&2
  return 1
}

step() {
  CURRENT_STEP="$1"
  shift
  log "$CURRENT_STEP"
  "$@"
}

report_error() {
  local status="$1" command="$2"
  printf 'Error: %s failed (%s): %s\n' "${CURRENT_STEP:-command}" "$status" "$command" >&2
  if [[ -n "${GITHUB_REPO_URL_BASE:-}" ]]; then
    printf 'Repository: %s\n' "$GITHUB_REPO_URL_BASE" >&2
  fi
  exit "$status"
}

load_repository_url() {
  local remote
  GITHUB_REPO_URL_BASE=""
  command -v git >/dev/null 2>&1 || return 0
  remote="$(git -C "$ROOT" config --get remote.origin.url)" || return 0
  case "$remote" in
    git@*:*)
      remote="${remote#git@}"
      remote="https://${remote%%:*}/${remote#*:}"
      ;;
    ssh://git@*) remote="https://${remote#ssh://git@}" ;;
    https://*|http://*) ;;
    *) return 0 ;;
  esac
  remote="${remote%/}"
  GITHUB_REPO_URL_BASE="${remote%.git}"
}

configure_brew() {
  local executable
  if command -v brew >/dev/null 2>&1; then
    return 0
  fi
  for executable in /opt/homebrew/bin/brew /usr/local/bin/brew; do
    if [[ -x "$executable" ]]; then
      eval "$("$executable" shellenv)"
      return 0
    fi
  done
  return 1
}
