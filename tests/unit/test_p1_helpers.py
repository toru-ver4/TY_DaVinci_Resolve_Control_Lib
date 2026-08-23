# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_p1_helpers.py -q

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from ty_davinci_resolve import (
    MediaStorageItem,
    Page,
    ResolveOperationError,
    ResolveSession,
    ResolveValidationError,
    add_dctl_tool,
    add_transparent_background,
    append_fusion_composition,
    build_line,
    connect_default_output,
    connect_merge,
    delete_render_preset,
    get_current_page,
    get_current_timeline,
    get_timeline_resolution,
    get_timeline_setting,
    import_media_storage_items,
    import_render_preset,
    insert_generator,
    make_video_monitor_format,
    open_page,
    refresh_fusion_color_management,
    refresh_lut_list,
    render_current_settings,
    require_fusion_font,
    set_background_color,
    set_current_timecode,
    set_timeline_settings,
)


class FakeTool:
    def __init__(self, name: str = "Background1") -> None:
        self.Name = name
        self.values: dict[str, object] = {}
        self.connections: list[tuple[str, object]] = []
        self.deleted = False

    def SetInput(self, name: str, value: object) -> None:
        self.values[name] = value

    def GetInput(self, name: str) -> object:
        return self.values[name]

    def ConnectInput(self, name: str, source: object) -> bool:
        self.connections.append((name, source))
        return True

    def Delete(self) -> bool:
        self.deleted = True
        return True


class FakeComp:
    def __init__(self, initial_tools: list[FakeTool] | None = None) -> None:
        self.tools = list(initial_tools or [])

    def AddTool(self, tool_type: str, x: float, y: float) -> FakeTool:
        tool = FakeTool(f"{tool_type}{len(self.tools) + 1}")
        tool.tool_type = tool_type
        tool.position = (x, y)
        self.tools.append(tool)
        return tool

    def GetToolList(self) -> dict[int, FakeTool]:
        return {index: tool for index, tool in enumerate(self.tools, 1)}


def make_session(resolve: object, fusion: object | None = None) -> ResolveSession:
    return ResolveSession(resolve, fusion or object(), "Resolve", (21, 0, 4, 5), "21.0.4.5")


def test_page_helpers_validate_and_switch() -> None:
    opened: list[str] = []
    resolve = SimpleNamespace(
        GetCurrentPage=lambda: "edit",
        OpenPage=lambda page: opened.append(page) is None,
    )
    resolve.OpenPage = lambda page: opened.append(page) or True
    session = make_session(resolve)

    assert get_current_page(session) is Page.EDIT
    open_page(session, Page.FUSION)
    assert opened == ["fusion"]
    with pytest.raises(ResolveValidationError):
        open_page(session, "invalid")


def test_project_resolution_monitor_format_and_lut_refresh() -> None:
    project = SimpleNamespace(
        GetSetting=lambda name: {"timelineResolutionWidth": "1280", "timelineResolutionHeight": "720"}[name],
        RefreshLUTList=lambda: True,
    )
    assert get_timeline_resolution(project) == (1280, 720)
    assert make_video_monitor_format(1280, 720, 23.976) == "HD 720p 23.976"
    refresh_lut_list(project)
    with pytest.raises(ResolveValidationError):
        make_video_monitor_format(1000, 720, 24)


def test_media_storage_import_supports_paths_and_ranges(tmp_path: Path) -> None:
    media = tmp_path / "dummy.mov"
    media.write_bytes(b"dummy")
    captured: list[object] = []
    storage = SimpleNamespace(AddItemListToMediaPool=lambda items: captured.extend(items) or [object(), object()])

    result = import_media_storage_items(storage, [media, MediaStorageItem(media, 1, 5)])

    assert len(result) == 2
    assert captured == [str(media), {"media": str(media), "startFrame": 1, "endFrame": 5}]


class FakeTimeline:
    def __init__(self) -> None:
        self.timecode = "01:00:00:00"
        self.settings: dict[str, str] = {"timelineFrameRate": "24"}
        self.setting_calls: list[tuple[str, str]] = []

    def SetCurrentTimecode(self, value: str) -> bool:
        self.timecode = value
        return True

    def GetCurrentTimecode(self) -> str:
        return self.timecode

    def GetSetting(self, name: str) -> str:
        return self.settings[name]

    def SetSetting(self, name: str, value: str) -> bool:
        self.setting_calls.append((name, value))
        self.settings[name] = value
        return True

    def InsertGeneratorIntoTimeline(self, name: str) -> object:
        return {"name": name}


def test_timeline_playhead_settings_and_generator() -> None:
    timeline = FakeTimeline()
    project = SimpleNamespace(GetCurrentTimeline=lambda: timeline)
    assert get_current_timeline(project) is timeline
    set_current_timecode(timeline, "01:00:01:00")
    assert get_timeline_setting(timeline, "timelineFrameRate") == "24"
    set_timeline_settings(timeline, {"timelineResolutionWidth": "1280"})
    assert timeline.setting_calls == [("useCustomSettings", "1"), ("timelineResolutionWidth", "1280")]
    assert insert_generator(timeline, "Solid Color") == {"name": "Solid Color"}


def test_playhead_verification_can_be_explicitly_disabled() -> None:
    timeline = SimpleNamespace(
        SetCurrentTimecode=lambda value: True,
        GetCurrentTimecode=lambda: "01:00:04:00",
    )
    with pytest.raises(ResolveOperationError):
        set_current_timecode(timeline, "01:00:00:00")
    set_current_timecode(timeline, "01:00:00:00", verify=False)


class FakeRenderProject:
    def __init__(self) -> None:
        self.deleted: list[str] = []
        self.statuses: Iterator[dict[str, object]] = iter([{"JobStatus": "Complete", "CompletionPercentage": 100}])

    def AddRenderJob(self) -> str:
        return "job-1"

    def StartRendering(self, job_id: str) -> bool:
        return job_id == "job-1"

    def GetRenderJobStatus(self, job_id: str) -> dict[str, object]:
        return next(self.statuses)

    def DeleteRenderJob(self, job_id: str) -> bool:
        self.deleted.append(job_id)
        return True

    def GetRenderPresetList(self) -> list[str]:
        return ["Existing"]

    def DeleteRenderPreset(self, name: str) -> bool:
        self.deleted.append(name)
        return True


def test_render_convenience_and_presets(tmp_path: Path) -> None:
    project = FakeRenderProject()
    status = render_current_settings(project, timeout=1, poll_interval=0.001, delete_completed_job=True)
    assert status.state == "Complete"
    assert project.deleted == ["job-1"]
    delete_render_preset(project, "Existing")
    assert project.deleted[-1] == "Existing"

    preset = tmp_path / "NewPreset.xml"
    preset.write_text("preset", encoding="utf-8")
    imported: list[str] = []
    resolve = SimpleNamespace(ImportRenderPreset=lambda path: imported.append(path) or True)
    import_render_preset(resolve, project, preset)
    assert imported == [str(preset)]


def test_fusion_connections_color_font_and_builders(tmp_path: Path) -> None:
    source = FakeTool("Source")
    source.Output = object()
    target = FakeTool("Target")
    connected: list[object] = []
    target.Input = SimpleNamespace(ConnectTo=lambda output: connected.append(output) or True)
    connect_default_output(source, target)
    assert connected == [source.Output]

    merge = FakeTool("Merge1")
    connect_merge(merge, foreground=source)
    assert merge.connections == [("Foreground", source)]
    set_background_color(source, (0.1, 0.2, 0.3, 1.0))
    assert source.values["TopLeftAlpha"] == 1.0
    fusion = SimpleNamespace(FontManager=SimpleNamespace(GetFontList=lambda: {"Noto Sans": {"Regular": object()}}))
    require_fusion_font(fusion, "Noto Sans", "Regular")

    comp = FakeComp()
    transparent = add_transparent_background(comp)
    assert transparent.values["TopLeftAlpha"] == 0.0
    line = build_line(comp, (1.0, 1.0, 1.0, 1.0), 1.0, 0.01)
    assert line.tool_type == "Merge"
    assert line.connections[0][0] == "Foreground"

    lut_root = tmp_path / "LUT"
    dctl = lut_root / "TY_DCTL" / "example.dctl"
    dctl.parent.mkdir(parents=True)
    dctl.write_text("__DEVICE__", encoding="utf-8")
    dctl_tool = add_dctl_tool(comp, "TY_DCTL/example.dctl", lut_root=lut_root, options={"sliderFloatParam0": 0.5})
    assert dctl_tool.values["DCTLs"] == str(Path("TY_DCTL/example.dctl"))


def test_append_fusion_composition_native_and_fixed(tmp_path: Path) -> None:
    native_comp = object()
    native_item = SimpleNamespace(GetFusionCompCount=lambda: 1, GetFusionCompByIndex=lambda index: native_comp)
    timeline = SimpleNamespace(InsertFusionCompositionIntoTimeline=lambda: native_item)
    assert append_fusion_composition(timeline) == (native_item, native_comp)

    dummy = tmp_path / "dummy.mov"
    dummy.write_bytes(b"dummy")
    media_in = FakeTool("MediaIn1")
    comp = FakeComp([media_in])
    fixed_item = SimpleNamespace(AddFusionComp=lambda: comp)
    arguments: list[object] = []
    clip = object()
    pool = SimpleNamespace(
        ImportMedia=lambda items: [clip],
        AppendToTimeline=lambda items: arguments.extend(items) or [fixed_item],
    )

    item, returned_comp = append_fusion_composition(
        timeline,
        duration_frames=24,
        record_frame=100,
        media_pool=pool,
        dummy_media=dummy,
    )
    assert (item, returned_comp) == (fixed_item, comp)
    assert arguments[0]["endFrame"] == 24
    assert media_in.deleted


def test_append_fusion_composition_selects_packaged_media_from_timeline(
    tmp_path: Path,
) -> None:
    dummy = tmp_path / "dummy_video_1280x720_23.976P.mp4"
    dummy.write_bytes(b"dummy")
    settings = {
        "timelineResolutionWidth": "1280",
        "timelineResolutionHeight": "720",
        "timelineFrameRate": "23.976",
    }
    timeline = SimpleNamespace(GetSetting=lambda name: settings[name])
    media_in = FakeTool("MediaIn1")
    comp = FakeComp([media_in])
    fixed_item = SimpleNamespace(AddFusionComp=lambda: comp)
    clip = object()
    imported: list[str] = []
    pool = SimpleNamespace(
        ImportMedia=lambda items: imported.extend(items) or [clip],
        AppendToTimeline=lambda items: [fixed_item],
    )

    with patch(
        "ty_davinci_resolve.fusion.get_packaged_fusion_duration_media",
        return_value=dummy,
    ) as select_media:
        append_fusion_composition(
            timeline,
            duration_frames=24,
            media_pool=pool,
        )

    select_media.assert_called_once_with(1280, 720, "23.976")
    assert imported == [str(dummy)]
    assert media_in.deleted


def test_rcm_workaround_is_version_limited() -> None:
    pages: list[str] = []
    resolve = SimpleNamespace(OpenPage=lambda page: pages.append(page) or True)
    with patch("ty_davinci_resolve.fusion.time.sleep"):
        refresh_fusion_color_management(make_session(resolve), delay=0.01)
    assert pages == ["fusion", "edit"]
    unsupported = ResolveSession(resolve, object(), "Resolve", (21, 1, 0), "21.1.0")
    with pytest.raises(ResolveValidationError):
        refresh_fusion_color_management(unsupported)
