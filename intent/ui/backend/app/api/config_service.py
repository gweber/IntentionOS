from __future__ import annotations

"""Backend-local wrapper around intent config store.

The UI backend is a separate app, but it lives in-repo and can import the
canonical store under intent/scripts/core.
"""

from typing import Any

# The UI backend runs with `--app-dir backend` (so only intent/ui/backend is on
# sys.path). Add repo root so we can import the canonical `intent` package.
import sys
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parents[5]
if str(_REPO_ROOT) not in sys.path:
    sys.path.append(str(_REPO_ROOT))


from intent.scripts.core.config_store import (  # noqa: E402
    load_config_yaml,
    load_env_from_intent_dotenv,
    save_config_yaml_atomic,
    validate_config_schema,
)


def get_config() -> dict[str, Any]:
    return load_config_yaml()


def save_config(cfg: dict[str, Any]) -> dict[str, Any]:
    normalized = validate_config_schema(cfg)
    save_config_yaml_atomic(normalized)
    return normalized


def test_profile(profile_id: str, cfg_override: dict[str, Any] | None = None) -> dict[str, Any]:
    import os

    # Prefer draft config from UI (unsaved edits), but still validate/normalize.
    cfg = validate_config_schema(cfg_override) if cfg_override is not None else load_config_yaml()
    llms = cfg["llms"]
    profiles: list[dict[str, Any]] = llms["profiles"]
    prof = next((p for p in profiles if p.get("id") == profile_id), None)
    if not prof:
        raise KeyError(profile_id)

    load_env_from_intent_dotenv(override=False)
    env_name = str(prof.get("api_key_env") or "")
    provider = str(prof.get("provider") or "")
    # For our UI "Test" we treat openai-compatible providers as not requiring a
    # key because local backends (ollama/llama.cpp) frequently ignore auth.
    #
    # If you *do* want to enforce api key presence for a profile, set api_key_env
    # and ensure it exists; the check below will still report it.
    requires_api_key = provider in {"openai", "anthropic_compatible"}
    present = bool(env_name) and env_name in os.environ and bool(os.environ.get(env_name))
    return {
        "ok": True,
        "profile_id": profile_id,
        "checks": {
            "provider": provider,
            "requires_api_key": requires_api_key,
            "api_key_env": env_name,
            "api_key_present": present,
        },
        "note": "validation-only (no network)",
    }
