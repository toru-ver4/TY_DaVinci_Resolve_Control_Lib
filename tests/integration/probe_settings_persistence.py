# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: .venv313/Scripts/python.exe tests/integration/probe_settings_persistence.py
# Run alone; compares legacy/canonical calls in fresh disposable Custom projects.

"""Distinguish settings persistence limitations from convention migration regressions."""

import json
import time
from pathlib import Path
from uuid import uuid4

from ty_davinci_resolve import (
    BT2100_PROJECT_SETTINGS, ResolveSession, close_project, create_project,
    delete_project, list_projects, load_project, save_project, set_project_settings,
)


def main() -> None:
    """Compare one-key writes, readback and reload using both conventions.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Notes
    -----
    Persistence mismatches are recorded observations. Lifecycle failures stop
    the probe, and every explicitly created project is deleted in ``finally``.

    Examples
    --------
    >>> main()  # doctest: +SKIP
    """
    session = ResolveSession.connect()
    if session.version[:3] != (21, 1, 0):
        raise RuntimeError("This convention comparison requires Resolve 21.1.0.")
    manager = session.project_manager
    original = manager.GetCurrentProject()
    original_name = original.GetName() if original else None
    names = list_projects(session)
    observations = []
    try:
        for convention in ("SetSetting", "SetSettings"):
            for key, value in (("rcmPresetMode", "SDR Rec.709"),
                               ("rcmPresetMode", "HDR DaVinci Wide Gamut Intermediate"),
                               ("isAutoColorManage", "1")):
                name = "TY_PERSIST_" + uuid4().hex[:12]
                try:
                    project = create_project(session, name)
                    set_project_settings(project, BT2100_PROJECT_SETTINGS, settle_delay=0.1)
                    set_project_settings(project, {"isAutoColorManage": "0"}, settle_delay=0.1)
                    save_project(session)
                    close_project(session, project)
                    project = load_project(session, name)
                    before = project.GetSettings()
                    accepted = (project.SetSetting(key, value) if convention == "SetSetting"
                                else project.SetSettings({key: value}))
                    time.sleep(0.5)
                    readback = project.GetSettings()
                    save_project(session)
                    close_project(session, project)
                    project = load_project(session, name)
                    reloaded = project.GetSettings()
                    observations.append(dict(convention=convention, key=key, value=value,
                                             accepted=accepted, before=before, readback=readback,
                                             reloaded=reloaded, persisted=str(reloaded[key]) == value))
                    print(convention, key, value, accepted, readback[key], reloaded[key], flush=True)
                finally:
                    if name in list_projects(session):
                        current = manager.GetCurrentProject()
                        if current and current.GetName() == name:
                            close_project(session, current)
                        delete_project(session, name)
    finally:
        if original_name and original_name in names:
            load_project(session, original_name)
    path = Path("docs/verification/21.1.0.17/settings-persistence-conventions.json")
    path.write_text(json.dumps(dict(resolve=session.version_string, observations=observations),
                               indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
