#!/usr/bin/env bash

install_prerequisites() {
  local installer
  case "$(uname -s)" in
  Darwin)
    if ! xcode-select -p >/dev/null 2>&1; then
      xcode-select --install
      fail "Finish installing Command Line Tools, then rerun make install."
      return 1
    fi
    if ! configure_brew; then
      installer="$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
      bash -c "$installer"
      configure_brew
    fi
    ;;
  Linux) ;;
  *) fail "Unsupported operating system: $(uname -s)" ;;
  esac
}

install_packages() {
  case "$(uname -s)" in
  Darwin)
    configure_brew || {
      fail "Homebrew is missing; run make install."
      return 1
    }
    HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_CLEANUP=1 \
      brew bundle install --no-upgrade --verbose --file="$ROOT/Brewfile"
    ;;
  Linux)
    if command -v apt-get >/dev/null 2>&1; then
      sudo apt-get update
      sudo apt-get install -y git curl python3 fzf
    elif command -v dnf >/dev/null 2>&1; then
      sudo dnf install -y git curl python3 fzf
    elif command -v pacman >/dev/null 2>&1; then
      sudo pacman -S --needed --noconfirm git curl python fzf
    else
      fail "Supported Linux package managers: apt-get, dnf, pacman."
      return 1
    fi
    if ! command -v sheldon >/dev/null 2>&1; then
      curl --proto '=https' -fLsS https://rossmacarthur.github.io/install/crate.sh |
        bash -s -- --repo rossmacarthur/sheldon --to "$HOME/.local/bin"
    fi
    if ! command -v uv >/dev/null 2>&1; then
      curl -fsSL https://astral.sh/uv/install.sh |
        UV_INSTALL_DIR="$HOME/.local/bin" UV_NO_MODIFY_PATH=1 sh
    fi
    log "Linux installs a minimal CLI set; additional tools are listed in Brewfile."
    ;;
  *) fail "Unsupported operating system: $(uname -s)" ;;
  esac
}

update_packages() {
  case "$(uname -s)" in
  Darwin)
    configure_brew || {
      fail "Homebrew is missing; run make install."
      return 1
    }
    brew update
    HOMEBREW_NO_AUTO_UPDATE=1 HOMEBREW_NO_INSTALL_CLEANUP=1 brew upgrade --greedy
    install_packages
    ;;
  Linux)
    if command -v apt-get >/dev/null 2>&1; then
      sudo apt-get update
      sudo apt-get upgrade -y
    elif command -v dnf >/dev/null 2>&1; then
      sudo dnf upgrade -y
    elif command -v pacman >/dev/null 2>&1; then
      sudo pacman -Syu --noconfirm
    else
      fail "Supported Linux package managers: apt-get, dnf, pacman."
      return 1
    fi
    install_packages
    uv self update
    ;;
  *) fail "Unsupported operating system: $(uname -s)" ;;
  esac
}

cleanup_packages() {
  case "$(uname -s)" in
  Darwin)
    configure_brew || {
      fail "Homebrew is missing; run make install."
      return 1
    }
    brew cleanup
    ;;
  Linux)
    if command -v apt-get >/dev/null 2>&1; then
      sudo apt-get clean
    elif command -v dnf >/dev/null 2>&1; then
      sudo dnf clean packages
    elif command -v pacman >/dev/null 2>&1; then
      sudo pacman -Sc
    else
      fail "Supported Linux package managers: apt-get, dnf, pacman."
    fi
    ;;
  *) fail "Unsupported operating system: $(uname -s)" ;;
  esac
}
