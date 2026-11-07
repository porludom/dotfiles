#!/usr/bin/env bash

enable_touch_id() {
  local config=/etc/pam.d/sudo_local source_config temporary
  if grep -Eq '^auth[[:space:]]+sufficient[[:space:]]+pam_tid\.so([[:space:]]|$)' "$config" 2>/dev/null; then
    log "Touch ID for sudo is already enabled."
    return
  fi

  source_config="$config"
  if [[ ! -f "$source_config" ]]; then
    source_config=/etc/pam.d/sudo_local.template
  fi
  temporary="$(mktemp)"
  # Keep custom PAM entries and enable only Apple's optional Touch ID module.
  sed -E 's/^#(auth[[:space:]]+sufficient[[:space:]]+pam_tid\.so)/\1/' "$source_config" >"$temporary"
  if ! grep -Eq '^auth[[:space:]]+sufficient[[:space:]]+pam_tid\.so([[:space:]]|$)' "$temporary"; then
    rm -f "$temporary"
    fail "No Touch ID entry found in $config or its macOS template."
    return 1
  fi
  sudo install -o root -g wheel -m 0444 "$temporary" "$config"
  rm -f "$temporary"
  log "Enabled Touch ID for sudo."
}

apply_macos_preferences() {
  if [ "$(uname)" != "Darwin" ]; then
    return
  fi

  enable_touch_id

  # You can find other defaults at https://macos-defaults.com
  log "Writing to apple defaults. You can find what changes in scripts/macos.sh"

  # Close System Preferences panes, to prevent them from overriding settings we’re about to change
  osascript -e 'tell application "System Preferences" to quit'

  # Settings > Control Center
  # Bluetooth: always show in menu bar
  defaults -currentHost write com.apple.controlcenter Bluetooth -int 18
  # Sound: always show in menu bar
  defaults -currentHost write com.apple.controlcenter Sound -int 18

  # Settings > Desktop & Dock
  # Enable expose
  defaults write com.apple.dock "scroll-to-open" -bool true
  defaults write com.apple.dock showAppExposeGestureEnabled -bool true
  # Mission control: Disable automatically rearrange spaces
  defaults write com.apple.dock "mru-spaces" -bool false
  # Hot corners: Screen saver in bottom left
  defaults write com.apple.dock "wvous-bl-corner" -int 5
  defaults write com.apple.dock "wvous-bl-modifier" -int 0

  killall Dock 2>/dev/null || true

  # Settings > Keyboard
  # Disable dot after double spaces
  defaults write -g NSAutomaticPeriodSubstitutionEnabled -bool false
  # Disable quotes replacements
  defaults write -g NSAutomaticQuoteSubstitutionEnabled -bool false
  defaults write ru.keepcoder.Telegram AutomaticQuoteSubstitutionEnabledTGGrowingTextView -bool false
  # Disable press and hold symbols
  defaults write NSGlobalDomain ApplePressAndHoldEnabled -bool false

  # Finder
  # Show all extensions
  defaults write NSGlobalDomain AppleShowAllExtensions -bool true
  # Disable warning for changing file extension
  defaults write com.apple.finder FXEnableExtensionChangeWarning -bool false
  # Show hidden files
  defaults write com.apple.finder AppleShowAllFiles -bool true
  # Show path bar and title
  defaults write com.apple.finder ShowPathbar -bool true
  defaults write com.apple.finder _FXShowPosixPathInTitle -bool true
  # Show folders first
  defaults write com.apple.finder _FXSortFoldersFirst -bool true

  # Set VSCode as default for text files
  duti -s com.microsoft.VSCode public.plain-text all
  duti -s com.microsoft.VSCode public.source-code all
  duti -s com.microsoft.VSCode public.shell-script all
  duti -s com.microsoft.VSCode public.json all
  duti -s com.microsoft.VSCode public.yaml all
  duti -s com.microsoft.VSCode net.daringfireball.markdown all

  killall Finder 2>/dev/null || true
}
