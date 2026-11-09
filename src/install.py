"""Choose setup stages, link dotfiles and apply settings."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from . import apps
from .config import ROOT, Plan, collect_packages, load, load_catalog, path, resolve


def prune_local(root: Path, plan: Plan):
    for stage in plan.deleted:
        for config in stage.configuration:
            source = root / config.source
            if config.destination and (Path.home() / config.destination).resolve().is_relative_to(
                source.resolve()
            ):
                print(f"Keeping {config.source}: live configuration uses it.")
                continue
            if source.is_dir() and not source.is_symlink():
                shutil.rmtree(source)
            else:
                source.unlink(missing_ok=True)
            print(f"Deleted {config.source}")


def run_shell(name, *args, **kwargs):
    return subprocess.run(
        ["bash", str(ROOT / "src/system.sh"), "--" + name, *map(str, args)],
        check=True,
        **kwargs,
    )


def link(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and source.exists() and destination.samefile(source):
        return
    preserve(destination)
    destination.symlink_to(source, target_is_directory=source.is_dir())


def preserve(destination):
    if destination.exists() or destination.is_symlink():
        backup = (
            Path(tempfile.mkdtemp(prefix="dotfiles-backup-", dir=Path.home())) / destination.name
        )
        shutil.move(str(destination), backup)
        print(f"Preserved {destination} at {backup}")


def link_home(source, destination):
    if not source.is_dir() or source.is_symlink():
        link(source, destination)
        return
    if destination.is_symlink():
        existing = destination.resolve()
        preserve(destination)
        destination.mkdir(parents=True)
        if existing.is_dir():
            link_home(existing, destination)
    elif destination.exists() and not destination.is_dir():
        preserve(destination)
    destination.mkdir(parents=True, exist_ok=True)
    for entry in source.iterdir():
        link_home(entry, destination / entry.name)


def check_sources(root: Path, plan: Plan):
    if not (root / "home").is_dir():
        raise RuntimeError("Restore the repository home/ directory before applying dotfiles.")
    for stage in plan.installed:
        for config in stage.configuration:
            if not (root / config.source).exists():
                raise RuntimeError(f"Restore missing selected configuration first: {config.source}")


def apply(root: Path, plan: Plan, command="apply"):
    check_sources(root, plan)
    link_home(root / "home", Path.home())
    for stage in plan.installed:
        print(f"Stage: {stage.title}")
        if command in {"install", "update"} and stage.packages:
            selected = collect_packages((stage,))
            with tempfile.NamedTemporaryFile(mode="w", suffix=".Brewfile") as temporary:
                temporary.write("\n".join(p.brew_line() for p in selected) + "\n")
                temporary.flush()
                run_shell(
                    "packages",
                    command,
                    temporary.name,
                    *[
                        v
                        for p in selected
                        for v in (p.kind, str(p.id) if p.kind == "mas" else p.name)
                    ],
                )
        for config in stage.configuration:
            if not config.destination:
                continue
            source, destination = root / config.source, Path.home() / config.destination
            if config.mode == "seed":
                if not destination.exists() and not destination.is_symlink():
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source, destination)
            else:
                link(source, destination)
        for extra in stage.actions:
            if extra == "shell-plugins":
                run_shell("packages", "plugins", "update" if command == "update" else "install")
            elif extra == "sudo-touch-id" and command == "install":
                touch_id = load("macos")["touch_id"]
                if touch_id["enabled"]:
                    run_shell("touch-id", path(touch_id["path"]), path(touch_id["template"]))
            elif extra == "macos-defaults" and command == "install":
                macos_preferences()
            elif extra == "vscode" and command == "install":
                for association in load("vscode")["file_associations"]:
                    subprocess.run(shlex.split(association), check=True)
    apps.sync_apps(root, plan.apps)


def macos_preferences():
    settings = load("macos")
    subprocess.run(["osascript", "-e", 'tell application "System Preferences" to quit'], check=True)
    for command in settings["defaults"]:
        subprocess.run(shlex.split(command), check=True)
    for name in settings["restart"]:
        subprocess.run(["killall", name], capture_output=True, check=False)


def prompt(stages):
    choices = {}
    print(
        "Install missing software/configuration, delete local stage sources, or keep untouched. No application is uninstalled."
    )
    for stage in stages:
        while True:
            answer = (
                input(
                    f"\n{stage.title}: {stage.description}\n[i] Install  [d] Delete from local  [k] Keep local [k]: "
                )
                .strip()
                .lower()
                or "k"
            )
            if answer in {"i", "d", "k"}:
                choices[stage.id] = answer
                break
            print("Choose i, d or k.")
    return choices


def main(argv=None, root=ROOT):
    parser = argparse.ArgumentParser(prog="./install", description=__doc__)
    parser.add_argument(
        "command",
        choices=["install", "apply", "update", "sync", "cleanup"],
        nargs="?",
        default="install",
    )
    parser.add_argument(
        "--choose", action="store_true", help="Review stage choices again during installation"
    )
    args = parser.parse_args(argv)
    if sys.platform != "darwin":
        parser.error("This installer supports macOS only.")
    os.environ["PATH"] = (
        f"{Path.home() / '.local/bin'}:/opt/homebrew/bin:/usr/local/bin:"
        + os.environ.get("PATH", "")
    )
    command = args.command
    if command == "cleanup":
        run_shell("packages", "cleanup")
        print("Package caches cleaned.")
        return
    if command == "update" and not os.environ.get("DOTFILES_AFTER_PULL"):
        os.execv("/bin/bash", ["bash", str(ROOT / "src/system.sh"), "--update", str(root)])
        return

    state = root / ".install/choices.local.json"
    fresh = command == "install" and (args.choose or not state.exists())
    if not fresh and not state.exists():
        raise RuntimeError("Choose stages with make install before apply/update/sync.")
    catalog = load_catalog(root / "install.yaml")
    choices = prompt(catalog) if fresh else json.loads(state.read_text())
    plan = resolve(catalog, choices)
    if fresh:
        state.parent.mkdir(exist_ok=True)
        state.write_text(json.dumps(choices, indent=2) + "\n")
        state.chmod(0o600)
    if command == "sync":
        apps.sync_apps(root, plan.apps, register_agent=False)
        return
    apply(root, plan, command=command)
    if command == "install":
        prune_local(root, plan)
        if fresh:
            answer = input("\nCreate a GitHub fork and use it as origin? [y/N]: ")
            run_shell("fork", answer, cwd=root)
    print("Dotfiles applied. Review changes, then stage, commit and push them yourself.")


if __name__ == "__main__":
    try:
        main()
    except (EOFError, KeyboardInterrupt):
        raise SystemExit("Interrupted; no consent was assumed.") from None
