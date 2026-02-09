from __future__ import annotations

from dataclasses import dataclass

from intent.scripts.core.errors import ValidationError


@dataclass(frozen=True)
class Workflow:
    name: str
    steps: tuple[str, ...]
    typical_roles: tuple[str, ...]


def registry() -> dict[str, Workflow]:
    return {
        "Idea → Execution": Workflow(
            name="Idea → Execution",
            steps=(
                "Capture intent + success criteria.",
                "Define the smallest valuable artifact.",
                "Identify risks/unknowns and the shortest test.",
                "Produce a plan (steps, constraints, definition of done).",
                "Execute in small increments.",
                "Record decisions/assumptions and update memory.",
            ),
            typical_roles=("Visioneer", "Strategist", "Architect", "Breaker", "Curator"),
        ),
        "Friction → Fix": Workflow(
            name="Friction → Fix",
            steps=(
                "Describe the friction in observable terms (symptoms, frequency, cost).",
                "Reproduce or bound it (what conditions trigger it?).",
                "Propose a minimal fix and a guardrail.",
                "Validate the fix (tests/checklist).",
                "Codify into a rule/runbook.",
            ),
            typical_roles=("Breaker", "Architect", "Curator"),
        ),
    }


def validate_workflow_name(name: str) -> str:
    r = registry()
    if name not in r:
        raise ValidationError(f"Unknown workflow: {name}. Options: {sorted(r.keys())}")
    return name


def choose_workflow(intent: str, override: str | None) -> Workflow:
    r = registry()
    if override:
        return r[validate_workflow_name(override)]

    i = (intent or "").lower()
    if "confusing" in i or "slow" in i:
        return r["Friction → Fix"]
    return r["Idea → Execution"]
