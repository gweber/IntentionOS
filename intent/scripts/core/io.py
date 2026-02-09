from __future__ import annotations

import os
from pathlib import Path
from typing import Final


_ENCODING: Final[str] = "utf-8"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding=_ENCODING)


def atomic_write_text(path: Path, content: str) -> None:
    """Atomic write: write to temp file then os.replace()."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_name(path.name + ".tmp")
    tmp_path.write_text(content, encoding=_ENCODING)
    os.replace(tmp_path, path)


def atomic_append_text(path: Path, suffix: str) -> None:
    """Append-only via atomic rewrite (safe for small markdown logs)."""
    existing = read_text(path)
    atomic_write_text(path, existing + suffix)
