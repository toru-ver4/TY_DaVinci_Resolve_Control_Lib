# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python tests/stress/project_lifecycle_stress.py --iterations 20

"""Repeatedly exercise asynchronous Resolve project lifecycle APIs."""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess
import sys
import time
from uuid import uuid4

from ty_davinci_resolve import (
    ResolveSession,
    close_project,
    create_project,
    delete_project,
    list_projects,
    load_project,
    save_project,
    set_project_settings,
)


def _run_one(name: str) -> None:
    """Run one project lifecycle against Resolve.

    Parameters
    ----------
    name
        Unique temporary project name.

    Returns
    -------
    None

    Examples
    --------
    >>> _run_one("TY_DRC_STRESS_example")  # doctest: +SKIP
    """
    session = ResolveSession.connect()
    project = None
    try:
        project = create_project(session, name)
        set_project_settings(
            project,
            {
                "timelineResolutionWidth": "1280",
                "timelineResolutionHeight": "720",
            },
        )
        save_project(session)
        close_project(session, project)
        project = load_project(session, name)
        if project.GetName() != name:
            raise RuntimeError(f"Unexpected current project: {project.GetName()!r}")
        close_project(session, project)
        project = None
        delete_project(session, name)
    finally:
        if name in list_projects(session):
            current = session.project_manager.GetCurrentProject()
            if current is not None and current.GetName() == name:
                close_project(session, current)
            delete_project(session, name)


def _run_parent(iterations: int, timeout: float) -> None:
    """Run isolated lifecycle workers and enforce a per-iteration timeout.

    Parameters
    ----------
    iterations
        Number of lifecycle iterations.
    timeout
        Maximum worker duration in seconds.

    Returns
    -------
    None

    Examples
    --------
    >>> _run_parent(1, 45.0)  # doctest: +SKIP
    """
    script = Path(__file__).resolve()
    started = time.monotonic()
    for index in range(1, iterations + 1):
        name = f"TY_DRC_STRESS_{uuid4().hex}"
        iteration_started = time.monotonic()
        result = subprocess.run(
            [sys.executable, str(script), "--worker", name],
            cwd=script.parents[2],
            timeout=timeout,
            check=False,
        )
        if result.returncode != 0:
            raise RuntimeError(
                f"Stress iteration {index}/{iterations} failed with "
                f"exit code {result.returncode}."
            )
        elapsed = time.monotonic() - iteration_started
        print(f"PASS {index}/{iterations} ({elapsed:.2f}s)", flush=True)
    print(
        f"Completed {iterations} iterations in {time.monotonic() - started:.2f}s.",
        flush=True,
    )


def main() -> None:
    """Parse arguments and run the lifecycle stress test.

    Returns
    -------
    None

    Examples
    --------
    >>> main()  # doctest: +SKIP
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=20)
    parser.add_argument("--timeout", type=float, default=45.0)
    parser.add_argument("--worker", metavar="PROJECT_NAME")
    args = parser.parse_args()
    if args.worker:
        _run_one(args.worker)
        return
    if args.iterations <= 0 or args.timeout <= 0:
        parser.error("--iterations and --timeout must be positive")
    _run_parent(args.iterations, args.timeout)


if __name__ == "__main__":
    main()
