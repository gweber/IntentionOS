from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Paths:
    repo_root: Path
    docs_dir: Path
    inbox_path: Path
    memory_dir: Path
    artifacts_dir: Path
    decisions_path: Path
    assumptions_path: Path
    rejections_path: Path
    glossary_path: Path


def default_paths() -> Paths:
    repo_root = Path(__file__).resolve().parents[2]
    docs_dir = repo_root / "intent/docs"
    inbox_path = docs_dir / "intent_inbox.md"
    memory_dir = docs_dir / "memory"
    artifacts_dir = docs_dir / "artifacts"
    return Paths(
        repo_root=repo_root,
        docs_dir=docs_dir,
        inbox_path=inbox_path,
        memory_dir=memory_dir,
        artifacts_dir=artifacts_dir,
        decisions_path=memory_dir / "decisions.md",
        assumptions_path=memory_dir / "assumptions.md",
        rejections_path=memory_dir / "rejections.md",
        glossary_path=memory_dir / "glossary.md",
    )
