from __future__ import annotations

from intent.scripts.core.config_store import validate_config_schema


def test_validate_config_schema_ok() -> None:
    cfg = {
        "version": 1,
        "llms": {
            "active": "a",
            "profiles": [
                {
                    "id": "a",
                    "label": "A",
                    "provider": "openai_compatible",
                    "base_url": "http://localhost:11434/v1",
                    "model": "llama",
                    "api_key_env": "LOCAL_API_KEY",
                    "headers": {"x-test": "${SOME_HEADER_ENV}"},
                }
            ],
        },
    }
    out = validate_config_schema(cfg)
    assert out["version"] == 1
    assert out["llms"]["active"] == "a"
    assert out["llms"]["profiles"][0]["headers"]["x-test"] == "${SOME_HEADER_ENV}"


def test_validate_config_schema_allows_empty_api_key_env_for_openai_compatible() -> None:
    cfg = {
        "version": 1,
        "llms": {
            "active": "a",
            "profiles": [
                {
                    "id": "a",
                    "label": "A",
                    "provider": "openai_compatible",
                    "base_url": "http://172.20.200.169:8080",
                    "model": "not_needed",
                    "api_key_env": "",
                    "headers": {},
                }
            ],
        },
    }
    out = validate_config_schema(cfg)
    assert out["llms"]["profiles"][0]["api_key_env"] == ""


def test_validate_config_schema_rejects_header_secrets() -> None:
    cfg = {
        "version": 1,
        "llms": {
            "active": "a",
            "profiles": [
                {
                    "id": "a",
                    "label": "A",
                    "provider": "openai_compatible",
                    "base_url": "http://localhost:11434/v1",
                    "model": "llama",
                    "api_key_env": "LOCAL_API_KEY",
                    "headers": {"authorization": "Bearer sk-live"},
                }
            ],
        },
    }

    try:
        validate_config_schema(cfg)
    except Exception as e:
        assert "no secrets" in str(e).lower()
    else:  # pragma: no cover
        raise AssertionError("expected schema to reject secrets in headers")
