from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_scripts.core.md_parse import append_inbox_entry, read_inbox_entries


class TestInboxParse(unittest.TestCase):
    def test_read_inbox_entries_ignores_code_fences_and_empty(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "intent_inbox.md"
            p.write_text(
                """
Header text

```
2026-02-09 09:05 — inside fence should be ignored #x
```

2026-02-09 09:12 — A real entry #tag1 #tag2

""".lstrip(),
                encoding="utf-8",
            )

            entries = read_inbox_entries(p)
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0].ts, "2026-02-09 09:12")
            self.assertEqual(entries[0].statement, "A real entry")
            self.assertEqual(entries[0].tags, ("tag1", "tag2"))

    def test_append_inbox_entry_validates_format(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "intent_inbox.md"
            append_inbox_entry(p, "2026-02-09 09:12 — Something #a")
            entries = read_inbox_entries(p)
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0].statement, "Something")


if __name__ == "__main__":
    unittest.main()
