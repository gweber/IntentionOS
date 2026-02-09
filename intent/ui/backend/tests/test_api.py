from __future__ import annotations

from fastapi.testclient import TestClient

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
