from __future__ import annotations

import argparse
import sys

from agent_scripts.core.engine import run_once
from agent_scripts.core.errors import GuardViolation, ValidationError
from agent_scripts.core.logging import log


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m agent_scripts.run")
    p.add_argument("--once", action="store_true", help="Process most recent inbox entry")
    p.add_argument("--intent", help="Run with an explicit intent (does not modify inbox)")
    p.add_argument("--workflow", help="Workflow name override")
    p.add_argument("--role", help="Role name override")
    p.add_argument("--dry-run", action="store_true", help="No files written; print what would happen")
    p.add_argument(
        "--print-plan",
        action="store_true",
        help="Print selected workflow steps + role order (implies dry-run)",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        state = run_once(
            intent=args.intent,
            once=args.once,
            workflow_override=args.workflow,
            role_override=args.role,
            dry_run=bool(args.dry_run or args.print_plan),
            print_plan=args.print_plan,
        )
    except ValidationError as e:
        log("error", kind="validation", message=str(e))
        return 2
    except GuardViolation as e:
        log("error", kind="guard", message=str(e))
        return 3

    if args.print_plan:
        # run_once already printed plan. Keep exit code semantics simple.
        return 0

    log(
        "run_complete",
        artifact_paths=[str(p) for p in state.artifacts_written],
        memory_appends=state.memory_appends,
        dry_run=state.dry_run,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
