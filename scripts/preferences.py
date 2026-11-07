"""Shared storage and atomic writes for application preferences."""

import os
import tempfile
from pathlib import Path

STATE = Path.home() / ".local/state/dotfiles"


def write_if_changed(target: Path, content: str) -> None:
    """Atomically replace generated files, keeping private data owner-readable."""
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.is_symlink() and target.exists() and target.read_text() == content:
        if target.stat().st_mode & 0o777 != 0o600:
            target.chmod(0o600)
        return
    descriptor, temporary = tempfile.mkstemp(dir=target.parent, prefix=".dotfiles-")
    try:
        with os.fdopen(descriptor, "w") as stream:
            stream.write(content)
        os.replace(temporary, target)
    finally:
        Path(temporary).unlink(missing_ok=True)
