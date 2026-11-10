"""Common application configuration, backups and atomic file writes."""

from __future__ import annotations

import os
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path

from ..config import load, path

SYNC = load("sync")
STATE = path(SYNC["state"])


def save_backup(content: bytes, directory: Path, name: str, suffix: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix=name + "-", suffix=suffix, dir=directory, delete=False
    ) as output:
        output.write(content)
        return Path(output.name)


def write_if_changed(target: Path, content: str, backups: Path | None = None) -> None:
    """Atomically replace generated files, keeping private data owner-readable."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.is_symlink() and target.exists() and target.read_text() == content:
        if target.stat().st_mode & 0o777 != 0o600:
            target.chmod(0o600)
        return
    if backups is not None and target.exists():
        backup = save_backup(target.read_bytes(), backups, target.stem, target.suffix)
        print(f"Preserved {target} at {backup}")
    descriptor, temporary = tempfile.mkstemp(dir=target.parent, prefix=".dotfiles-")
    try:
        with os.fdopen(descriptor, "w") as stream:
            stream.write(content)
        os.replace(temporary, target)
    finally:
        Path(temporary).unlink(missing_ok=True)


class App(ABC):
    NAME: str

    def __init__(self):
        self.CONFIG = load(self.NAME)
        self.SHARED = path(self.CONFIG["shared"])
        self.BACKUPS = path(self.CONFIG["backups"])
        self.WATCH_PATHS: tuple[Path, ...] = (self.SHARED,)

    @abstractmethod
    def sync(self) -> None:
        """Reconcile this application's selected configuration."""

    def write(self, target: Path, content: str) -> None:
        write_if_changed(target, content, self.BACKUPS)

    def save_backup(self, content: bytes, name: str, suffix: str) -> None:
        backup = save_backup(content, self.BACKUPS, name, suffix)
        print(f"Preserved {name} at {backup}")
