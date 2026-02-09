# Tooling Policy
Non-interactive. Deterministic. Token-efficient.

Purpose: Make tool output consistent, fully captured, and cheap to read.

---

## 1) Global rules
- Never allow interactive pagers (`less`, `more`).
- Prefer stable, machine-capturable output.
- Always bound output size (counts, summaries, small slices).
- Prefer simple commands over clever pipelines.
- If a command could explode output, run a summary/count first.

---

## 2) Environment defaults (set for every tool session)
Set these before running commands:

- `PAGER=cat`
- `LESS=-FRSX`
- `GIT_PAGER=cat`
- `GIT_TERMINAL_PROMPT=0`

Notes:
- Prevents paging and hanging prompts.
- Ensures output is captured in logs.

---

## 3) Output bounding (token budget rules)
### Always cap unbounded outputs
Use one of:
- `head -n 50`
- `tail -n 50`
- add a tool-specific limit flag (`-n`, `--max-count`, etc.)

### Prefer summaries before details
Examples:
- `git diff --stat` before `git diff`
- `git diff --name-only` before any full patch
- `du -sh * | sort -h` before deep disk inspection

### Never dump entire files unless explicitly requested
Instead:
- show the relevant section: `sed -n 'START,ENDp' file`
- or show matches only: `rg -n "pattern" file`

---

## 4) “Do we even have matches?” gates (cheap first step)
Before doing complex filtering/transforms, run a count or quick preview:

- `rg -n "PATTERN" PATH | head -n 20`
- `rg -n "PATTERN" PATH | wc -l`
- `find PATH -maxdepth 3 -type f -name "GLOB" | wc -l`
- `git ls-files | rg "PATTERN" | wc -l`

If count is 0: stop and report “no matches”.

---

## 5) Search conventions (prefer rg)
Use ripgrep (`rg`) over recursive grep.

Recommended patterns:
- Case-smart: `rg -n "PATTERN" PATH -S`
- Limit file types: `rg -n "PATTERN" -g'*.php' PATH`
- Find files only: `rg --files PATH | rg '\.md$' | head -n 50`

Avoid:
- `grep -R` without file globs or depth bounds.
- searching the world when you only need one directory.

---

## 6) File listing conventions (avoid recursion explosions)
Preferred order:
1) `ls -la`
2) bounded `find`:
   - `find . -maxdepth 3 -type f | head -n 200`
3) optional structure:
   - `tree -L 3` (only if output stays reasonable)

Rule:
- Any recursive listing MUST have a depth limit.

---

## 7) Git conventions (stable + low-noise)
Always disable pager:
- Prefer: `git --no-pager <cmd>`
- Or ensure env: `GIT_PAGER=cat`

Stable formats:
- Status: `git status --porcelain=v1`
- Files changed: `git diff --name-only`
- Patch summary: `git diff --stat`
- Recent history: `git log --oneline --decorate -n 30`

Avoid:
- unbounded `git log`
- unbounded `git diff`

---

## 8) JSON/YAML shaping (when needed)
- JSON: use `jq` to extract only what matters, then bound output:
  - `jq '.key' file.json | head -n 50`
- YAML: do not parse unless necessary; bound output aggressively.

---

## 9) Command complexity guardrail
If a command is:
- longer than one line, OR
- uses more than 2 pipes (`|`),

then you MUST include:
- `WHY:` one sentence explaining why simple alternatives are insufficient.

Prefer 2–3 simple commands over one fragile pipeline.

---

## 10) Logging format for every tool call (recommended)
When running tools, record:

- COMMAND:
- WHY:
- EXPECTED OUTPUT SHAPE:
- RESULT: success/fail + key lines

If a command would require interaction:
- do NOT run it
- output the blocked command + reason
