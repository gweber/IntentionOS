from __future__ import annotations

import json
import sys
from datetime import datetime


def log(event: str, **fields) -> None:
    payload = {
        "ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "event": event,
        **fields,
    }
    sys.stdout.write(json.dumps(payload, ensure_ascii=False) + "\n")
