# Language Profile: bash

## Purpose
- Enforce safe, portable, and maintainable shell scripting.
- Prevent common security and portability issues.
- Support automation and deployment consistency.

## Hard Rules
- DO use `set -euo pipefail` at the top of all scripts.
- DO use `[[` instead of `[` for conditionals.
- DO use `"$VAR"` for variable expansion; never use `$VAR`.
- DO use `declare -r` for constants.
- DO use `$(command)` instead of backticks.
- DO NOT use `eval`.
- DO NOT use `source` on untrusted scripts.
- DO NOT use `set +u` unless absolutely necessary.
- DO NOT use `echo` for output; use `printf`.
- DO NOT use `cat` to read files; use `while read` or `$(cat file)`.

## Defaults
- Naming: `snake_case` for variables, `PascalCase` for functions.
- Formatting: Use 2-space indentation; no trailing whitespace.
- Error handling: Use `set -euo pipefail` and `trap` for cleanup.
- Testing: Use `shunit2` or `bats` for unit testing.

## Patterns We Prefer
- Use `set -euo pipefail` for safety:
  ```bash
  #!/bin/bash
  set -euo pipefail

  declare -r SCRIPT_DIR=$(cd $(dirname $0) && pwd)

  main() {
      local -r input_file="$1"
      if [[ ! -f "$input_file" ]]; then
          printf 'Error: File not found: %s\n' "$input_file" >&2
          exit 1
      fi

      printf 'Processing %s...\n' "$input_file"
      # Your logic here
  }

  main "$@"
  ```
- Use `declare -r` for constants:
  ```bash
  declare -r MAX_RETRIES=3
  declare -r LOG_FILE="/var/log/app.log"
  ```

## Footguns to Avoid
- Avoid `eval` on user input.
- Avoid `source` without verifying file integrity.
- Avoid `cat file | grep` without error handling.
- Avoid `$(cat file)` on large files.

## Definition of Done
- [ ] File exists at `intent/docs/language_profiles/bash.md`
- [ ] Follows template exactly
- [ ] Includes `Definition of Done` checklist
- [ ] Uses `DO`/`DO NOT` in Hard Rules
- [ ] Contains at least one code snippet
- [ ] No external modifications made
- [ ] All sections present and filled
- [ ] No markdown linting errors
- [ ] No unused or redundant lines
- [ ] Matches final formatted state in search/replace
