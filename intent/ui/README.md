# Agent UI (local demo)

Self-contained FastAPI + React (Vite) app to create “jobs” and watch live streamed updates via **SSE** (Server-Sent Events).

## Folder structure

```text
intent/ui/
  backend/        # FastAPI app (Python 3.11+)
  frontend/       # Vite + React + TS + Tailwind
  package.json    # root scripts to run both (npm workspaces)
  pytest.ini      # makes `backend/` importable in tests
  .env.example
```

---

## Prereqs

- Python **3.11+**
- Node **18+**

---

## Setup

### Backend

```bash
cd intent/ui
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
```

### Frontend

With npm workspaces, a single install at the folder root installs frontend deps too:

```bash
cd intent/ui
npm install
```

Optional: env (defaults are fine)

```bash
cp .env.example frontend/.env
```

---

## Run (dev)

One command starts **backend (8000)** + **frontend (5173)**:

```bash
cd intent/ui
npm run dev
```

- Frontend: http://localhost:5173
- Backend: http://localhost:8000/health

---

## Run (prod-ish)

Build the frontend and serve it from the backend at **/ui**.

```bash
cd intent/ui
npm run prod
```

- UI: http://localhost:8000/ui
- API: http://localhost:8000/health

---

## Backend tests

```bash
cd intent/ui
source .venv/bin/activate
pytest -q
```

---

## Smoke test (API + SSE)

If you want a copy/paste-safe demo without worrying about shell quote escaping:

```bash
cd intent/ui
./scripts/smoke.sh
```

Note: the script intentionally truncates the SSE stream output.

---

## API summary

- `GET /health` -> `{ "ok": true }`
- `POST /jobs` -> create job; body: `{ "kind": "demo", "input": {...} }`
- `GET /jobs` -> list
- `GET /jobs/{id}` -> detail
- `POST /jobs/{id}/cancel` -> cancel
- `GET /jobs/{id}/events` -> **SSE** stream of JobEvent JSON (`event: message`, `data: {...}`)
