# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python tests/integration/probe_project_setting_keys.py

"""Probe snapshot keys not yet represented by ``ProjectSetting``."""

from __future__ import annotations

import time
from uuid import uuid4

from ty_davinci_resolve import (
    ProjectSetting,
    ResolveSession,
    close_project,
    create_project,
    delete_project,
    list_projects,
)


def main() -> None:
    """Report missing keys whose current value is accepted and read back."""
    session = ResolveSession.connect()
    name = f"TY_SETTING_KEY_PROBE_{uuid4().hex}"
    project = None
    try:
        project = create_project(session, name)
        snapshot = project.GetSetting()
        known = {item.value for item in ProjectSetting}
        accepted: list[tuple[str, object]] = []
        rejected: list[tuple[str, object]] = []
        for key in sorted(set(snapshot) - known):
            value = snapshot[key]
            result = project.SetSetting(key, value)
            time.sleep(0.05)
            actual = project.GetSetting(key)
            target = accepted if result is True and actual == value else rejected
            target.append((key, value))
        print(f"snapshot={len(snapshot)} known={len(known)}")
        print("accepted missing keys:")
        for item in accepted:
            print(repr(item))
        print("rejected missing keys:")
        for item in rejected:
            print(repr(item))
    finally:
        manager = session.project_manager
        current = manager.GetCurrentProject()
        if current is not None and current.GetName() == name:
            close_project(session, current)
        if name in list_projects(session):
            delete_project(session, name)


if __name__ == "__main__":
    main()
