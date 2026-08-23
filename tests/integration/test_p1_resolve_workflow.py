# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest -m resolve_integration tests/integration/test_p1_resolve_workflow.py -q

from __future__ import annotations

from pathlib import Path
from uuid import uuid4

import pytest

from ty_davinci_resolve import (
    Page,
    ResolveSession,
    add_dctl_tool,
    add_transparent_background,
    append_fusion_composition,
    build_line,
    close_project,
    create_empty_timeline,
    create_project,
    delete_project,
    get_current_page,
    get_current_timeline,
    get_media_pool,
    get_timeline_resolution,
    get_timeline_setting,
    insert_generator,
    list_projects,
    load_project,
    make_video_monitor_format,
    open_page,
    refresh_fusion_color_management,
    refresh_lut_list,
    require_fusion_font,
    set_current_timecode,
    set_settings,
    set_timeline_settings,
)


@pytest.mark.resolve_integration
def test_p1_helpers_on_resolve_21_0_4() -> None:
    session = ResolveSession.connect()
    manager = session.project_manager
    original = manager.GetCurrentProject()
    original_name = original.GetName() if original is not None else None
    original_names = tuple(manager.GetProjectListInCurrentFolder())
    project_name = f"TY_P1_{uuid4().hex[:16]}"
    lut_root = Path(r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\LUT")

    try:
        project = create_project(session, project_name)
        set_settings(
            project,
            {
                "timelineResolutionWidth": "1280",
                "timelineResolutionHeight": "720",
                "videoMonitorFormat": make_video_monitor_format(1280, 720, 23.976),
                "timelineFrameRate": "23.976",
            },
        )
        assert get_timeline_resolution(project) == (1280, 720)
        refresh_lut_list(project)

        media_pool = get_media_pool(project)
        timeline = create_empty_timeline(media_pool, "P1 Helpers")
        assert get_current_timeline(project) is not None
        open_page(session, Page.EDIT)
        assert get_current_page(session) is Page.EDIT
        set_current_timecode(timeline, "01:00:00:00")
        set_timeline_settings(
            timeline,
            {
                "timelineResolutionWidth": "1280",
                "timelineResolutionHeight": "720",
            },
        )
        assert get_timeline_setting(timeline, "timelineResolutionWidth") == "1280"
        assert get_timeline_setting(timeline, "timelineResolutionHeight") == "720"

        fixed_item, fixed_comp = append_fusion_composition(
            timeline,
            duration_frames=24,
            record_frame=86448,
            media_pool=media_pool,
        )
        assert fixed_comp is not None
        assert fixed_item.GetDuration() == 24

        assert insert_generator(timeline, "Solid Color") is not None

        native_item, native_comp = append_fusion_composition(timeline)
        assert native_item.GetFusionCompCount() >= 1
        transparent = add_transparent_background(native_comp, (0, 0))
        assert transparent is not None
        assert build_line(native_comp, (1.0, 1.0, 1.0, 1.0), 1.0, 0.01, position=(1, 2)) is not None
        require_fusion_font(session.fusion, "Noto Sans", "Regular")
        assert add_dctl_tool(
            native_comp,
            "TY_DCTL/draw_45deg_lines.dctl",
            lut_root=lut_root,
            position=(3, 2),
        ) is not None

        refresh_fusion_color_management(session)
        assert get_current_page(session) is Page.EDIT
    finally:
        current = manager.GetCurrentProject()
        if current is not None and current.GetName() == project_name:
            close_project(session, current)
        if project_name in list_projects(session):
            delete_project(session, project_name)
        if original_name in original_names:
            load_project(session, original_name)
