# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest -m resolve_integration tests/integration/test_p2_resolve_workflow.py -q -s

from __future__ import annotations

from uuid import uuid4

import pytest

from ty_davinci_resolve import (
    Page,
    ResolveSession,
    append_fusion_composition,
    build_rectangle,
    close_project,
    create_empty_timeline,
    create_project,
    delete_project,
    get_current_page,
    get_fusion_fonts,
    get_media_pool,
    get_packaged_fusion_duration_media,
    list_projects,
    load_project,
    make_video_monitor_format,
    open_page,
    set_settings,
    set_tool_position,
)


@pytest.mark.resolve_integration
def test_p2_helpers_on_resolve_21_0_4() -> None:
    session = ResolveSession.connect()
    manager = session.project_manager
    original = manager.GetCurrentProject()
    original_name = original.GetName() if original is not None else None
    original_names = tuple(manager.GetProjectListInCurrentFolder())
    project_name = f"TY_P2_{uuid4().hex[:16]}"

    try:
        project = create_project(session, project_name)
        set_settings(
            project,
            {
                "timelineResolutionWidth": "1280",
                "timelineResolutionHeight": "720",
                "videoMonitorFormat": make_video_monitor_format(
                    1280, 720, 23.976
                ),
                "timelineFrameRate": "23.976",
            },
        )
        media_pool = get_media_pool(project)
        timeline = create_empty_timeline(media_pool, "P2 Helpers")
        open_page(session, Page.EDIT)
        _, comp = append_fusion_composition(timeline)

        rectangle = build_rectangle(
            comp,
            (0.1, 0.2, 0.3, 0.4),
            center=(0.25, 0.75),
            width=0.2,
            height=0.3,
            position=(2, 4),
        )
        assert rectangle.GetInput("TopLeftAlpha") == pytest.approx(0.4)

        fonts = get_fusion_fonts(session.fusion)
        assert "Noto Sans" in fonts
        assert "Regular" in fonts["Noto Sans"]

        selected = get_packaged_fusion_duration_media(1280, 720, "23.9760")
        assert selected.name == "dummy_video_1280x720_23.976P.mp4"

        open_page(session, Page.EDIT)
        activation_was_required = comp.CurrentFrame is None
        set_tool_position(
            comp,
            rectangle,
            (5, 3),
            session=session,
            activate_fusion_page=True,
        )
        if activation_was_required:
            assert get_current_page(session) is Page.FUSION
    finally:
        current = manager.GetCurrentProject()
        if current is not None and current.GetName() == project_name:
            close_project(session, current)
        if project_name in list_projects(session):
            delete_project(session, project_name)
        if original_name in original_names:
            load_project(session, original_name)
