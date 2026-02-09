from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


JobKind = Literal["demo"]


class JobEvent(BaseModel):
    timestamp: datetime
    job_id: UUID
    type: Literal["status", "thought", "log", "result", "error"]
    message: str
    payload: dict[str, Any] | None = None


class Job(BaseModel):
    id: UUID
    kind: JobKind
    status: JobStatus
    created_at: datetime

    started_at: datetime | None = None
    finished_at: datetime | None = None

    result: dict[str, Any] | None = None
    error: str | None = None
    last_event: JobEvent | None = None


class JobCreateRequest(BaseModel):
    kind: JobKind = Field(description="Job type")
    input: dict[str, Any] = Field(default_factory=dict)


class ErrorBody(BaseModel):
    code: str
    message: str
    details: Any | None = None


class ErrorResponse(BaseModel):
    error: ErrorBody
