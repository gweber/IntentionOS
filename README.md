# Intention

A solo-company system for turning intent into action.

## Stack

- **Language:** Python
- **Package Manager:** pip
- **Tools:** git, openai
- **Execution System:** `scripts/company_engine.py` (AI-driven, intent-based)

## Setup

1. Clone the repo.
2. Create a virtual environment: `python -m venv .venv`
3. Activate: `. .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment: copy `.env.example` to `.env` (if exists) and fill in values.
6. Run: `python scripts/company_engine.py "your intent here"`

## Usage

- Use `docs/intent_inbox.md` to capture raw intent.
- Run `scripts/company_engine.py` with a prompt to generate a patch.
- Review and commit changes.

## Project Facts

- **Purpose:** Turn user intent into executable actions via AI.
- **Structure:** Minimal, documentation-first, memory-compounding.
- **Workflows:** See `docs/workflows.md` for execution paths.

## TODO

- Add a license (e.g., MIT).
- Add `.env.example` for environment variables.
- Add CI/CD pipeline (e.g., GitHub Actions).
- Add `CHANGELOG.md` for audit findings.
