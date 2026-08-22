# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest -m resolve_integration tests/integration/test_project_lifecycle.py -q

from __future__ import annotations

from uuid import uuid4

import pytest

from ty_davinci_resolve import (
    ResolveSession,
    close_project,
    create_project,
    delete_project,
    list_projects,
    load_project,
    save_project,
    set_settings,
)


@pytest.mark.resolve_integration
def test_project_create_save_close_load_delete() -> None:
    session = ResolveSession.connect()
    manager = session.project_manager
    original = manager.GetCurrentProject()
    original_name = original.GetName() if original is not None else None
    test_name = f"TY_DRC_TEST_{uuid4().hex}"

    try:
        project = create_project(session, test_name)
        assert project.GetName() == test_name
        set_settings(
            project,
            {
                "timelineResolutionWidth": "1280",
                "timelineResolutionHeight": "720",
            },
        )
        save_project(session)
        close_project(session, project)

        loaded = load_project(session, test_name)
        assert loaded.GetName() == test_name
        close_project(session, loaded)
        delete_project(session, test_name)
        assert test_name not in list_projects(session)
    finally:
        current = manager.GetCurrentProject()
        if current is not None and current.GetName() == test_name:
            manager.CloseProject(current)
        if test_name in manager.GetProjectListInCurrentFolder():
            manager.DeleteProject(test_name)
        if original_name and original_name in manager.GetProjectListInCurrentFolder():
            manager.LoadProject(original_name)
