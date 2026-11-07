"""Install portable iTerm profiles while retaining machine-local profiles."""

import json
import os
import plistlib
import subprocess
import tempfile
import uuid
from copy import deepcopy
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

DOMAIN = "com.googlecode.iterm2"
SHARED = Path(__file__).resolve().parent
DESTINATION = (
    Path.home() / "Library/Application Support/iTerm2/DynamicProfiles/dotfiles.json"
)
BACKUPS = Path.home() / ".local/state/dotfiles/iterm2"
THEME_LIBRARY = (
    "https://raw.githubusercontent.com/mbadolato/iTerm2-Color-Schemes/"
    "b84cd1e68c9033d967fccd9febbac3072d127b7b/schemes/"
)


def load_theme(preferences: dict, name: str) -> dict:
    """Reuse an imported preset or import it from the pinned theme library."""
    preset = preferences.get("Custom Color Presets", {}).get(name)
    if preset is not None:
        return preset
    with urlopen(f"{THEME_LIBRARY}{quote(name)}.itermcolors", timeout=15) as response:
        return plistlib.loads(response.read())


def merge_profile(profile: dict, settings: dict) -> None:
    """Merge key bindings without dropping machine-local shortcuts."""
    values = deepcopy(settings)
    keymap = values.pop("Keyboard Map", {})
    for action in keymap.values():
        if action.get("Text") == "$PROFILE_GUID":
            action["Text"] = profile["Guid"]
    profile.update(values)
    profile.setdefault("Keyboard Map", {}).update(keymap)


def prepare(preferences: dict) -> tuple[dict, dict]:
    """Apply shared settings while preserving native identities and local fields."""
    preferences = deepcopy(preferences)
    settings = json.loads((SHARED / "settings.json").read_text())
    theme = load_theme(preferences, settings["Theme"])
    common = {**settings["Profile"], **theme}
    native = [
        profile
        for profile in preferences.get("New Bookmarks", [])
        if profile.get("Guid") != settings["Remote"]["Guid"]
        and not profile.get("Dynamic Profile")
    ]
    if not native:
        raise ValueError("Open iTerm once to create its default profile, then retry.")
    parent = next(
        (
            profile
            for profile in native
            if profile["Guid"] == preferences.get("Default Bookmark Guid")
        ),
        native[0],
    )
    hotkeys = [profile for profile in native if profile.get("Has Hotkey")]
    if not hotkeys:
        hotkey = deepcopy(parent)
        hotkey.update({"Name": "Hotkey Window", "Guid": str(uuid.uuid4()).upper()})
        preferences["New Bookmarks"].append(hotkey)
        native.append(hotkey)
        hotkeys.append(hotkey)
    for profile in native:
        merge_profile(profile, common)
    for profile in hotkeys:
        merge_profile(profile, settings["Hotkey"])
    global_settings = deepcopy(settings["Global"])
    keymap = global_settings.pop("GlobalKeyMap", {})
    preferences.update(global_settings)
    preferences.setdefault("GlobalKeyMap", {}).update(keymap)
    preferences.setdefault("Custom Color Presets", {})[settings["Theme"]] = theme
    remote = settings["Remote"]
    remote["Dynamic Profile Parent GUID"] = parent["Guid"]
    return preferences, {"Profiles": [remote]}


def install() -> None:
    """Back up native preferences and install shared settings and the SSH profile."""
    running = subprocess.run(
        ["pgrep", "-x", "iTerm2"], stdout=subprocess.DEVNULL, check=False
    )
    if running.returncode == 0:
        raise SystemExit(
            "Quit iTerm before installing preferences; "
            "active sessions are not closed automatically."
        )
    if running.returncode != 1:
        running.check_returncode()
    raw = subprocess.run(
        ["defaults", "export", DOMAIN, "-"],
        check=True,
        capture_output=True,
    ).stdout
    # Native conversion preserves control characters in hotkey definitions.
    exported = subprocess.run(
        ["plutil", "-convert", "binary1", "-o", "-", "-"],
        input=raw,
        check=True,
        capture_output=True,
    ).stdout
    preferences, profiles = prepare(plistlib.loads(exported))
    BACKUPS.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix="preferences-", suffix=".plist", dir=BACKUPS, delete=False
    ) as backup:
        backup.write(exported)
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    if DESTINATION.exists():
        with tempfile.NamedTemporaryFile(
            prefix="profiles-", suffix=".json", dir=BACKUPS, delete=False
        ) as previous:
            previous.write(DESTINATION.read_bytes())
    with tempfile.NamedTemporaryFile(
        mode="w", dir=DESTINATION.parent, delete=False
    ) as output:
        json.dump(profiles, output, indent=2)
        output.write("\n")
    os.replace(output.name, DESTINATION)
    with tempfile.NamedTemporaryFile(suffix=".plist") as merged:
        merged.write(plistlib.dumps(preferences, fmt=plistlib.FMT_BINARY))
        merged.flush()
        subprocess.run(["defaults", "import", DOMAIN, merged.name], check=True)
    print(f"Installed shared settings and SSH profile: {DESTINATION}")
    print(f"Preferences backup: {backup.name}")
    print("Restart iTerm when convenient to reload native and hotkey profile settings.")


if __name__ == "__main__":
    install()
