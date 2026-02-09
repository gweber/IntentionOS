from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path


@dataclass
class RunState:
    intent: str
    workflow: str
    role_sequence: list[str]
    workflow_steps: list[str]
    success_criteria: list[str]
    dry_run: bool
    created_at: datetime
    artifact_path: Path
    artifacts_written: list[Path] = field(default_factory=list)
    memory_appends: dict[str, int] = field(default_factory=dict)  # filename -> count
