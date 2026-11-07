"""Install and sync VS Code and iTerm preferences from dotfiles."""

import argparse
import fcntl
import os
import plistlib
import subprocess
import sys
from pathlib import Path
from types import ModuleType

from iterm2 import install as iterm
from scripts.preferences import STATE, write_if_changed
from vscode import install as vscode

ROOT = Path(__file__).resolve().parent
APPS = {"vscode": vscode, "iterm2": iterm}
LABEL = "com.dotfiles.sync"
AGENT = Path.home() / f"Library/LaunchAgents/{LABEL}.plist"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--setup", nargs="?", const="ask", choices=["ask", "dotfiles", "native"])
    parser.add_argument("--app", choices=APPS)
    args = parser.parse_args()
    STATE.mkdir(parents=True, exist_ok=True)
    if args.setup:
        unload_sync_agent()
    failed = False
    with (STATE / "sync.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        try:
            for name, app in APPS.items():
                if args.app and name != args.app:
                    continue
                try:
                    selected = args.setup or read_sync_mode(app)
                    if selected == "ask":
                        default = read_sync_mode(app) if app.MODE.exists() else "dotfiles"
                        selected = (
                            input(f"{name}: dotfiles/native [{default}]: ").strip() or default
                        )
                    if selected not in {"dotfiles", "native"}:
                        raise ValueError("Choose dotfiles or native.")
                    if selected == "dotfiles":
                        app.sync()
                    if args.setup:
                        write_if_changed(app.MODE, selected + "\n")
                        print(f"{name}: {selected} owns settings.")
                except Exception as error:  # noqa: BLE001 -- One app must not stop the other.
                    print(f"{name}: {error}", file=sys.stderr)
                    failed = True
        finally:
            if args.setup:
                load_sync_agent()
    if failed:
        raise SystemExit(1)


def unload_sync_agent() -> None:
    for label in ("com.dotfiles.vscode-sync", LABEL):
        subprocess.run(
            ["launchctl", "bootout", f"gui/{os.getuid()}/{label}"],
            capture_output=True,
            check=False,
        )
        (AGENT.parent / f"{label}.plist").unlink(missing_ok=True)


def load_sync_agent() -> None:
    managed = [app for app in APPS.values() if read_sync_mode(app) == "dotfiles"]
    if not managed:
        return
    log = STATE / "sync.log"
    log.touch(mode=0o600, exist_ok=True)
    AGENT.parent.mkdir(parents=True, exist_ok=True)
    AGENT.write_bytes(
        plistlib.dumps(
            {
                "Label": LABEL,
                "ProgramArguments": [sys.executable, str(ROOT / "sync.py")],
                "WatchPaths": [
                    str(ROOT / "sync.py"),
                    str(ROOT / "scripts/preferences.py"),
                ]
                + [str(path) for app in managed for path in app.WATCH_PATHS],
                "StartInterval": 4 * 60 * 60,
                "RunAtLoad": True,
                "StandardErrorPath": str(log),
            }
        )
    )
    subprocess.run(["launchctl", "bootstrap", f"gui/{os.getuid()}", str(AGENT)], check=True)


def read_sync_mode(app: ModuleType) -> str:
    return app.MODE.read_text().strip() if app.MODE.exists() else "native"


if __name__ == "__main__":
    main()
