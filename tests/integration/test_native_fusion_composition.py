# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest -m resolve_integration tests/integration/test_native_fusion_composition.py -q

from __future__ import annotations

from uuid import uuid4

import pytest

from ty_davinci_resolve import (
    ResolveSession,
    close_project,
    create_empty_timeline,
    create_project,
    delete_project,
    get_media_pool,
    insert_fusion_composition,
    list_projects,
    load_project,
)


@pytest.mark.resolve_integration
def test_insert_native_fusion_composition() -> None:
    session = ResolveSession.connect()
    manager = session.project_manager
    original = manager.GetCurrentProject()
    original_name = original.GetName() if original is not None else None
    original_names = tuple(manager.GetProjectListInCurrentFolder())
    project_name = f"TY_FC_{uuid4().hex[:16]}"

    try:
        project = create_project(session, project_name)
        timeline = create_empty_timeline(get_media_pool(project), "Native Fusion")
        assert session.resolve.OpenPage("edit") is True

        item = insert_fusion_composition(timeline)

        assert item is not None
        assert item.GetFusionCompCount() >= 1
    finally:
        current = manager.GetCurrentProject()
        if current is not None and current.GetName() == project_name:
            close_project(session, current)
        if project_name in list_projects(session):
            delete_project(session, project_name)
        if original_name in original_names:
            load_project(session, original_name)
