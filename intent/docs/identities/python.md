# Identity: python

## Purpose
- Enforce clean, readable, and maintainable Python code.
- Promote type safety, predictable I/O, and testability.
- Prevent common anti-patterns in dynamic language usage.

## Hard Rules
- DO use type hints for all function parameters and return values.
- DO use `dataclass` for structured data; avoid raw `dict` or `namedtuple`.
- DO use `pathlib.Path` instead of `os.path` for file operations.
- DO use `logging` module for all output; avoid `print()` in production.
- DO not use `__import__()` or `exec()`.
- DO use `f-strings` for string formatting.
- DO name variables using `snake_case`.
- DO NOT use `global` keyword.
- DO NOT use `eval()` or `exec()`.
- DO NOT use `any` in type annotations.

## Defaults
- Naming: `snake_case` for variables, `PascalCase` for classes.
- Formatting: Black with `--line-length=88`.
- Error handling: Use `try/except` with specific exceptions; avoid bare `except`.
- Testing: Unit tests in `tests/` directory using `unittest` or `pytest`.

## Patterns We Prefer
- Use `dataclass` for structured data:
  ```python
  from dataclasses import dataclass
  from typing import Optional

  @dataclass
  class User:
      id: int
      name: str
      email: str
      created_at: Optional[datetime] = None

      def __post_init__(self):
          if self.created_at is None:
              self.created_at = datetime.now()
  ```
- Use `pathlib` for file paths:
  ```python
  from pathlib import Path

  config_path = Path("/etc/app/config.json")
  if config_path.exists():
      with config_path.open() as f:
          config = json.load(f)
  ```

## Footguns to Avoid
- Avoid `__import__()` or `exec()` in any context.
- Avoid `eval()` on user input.
- Avoid `dict` mutation during iteration.
- Avoid `global` state in modules.

## Definition of Done
- [ ] File exists at `docs/identities/python.md`
- [ ] Follows template exactly
- [ ] Includes `Definition of Done` checklist
- [ ] Uses `DO`/`DO NOT` in Hard Rules
- [ ] Contains at least one code snippet
- [ ] No external modifications made
- [ ] All sections present and filled
- [ ] No markdown linting errors
- [ ] No unused or redundant lines
- [ ] Matches final formatted state in search/replace
