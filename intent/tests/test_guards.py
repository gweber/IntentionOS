from __future__ import annotations

import unittest
from pathlib import Path

from intent.scripts.core.errors import GuardViolation, ValidationError
from intent.scripts.core.guards import (
    ensure_artifact_enforced,
    ensure_single_role_sequence,
    ensure_single_workflow,
)


class TestGuards(unittest.TestCase):
    def test_single_workflow_required(self) -> None:
        with self.assertRaises(ValidationError):
            ensure_single_workflow(None)

    def test_role_sequence_required(self) -> None:
        with self.assertRaises(ValidationError):
            ensure_single_role_sequence([])

    def test_artifact_required_when_not_dry_run(self) -> None:
        with self.assertRaises(GuardViolation):
            ensure_artifact_enforced(Path("x.md"), written_paths=[], dry_run=False)

    def test_artifact_path_required_in_dry_run(self) -> None:
        # Path object is required even in dry run.
        ensure_artifact_enforced(Path("x.md"), written_paths=[], dry_run=True)


if __name__ == "__main__":
    unittest.main()
