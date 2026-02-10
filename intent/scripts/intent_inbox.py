#!/usr/bin/env python3
"""scripts/intent_inbox.py

Purpose
- Append the raw intent to docs/intent_inbox.md with a timestamp (append-only).
- Provide the governing docs as context to an LLM which returns a git-apply patch.

Primary bug fixed
- Dates were "missing" because this script did not reliably write a timestamped
  intent line before invoking the model, and it also contained invalid top-level
  code referencing undefined variables.

Design
- The inbox entry is created by THIS script (not by the model), guaranteeing the
  required timestamp format.
- The model may still append follow-up notes/metadata, but the initial entry is
  always present and correctly formatted.
"""

import argparse
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]

INTENT_INBOX = ROOT / "intent/docs/intent_inbox.md"
TIMEZONE = ZoneInfo("Europe/Berlin")

PATCH_RE = re.compile(r"<patch>\s*(.*?)\s*</patch>", re.DOTALL)


def now_ts() -> str:
    """Timestamp for intent inbox entries: YYYY-MM-DD HH:MM (Europe/Berlin)."""
    return datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M")


def format_intent_line(raw_intent: str) -> str:
    """Format a single append-only inbox line."""
    intent = (raw_intent or "").strip()
    if not intent:
        raise ValueError("Intent must be a non-empty string")
    return f"{now_ts()} — {intent}\n"


def append_intent_line(raw_intent: str) -> str:
    """Append the raw intent to intent/docs/intent_inbox.md and return the written line."""
    INTENT_INBOX.parent.mkdir(parents=True, exist_ok=True)
    line = format_intent_line(raw_intent)
    with INTENT_INBOX.open("a", encoding="utf-8") as f:
        f.write(line)
    return line


def extract_patch(text: str) -> str:
    text = text or ""
    m = PATCH_RE.search(text)
    if m:
        return (m.group(1) or "").strip()
    return text.strip()


def looks_like_patch(p: str) -> bool:
    p = (p or "").lstrip()
    if p.startswith("<patch>"):
        return True  # extract_patch should remove it, but be tolerant
    return p.startswith("diff --git") or (p.startswith("--- ") and "\n+++ " in p)


def normalize_patch(p: str) -> str:
    # Minimal normalization; git apply accepts patches with or without diff --git
    return (p or "").strip()


GOVERNING_FILES = [
    "AGENTS.md",
    "intent/AGENTS.md"
    ".clinerules/core.md",
    "intent/docs/company_driver.md",
    "intent/docs/workflows.md",
    "intent/docs/ai_roles.md",
    "intent/docs/ai_constraints.md",
    "intent/docs/intent_inbox.md",
    "intent/docs/memory/decisions.md",
    "intent/docs/memory/assumptions.md",
    "intent/docs/memory/rejections.md",
    "intent/docs/memory/glossary.md",
]

MASTER_PROMPT = r"""
You are an autonomous AI agent operating inside a one-person company.

You MUST obey the Operating Hierarchy:
1) intent/docs/company_driver.md
2) intent/docs/workflows.md
3) intent/docs/ai_roles.md
4) intent/docs/ai_constraints.md
5) intent/docs/memory/*

Hard Rules:
- Select exactly ONE workflow.
- Activate exactly ONE role at a time.
- Produce at least ONE durable artifact.
- No silent scope expansion.
- Prefer small, checkable steps.
- If blocked, write a blocker artifact and stop.

OUTPUT FORMAT (MANDATORY):
Return ONLY a unified diff patch wrapped between the exact markers:

<patch>
diff --git a/FILE b/FILE
...
</patch>

No prose. No markdown. No code fences. No explanations.
If you cannot comply, return an empty patch:
<patch></patch>

WRITE PERMISSIONS OVERRIDE:
If the user message contains "WRITE PERMISSIONS", you MUST treat it as a hard constraint.
Never modify files outside that list.
When asked to "suggest a workflow", you MUST NOT edit intent/docs/workflows.md.
You must store the selected workflow as metadata in intent/docs/intent_inbox.md (e.g. #workflow=<NAME>).

INTENT INBOX FORMAT (MANDATORY WHEN WRITING TO docs/intent_inbox.md):
- Append-only. Never rewrite or reorder existing entries.
- Each new intent line must start with: YYYY-MM-DD HH:MM —
- Use Europe/Berlin local time.
"""


def read_files() -> str:
    parts: list[str] = []
    for rel in GOVERNING_FILES:
        p = ROOT / rel
        if p.exists():
            parts.append(f"\n\n### FILE: {rel}\n{p.read_text(encoding='utf-8')}")
        else:
            parts.append(f"\n\n### FILE: {rel}\n<missing>")
    return "\n".join(parts)


def ensure_git() -> None:
    if not (ROOT / ".git").exists():
        raise SystemExit("This repo is not a git repository. Run: git init")


def touched_files(patch: str) -> list[str]:
    files: list[str] = []

    # primary: diff --git headers
    for ln in patch.splitlines():
        if ln.startswith("diff --git "):
            parts = ln.split()
            if len(parts) >= 4:
                b = parts[3][2:] if parts[3].startswith("b/") else parts[3]
                files.append(b)

    if files:
        return files

    # fallback: --- a/... +++ b/...
    for ln in patch.splitlines():
        if ln.startswith("+++ "):
            b_path = ln[4:].strip()
            if b_path.startswith("b/"):
                b_path = b_path[2:]
            if b_path != "/dev/null":
                files.append(b_path)

    return files


def enforce_allowlist(files: list[str], allow: list[str]) -> None:
    if not allow:
        return

    allow_set = {Path(a).as_posix() for a in allow}
    bad = []

    for f in files:
        f_norm = Path(f).as_posix()
        if f_norm not in allow_set:
            bad.append(f)

    if bad:
        raise SystemExit(
            f"Patch touches disallowed files: {bad}. "
            f"Allowed: {sorted(allow_set)}"
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("intent", help="Raw intent to process")
    parser.add_argument("--model", default=os.environ.get("LOCAL_MODEL", "llama"))
    parser.add_argument(
        "--base-url",
        default=os.environ.get("LOCAL_BASE_URL", "http://localhost:11434/v1/"),
    )
    parser.add_argument("--api-key", default=os.environ.get("LOCAL_API_KEY", "ollama"))
    parser.add_argument("--dry-run", action="store_true", help="Print patch only, do not apply")
    parser.add_argument(
        "--allow-write",
        action="append",
        default=[],
        help=(
            "Relative path allowed to be modified; can be repeated. "
            "If empty, allow all."
        ),
    )

    args = parser.parse_args()

    ensure_git()

    # 1) Always append the raw intent with a timestamp BEFORE model execution.
    # This prevents missing-date entries and makes the run observable.
    appended_line = append_intent_line(args.intent)

    context = read_files()
    allowed = ", ".join(args.allow_write) if args.allow_write else "ANY"

    user_msg = f"""
INTENT (raw):
{args.intent}

INTENT INBOX (just appended by the script):
{appended_line.strip()}

REPO CONTEXT (governing files):
{context}

WRITE PERMISSIONS:
You may ONLY modify these files or directories:
{allowed}

If you believe other files should change:
- DO NOT modify them.
- Instead append a NOTE inside docs/intent_inbox.md.

TASK:
Pick EXACTLY ONE workflow and run it.
Produce at least ONE durable artifact.
Output ONLY a git-apply compatible unified diff patch.
"""

    client = OpenAI(base_url=args.base_url, api_key=args.api_key)
    resp = client.chat.completions.create(
        model=args.model,
        messages=[
            {"role": "system", "content": MASTER_PROMPT.strip()},
            {"role": "user", "content": user_msg.strip()},
        ],
        temperature=0,
        top_p=1,
    )

    raw = resp.choices[0].message.content or ""
    (ROOT / ".engine_last_raw.txt").write_text(raw, encoding="utf-8")

    patch = extract_patch(raw)
    patch = normalize_patch(patch)

    if not looks_like_patch(patch):
        raise SystemExit(
            "Model did not return a patch. Re-run with --dry-run to inspect raw output."
        )

    files = touched_files(patch)
    enforce_allowlist(files, args.allow_write)

    if args.dry_run:
        print(patch)
        return

    proc = subprocess.run(
        ["git", "apply", "--whitespace=nowarn", "-"],
        input=patch.encode("utf-8"),
    )
    if proc.returncode != 0:
        raise SystemExit("git apply failed. Re-run with --dry-run to inspect the patch.")

    print("Applied patch successfully.")
    print("Next: review changes via `git diff` and commit when satisfied.")


if __name__ == "__main__":
    main()
