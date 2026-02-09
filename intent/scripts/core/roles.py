from __future__ import annotations

from dataclasses import dataclass

from intent.scripts.core.errors import GuardViolation, ValidationError


@dataclass(frozen=True)
class Role:
    name: str
    trigger: str


def registry() -> dict[str, Role]:
    return {
        "Strategist": Role("Strategist", "What’s the highest-leverage next move?"),
        "Visioneer": Role("Visioneer", "What could this become if it worked extremely well?"),
        "Architect": Role("Architect", "What is the smallest structure that makes this executable?"),
        "Breaker": Role("Breaker", "How will this fail in the real world?"),
        "Curator": Role("Curator", "How do we make this easier next time?"),
    }


def validate_role_name(name: str) -> str:
    r = registry()
    if name not in r:
        raise ValidationError(f"Unknown role: {name}. Options: {sorted(r.keys())}")
    return name


class RoleStack:
    """Enforce 'one role active at a time'."""

    def __init__(self) -> None:
        self._stack: list[str] = []

    def activate(self, role: str):
        validate_role_name(role)
        if self._stack:
            raise GuardViolation(
                f"Role already active: {self._stack[-1]}. Must deactivate before activating {role}."
            )
        self._stack.append(role)

        class _Ctx:
            def __enter__(_self):
                return role

            def __exit__(_self, exc_type, exc, tb):
                self._stack.pop()

        return _Ctx()
