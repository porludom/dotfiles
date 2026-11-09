"""VS Code settings, extension membership and UI state."""

from __future__ import annotations

import json
import re
import shutil
import sqlite3
import subprocess
from pathlib import Path
from typing import Any

from ..config import path
from .base import STATE, App, write_if_changed


class VSCode(App):
    NAME = "vscode"

    def __init__(self):
        super().__init__()
        self.PRIVATE = path(self.CONFIG["private"])
        self.USER = path(self.CONFIG["user"])
        self.EXTENSIONS = path(self.CONFIG["extensions"])
        self.EXTENSION_BASELINE = STATE / self.CONFIG["baseline"]
        self.WATCH_PATHS = (self.SHARED, self.PRIVATE.parent, self.EXTENSIONS)
        self.LAYOUT_KEYS = frozenset(self.CONFIG["layout_keys"])

    def sync(self) -> None:
        values = {}
        database = self.USER / "globalStorage/state.vscdb"
        if database.exists():
            with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as connection:
                values = dict(connection.execute("SELECT key, value FROM ItemTable"))
        if values.get("sync.enable") == "true":
            raise RuntimeError("Turn off Settings Sync in VS Code before using dotfiles sync.")
        self.sync_settings()
        self.sync_extensions()
        if values:
            self.export_ui_state(values, self.SHARED / "ui-state.code-profile")

    def sync_settings(self, user_dir: Path | None = None) -> None:
        user_dir = self.USER if user_dir is None else user_dir
        settings = self.read_jsonc(self.SHARED / "settings.jsonc")
        settings.update(self.read_jsonc(self.SHARED / "extras.jsonc"))
        private = self.read_jsonc(self.PRIVATE) if self.PRIVATE.exists() else {}
        settings.update(private)
        # Keep private overrides out of cloud Sync if native mode is selected later.
        settings["settingsSync.ignoredSettings"] = sorted(
            set(settings.get("settingsSync.ignoredSettings", [])) | set(private)
        )
        keybindings = (
            (self.SHARED / "keybindings.json")
            .read_text()
            .replace("${vscodeDir}", self.SHARED.as_uri())
        )
        user_dir.mkdir(parents=True, exist_ok=True)
        self.write(
            user_dir / "settings.json", json.dumps(settings, indent=2, ensure_ascii=False) + "\n"
        )
        self.write(user_dir / "keybindings.json", keybindings)

    def sync_extensions(self) -> None:
        """Merge local and repository membership changes since the last sync."""
        manifest = self.SHARED / "extensions.txt"
        original = manifest.read_text()
        requested = {
            line.strip().lower()
            for line in original.splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        if self.EXTENSION_BASELINE.exists() and not self.EXTENSIONS.exists():
            raise FileNotFoundError(
                "VS Code extension inventory is unavailable; keeping the manifest."
            )
        installed = self.read_installed_extensions()
        desired = installed | requested
        if self.EXTENSION_BASELINE.exists():
            previous = set(json.loads(self.EXTENSION_BASELINE.read_text()))
            # Apply repo edits; preserve local edits where the repo did not change.
            desired = (installed | (requested - previous)) - (previous - requested)
        additions, removals = desired - installed, installed - desired
        if additions or removals:
            code = shutil.which("code") or str(path(self.CONFIG["cli"]))
            for option, extensions in (
                ("--install-extension", additions),
                ("--uninstall-extension", removals),
            ):
                for extension in sorted(extensions):
                    subprocess.run(
                        [code, option, extension],
                        check=True,
                        timeout=self.CONFIG["extension_timeout_seconds"],
                    )
            installed = self.read_installed_extensions()
            if desired - installed or removals & installed:
                raise RuntimeError(
                    "Extension inventory did not reflect CLI changes; retrying next sync."
                )
        if manifest.read_text() != original:
            raise RuntimeError(
                "Extension manifest changed during sync; retrying without overwriting it."
            )
        write_if_changed(
            manifest,
            "# Synced with local VS Code installs and uninstalls.\n"
            + "\n".join(sorted(installed))
            + "\n",
        )
        write_if_changed(self.EXTENSION_BASELINE, json.dumps(sorted(installed), indent=2) + "\n")

    def export_ui_state(self, values: dict, destination: Path) -> None:
        targets = json.loads(values.get("__$__targetStorageMarker", "{}"))
        storage = {
            key: value
            for key, value in sorted(values.items())
            if targets.get(key) == 0
            and (
                key in self.LAYOUT_KEYS
                or key.startswith(("workbench.", "~remote."))
                and key.endswith(".hidden")
            )
        }
        profile = {"name": "Dotfiles UI", "globalState": json.dumps({"storage": storage})}
        content = json.dumps(profile, indent=2, ensure_ascii=False) + "\n"
        write_if_changed(destination, content)

    def read_jsonc(self, path: Path) -> dict[str, Any]:
        """Read JSON with comments and trailing commas without altering strings."""
        text = path.read_text()
        string = r'"(?:\\.|[^"\\])*"'
        text = re.sub(
            rf"({string})|//[^\n]*|/\*[\s\S]*?\*/",
            lambda match: match[1] or "",
            text,
        )
        text = re.sub(
            rf"({string})|,\s*(?=[}}\]])",
            lambda match: match[1] or "",
            text,
        )
        return json.loads(text)

    def read_installed_extensions(self) -> set[str]:
        """Read the default profile's inventory without starting VS Code's CLI."""
        return (
            {entry["identifier"]["id"].lower() for entry in json.loads(self.EXTENSIONS.read_text())}
            if self.EXTENSIONS.exists()
            else set()
        )
