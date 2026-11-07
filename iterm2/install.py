"""Install portable iTerm profiles while retaining machine-local profiles."""

import json
import plistlib
import subprocess
import tempfile
import uuid
from copy import deepcopy
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

from scripts.preferences import STATE, write_if_changed

DOMAIN = "com.googlecode.iterm2"
SHARED = Path(__file__).resolve().parent
DESTINATION = Path.home() / "Library/Application Support/iTerm2/DynamicProfiles/dotfiles.json"
BACKUPS = STATE / "iterm2"
MODE = BACKUPS / "sync-mode"
WATCH_PATHS = [SHARED]
THEME_LIBRARY = (
    "https://raw.githubusercontent.com/mbadolato/iTerm2-Color-Schemes/"
    "b84cd1e68c9033d967fccd9febbac3072d127b7b/schemes/"
)


def sync() -> None:
    raw = subprocess.run(
        ["defaults", "export", DOMAIN, "-"], check=True, capture_output=True
    ).stdout
    # Native conversion preserves control characters in hotkey definitions.
    exported = subprocess.run(
        ["plutil", "-convert", "binary1", "-o", "-", "-"],
        input=raw,
        check=True,
        capture_output=True,
    ).stdout
    original = plistlib.loads(exported)
    if original.get("LoadPrefsFromCustomFolder"):
        raise RuntimeError("Disable iTerm's custom preferences folder before using dotfiles sync.")
    preferences, profiles = build_preferences(original)
    content = json.dumps(profiles, indent=2) + "\n"
    if DESTINATION.exists() and DESTINATION.read_text() != content:
        save_backup(DESTINATION.read_bytes(), "profiles", ".json")
    write_if_changed(DESTINATION, content)
    if preferences == original:
        return
    running = subprocess.run(["pgrep", "-x", "iTerm2"], stdout=subprocess.DEVNULL, check=False)
    if running.returncode == 0:
        return  # Reconcile native preferences after iTerm exits, preserving sessions.
    if running.returncode != 1:
        running.check_returncode()
    save_backup(exported, "preferences", ".plist")
    with tempfile.NamedTemporaryFile(suffix=".plist") as merged:
        merged.write(plistlib.dumps(preferences, fmt=plistlib.FMT_BINARY))
        merged.flush()
        subprocess.run(["defaults", "import", DOMAIN, merged.name], check=True)


def build_preferences(preferences: dict) -> tuple[dict, dict]:
    """Apply shared settings while preserving native identities and local fields."""
    preferences = deepcopy(preferences)
    settings = json.loads((SHARED / "settings.json").read_text())
    theme = load_theme(preferences, settings["Theme"])
    common = {**settings["Profile"], **theme}
    native = [
        profile
        for profile in preferences.get("New Bookmarks", [])
        if profile.get("Guid") != settings["Remote"]["Guid"] and not profile.get("Dynamic Profile")
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
        apply_profile_settings(profile, common)
    for profile in hotkeys:
        apply_profile_settings(profile, settings["Hotkey"])
    global_settings = deepcopy(settings["Global"])
    keymap = global_settings.pop("GlobalKeyMap", {})
    preferences.update(global_settings)
    preferences.setdefault("GlobalKeyMap", {}).update(keymap)
    preferences.setdefault("Custom Color Presets", {})[settings["Theme"]] = theme
    remote = {**common, **settings["Remote"]}
    remote["Dynamic Profile Parent GUID"] = parent["Guid"]
    return preferences, {"Profiles": [remote]}


def apply_profile_settings(profile: dict, settings: dict) -> None:
    """Merge key bindings without dropping machine-local shortcuts."""
    values = deepcopy(settings)
    keymap = values.pop("Keyboard Map", {})
    for action in keymap.values():
        if action.get("Text") == "$PROFILE_GUID":
            action["Text"] = profile["Guid"]
    profile.update(values)
    profile.setdefault("Keyboard Map", {}).update(keymap)


def load_theme(preferences: dict, name: str) -> dict:
    """Reuse an imported preset or import it from the pinned theme library."""
    preset = preferences.get("Custom Color Presets", {}).get(name)
    if preset is not None:
        return preset
    cache = STATE / "iterm2/themes" / f"{quote(name, safe='')}.json"
    if cache.exists():
        return json.loads(cache.read_text())
    with urlopen(f"{THEME_LIBRARY}{quote(name)}.itermcolors", timeout=15) as response:
        theme = plistlib.loads(response.read())
    write_if_changed(cache, json.dumps(theme))
    return theme


def save_backup(content: bytes, name: str, suffix: str) -> None:
    BACKUPS.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix=name + "-", suffix=suffix, dir=BACKUPS, delete=False
    ) as output:
        output.write(content)
