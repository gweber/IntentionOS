from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Prefer the repo's canonical dotenv at intent/.env.
    _repo_root = Path(__file__).resolve().parents[4]
    model_config = SettingsConfigDict(
        env_prefix="INTENT_UI_",
        env_file=[str((_repo_root / "intent" / ".env").resolve()), ".env"],
        extra="ignore",
    )

    # must match Vite dev server origin for CORS
    frontend_origin: str = "http://localhost:5173"
    log_level: str = "INFO"


settings = Settings()
