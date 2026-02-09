from __future__ import annotations

import asyncio
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import AsyncIterator
from uuid import UUID

from ..models import Job, JobEvent, JobKind, JobStatus


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class JobRecord:
    job: Job
    events: list[JobEvent]
    task: asyncio.Task[None] | None
    cancelled_requested: bool
    subscribers: set[asyncio.Queue[JobEvent]]


class InMemoryJobRepository:
    """In-memory job store + per-job pub/sub for streamed events."""

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._jobs: dict[UUID, JobRecord] = {}

    async def create(self, *, job_id: UUID, kind: JobKind) -> Job:
        async with self._lock:
            job = Job(
                id=job_id,
                kind=kind,
                status=JobStatus.queued,
                created_at=utcnow(),
                started_at=None,
                finished_at=None,
                result=None,
                error=None,
                last_event=None,
            )
            self._jobs[job_id] = JobRecord(
                job=job,
                events=[],
                task=None,
                cancelled_requested=False,
                subscribers=set(),
            )
            return job

    async def list(self) -> list[Job]:
        async with self._lock:
            return [rec.job for rec in self._jobs.values()]

    async def get(self, job_id: UUID) -> Job | None:
        async with self._lock:
            rec = self._jobs.get(job_id)
            return rec.job if rec else None

    async def set_task(self, job_id: UUID, task: asyncio.Task[None]) -> None:
        async with self._lock:
            self._jobs[job_id].task = task

    async def request_cancel(self, job_id: UUID) -> None:
        async with self._lock:
            self._jobs[job_id].cancelled_requested = True

    async def is_cancel_requested(self, job_id: UUID) -> bool:
        async with self._lock:
            return self._jobs[job_id].cancelled_requested

    async def update_job(self, job_id: UUID, **fields) -> Job:
        async with self._lock:
            rec = self._jobs[job_id]
            rec.job = rec.job.model_copy(update=fields)
            self._jobs[job_id] = rec
            return rec.job

    async def append_event(self, event: JobEvent) -> None:
        async with self._lock:
            rec = self._jobs[event.job_id]
            rec.events.append(event)
            rec.job = rec.job.model_copy(update={"last_event": event})
            subscribers = list(rec.subscribers)

        for q in subscribers:
            try:
                q.put_nowait(event)
            except asyncio.QueueFull:
                pass

    async def subscribe(self, job_id: UUID, *, max_queue: int = 500) -> AsyncIterator[JobEvent]:
        q: asyncio.Queue[JobEvent] = asyncio.Queue(maxsize=max_queue)
        async with self._lock:
            self._jobs[job_id].subscribers.add(q)

        try:
            while True:
                yield await q.get()
        finally:
            async with self._lock:
                rec = self._jobs.get(job_id)
                if rec:
                    rec.subscribers.discard(q)

    async def cancel_task(self, job_id: UUID) -> bool:
        async with self._lock:
            task = self._jobs[job_id].task
        if task and not task.done():
            task.cancel()
            return True
        return False
