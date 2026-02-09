# Intention

A solo-company system for turning intent into action.

## Stack

- **Language:** Python
- **Package Manager:** pip
- **Tools:** git
- **Execution System:** `python -m agent_scripts.run` (deterministic, intent-based)

## Setup

1. Clone the repo.
2. Create a virtual environment: `python -m venv .venv`
3. Activate: `. .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment: copy `.env.example` to `.env` (if exists) and fill in values.
6. Run: `python -m agent_scripts.run --intent "your intent here" --dry-run`

## Framework Runner

Run latest inbox entry:

```bash
python -m agent_scripts.run --once
```

Run explicit intent with explicit workflow/role:

```bash
python -m agent_scripts.run --intent "..." --workflow "Friction → Fix" --role "Architect"
```

Dry run + print plan (no files written):

```bash
python -m agent_scripts.run --intent "..." --print-plan
```

## Usage

- Use `intent/docs/intent_inbox.md` to capture raw intent (append-only).
- Run the framework runner to produce artifacts in `intent/docs/artifacts/`.

## Project Facts

- **Purpose:** Turn user intent into executable actions via AI.
- **Structure:** Minimal, documentation-first, memory-compounding.
- **Workflows:** See `intent/docs/workflows.md` for execution paths.

## TODO

- Add a license (e.g., MIT).
- Add `.env.example` for environment variables.
- Add CI/CD pipeline (e.g., GitHub Actions).
- Add `CHANGELOG.md` for audit findings.
