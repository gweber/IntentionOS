from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ApiError(Exception):
    status_code: int
    code: str
    message: str
    details: Any | None = None


def not_found(entity: str, entity_id: str) -> ApiError:
    return ApiError(
        status_code=404,
        code=f"{entity}_not_found",
        message=f"{entity} not found",
        details={"id": entity_id},
    )
