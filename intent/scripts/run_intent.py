#!/usr/bin/env python3
"""scripts/run_intent.py

Run an intent-driven execution cycle.

Responsibilities
- Read governing docs (AGENTS.md, .clinerules/core.md, docs/*) as *context*.
- Invoke an LLM to produce a git-apply compatible unified diff patch.
- Optionally enforce an allowlist for modified files.
- Optionally apply the patch via `git apply`.

Non-responsibilities
- Writing new intent lines to docs/intent_inbox.md (capture happens elsewhere).
  This script may *append* a NOTE entry only if explicitly instructed by the prompt
  and only in append-only fashion.

Usage examples
- Dry run (print patch):
  ./scripts/run_intent.py --latest --dry-run

- Run explicit intent (does NOT write to inbox):
  ./scripts/run_intent.py "Fix date parsing in intent capture" --dry-run

- Apply patch with allowlist:
  ./scripts/run_intent.py --latest --allow-write docs/intent_inbox.md --allow-write docs/memory/decisions.md

Environment
- LOCAL_MODEL: model name
- LOCAL_BASE_URL: OpenAI-compatible base URL
- LOCAL_API_KEY: API key

Note
- Timezone for any timestamp logic (if needed) is Europe/Berlin.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
TIMEZONE = ZoneInfo("Europe/Berlin")

INTENT_INBOX = ROOT / "docs/intent_inbox.md"
ENGINE_LAST_RAW = ROOT / ".engine_last_raw.txt"

PATCH_RE = re.compile(r"<patch>\s*(.*?)\s*</patch>", re.DOTALL)

# Keep this list small and stable. Add files only when they become governing.
GOVERNING_FILES = [
    "AGENTS.md",
    ".clinerules/core.md",
    "docs/company_driver.md",
    "docs/workflows.md",
    "docs/ai_roles.md",
    "docs/ai_constraints.md",
    "docs/intent_inbox.md",
    "docs/memory/decisions.md",
    "docs/memory/assumptions.md",
    "docs/memory/rejections.md",
    "docs/memory/glossary.md",
]

MASTER_PROMPT = r"""
You are an autonomous AI agent operating inside a one-person company.

You MUST obey the Operating Hierarchy:
1) docs/company_driver.md
2) docs/workflows.md
3) docs/ai_roles.md
4) docs/ai_constraints.md
5) docs/memory/*

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
When asked to "suggest a workflow", you MUST NOT edit docs/workflows.md.
If you write to docs/intent_inbox.md, it MUST be append-only and every new line MUST start with:
YYYY-MM-DD HH:MM — (Europe/Berlin time).
""".strip()


def ensure_git_repo() -> None:
    if not (ROOT / ".git").exists():
        raise SystemExit("This repo is not a git repository. Run: git init")


def read_governing_files() -> str:
    parts: list[str] = []
    for rel in GOVERNING_FILES:
        p = ROOT / rel
        if p.exists():
            parts.append(f"\n\n### FILE: {rel}\n{p.read_text(encoding='utf-8')}")
        else:
            parts.append(f"\n\n### FILE: {rel}\n<missing>")
    return "\n".join(parts)


def extract_patch(text: str) -> str:
    text = text or ""
    m = PATCH_RE.search(text)
    if m:
        return (m.group(1) or "").strip()
    return text.strip()


def looks_like_patch(p: str) -> bool:
    p = (p or "").lstrip()
    if not p:
        return False
    return p.startswith("diff --git") or (p.startswith("--- ") and "\n+++ " in p)


def touched_files(patch: str) -> list[str]:
    files: list[str] = []

    for ln in patch.splitlines():
        if ln.startswith("diff --git "):
            parts = ln.split()
            if len(parts) >= 4:
                b = parts[3]
                if b.startswith("b/"):
                    b = b[2:]
                files.append(b)

    if files:
        return files

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
    bad = [f for f in files if Path(f).as_posix() not in allow_set]

    if bad:
        raise SystemExit(
            f"Patch touches disallowed files: {bad}. Allowed: {sorted(allow_set)}"
        )


def read_latest_intent_line() -> str:
    if not INTENT_INBOX.exists():
        raise SystemExit("docs/intent_inbox.md not found. Capture an intent first.")

    lines = INTENT_INBOX.read_text(encoding="utf-8").splitlines()
    # Find last non-empty line that is not inside a code block.
    for ln in reversed(lines):
        if ln.strip():
            return ln.strip()

    raise SystemExit("docs/intent_inbox.md is empty.")


def berlin_now_line_prefix() -> str:
    return datetime.now(TIMEZONE).strftime("%Y-%m-%d %H:%M")


def build_user_message(intent: str, context: str, allow_write: list[str]) -> str:
    allowed = ", ".join(allow_write) if allow_write else "ANY"

    # Keep the user message extremely explicit to reduce model creativity.
    return f"""
INTENT:
{intent}

REPO CONTEXT (governing files):
{context}

WRITE PERMISSIONS:
You may ONLY modify these files or directories:
{allowed}

If you believe other files should change:
- DO NOT modify them.
- Instead append a NOTE inside docs/intent_inbox.md using this exact prefix:
  {berlin_now_line_prefix()} — NOTE: ...

TASK:
Pick EXACTLY ONE workflow and run it.
Produce at least ONE durable artifact.
Output ONLY a git-apply compatible unified diff patch.
""".strip()


def call_model(model: str, base_url: str, api_key: str, user_msg: str) -> str:
    client = OpenAI(base_url=base_url, api_key=api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": MASTER_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        temperature=0,
        top_p=1,
    )
    return resp.choices[0].message.content or ""


def apply_patch(patch: str) -> None:
    proc = subprocess.run(
        ["git", "apply", "--whitespace=nowarn", "-"],
        input=patch.encode("utf-8"),
    )
    if proc.returncode != 0:
        raise SystemExit("git apply failed. Re-run with --dry-run to inspect the patch.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("intent", nargs="?", help="Explicit intent to run")
    parser.add_argument(
        "--latest",
        action="store_true",
        help="Use the last non-empty line from docs/intent_inbox.md as the intent",
    )
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

    ensure_git_repo()

    if args.latest:
        intent = read_latest_intent_line()
    else:
        intent = (args.intent or "").strip()

    if not intent:
        raise SystemExit("Provide an intent string, or pass --latest.")

    context = read_governing_files()
    user_msg = build_user_message(intent=intent, context=context, allow_write=args.allow_write)

    raw = call_model(
        model=args.model,
        base_url=args.base_url,
        api_key=args.api_key,
        user_msg=user_msg,
    )
    ENGINE_LAST_RAW.write_text(raw, encoding="utf-8")

    patch = extract_patch(raw).strip()

    if not patch:
        raise SystemExit("Model returned an empty patch.")

    if not looks_like_patch(patch):
        raise SystemExit(
            "Model did not return a git-apply compatible patch. "
            "Inspect .engine_last_raw.txt for the raw output."
        )

    files = touched_files(patch)
    enforce_allowlist(files, args.allow_write)

    if args.dry_run:
        print(patch)
        return

    apply_patch(patch)

    print("Applied patch successfully.")
    print("Next: review changes via `git diff` and commit when satisfied.")


if __name__ == "__main__":
    main()
