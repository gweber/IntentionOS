from __future__ import annotations

from datetime import datetime
import re

from agent_scripts.core.artifacts import Artifact, artifact_path, build_artifact_markdown, write_artifact
from agent_scripts.core.config import default_paths
from agent_scripts.core.errors import ValidationError
from agent_scripts.core.guards import (
    ensure_artifact_enforced,
    ensure_single_role_sequence,
    ensure_single_workflow,
)
from agent_scripts.core.logging import log
from agent_scripts.core.md_parse import read_inbox_entries
from agent_scripts.core.memory import apply_memory_updates, extract_memory_updates
from agent_scripts.core.roles import RoleStack, validate_role_name
from agent_scripts.core.state import RunState
from agent_scripts.core.workflows import choose_workflow


def _select_intent(intent: str | None, once: bool) -> str:
    paths = default_paths()
    if intent and intent.strip():
        return intent.strip()
    if not once:
        raise ValidationError("Provide --intent or pass --once to use the latest inbox entry.")

    entries = read_inbox_entries(paths.inbox_path)
    if not entries:
        raise ValidationError(f"No inbox entries found in {paths.inbox_path}.")
    return entries[-1].statement


_INLINE_DECISION_RE = re.compile(r"^\s*Decision:\s*(.+?)\s*$", re.IGNORECASE)
_INLINE_ASSUMPTION_RE = re.compile(r"^\s*Assumption:\s*(.+?)\s*$", re.IGNORECASE)


def _extract_inline_notes(raw_intent: str) -> tuple[str, list[str], list[str]]:
    """Extract optional inline notes from an intent.

    Supported (one per line):
      Decision: ...
      Assumption: ...

    Returns: (clean_intent, decisions, assumptions)
    """
    decisions: list[str] = []
    assumptions: list[str] = []
    kept: list[str] = []

    # Support both literal newlines and user-provided "\\n" sequences from shells.
    normalized = (raw_intent or "").replace("\\n", "\n")
    for ln in normalized.splitlines():
        if not ln.strip():
            continue
        m = _INLINE_DECISION_RE.match(ln)
        if m:
            decisions.append(m.group(1).strip())
            continue
        m = _INLINE_ASSUMPTION_RE.match(ln)
        if m:
            assumptions.append(m.group(1).strip())
            continue
        kept.append(ln.strip())

    clean_intent = " ".join(kept).strip()
    return clean_intent, decisions, assumptions


def run_once(
    *,
    intent: str | None,
    once: bool,
    workflow_override: str | None,
    role_override: str | None,
    dry_run: bool,
    print_plan: bool,
) -> RunState:
    paths = default_paths()
    selected_intent_raw = _select_intent(intent=intent, once=once)
    selected_intent, decisions, assumptions = _extract_inline_notes(selected_intent_raw)
    if not selected_intent:
        raise ValidationError("Intent must contain a non-empty statement.")

    wf = choose_workflow(selected_intent, workflow_override)

    role = validate_role_name(role_override or "Architect")
    role_sequence = [role]

    created_at = datetime.now()
    art_path = artifact_path(paths.artifacts_dir, created_at, selected_intent)

    ensure_single_workflow(wf.name)
    ensure_single_role_sequence(role_sequence)

    success_criteria = [
        "An artifact markdown file is created under intent/docs/artifacts/YYYY-MM-DD/.",
        "The artifact includes required sections (Intent, Success criteria, Selected workflow, Role sequence, Decisions, Assumptions, Next intent, Next smallest step).",
        "If Decisions/Assumptions are present, memory files are appended atomically.",
    ]

    # Deterministic defaults: no decisions/assumptions unless explicitly provided inline.
    next_intent = "Review this artifact and append the next concrete intent to intent/docs/intent_inbox.md."
    next_step = f"Open {art_path.as_posix()} and replace placeholders with concrete next actions (≤10 minutes)."

    # Enforce role activation: one at a time.
    stack = RoleStack()
    with stack.activate(role):
        artifact_md = build_artifact_markdown(
            created_at=created_at,
            intent=selected_intent,
            workflow=wf.name,
            workflow_steps=list(wf.steps),
            role_sequence=role_sequence,
            success_criteria=success_criteria,
            decisions=decisions,
            assumptions=assumptions,
            next_intent=next_intent,
            next_step=next_step,
        )

    updates = extract_memory_updates(artifact_md)

    if print_plan:
        log("plan", intent=selected_intent, workflow=wf.name, workflow_steps=list(wf.steps), typical_roles=list(wf.typical_roles), role_sequence=role_sequence)

    state = RunState(
        intent=selected_intent,
        workflow=wf.name,
        role_sequence=role_sequence,
        workflow_steps=list(wf.steps),
        success_criteria=success_criteria,
        dry_run=dry_run,
        created_at=created_at,
        artifact_path=art_path,
    )

    if dry_run:
        log(
            "dry_run",
            would_write_artifact=str(art_path),
            would_append_decisions=len(updates.decisions),
            would_append_assumptions=len(updates.assumptions),
        )
        ensure_artifact_enforced(artifact_path=art_path, written_paths=[], dry_run=True)
        return state

    # Write artifact first; memory appends only happen after artifact exists.
    artifact = Artifact(path=art_path, content=artifact_md)
    write_artifact(artifact)
    state.artifacts_written.append(art_path)

    source = art_path.as_posix()
    state.memory_appends = apply_memory_updates(
        decisions_path=paths.decisions_path,
        assumptions_path=paths.assumptions_path,
        created_at=created_at,
        artifact_md=artifact_md,
        source=source,
    )

    ensure_artifact_enforced(artifact_path=art_path, written_paths=state.artifacts_written, dry_run=False)
    return state
