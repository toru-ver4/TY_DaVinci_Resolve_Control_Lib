# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: .venv313/Scripts/python.exe tests/integration/probe_resolve_upgrade.py snapshot LABEL
# Commands: set LABEL KEY VALUE; reload LABEL; cleanup

"""Record full snapshots of the explicitly named disposable GUI project."""

import argparse
import json
import time
from pathlib import Path

from ty_davinci_resolve import (
    ResolveSession, close_project, delete_project, load_project, save_project,
    set_project_setting,
)

PROJECT_NAME = "TY_UPGRADE_GUI_20261004"
OUTPUT = Path("docs/verification/21.1.0.17")


def main() -> None:
    """Record a controlled setting change or clean up the probe project.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Examples
    --------
    >>> main()  # doctest: +SKIP
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("snapshot", "set", "reload", "cleanup"))
    parser.add_argument("label", nargs="?")
    parser.add_argument("key", nargs="?")
    parser.add_argument("value", nargs="?")
    args = parser.parse_args()
    session = ResolveSession.connect()
    if session.version[:3] != (21, 1, 0):
        raise RuntimeError("This evidence probe requires Resolve 21.1.0.")
    project = session.project_manager.GetCurrentProject()
    if project is None or project.GetName() != PROJECT_NAME:
        raise RuntimeError("The disposable upgrade project must be current.")
    if args.action == "cleanup":
        close_project(session, project)
        delete_project(session, PROJECT_NAME)
        return
    if not args.label or not all(c.isalnum() or c in "-_" for c in args.label):
        raise ValueError("A simple filename label is required.")
    path = OUTPUT / f"{args.label}.json"
    if path.exists():
        raise FileExistsError(f"Evidence already exists: {path}")
    before = project.GetSettings()
    if not isinstance(before, dict):
        raise RuntimeError("GetSettings did not return the initial snapshot.")
    if args.action == "set":
        if args.key is None or args.value is None:
            raise ValueError("set requires a key and value.")
        set_project_setting(project, args.key, args.value)
        time.sleep(0.5)
    elif args.action == "reload":
        save_project(session)
        close_project(session, project)
        project = load_project(session, PROJECT_NAME)
    after = project.GetSettings()
    if not isinstance(before, dict) or not isinstance(after, dict):
        raise RuntimeError("GetSettings did not return a snapshot.")
    if args.action == "set" and str(after.get(args.key)) != args.value:
        try:
            matches = float(after[args.key]) == float(args.value)
        except (KeyError, TypeError, ValueError):
            matches = False
        if not matches:
            raise RuntimeError(f"Readback mismatch for {args.key!r}: {after.get(args.key)!r}")
    result = {"action": args.action, "resolve": session.version_string,
              "key": args.key, "value": args.value, "before": before, "after": after,
              "diff": {k: {"before": before.get(k), "after": after.get(k)}
                       for k in sorted(before.keys() | after.keys())
                       if before.get(k) != after.get(k)}}
    OUTPUT.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["diff"], indent=2))


if __name__ == "__main__":
    main()
