"""Load and validate setup stages."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
SYNC_EXTRAS = {"vscode-sync": "vscode", "iterm-sync": "iterm", "codex-sync": "codex"}


def load(name: str) -> dict[str, Any]:
    document = yaml.safe_load((ROOT / "config/setup.yaml").read_text())
    return document["settings"]["sync"] if name == "sync" else document["setup-" + name]["settings"]


def path(value: str) -> Path:
    expanded = Path.home() / value[2:] if value.startswith("~/") else Path(value)
    return expanded if expanded.is_absolute() else ROOT / expanded


@dataclass(frozen=True)
class Package:
    kind: str
    name: str
    id: int = 0

    def brew_line(self) -> str:
        suffix = f", id: {self.id}" if self.kind == "mas" else ""
        return f'{self.kind} "{self.name}"{suffix}'


@dataclass(frozen=True)
class Configuration:
    source: str
    destination: str = ""
    mode: str = "link"
    adapter: str = ""

    def __post_init__(self):
        for name in ("source", "destination"):
            value = getattr(self, name)
            if name == "destination" and not value:
                continue
            relative = Path(value)
            if not relative.parts or relative.is_absolute() or ".." in relative.parts:
                raise ValueError(f"Stage paths must remain relative and nonempty: {value}")
            object.__setattr__(self, name, relative.as_posix())
        if self.mode not in {"link", "seed"}:
            raise ValueError(f"Unknown configuration mode: {self.mode}")


@dataclass(frozen=True)
class Stage:
    id: str
    title: str
    description: str
    packages: tuple[Package, ...]
    configuration: tuple[Configuration, ...]
    actions: tuple[str, ...] = ()


def load_catalog(root: Path) -> tuple[Stage, ...]:
    stages = []
    owners: dict[Path, str] = {}
    destinations: set[str] = set()
    root = root.resolve()
    document = yaml.safe_load((root / "config/setup.yaml").read_text())
    for stage_id, settings in document.items():
        if stage_id == "settings":
            continue
        unknown = set(settings) - {
            "title",
            "description",
            "brew",
            "cask",
            "mas",
            "link",
            "extras",
            "settings",
        }
        if unknown:
            raise ValueError(f"Unknown actions in {stage_id}: {', '.join(sorted(unknown))}")
        extras = settings.get("extras", ())
        if set(extras) - {"shell-plugins", "sudo-touch-id", "macos-defaults"} - SYNC_EXTRAS.keys():
            raise ValueError(f"Unknown extras in {stage_id}.")
        for kind in ("brew", "cask", "mas"):
            if kind in settings:
                values = settings[kind]
                if kind == "mas":
                    valid = isinstance(values, dict) and all(
                        isinstance(k, str) and type(v) is int for k, v in values.items()
                    )
                else:
                    valid = isinstance(values, list) and all(isinstance(v, str) for v in values)
                if not valid:
                    raise ValueError(
                        f"{stage_id}.{kind} must be a package list or App Store name/ID mapping."
                    )
        configs = tuple(Configuration(**c) for c in settings.get("link", ())) + tuple(
            Configuration(document["setup-" + name]["settings"]["shared"], adapter=name)
            for name in (SYNC_EXTRAS[extra] for extra in extras if extra in SYNC_EXTRAS)
        )
        packages = tuple(
            Package(kind, name, values[name] if kind == "mas" else 0)
            for kind, values in settings.items()
            if kind in {"brew", "cask", "mas"}
            for name in values
        )
        stage = Stage(
            stage_id,
            settings["title"],
            settings["description"],
            packages,
            configs,
            tuple(extras),
        )
        for config in configs:
            source = root / config.source
            source = source.parent.resolve() / source.name
            if not source.is_relative_to(root):
                raise ValueError(f"Configuration source escapes the repository: {config.source}")
            for owned, owner in owners.items():
                if source.is_relative_to(owned) or owned.is_relative_to(source):
                    raise ValueError(f"Configuration has overlapping owners: {owner}, {stage.id}")
            owners[source] = stage.id
            if config.destination:
                if any(
                    config.destination == d
                    or config.destination.startswith(d + "/")
                    or d.startswith(config.destination + "/")
                    for d in destinations
                ):
                    raise ValueError(f"Duplicate configuration destination: {config.destination}")
                destinations.add(config.destination)
        stages.append(stage)
    return tuple(stages)


def collect_packages(stages: tuple[Stage, ...]) -> tuple[Package, ...]:
    packages = {(p.kind, p.name): p for stage in stages for p in stage.packages}
    if any(p.kind == "mas" for p in packages.values()):
        packages[("brew", "mas")] = Package("brew", "mas")
    return tuple(packages.values())


def collect_apps(stages: tuple[Stage, ...]) -> tuple[str, ...]:
    return tuple(c.adapter for stage in stages for c in stage.configuration if c.adapter)
