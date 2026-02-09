class ValidationError(Exception):
    """User input / configuration errors (exit code 2)."""


class GuardViolation(Exception):
    """Framework invariant violations (exit code 3)."""
