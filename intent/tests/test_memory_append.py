from __future__ import annotations

import tempfile
import unittest
from datetime import datetime
from pathlib import Path

from agent_scripts.core.memory import append_assumptions, append_decisions, extract_memory_updates


class TestMemoryAppend(unittest.TestCase):
    def test_extract_and_append(self) -> None:
        md = """
## Decisions
- Decision: Use atomic writes

## Assumptions
- Assumption: The filesystem is writable
""".lstrip()

        updates = extract_memory_updates(md)
        self.assertEqual(updates.decisions, ("Use atomic writes",))
        self.assertEqual(updates.assumptions, ("The filesystem is writable",))

        with tempfile.TemporaryDirectory() as td:
            d = Path(td) / "decisions.md"
            a = Path(td) / "assumptions.md"
            now = datetime(2026, 2, 9, 12, 0)
            self.assertEqual(append_decisions(d, now, list(updates.decisions), source="artifact.md"), 1)
            self.assertEqual(append_assumptions(a, now, list(updates.assumptions), source="artifact.md"), 1)
            self.assertIn("2026-02-09 12:00", d.read_text(encoding="utf-8"))
            self.assertIn("Use atomic writes", d.read_text(encoding="utf-8"))
            self.assertIn("The filesystem is writable", a.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
