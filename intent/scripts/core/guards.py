from __future__ import annotations

from pathlib import Path

from intent.scripts.core.errors import GuardViolation, ValidationError


def ensure_single_workflow(workflow_name: str | None) -> None:
    if not workflow_name or not isinstance(workflow_name, str):
        raise ValidationError("Exactly one workflow must be selected for the run.")


def ensure_single_role_sequence(role_sequence: list[str]) -> None:
    # One role *at a time* is enforced by RoleStack; here we ensure the sequence is explicit.
    if not role_sequence or any(not isinstance(r, str) or not r for r in role_sequence):
        raise ValidationError("Role sequence must contain at least one role name.")


def ensure_artifact_enforced(artifact_path: Path, written_paths: list[Path], dry_run: bool) -> None:
    if dry_run:
        # In dry-run we don't write files, but we still require a concrete plan to do so.
        if not artifact_path:
            raise GuardViolation("Dry-run must still compute an artifact path.")
        return
    if not written_paths:
        raise GuardViolation("Run must produce at least one artifact file.")
