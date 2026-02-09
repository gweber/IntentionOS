from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

from intent.scripts.core.errors import ValidationError
from intent.scripts.core.io import atomic_append_text, read_text


INBOX_LINE_RE = re.compile(
    r"^(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s+—\s+(?P<body>.+)$"
)

TAG_RE = re.compile(r"(^|\s)(#(?P<tag>[A-Za-z0-9_\-]+))")


@dataclass(frozen=True)
class InboxEntry:
    ts: str
    statement: str
    tags: tuple[str, ...]
    raw: str

    def dt(self) -> datetime:
        return datetime.strptime(self.ts, "%Y-%m-%d %H:%M")


def _iter_non_code_lines(lines: Iterable[str]) -> Iterable[str]:
    in_fence = False
    for ln in lines:
        if ln.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        yield ln


def parse_inbox_line(line: str) -> InboxEntry | None:
    ln = (line or "").rstrip("\n")
    if not ln.strip():
        return None
    m = INBOX_LINE_RE.match(ln.strip())
    if not m:
        return None

    ts = m.group("ts")
    body = m.group("body").strip()

    tags = [t.group("tag") for t in TAG_RE.finditer(body)]
    # Remove tags from statement (keep order stable, collapse whitespace).
    stmt = TAG_RE.sub(" ", body)
    stmt = " ".join(stmt.split()).strip()

    return InboxEntry(ts=ts, statement=stmt, tags=tuple(tags), raw=ln)


def read_inbox_entries(path: Path) -> list[InboxEntry]:
    text = read_text(path)
    if not text:
        return []
    entries: list[InboxEntry] = []
    for ln in _iter_non_code_lines(text.splitlines()):
        e = parse_inbox_line(ln)
        if e is not None:
            entries.append(e)
    return entries


def append_inbox_entry(path: Path, line: str) -> None:
    """Append a validated inbox entry line (must match required format)."""
    e = parse_inbox_line(line)
    if e is None:
        raise ValidationError(
            "Inbox line must match: YYYY-MM-DD HH:MM — intent statement (one sentence) #tag"
        )

    suffix = e.raw
    if not suffix.endswith("\n"):
        suffix += "\n"
    atomic_append_text(path, suffix)
