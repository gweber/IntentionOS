from __future__ import annotations

import asyncio
import json
from collections.abc import AsyncIterator
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from ..deps import get_job_service
from ..models import Job, JobCreateRequest
from ..services.job_service import JobService


router = APIRouter(tags=["jobs"])


def _sse_message(data: dict) -> bytes:
    # Spec: send events named "message" with JSON payload lines.
    return (
        "event: message\n" + f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
    ).encode("utf-8")


@router.post("/jobs", response_model=Job)
async def create_job(req: JobCreateRequest, svc: JobService = Depends(get_job_service)) -> Job:
    return await svc.create_job(req)


@router.get("/jobs", response_model=list[Job])
async def list_jobs(svc: JobService = Depends(get_job_service)) -> list[Job]:
    return await svc.list_jobs()


@router.get("/jobs/{job_id}", response_model=Job)
async def get_job(job_id: UUID, svc: JobService = Depends(get_job_service)) -> Job:
    return await svc.get_job(job_id)


@router.post("/jobs/{job_id}/cancel", response_model=Job)
async def cancel_job(job_id: UUID, svc: JobService = Depends(get_job_service)) -> Job:
    return await svc.cancel_job(job_id)


@router.get("/jobs/{job_id}/events")
async def stream_job_events(job_id: UUID, svc: JobService = Depends(get_job_service)) -> StreamingResponse:
    subscription = await svc.subscribe_events(job_id)

    async def gen() -> AsyncIterator[bytes]:
        # immediate snapshot to show “connected” and give latest state
        job = await svc.get_job(job_id)
        if job.last_event:
            yield _sse_message(job.last_event.model_dump(mode="json"))
        yield b": connected\n\n"

        while True:
            try:
                ev = await asyncio.wait_for(anext(subscription), timeout=15.0)
                yield _sse_message(ev.model_dump(mode="json"))
            except asyncio.TimeoutError:
                # keep-alive
                yield b": keep-alive\n\n"

    return StreamingResponse(gen(), media_type="text/event-stream")
