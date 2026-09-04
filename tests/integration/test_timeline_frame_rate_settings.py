# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest -m resolve_integration tests/integration/test_timeline_frame_rate_settings.py -q

from __future__ import annotations

from uuid import uuid4

import pytest

from ty_davinci_resolve import (
    FrameRate,
    ProjectSetting,
    ResolveSession,
    TimelineSetting,
    close_project,
    create_empty_timeline,
    create_project,
    delete_project,
    get_media_pool,
    get_timeline_setting,
    list_projects,
    load_project,
    set_project_setting,
    set_timeline_settings,
)


@pytest.mark.resolve_integration
def test_project_and_timeline_frame_rate_settings_have_distinct_scopes() -> None:
    session = ResolveSession.connect()
    manager = session.project_manager
    original = manager.GetCurrentProject()
    original_name = original.GetName() if original is not None else None
    original_names = tuple(manager.GetProjectListInCurrentFolder())
    project_name = f"TY_TIMELINE_FPS_{uuid4().hex[:16]}"

    try:
        project = create_project(session, project_name)
        set_project_setting(
            project,
            ProjectSetting.TIMELINE_FRAME_RATE,
            FrameRate.FPS_24,
        )
        assert (
            project.SetSetting(
                ProjectSetting.TIMELINE_PLAYBACK_FRAME_RATE,
                FrameRate.FPS_25,
            )
            is False
        )

        timeline = create_empty_timeline(get_media_pool(project), "25 fps Timeline")
        assert (
            timeline.SetSetting(
                TimelineSetting.TIMELINE_PLAYBACK_FRAME_RATE,
                FrameRate.FPS_25,
            )
            is False
        )

        set_timeline_settings(
            timeline,
            {TimelineSetting.TIMELINE_FRAME_RATE: FrameRate.FPS_25},
        )

        assert get_timeline_setting(
            timeline,
            TimelineSetting.USE_CUSTOM_SETTINGS,
        ) == "1"
        assert float(
            get_timeline_setting(timeline, TimelineSetting.TIMELINE_FRAME_RATE)
        ) == 25.0
        assert float(project.GetSetting(ProjectSetting.TIMELINE_FRAME_RATE)) == 24.0
        assert project.GetSetting(ProjectSetting.TIMELINE_PLAYBACK_FRAME_RATE) == "24"
    finally:
        current = manager.GetCurrentProject()
        if current is not None and current.GetName() == project_name:
            close_project(session, current)
        if project_name in list_projects(session):
            delete_project(session, project_name)
        if original_name in original_names:
            load_project(session, original_name)
