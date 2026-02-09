from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from agent_scripts.core.io import atomic_append_text


DECISION_LINE_RE = re.compile(r"^\s*(?:[-*]\s*)?Decision:\s*(.+?)\s*$")
ASSUMPTION_LINE_RE = re.compile(r"^\s*(?:[-*]\s*)?Assumption:\s*(.+?)\s*$")


@dataclass(frozen=True)
class MemoryUpdates:
    decisions: tuple[str, ...]
    assumptions: tuple[str, ...]


def extract_memory_updates(artifact_md: str) -> MemoryUpdates:
    decisions: list[str] = []
    assumptions: list[str] = []
    for ln in (artifact_md or "").splitlines():
        m = DECISION_LINE_RE.match(ln)
        if m:
            decisions.append(m.group(1).strip())
            continue
        m = ASSUMPTION_LINE_RE.match(ln)
        if m:
            assumptions.append(m.group(1).strip())
    return MemoryUpdates(decisions=tuple(decisions), assumptions=tuple(assumptions))


def _stamp(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M")


def append_decisions(path: Path, created_at: datetime, items: list[str], source: str) -> int:
    if not items:
        return 0
    block = "".join(
        f"- {_stamp(created_at)} — {txt} (source: {source})\n" for txt in items
    )
    atomic_append_text(path, block)
    return len(items)


def append_assumptions(path: Path, created_at: datetime, items: list[str], source: str) -> int:
    if not items:
        return 0
    block = "".join(
        f"- {_stamp(created_at)} — {txt} (source: {source})\n" for txt in items
    )
    atomic_append_text(path, block)
    return len(items)


def apply_memory_updates(
    *,
    decisions_path: Path,
    assumptions_path: Path,
    created_at: datetime,
    artifact_md: str,
    source: str,
) -> dict[str, int]:
    """Apply memory updates derived from the artifact markdown.

    Returns a {filename: count} map of appended entries.
    """
    updates = extract_memory_updates(artifact_md)
    out: dict[str, int] = {}
    d = append_decisions(decisions_path, created_at, list(updates.decisions), source=source)
    a = append_assumptions(assumptions_path, created_at, list(updates.assumptions), source=source)
    if d:
        out[decisions_path.name] = d
    if a:
        out[assumptions_path.name] = a
    return out
