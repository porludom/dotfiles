"""iTerm native preferences and dynamic profiles."""

from __future__ import annotations

import json
import plistlib
import subprocess
import tempfile
import uuid
from copy import deepcopy
from pathlib import Path
from urllib.parse import quote
from urllib.request import urlopen

from ..config import path
from .base import STATE, App, write_if_changed


class ITerm(App):
    NAME = "iterm"

    def __init__(self):
        super().__init__()
        self.DOMAIN = self.CONFIG["domain"]
        self.DESTINATION = path(self.CONFIG["destination"])
        self.THEME_LIBRARY = self.CONFIG["theme_library"]
        self.PREFERENCES = Path.home() / "Library/Preferences" / (self.DOMAIN + ".plist")
        self.WATCH_PATHS = (self.SHARED, self.PREFERENCES)

    def sync(self) -> None:
        try:
            raw = subprocess.run(
                ["defaults", "export", self.DOMAIN, "-"], check=True, capture_output=True
            ).stdout
        except subprocess.CalledProcessError:
            if self.PREFERENCES.exists():
                raise
            print("iTerm: open it once; settings will be applied automatically after first launch.")
            return
        # Native conversion preserves control characters in hotkey definitions.
        exported = subprocess.run(
            ["plutil", "-convert", "binary1", "-o", "-", "-"],
            input=raw,
            check=True,
            capture_output=True,
        ).stdout
        original = plistlib.loads(exported)
        if original.get("LoadPrefsFromCustomFolder"):
            raise RuntimeError(
                "Disable iTerm's custom preferences folder before using dotfiles sync."
            )
        if not original.get("New Bookmarks"):
            print("iTerm: open it once; settings will be applied automatically after first launch.")
            return
        preferences, profiles = self.build_preferences(original)
        content = json.dumps(profiles, indent=2) + "\n"
        self.write(self.DESTINATION, content)
        if preferences == original:
            return
        running = subprocess.run(
            ["pgrep", "-x", self.CONFIG["process"]], stdout=subprocess.DEVNULL, check=False
        )
        if running.returncode == 0:
            return  # Reconcile native preferences after iTerm exits, preserving sessions.
        if running.returncode != 1:
            running.check_returncode()
        self.save_backup(exported, "preferences", ".plist")
        with tempfile.NamedTemporaryFile(suffix=".plist") as merged:
            merged.write(plistlib.dumps(preferences, fmt=plistlib.FMT_BINARY))
            merged.flush()
            subprocess.run(["defaults", "import", self.DOMAIN, merged.name], check=True)

    def build_preferences(self, preferences: dict) -> tuple[dict, dict]:
        preferences = deepcopy(preferences)
        settings = json.loads((self.SHARED / "settings.json").read_text())
        native = [
            profile
            for profile in preferences.get("New Bookmarks", [])
            if profile.get("Guid") != settings["Remote"]["Guid"]
            and not profile.get("Dynamic Profile")
        ]
        if not native:
            raise ValueError("Open iTerm once to create its default profile, then retry.")
        theme = self.load_theme(preferences, settings["Theme"])
        common = {**settings["Profile"], **theme}
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
            self.apply_profile_settings(profile, common)
        for profile in hotkeys:
            self.apply_profile_settings(profile, settings["Hotkey"])
        global_settings = deepcopy(settings["Global"])
        keymap = global_settings.pop("GlobalKeyMap", {})
        preferences.update(global_settings)
        preferences.setdefault("GlobalKeyMap", {}).update(keymap)
        preferences.setdefault("Custom Color Presets", {})[settings["Theme"]] = theme
        remote = {**common, **settings["Remote"]}
        remote["Dynamic Profile Parent GUID"] = parent["Guid"]
        return preferences, {"Profiles": [remote]}

    def apply_profile_settings(self, profile: dict, settings: dict) -> None:
        values = deepcopy(settings)
        keymap = values.pop("Keyboard Map", {})
        for action in keymap.values():
            if action.get("Text") == "$PROFILE_GUID":
                action["Text"] = profile["Guid"]
        profile.update(values)
        profile.setdefault("Keyboard Map", {}).update(keymap)

    def load_theme(self, preferences: dict, name: str) -> dict:
        preset = preferences.get("Custom Color Presets", {}).get(name)
        if preset is not None:
            return preset
        cache = STATE / self.CONFIG["theme_cache"] / f"{quote(name, safe='')}.json"
        if cache.exists():
            return json.loads(cache.read_text())
        with urlopen(
            f"{self.THEME_LIBRARY}{quote(name)}.itermcolors",
            timeout=self.CONFIG["theme_timeout_seconds"],
        ) as response:
            theme = plistlib.loads(response.read())
        write_if_changed(cache, json.dumps(theme))
        return theme
