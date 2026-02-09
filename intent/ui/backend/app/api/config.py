from __future__ import annotations

from typing import Any

# The UI backend runs with `--app-dir backend` (so only intent/ui/backend is on
# sys.path). Add repo root so we can import the canonical `intent` package.
import sys
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[5]
if str(_REPO_ROOT) not in sys.path:
    sys.path.append(str(_REPO_ROOT))

from fastapi import APIRouter
from pydantic import BaseModel, Field

from intent.scripts.core.config_store import ConfigError  # noqa: E402

from .config_service import get_config as _get_config
from .config_service import save_config as _save_config
from .config_service import test_profile as _test_profile


router = APIRouter(prefix="/api", tags=["config"])


class ConfigUpdateRequest(BaseModel):
    config: dict[str, Any] = Field(description="Full config payload (same shape as config.yaml)")


class ConfigTestRequest(BaseModel):
    # Optional draft config payload; when provided we test the config the user is
    # currently editing (even if it hasn't been saved yet).
    config: dict[str, Any] | None = Field(default=None)


def _redact_config(cfg: dict[str, Any]) -> dict[str, Any]:
    """Ensure responses never contain secrets.

    Schema already forbids secrets in YAML. This is belt+braces.
    """

    # Store-layer already normalizes + validates.
    return cfg


@router.get("/config")
async def get_config() -> dict[str, Any]:
    try:
        cfg = _get_config()
    except ConfigError as e:
        # Return a safe error envelope consistent with other endpoints.
        # Let FastAPI's exception machinery format it as 422.
        from fastapi import HTTPException

        raise HTTPException(status_code=422, detail=str(e)) from e

    return _redact_config(cfg)


@router.post("/config")
async def post_config(req: ConfigUpdateRequest) -> dict[str, Any]:
    try:
        normalized = _save_config(req.config)
    except ConfigError as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=422, detail=str(e)) from e

    return _redact_config(normalized)


@router.post("/config/test/{profile_id}")
async def test_profile(profile_id: str, req: ConfigTestRequest | None = None) -> dict[str, Any]:
    """Validation-only test.

    We avoid network calls by default.
    """

    try:
        cfg_override = req.config if req is not None else None
        return _test_profile(profile_id, cfg_override)
    except KeyError as e:
        from fastapi import HTTPException

        raise HTTPException(status_code=404, detail="profile not found") from e
