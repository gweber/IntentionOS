from __future__ import annotations

import asyncio
import logging
from typing import Any
from uuid import UUID, uuid4

from ..errors import ApiError, not_found
from ..models import Job, JobCreateRequest, JobEvent, JobStatus
from ..repositories.jobs import InMemoryJobRepository, utcnow
from ..runners.demo import run_demo_job

logger = logging.getLogger("intent_ui.job_service")


class JobService:
    def __init__(self, repo: InMemoryJobRepository) -> None:
        self._repo = repo

    async def list_jobs(self) -> list[Job]:
        jobs = await self._repo.list()
        return sorted(jobs, key=lambda j: j.created_at, reverse=True)

    async def get_job(self, job_id: UUID) -> Job:
        job = await self._repo.get(job_id)
        if not job:
            raise not_found("job", str(job_id))
        return job

    async def create_job(self, req: JobCreateRequest) -> Job:
        job_id = uuid4()
        job = await self._repo.create(job_id=job_id, kind=req.kind)

        await self._repo.append_event(
            JobEvent(timestamp=utcnow(), job_id=job_id, type="status", message="queued", payload={"kind": req.kind})
        )

        task = asyncio.create_task(self._run_job(job_id=job_id, kind=req.kind, input=req.input))
        await self._repo.set_task(job_id, task)
        return job

    async def cancel_job(self, job_id: UUID) -> Job:
        job = await self._repo.get(job_id)
        if not job:
            raise not_found("job", str(job_id))

        if job.status in {JobStatus.completed, JobStatus.failed, JobStatus.cancelled}:
            raise ApiError(status_code=409, code="job_not_cancellable", message=f"job is {job.status}")

        await self._repo.request_cancel(job_id)
        await self._repo.append_event(
            JobEvent(timestamp=utcnow(), job_id=job_id, type="status", message="cancellation requested")
        )
        await self._repo.cancel_task(job_id)
        return await self.get_job(job_id)

    async def subscribe_events(self, job_id: UUID):
        _ = await self.get_job(job_id)
        return self._repo.subscribe(job_id)

    async def _run_job(self, *, job_id: UUID, kind: str, input: dict[str, Any]) -> None:
        extra = {"job_id": str(job_id), "kind": kind}
        logger.info("job_started", extra=extra)

        async def publish(ev: JobEvent) -> None:
            await self._repo.append_event(ev)

        async def is_cancelled() -> bool:
            return await self._repo.is_cancel_requested(job_id)

        try:
            await self._repo.update_job(job_id, status=JobStatus.running, started_at=utcnow())
            await publish(JobEvent(timestamp=utcnow(), job_id=job_id, type="status", message="running"))

            if kind == "demo":
                result = await run_demo_job(job_id=job_id, input=input, publish=publish, is_cancelled=is_cancelled)
            else:
                raise ApiError(status_code=400, code="unsupported_job_kind", message=f"Unsupported kind: {kind}")

            await self._repo.update_job(job_id, status=JobStatus.completed, finished_at=utcnow(), result=result, error=None)
            await publish(JobEvent(timestamp=utcnow(), job_id=job_id, type="status", message="completed"))
            logger.info("job_completed", extra=extra)

        except asyncio.CancelledError:
            await self._repo.update_job(job_id, status=JobStatus.cancelled, finished_at=utcnow())
            await publish(JobEvent(timestamp=utcnow(), job_id=job_id, type="status", message="cancelled"))
            logger.info("job_cancelled", extra=extra)
            raise

        except ApiError as e:
            await self._repo.update_job(job_id, status=JobStatus.failed, finished_at=utcnow(), error=e.message)
            await publish(
                JobEvent(timestamp=utcnow(), job_id=job_id, type="error", message=e.message, payload={"code": e.code})
            )
            logger.warning("job_failed", extra={**extra, "code": e.code})

        except Exception as e:  # noqa: BLE001
            msg = f"Unhandled error: {type(e).__name__}"
            await self._repo.update_job(job_id, status=JobStatus.failed, finished_at=utcnow(), error=msg)
            await publish(JobEvent(timestamp=utcnow(), job_id=job_id, type="error", message=msg))
            logger.exception("job_failed_unhandled", extra=extra)
