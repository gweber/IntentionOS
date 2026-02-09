from __future__ import annotations

import asyncio
import random
from typing import Awaitable, Callable
from uuid import UUID

from ..models import JobEvent
from ..repositories.jobs import utcnow


Publish = Callable[[JobEvent], Awaitable[None]]
IsCancelled = Callable[[], Awaitable[bool]]


async def run_demo_job(*, job_id: UUID, input: dict, publish: Publish, is_cancelled: IsCancelled) -> dict:
    """Simulated job that emits incremental trace events.

    "Thinking" means explicit intermediate steps emitted by the runner.
    """

    steps = random.randint(10, 20)
    topic = input.get("topic") or "demo"

    await publish(
        JobEvent(timestamp=utcnow(), job_id=job_id, type="status", message="starting", payload={"steps": steps})
    )
    await publish(
        JobEvent(timestamp=utcnow(), job_id=job_id, type="thought", message="Planning", payload={"topic": topic})
    )

    for i in range(1, steps + 1):
        if await is_cancelled():
            raise asyncio.CancelledError()

        await publish(
            JobEvent(
                timestamp=utcnow(),
                job_id=job_id,
                type="thought",
                message=f"Executing step {i}/{steps}",
                payload={"step": i, "steps": steps},
            )
        )
        await publish(
            JobEvent(
                timestamp=utcnow(),
                job_id=job_id,
                type="log",
                message="working",
                payload={"step": i, "op": random.choice(["search", "analyze", "write", "verify"])},
            )
        )
        await asyncio.sleep(random.uniform(0.2, 0.6))

    result = {
        "summary": f"Demo job finished after {steps} steps.",
        "topic": topic,
        "metrics": {"steps": steps, "score": round(random.uniform(0.7, 0.99), 3)},
    }
    await publish(JobEvent(timestamp=utcnow(), job_id=job_id, type="result", message="result", payload=result))
    return result
