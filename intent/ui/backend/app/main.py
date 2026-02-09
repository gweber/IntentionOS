from __future__ import annotations

import logging
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from .api.jobs import router as jobs_router
from .config import settings
from .errors import ApiError
from .logging import setup_logging
from .models import ErrorBody, ErrorResponse
from .repositories.jobs import InMemoryJobRepository
from .services.job_service import JobService


def create_app() -> FastAPI:
    setup_logging(settings.log_level)
    log = logging.getLogger("intent_ui")

    app = FastAPI(title="Agent UI Backend", version="0.1.0")

    repo = InMemoryJobRepository()
    app.state.job_service = JobService(repo)

    @app.exception_handler(ApiError)
    async def api_error_handler(_: Request, exc: ApiError):
        body = ErrorResponse(error=ErrorBody(code=exc.code, message=exc.message, details=exc.details))
        return JSONResponse(status_code=exc.status_code, content=body.model_dump(mode="json"))

    @app.exception_handler(StarletteHTTPException)
    async def http_error_handler(_: Request, exc: StarletteHTTPException):
        # Normalize into our error envelope
        body = ErrorResponse(
            error=ErrorBody(
                code="http_error",
                message=str(exc.detail) if exc.detail else "HTTP error",
                details={"status_code": exc.status_code},
            )
        )
        return JSONResponse(status_code=exc.status_code, content=body.model_dump(mode="json"))

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_: Request, exc: RequestValidationError):
        body = ErrorResponse(
            error=ErrorBody(code="validation_error", message="Invalid request", details=exc.errors())
        )
        return JSONResponse(status_code=422, content=body.model_dump(mode="json"))

    @app.exception_handler(Exception)
    async def unhandled_error_handler(_: Request, exc: Exception):  # noqa: BLE001
        log.exception("unhandled_error")
        body = ErrorResponse(error=ErrorBody(code="internal_error", message="Internal server error"))
        return JSONResponse(status_code=500, content=body.model_dump(mode="json"))

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.frontend_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health")
    async def health():
        return {"ok": True}

    app.include_router(jobs_router)

    # Prod-ish: serve built frontend if present at /ui
    dist = Path(__file__).resolve().parents[2] / "frontend" / "dist"
    if dist.exists():
        assets = dist / "assets"
        if assets.exists():
            app.mount("/ui/assets", StaticFiles(directory=str(assets), html=False), name="ui-assets")

        @app.get("/")
        async def root_redirect():
            return RedirectResponse(url="/ui")

        @app.get("/ui")
        async def ui_index():
            return FileResponse(dist / "index.html")

        @app.get("/ui/{path:path}")
        async def ui_spa_fallback(path: str):
            file_path = dist / path
            if file_path.exists() and file_path.is_file():
                return FileResponse(file_path)
            return FileResponse(dist / "index.html")

    return app


app = create_app()
