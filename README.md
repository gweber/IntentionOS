# intention

A solo-company system for intent-driven automation and execution.

## Features

- Executes tasks based on user-defined intent
- Maintains state and memory across interactions
- Supports modular workflows and roles
- Enables self-running, autonomous operation

## Requirements

- Python 3.10+
- Node.js 18+
- Docker (optional, for environment isolation)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/gweber/InteractFlow.git
   cd InteractFlow
   ```

2. Set up the virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   npm install
   ```

## Configuration

Environment variables are loaded from `.env` file. Create a copy of `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` to set required values.

## Usage

Start the system:

```bash
make run
```

Or run manually:

```bash
source .venv/bin/activate
python scripts/company_engine.py
```

## Project Structure

- `docs/`: System documentation and design specs
- `scripts/`: Core execution and orchestration logic
- `AGENTS.md`: Agent role definitions and behavior rules
- `.clineignore`: Files and directories excluded from Cline processing
- `.clinerules/`: System-level execution rules

## Development

Run the development server:

```bash
make dev
```

Run tests:

```bash
make test
```

Lint code:

```bash
make lint
```

## Deployment (optional)

Deploy using Docker:

```bash
make docker-build
make docker-run
```

## Security

- Secrets are stored in `.env` and not committed to version control
- All API endpoints require authentication via JWT
- Environment variables are validated at startup

## Contributing

Please read `CONTRIBUTING.md` for guidelines on submitting changes.

## License

MIT License

## TODO

- Confirm runtime requirements for Node.js version
- Finalize `.env.example` with full variable list
- Add example workflow for new users
- Document error codes and recovery procedures
- Verify Dockerfile compatibility with target OS
- Add CI/CD pipeline configuration
- Update `make` targets to include health check
- Validate that all environment variables are documented
- Confirm that `company_engine.py` supports hot-reload
- Add example of role switching in usage section
