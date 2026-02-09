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
    # Anchor all paths to this repository checkout, not the current working directory.
    #
    #   intent/scripts/core/config.py
    #   ^ parents[2] = intent/
    #   ^ parents[3] = repo root
    intent_root = Path(__file__).resolve().parents[2]
    repo_root = intent_root.parent
    docs_dir = intent_root / "docs"
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


def bootstrap_docs(paths: Paths) -> None:
    """Create required directories/files if missing (safe bootstrap).

    This is intentionally minimal and only ensures the canonical structure exists.
    """

    paths.docs_dir.mkdir(parents=True, exist_ok=True)
    paths.memory_dir.mkdir(parents=True, exist_ok=True)
    paths.artifacts_dir.mkdir(parents=True, exist_ok=True)

    def _ensure_file(path: Path, header: str) -> None:
        if path.exists():
            return
        path.write_text(header, encoding="utf-8")

    _ensure_file(paths.decisions_path, "# Decisions\n\n")
    _ensure_file(paths.assumptions_path, "# Assumptions\n\n")
    _ensure_file(paths.rejections_path, "# Rejections\n\n")
    _ensure_file(paths.glossary_path, "# Glossary\n\n")
