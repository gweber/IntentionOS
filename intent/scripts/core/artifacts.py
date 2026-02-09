from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from intent.scripts.core.io import atomic_write_text


SLUG_RE = re.compile(r"[^a-z0-9]+")


def slugify(text: str, max_len: int = 60) -> str:
    t = (text or "").strip().lower()
    t = SLUG_RE.sub("-", t).strip("-")
    if not t:
        t = "run"
    return t[:max_len].rstrip("-")


@dataclass(frozen=True)
class Artifact:
    path: Path
    content: str


def artifact_path(base_dir: Path, created_at: datetime, intent: str) -> Path:
    day_dir = base_dir / created_at.strftime("%Y-%m-%d")
    slug = slugify(intent)
    path = day_dir / f"{slug}.md"
    if not path.exists():
        return path
    # Collision: add a small numeric suffix.
    for i in range(2, 50):
        p2 = day_dir / f"{slug}-{i}.md"
        if not p2.exists():
            return p2
    return day_dir / f"{slug}-{created_at.strftime('%H%M%S')}.md"


def build_artifact_markdown(
    *,
    created_at: datetime,
    intent: str,
    workflow: str,
    workflow_steps: list[str],
    role_sequence: list[str],
    success_criteria: list[str],
    decisions: list[str],
    assumptions: list[str],
    next_intent: str,
    next_step: str,
) -> str:
    def bullets(items: list[str], prefix: str = "- ") -> str:
        if not items:
            return "_None._\n"
        return "".join(f"{prefix}{x}\n" for x in items)

    steps = "".join(f"{i+1}. {s}\n" for i, s in enumerate(workflow_steps))
    roles = "".join(f"- {r}\n" for r in role_sequence)

    decision_lines = [f"Decision: {d}" for d in decisions]
    assumption_lines = [f"Assumption: {a}" for a in assumptions]

    return (
        f"# Run Artifact — {created_at.strftime('%Y-%m-%d %H:%M')}\n\n"
        f"## Intent\n{intent.strip()}\n\n"
        f"## Success criteria\n{bullets(success_criteria)}\n"
        f"## Selected workflow\n{workflow}\n\n"
        f"## Workflow steps\n{steps}\n"
        f"## Role sequence actually used\n{roles}\n"
        f"## Decisions\n{bullets(decision_lines)}\n"
        f"## Assumptions\n{bullets(assumption_lines)}\n"
        f"## Next intent\n{next_intent.strip()}\n\n"
        f"## Next smallest step\n{next_step.strip()}\n"
    )


def write_artifact(artifact: Artifact) -> None:
    atomic_write_text(artifact.path, artifact.content)
