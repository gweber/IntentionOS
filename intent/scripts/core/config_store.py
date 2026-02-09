from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final

from intent.scripts.core.io import atomic_write_text, read_text

try:
    import yaml
except Exception as e:  # pragma: no cover
    yaml = None  # type: ignore[assignment]
    _YAML_IMPORT_ERROR = e  # type: ignore[assignment]


_CONFIG_ENV_VAR: Final[str] = "INTENT_CONFIG_PATH"
_DOTENV_ENV_VAR: Final[str] = "INTENT_DOTENV_PATH"


class ConfigError(ValueError):
    """Raised when config.yaml is missing or invalid."""


@dataclass(frozen=True)
class ConfigPaths:
    intent_root: Path
    config_path: Path
    dotenv_path: Path


def default_intent_root() -> Path:
    # intent/scripts/core/config_store.py -> parents[2] == intent/
    return Path(__file__).resolve().parents[2]


def get_paths() -> ConfigPaths:
    intent_root = default_intent_root()

    cfg = os.environ.get(_CONFIG_ENV_VAR)
    if cfg:
        config_path = Path(cfg).expanduser().resolve()
    else:
        config_path = (intent_root / "config.yaml").resolve()

    dotenv = os.environ.get(_DOTENV_ENV_VAR)
    if dotenv:
        dotenv_path = Path(dotenv).expanduser().resolve()
    else:
        dotenv_path = (intent_root / ".env").resolve()

    return ConfigPaths(intent_root=intent_root, config_path=config_path, dotenv_path=dotenv_path)


def _ensure_under_intent_root(path: Path, intent_root: Path) -> None:
    # Path traversal guard: only allow writes under intent/.
    try:
        path.relative_to(intent_root)
    except ValueError as e:  # pragma: no cover
        raise ConfigError(f"Refusing to access path outside intent/: {path}") from e


def load_config_yaml() -> dict[str, Any]:
    """Load intent/config.yaml.
    """

    paths = get_paths()
    _ensure_under_intent_root(paths.config_path, paths.intent_root)

    raw = read_text(paths.config_path).strip()
    if not raw:
        raise ConfigError(f"Missing config file: {paths.config_path}")

    if yaml is None:  # pragma: no cover
        raise ConfigError(f"PyYAML is required to load config.yaml: {_YAML_IMPORT_ERROR}")

    try:
        data = yaml.safe_load(raw)
    except Exception as e:  # noqa: BLE001
        raise ConfigError(f"Invalid YAML in config.yaml: {e}") from e

    return validate_config_schema(data)


def save_config_yaml_atomic(cfg: dict[str, Any]) -> None:
    paths = get_paths()
    _ensure_under_intent_root(paths.config_path, paths.intent_root)

    if yaml is None:  # pragma: no cover
        raise ConfigError(f"PyYAML is required to save config.yaml: {_YAML_IMPORT_ERROR}")

    normalized = validate_config_schema(cfg)
    content = yaml.safe_dump(
        normalized,
        sort_keys=False,
        default_flow_style=False,
        width=120,
        allow_unicode=True,
    )
    if not content.endswith("\n"):
        content += "\n"
    atomic_write_text(paths.config_path, content)


_ENV_KEY_RE: Final[re.Pattern[str]] = re.compile(r"^[A-Z_][A-Z0-9_]*$")
_HEADER_ENV_REF_RE: Final[re.Pattern[str]] = re.compile(r"^\$\{([A-Z_][A-Z0-9_]*)\}$")


def _is_header_env_ref(value: str) -> bool:
    """Headers must not contain secrets; require env var indirection.

    Format: "${ENV_VAR_NAME}".
    """

    return bool(_HEADER_ENV_REF_RE.match(value))


def validate_config_schema(cfg: Any) -> dict[str, Any]:
    """Manual schema validation.

    Returns a normalized dict (unknown keys removed, defaults applied).
    """

    if not isinstance(cfg, dict):
        raise ConfigError("config must be a mapping")

    version = cfg.get("version")
    if version != 1:
        raise ConfigError("config.version must be 1")

    llms = cfg.get("llms")
    if not isinstance(llms, dict):
        raise ConfigError("config.llms must be a mapping")

    active = llms.get("active")
    profiles = llms.get("profiles")
    if not isinstance(active, str) or not active:
        raise ConfigError("llms.active must be a non-empty string")
    if not isinstance(profiles, list):
        raise ConfigError("llms.profiles must be a list")

    allowed_providers = {
        "openai",
        "openai_compatible",
        "anthropic_compatible",
    }

    normalized_profiles: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for i, p in enumerate(profiles):
        if not isinstance(p, dict):
            raise ConfigError(f"llms.profiles[{i}] must be a mapping")

        pid = p.get("id")
        label = p.get("label")
        provider = p.get("provider")
        base_url = p.get("base_url")
        model = p.get("model")
        api_key_env = p.get("api_key_env")
        headers = p.get("headers", {})

        if not isinstance(pid, str) or not pid:
            raise ConfigError(f"llms.profiles[{i}].id must be a non-empty string")
        if pid in seen_ids:
            raise ConfigError(f"Duplicate profile id: {pid}")
        seen_ids.add(pid)

        if not isinstance(label, str) or not label:
            raise ConfigError(f"llms.profiles[{i}].label must be a non-empty string")
        if provider not in allowed_providers:
            raise ConfigError(
                f"llms.profiles[{i}].provider must be one of: {sorted(allowed_providers)}"
            )
        if not isinstance(base_url, str) or not base_url:
            raise ConfigError(f"llms.profiles[{i}].base_url must be a non-empty string")
        if not isinstance(model, str) or not model:
            raise ConfigError(f"llms.profiles[{i}].model must be a non-empty string")
        # Some local providers (openai-compatible gateways like llama.cpp / ollama)
        # may not require an API key at all.
        if api_key_env is None:
            api_key_env = ""
        if not isinstance(api_key_env, str):
            raise ConfigError(f"llms.profiles[{i}].api_key_env must be a string")
        if provider in {"openai", "anthropic_compatible"}:
            if not api_key_env:
                raise ConfigError(f"llms.profiles[{i}].api_key_env must be a non-empty string")
            if not _ENV_KEY_RE.match(api_key_env):
                raise ConfigError(f"llms.profiles[{i}].api_key_env must look like an env var name")
        else:
            # openai_compatible: allow empty, otherwise validate the name.
            if api_key_env and not _ENV_KEY_RE.match(api_key_env):
                raise ConfigError(f"llms.profiles[{i}].api_key_env must look like an env var name")

        if headers is None:
            headers = {}
        if not isinstance(headers, dict):
            raise ConfigError(f"llms.profiles[{i}].headers must be a mapping")
        for hk, hv in headers.items():
            if not isinstance(hk, str) or not hk:
                raise ConfigError(f"llms.profiles[{i}].headers has invalid key")
            if not isinstance(hv, str):
                raise ConfigError(f"llms.profiles[{i}].headers[{hk!r}] must be a string")
            if hv and not _is_header_env_ref(hv):
                raise ConfigError(
                    f"llms.profiles[{i}].headers[{hk!r}] must reference an env var like ${{ENV_VAR}} (no secrets in YAML)"
                )

        normalized_profiles.append(
            {
                "id": pid,
                "label": label,
                "provider": provider,
                "base_url": base_url,
                "model": model,
                "api_key_env": api_key_env,
                "headers": headers,
            }
        )

    if active not in seen_ids:
        raise ConfigError("llms.active must match an existing profile id")

    return {"version": 1, "llms": {"active": active, "profiles": normalized_profiles}}


def load_env_from_intent_dotenv(*, override: bool = False) -> dict[str, str]:
    """Load env vars from intent/.env.

    By default, **does not** override already-set environment variables.
    Returns the loaded key/value pairs.
    """

    paths = get_paths()
    _ensure_under_intent_root(paths.dotenv_path, paths.intent_root)
    raw = read_text(paths.dotenv_path)
    if not raw:
        return {}

    loaded: dict[str, str] = {}
    for line in raw.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.startswith("export "):
            s = s[len("export ") :].lstrip()

        if "=" not in s:
            continue
        key, val = s.split("=", 1)
        key = key.strip()
        val = val.strip()

        if not key or not _ENV_KEY_RE.match(key):
            continue

        # remove optional quotes (very small subset)
        if len(val) >= 2 and ((val[0] == val[-1] == '"') or (val[0] == val[-1] == "'")):
            val = val[1:-1]

        loaded[key] = val
        if override or key not in os.environ:
            os.environ[key] = val

    return loaded
