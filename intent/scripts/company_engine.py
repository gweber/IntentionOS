#!/usr/bin/env python3
import argparse
import os
import re
import subprocess
from pathlib import Path


from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]

PATCH_RE = re.compile(r"<patch>\s*(.*?)\s*</patch>", re.DOTALL)

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
    # If model returned a patch without diff --git headers, try to convert.
    # Minimal salvage: if it starts with --- a/... +++ b/... keep it as is;
    # git apply accepts it, but your current check rejects it.
    return p.strip()



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
You must store the selected workflow as metadata in docs/intent_inbox.md (e.g. #workflow=<NAME>).

"""


def read_files():
    parts = []
    for rel in GOVERNING_FILES:
        p = ROOT / rel
        if p.exists():
            parts.append(f"\n\n### FILE: {rel}\n{p.read_text(encoding='utf-8')}")
        else:
            parts.append(f"\n\n### FILE: {rel}\n<missing>")
    return "\n".join(parts)

def ensure_git():
    if not (ROOT / ".git").exists():
        raise SystemExit("This repo is not a git repository. Run: git init")

def touched_files(patch: str) -> list[str]:
    files = []
    # primary: diff --git headers
    for line in patch.splitlines():
        if line.startswith("diff --git "):
            parts = line.split()
            if len(parts) >= 4:
                b = parts[3][2:] if parts[3].startswith("b/") else parts[3]
                files.append(b)

    if files:
        return files

    # fallback: --- a/... +++ b/...
    a_path = None
    for line in patch.splitlines():
        if line.startswith("--- "):
            a_path = line[4:].strip()
        elif line.startswith("+++ "):
            b_path = line[4:].strip()
            if b_path.startswith("b/"):
                b_path = b_path[2:]
            if b_path != "/dev/null":
                files.append(b_path)
            a_path = None

    return files

def enforce_allowlist(files: list[str], allow: list[str]):
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



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("intent", help="Raw intent to process")
    parser.add_argument("--model", default=os.environ.get("LOCAL_MODEL", "llama"))
    parser.add_argument("--base-url", default=os.environ.get("LOCAL_BASE_URL", "http://localhost:11434/v1/"))
    parser.add_argument("--api-key", default=os.environ.get("LOCAL_API_KEY", "ollama"))
    parser.add_argument("--dry-run", action="store_true", help="Print patch only, do not apply")
    parser.add_argument("--allow-write", action="append", default=[],
                    help="Relative path allowed to be modified; can be repeated. If empty, allow all.")

    args = parser.parse_args()

    ensure_git()

    context = read_files()
    allowed = ", ".join(args.allow_write) if args.allow_write else "ANY"

    user_msg = f"""
    INTENT (raw):
    {args.intent}

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
    (Path(ROOT) / ".engine_last_raw.txt").write_text(raw, encoding="utf-8")


    patch = resp.choices[0].message.content or ""
    patch = extract_patch(patch)
    patch = normalize_patch(patch)

    if not looks_like_patch(patch):
        raise SystemExit("Model did not return a patch. Re-run with --dry-run to inspect raw output.")

    files = touched_files(patch)
    enforce_allowlist(files, args.allow_write)

    if args.dry_run:
        print(patch)
        return

    proc = subprocess.run(
        ["git", "apply", "--whitespace=nowarn", "-"],
        input=patch.encode("utf-8")
    )
    if proc.returncode != 0:
        raise SystemExit("git apply failed. Re-run with --dry-run to inspect the patch.")

    print("Applied patch successfully.")
    print("Next: review changes via `git diff` and commit when satisfied.")


if __name__ == "__main__":
    main()
