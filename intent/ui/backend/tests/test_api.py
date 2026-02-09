from __future__ import annotations

import pytest

fastapi = pytest.importorskip("fastapi")
TestClient = pytest.importorskip("fastapi.testclient").TestClient

from app.main import create_app


def test_health_ok() -> None:
    app = create_app()
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


def test_create_and_list_jobs() -> None:
    app = create_app()
    client = TestClient(app)

    create = client.post("/jobs", json={"kind": "demo", "input": {"topic": "tests"}})
    assert create.status_code == 200
    job = create.json()
    assert job["kind"] == "demo"
    assert job["status"] == "queued"

    listed = client.get("/jobs")
    assert listed.status_code == 200
    jobs = listed.json()
    assert len(jobs) == 1
    assert jobs[0]["id"] == job["id"]


def test_get_config_ok() -> None:
    app = create_app()
    client = TestClient(app)
    resp = client.get("/api/config")
    assert resp.status_code == 200
    body = resp.json()
    assert body["version"] == 1
    assert "llms" in body


def test_test_profile_uses_draft_config_override() -> None:
    app = create_app()
    client = TestClient(app)

    draft = {
        "version": 1,
        "llms": {
            "active": "llama",
            "profiles": [
                {
                    "id": "llama",
                    "label": "Local llama.cpp",
                    "provider": "openai_compatible",
                    "base_url": "http://172.20.200.169:8080",
                    "model": "not_needed",
                    "api_key_env": "LOCAL_API_KEY",
                    "headers": {},
                }
            ],
        },
    }

    resp = client.post("/api/config/test/llama", json={"config": draft})
    assert resp.status_code == 200
    body = resp.json()
    assert body["profile_id"] == "llama"
    assert body["checks"]["requires_api_key"] is False
