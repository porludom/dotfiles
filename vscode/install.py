"""Install shared VS Code preferences with machine-local overrides."""

import json
import re
import shutil
import sqlite3
import subprocess
from pathlib import Path
from typing import Any

from scripts.preferences import STATE, write_if_changed

SHARED = Path(__file__).resolve().parent
PRIVATE = Path.home() / ".dotfiles_secret/vscode/settings.local.jsonc"
USER = Path.home() / "Library/Application Support/Code/User"
MODE = USER / "dotfiles-sync-mode"
EXTENSIONS = Path.home() / ".vscode/extensions/extensions.json"
EXTENSION_BASELINE = STATE / "vscode/extensions.json"
WATCH_PATHS = [SHARED, PRIVATE.parent, EXTENSIONS]


LAYOUT_KEYS = {
    "workbench.panel.pinnedPanels",
    "workbench.activity.pinnedViewlets2",
    "workbench.auxiliarybar.pinnedPanels",
    "workbench.statusbar.hidden",
    "workbench.panel.alignment",
    "workbench.activityBar.location",
    "views.customizations",
    "menu.hiddenCommands",
    "terminal.integrated.tabs.showDetailed",
    "tabs-list-width-horizontal",
    "terminal.hidden",
    "Comments.hidden",
    "refactorPreview.hidden",
}


def sync() -> None:
    values = {}
    database = USER / "globalStorage/state.vscdb"
    if database.exists():
        with sqlite3.connect(database.as_uri() + "?mode=ro", uri=True) as connection:
            values = dict(connection.execute("SELECT key, value FROM ItemTable"))
    if values.get("sync.enable") == "true":
        raise RuntimeError("Turn off Settings Sync in VS Code before using dotfiles sync.")
    sync_settings()
    sync_extensions()
    if values:
        export_ui_state(values, SHARED / "ui-state.code-profile")


def sync_settings(user_dir: Path = USER) -> None:
    settings = read_jsonc(SHARED / "settings.jsonc")
    settings.update(read_jsonc(SHARED / "extras.jsonc"))
    private = read_jsonc(PRIVATE) if PRIVATE.exists() else {}
    settings.update(private)
    # Keep private overrides out of cloud Sync if native mode is selected later.
    settings["settingsSync.ignoredSettings"] = sorted(
        set(settings.get("settingsSync.ignoredSettings", [])) | set(private)
    )
    keybindings = (SHARED / "keybindings.json").read_text().replace("${vscodeDir}", SHARED.as_uri())
    user_dir.mkdir(parents=True, exist_ok=True)
    write_if_changed(
        user_dir / "settings.json",
        json.dumps(settings, indent=2, ensure_ascii=False) + "\n",
    )
    write_if_changed(user_dir / "keybindings.json", keybindings)


def sync_extensions() -> None:
    """Merge local and repository membership changes since the last sync."""
    manifest = SHARED / "extensions.txt"
    original = manifest.read_text()
    requested = {
        line.strip().lower()
        for line in original.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    if EXTENSION_BASELINE.exists() and not EXTENSIONS.exists():
        raise FileNotFoundError("VS Code extension inventory is unavailable; keeping the manifest.")
    installed = read_installed_extensions()
    desired = installed | requested
    if EXTENSION_BASELINE.exists():
        previous = set(json.loads(EXTENSION_BASELINE.read_text()))
        # Apply repo edits; preserve local edits where the repo did not change.
        desired = (installed | (requested - previous)) - (previous - requested)
    additions, removals = desired - installed, installed - desired
    if additions or removals:
        code = (
            shutil.which("code")
            or "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
        )
        for option, extensions in (
            ("--install-extension", additions),
            ("--uninstall-extension", removals),
        ):
            for extension in sorted(extensions):
                subprocess.run([code, option, extension], check=True, timeout=600)
        installed = read_installed_extensions()
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
    write_if_changed(EXTENSION_BASELINE, json.dumps(sorted(installed), indent=2) + "\n")


def export_ui_state(values: dict, destination: Path) -> None:
    targets = json.loads(values.get("__$__targetStorageMarker", "{}"))
    storage = {
        key: value
        for key, value in sorted(values.items())
        if targets.get(key) == 0
        and (
            key in LAYOUT_KEYS
            or key.startswith(("workbench.", "~remote."))
            and key.endswith(".hidden")
        )
    }
    profile = {"name": "Dotfiles UI", "globalState": json.dumps({"storage": storage})}
    content = json.dumps(profile, indent=2, ensure_ascii=False) + "\n"
    write_if_changed(destination, content)


def read_jsonc(path: Path) -> dict[str, Any]:
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


def read_installed_extensions() -> set[str]:
    """Read the default profile's inventory without starting VS Code's CLI."""
    return (
        {entry["identifier"]["id"].lower() for entry in json.loads(EXTENSIONS.read_text())}
        if EXTENSIONS.exists()
        else set()
    )
