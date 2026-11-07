"""Install shared VS Code preferences with machine-local overrides."""

import argparse
import json
import os
import plistlib
import re
import subprocess
import sys
import tempfile
from pathlib import Path

SHARED = Path(__file__).resolve().parent
PRIVATE = Path.home() / ".dotfiles_secret/vscode/settings.local.jsonc"
USER = Path.home() / "Library/Application Support/Code/User"


def read_jsonc(path: Path) -> dict[str, object]:
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


def install(user_dir: Path = USER) -> None:
    settings = read_jsonc(SHARED / "settings.jsonc")
    settings.update(read_jsonc(SHARED / "extras.jsonc"))
    if PRIVATE.exists():
        settings.update(read_jsonc(PRIVATE))

    user_dir.mkdir(parents=True, exist_ok=True)
    content = json.dumps(settings, indent=2, ensure_ascii=False) + "\n"
    target = user_dir / "settings.json"
    if not target.exists() or target.read_text() != content:
        # Atomic replacement leaves the previous settings intact on parse failures.
        descriptor, temporary = tempfile.mkstemp(dir=user_dir, prefix=".settings-")
        try:
            with os.fdopen(descriptor, "w") as stream:
                stream.write(content)
            os.replace(temporary, target)
        finally:
            Path(temporary).unlink(missing_ok=True)
    elif target.stat().st_mode & 0o777 != 0o600:
        target.chmod(0o600)

    keybindings = user_dir / "keybindings.json"
    source = SHARED / "keybindings.json"
    if keybindings.is_symlink() and keybindings.resolve() == source:
        return
    keybindings.unlink(missing_ok=True)
    keybindings.symlink_to(source)


def enable_sync() -> None:
    """Register automatic updates for the current macOS login user."""
    label = "com.dotfiles.vscode-sync"
    agents = Path.home() / "Library/LaunchAgents"
    agents.mkdir(parents=True, exist_ok=True)
    log = Path.home() / "Library/Logs/dotfiles-vscode-sync.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    log.touch(mode=0o600, exist_ok=True)
    agent = {
        "Label": label,
        "ProgramArguments": [sys.executable, str(SHARED / "install.py")],
        "WatchPaths": [str(SHARED), str(PRIVATE.parent)],
        # WatchPaths can miss events, so reconcile periodically as well.
        "StartInterval": 30,
        "RunAtLoad": True,
        "StandardErrorPath": str(log),
    }
    path = agents / f"{label}.plist"
    path.write_bytes(plistlib.dumps(agent))
    service = f"gui/{os.getuid()}/{label}"
    subprocess.run(
        ["launchctl", "bootout", service], capture_output=True, check=False
    )
    subprocess.run(
        ["launchctl", "bootstrap", f"gui/{os.getuid()}", str(path)], check=True
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--enable-sync", action="store_true")
    args = parser.parse_args()
    install()
    if args.enable_sync:
        enable_sync()
