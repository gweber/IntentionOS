# Intent framework (package)

Canonical structure (source of truth):

```text
intent/
  docs/
  scripts/
  ui/                (optional)
  tests/
  README.md
  requirements.txt
  pyproject.toml
  .gitignore
```

## Run (from repo root)

```bash
python -m intent.scripts.run --dry-run --intent "smoke test"
```

## Tests

```bash
python -m unittest discover intent/tests
```
