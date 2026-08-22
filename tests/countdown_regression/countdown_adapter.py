"""Test-only adapter from Countdown V2 calls to the redesigned package."""

from __future__ import annotations

from functools import cache
from pathlib import Path
from typing import Any

import ty_davinci_resolve as api


RESOLVE_LUT_PATH = Path(
    r"C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\LUT"
)
LEGACY_VIDEO_PATH = Path(__file__).resolve().parents[3] / "videos"


@cache
def _session() -> api.ResolveSession:
    return api.ResolveSession.connect()


def get_current_project() -> Any:
    """Return the current project through the new package.

    Returns
    -------
    Any
        Resolve Project object.

    Examples
    --------
    >>> get_current_project()  # doctest: +SKIP
    """
    return api.get_current_project(_session())


def get_current_project_or_none() -> Any | None:
    """Return the current project or None when no project is open.

    Returns
    -------
    Any or None
        Resolve Project object or None.

    Examples
    --------
    >>> get_current_project_or_none()  # doctest: +SKIP
    """
    return _session().project_manager.GetCurrentProject()


def close_current_project() -> bool:
    """Close the current project if one exists.

    Returns
    -------
    bool
        True when a project was closed, otherwise False.

    Examples
    --------
    >>> close_current_project()  # doctest: +SKIP
    True
    """
    project = get_current_project_or_none()
    if project is None:
        return False
    api.close_project(_session(), project)
    return True


def delete_project(project_name: str) -> bool:
    """Delete a named project if it exists.

    Parameters
    ----------
    project_name
        Project name.

    Returns
    -------
    bool
        True after the project is absent.

    Examples
    --------
    >>> delete_project("Countdown Test")  # doctest: +SKIP
    True
    """
    if project_name in api.list_projects(_session()):
        api.delete_project(_session(), project_name)
    return True


def create_project(project_name: str) -> Any:
    """Create a named project.

    Parameters
    ----------
    project_name
        New project name.

    Returns
    -------
    Any
        Resolve Project object.

    Examples
    --------
    >>> create_project("Countdown Test")  # doctest: +SKIP
    """
    return api.create_project(_session(), project_name)


def setup_project_settings(params: dict[str, str]) -> bool:
    """Apply project settings using fail-fast new APIs.

    Parameters
    ----------
    params
        Project setting mapping.

    Returns
    -------
    bool
        True after all settings are accepted.

    Examples
    --------
    >>> setup_project_settings({"timelineFrameRate": "24"})  # doctest: +SKIP
    True
    """
    api.set_settings(get_current_project(), params)
    return True


def get_project_setting(name: str) -> str:
    """Return one project setting.

    Parameters
    ----------
    name
        Setting name.

    Returns
    -------
    str
        Setting value.

    Examples
    --------
    >>> get_project_setting("timelineFrameRate")  # doctest: +SKIP
    '23.976'
    """
    return api.get_setting(get_current_project(), name)


def get_project_resolution() -> list[int]:
    """Return current project width and height.

    Returns
    -------
    list of int
        Width and height.

    Examples
    --------
    >>> get_project_resolution()  # doctest: +SKIP
    [1280, 720]
    """
    return list(api.get_timeline_resolution(get_current_project()))


def make_videoMonitorFormat_str(width: int | str, height: int | str, framerate: float) -> str:
    """Build the legacy Resolve monitor-format setting.

    Parameters
    ----------
    width
        Timeline width.
    height
        Timeline height.
    framerate
        Timeline frame rate.

    Returns
    -------
    str
        Resolve monitor format string.

    Examples
    --------
    >>> make_videoMonitorFormat_str(1280, 720, 23.976)
    'HD 720p 23.976'
    """
    return api.make_video_monitor_format(width, height, framerate)


def refresh_lut_list() -> bool:
    """Refresh the current project's LUT list.

    Returns
    -------
    bool
        True after success.

    Examples
    --------
    >>> refresh_lut_list()  # doctest: +SKIP
    True
    """
    api.refresh_lut_list(get_current_project())
    return True


def create_empty_timeline(name: str = "timeline_x") -> Any:
    """Create an empty timeline in the current project.

    Parameters
    ----------
    name
        Timeline name.

    Returns
    -------
    Any
        Resolve Timeline object.

    Examples
    --------
    >>> create_empty_timeline("Main")  # doctest: +SKIP
    """
    return api.create_empty_timeline(api.get_media_pool(get_current_project()), name)


def get_current_timeline() -> Any:
    """Return the current timeline.

    Returns
    -------
    Any
        Resolve Timeline object.

    Examples
    --------
    >>> get_current_timeline()  # doctest: +SKIP
    """
    return api.get_current_timeline(get_current_project())


def add_file_to_media_pool(file_path: str, start_frame: int | None = None, end_frame: int | None = None) -> Any:
    """Import one file into the current Media Pool folder.

    Parameters
    ----------
    file_path
        Absolute existing media path.
    start_frame
        Optional source start frame.
    end_frame
        Optional source end frame.

    Returns
    -------
    Any
        Resolve MediaPoolItem object.

    Examples
    --------
    >>> add_file_to_media_pool("C:/media/audio.wav")  # doctest: +SKIP
    """
    if start_frame is not None or end_frame is not None:
        raise api.ResolveValidationError(
            "Countdown adapter does not use ranged MediaStorage imports."
        )
    pool = api.get_media_pool(get_current_project())
    return api.import_files(pool, [file_path])[0]


def append_clip_to_timeline(
    clip: Any,
    pos_frame_idx: float | None = None,
    start_frame: float | None = None,
    end_frame: float | None = None,
    media_type: int | None = None,
    track_index: int = 1,
) -> Any:
    """Append one clip using the new timeline API.

    Parameters
    ----------
    clip
        Resolve MediaPoolItem object.
    pos_frame_idx
        Destination record frame.
    start_frame
        Optional source start frame.
    end_frame
        Optional source end frame.
    media_type
        Optional video-only or audio-only selector.
    track_index
        One-based target track index.

    Returns
    -------
    Any
        Resolve TimelineItem object.

    Examples
    --------
    >>> append_clip_to_timeline(clip, media_type=1)  # doctest: +SKIP
    """
    return api.append_clip(
        api.get_media_pool(get_current_project()),
        clip,
        record_frame=pos_frame_idx,
        start_frame=start_frame,
        end_frame=end_frame,
        media_type=media_type,
        track_index=track_index,
    )


def append_fusion_composition_to_timeline(
    num_of_frame: float,
    pos_frame_idx: float | None = None,
) -> tuple[Any, Any]:
    """Create a fixed-length Fusion clip using the legacy dummy media asset.

    Parameters
    ----------
    num_of_frame
        Source end frame used by the reference workflow.
    pos_frame_idx
        Destination record frame.

    Returns
    -------
    tuple
        Timeline item and Fusion composition.

    Notes
    -----
    The dummy-media route is retained only because the reference output depends
    on its exact duration behavior.

    Examples
    --------
    >>> append_fusion_composition_to_timeline(24, 86400)  # doctest: +SKIP
    """
    fps_value = float(get_project_setting("timelineFrameRate"))
    fps_text = str(int(fps_value)) if fps_value.is_integer() else str(fps_value)
    width, height = get_project_resolution()
    dummy = LEGACY_VIDEO_PATH / f"dummy_video_{width}x{height}_{fps_text}P.mp4"
    return api.append_fusion_composition(
        get_current_timeline(),
        duration_frames=num_of_frame,
        record_frame=pos_frame_idx,
        media_pool=api.get_media_pool(get_current_project()),
        dummy_media=dummy.resolve(),
    )


def sec_to_frame_idx(sec: float) -> float:
    """Convert seconds using the project's nominal integer frame rate.

    Parameters
    ----------
    sec
        Seconds.

    Returns
    -------
    float
        Frame position used by the reference workflow.

    Examples
    --------
    >>> sec_to_frame_idx(1)  # doctest: +SKIP
    24
    """
    nominal_fps = int(round(float(get_project_setting("timelineFrameRate"))))
    return nominal_fps * sec


def timecode_to_frame_index(timecode: str, fps_float: float) -> int:
    """Convert non-drop timecode through the new package.

    Parameters
    ----------
    timecode
        ``HH:MM:SS:FF`` timecode.
    fps_float
        Frame rate.

    Returns
    -------
    int
        Frame index.

    Examples
    --------
    >>> timecode_to_frame_index("01:00:00:00", 24)
    86400
    """
    return api.timecode_to_frames(timecode, fps_float)


def set_current_timecode(timecode: str) -> bool:
    """Set the current timeline playhead.

    Parameters
    ----------
    timecode
        ``HH:MM:SS:FF`` timecode.

    Returns
    -------
    bool
        True after success.

    Examples
    --------
    >>> set_current_timecode("01:00:00:00")  # doctest: +SKIP
    True
    """
    api.set_current_timecode(get_current_timeline(), timecode, verify=False)
    return True


def get_timeline_items_in_track(timeline: Any, track_type: str = "video", track_idx: int = 1) -> list[Any]:
    """Return timeline items in a validated track.

    Parameters
    ----------
    timeline
        Resolve Timeline object.
    track_type
        Track type.
    track_idx
        One-based track index.

    Returns
    -------
    list of Any
        Timeline items.

    Examples
    --------
    >>> get_timeline_items_in_track(timeline)  # doctest: +SKIP
    """
    return list(api.get_track_items(timeline, track_type, track_idx))


def open_page(page_name: str = "edit") -> bool:
    """Open a Resolve page.

    Parameters
    ----------
    page_name
        Resolve page identifier.

    Returns
    -------
    bool
        True after success.

    Examples
    --------
    >>> open_page("fusion")  # doctest: +SKIP
    True
    """
    api.open_page(_session(), page_name)
    return True


def force_rcm_update_via_page_switch() -> None:
    """Apply the reference workflow's Fusion-to-Edit RCM workaround.

    Returns
    -------
    None

    Examples
    --------
    >>> force_rcm_update_via_page_switch()  # doctest: +SKIP
    """
    api.refresh_fusion_color_management(_session())


def set_render_format_codec_settings(format: str, codec: str) -> bool:
    """Select a host-validated render format and codec.

    Parameters
    ----------
    format
        Render format identifier.
    codec
        Codec identifier.

    Returns
    -------
    bool
        True after success.

    Examples
    --------
    >>> set_render_format_codec_settings("png", "RGB16")  # doctest: +SKIP
    True
    """
    api.set_render_format_codec(get_current_project(), format, codec)
    return True


def set_render_settings(setting_dict: dict[str, Any]) -> bool:
    """Apply render settings.

    Parameters
    ----------
    setting_dict
        Render setting mapping.

    Returns
    -------
    bool
        True after success.

    Examples
    --------
    >>> set_render_settings({"TargetDir": "C:/output"})  # doctest: +SKIP
    True
    """
    api.set_render_settings(get_current_project(), setting_dict)
    return True


def run_rendering_and_wait_until_finish(project: Any) -> None:
    """Render and delete only the job created by this call.

    Parameters
    ----------
    project
        Resolve Project object.

    Returns
    -------
    None

    Examples
    --------
    >>> run_rendering_and_wait_until_finish(project)  # doctest: +SKIP
    """
    api.render_current_settings(
        project,
        timeout=3600,
        poll_interval=0.5,
        delete_completed_job=True,
    )


def import_render_preset(preset_path: str) -> bool:
    """Import an existing Resolve render preset.

    Parameters
    ----------
    preset_path
        Absolute preset path.

    Returns
    -------
    bool
        True after success.

    Examples
    --------
    >>> import_render_preset("C:/preset.xml")  # doctest: +SKIP
    True
    """
    api.import_render_preset(
        _session().resolve,
        get_current_project(),
        preset_path,
    )
    return True


def get_comp_tool_by_name(comp: Any, name: str) -> Any:
    """Return a Fusion tool by name.

    Parameters
    ----------
    comp
        Fusion Composition object.
    name
        Tool instance name.

    Returns
    -------
    Any
        Fusion Tool object.

    Examples
    --------
    >>> get_comp_tool_by_name(comp, "MediaOut1")  # doctest: +SKIP
    """
    return api.get_tool(comp, name)


def add_comp_tool(comp: Any, name: str, pos: tuple[float, float] | list[float] = (2, 3)) -> Any:
    """Add a Fusion tool.

    Parameters
    ----------
    comp
        Fusion Composition object.
    name
        Fusion tool type.
    pos
        Flow-view position.

    Returns
    -------
    Any
        Fusion Tool object.

    Examples
    --------
    >>> add_comp_tool(comp, "Background")  # doctest: +SKIP
    """
    return api.add_tool(comp, name, pos)


def connect_tool(a: Any, b: Any) -> bool:
    """Connect a tool's default output to another tool's default input.

    Parameters
    ----------
    a
        Source tool.
    b
        Target tool.

    Returns
    -------
    bool
        True after success.

    Examples
    --------
    >>> connect_tool(source, target)  # doctest: +SKIP
    True
    """
    api.connect_default_output(a, b)
    return True


def connect_mediaout(mediaout: Any, source: Any) -> bool:
    """Connect a source tool to MediaOut.

    Parameters
    ----------
    mediaout
        MediaOut tool.
    source
        Source tool.

    Returns
    -------
    bool
        True after success.

    Examples
    --------
    >>> connect_mediaout(mediaout, source)  # doctest: +SKIP
    True
    """
    api.connect_input(mediaout, "Input", source)
    return True


def connect_dctl(dctl: Any, source: Any) -> bool:
    """Connect a source tool to a DCTL source input.

    Parameters
    ----------
    dctl
        DCTL tool.
    source
        Source tool.

    Returns
    -------
    bool
        True after success.

    Examples
    --------
    >>> connect_dctl(dctl, source)  # doctest: +SKIP
    True
    """
    api.connect_input(dctl, "Source", source)
    return True


def connect_merge_tool(merge_tool: Any, bg_tool: Any | None, fg_tool: Any | None) -> None:
    """Connect optional background and foreground Merge inputs.

    Parameters
    ----------
    merge_tool
        Merge tool.
    bg_tool
        Optional background source.
    fg_tool
        Optional foreground source.

    Returns
    -------
    None

    Examples
    --------
    >>> connect_merge_tool(merge, background, foreground)  # doctest: +SKIP
    """
    api.connect_merge(
        merge_tool,
        background=bg_tool,
        foreground=fg_tool,
    )


def set_tool_input(tool: Any, name: str, value: Any) -> bool:
    """Set and verify one Fusion input.

    Parameters
    ----------
    tool
        Fusion Tool object.
    name
        Input name.
    value
        Input value.

    Returns
    -------
    bool
        True after verification.

    Examples
    --------
    >>> set_tool_input(tool, "Gain", 1.0)  # doctest: +SKIP
    True
    """
    api.set_tool_input(tool, name, value)
    return True


def _assert_font_available(family: str, style: str) -> None:
    api.require_fusion_font(_session().fusion, family, style)


def set_multiple_tool_input(tool: Any, input_dict: dict[str, Any]) -> None:
    """Set and verify multiple Fusion inputs.

    Parameters
    ----------
    tool
        Fusion Tool object.
    input_dict
        Input mapping.

    Returns
    -------
    None

    Examples
    --------
    >>> set_multiple_tool_input(tool, {"Gain": 1.0})  # doctest: +SKIP
    """
    if "Font" in input_dict and "Style" in input_dict:
        _assert_font_available(input_dict["Font"], input_dict["Style"])
    api.set_tool_inputs(tool, input_dict)


def set_tool_topleft_color(tool: Any, rgba: list[float] | tuple[float, ...] = (0.18, 0.18, 0.18, 1.0)) -> bool:
    """Set a Background tool's top-left RGBA color.

    Parameters
    ----------
    tool
        Background tool.
    rgba
        Four channel values.

    Returns
    -------
    bool
        True after verification.

    Examples
    --------
    >>> set_tool_topleft_color(tool, [0, 0, 0, 1])  # doctest: +SKIP
    True
    """
    api.set_background_color(tool, rgba)
    return True


def set_tool_position(comp: Any, tool: Any, pos: tuple[float, float] | list[float] = (1, 1)) -> bool:
    """Set and verify a Fusion tool position.

    Parameters
    ----------
    comp
        Fusion Composition object.
    tool
        Fusion Tool object.
    pos
        Flow-view position.

    Returns
    -------
    bool
        True after verification.

    Examples
    --------
    >>> set_tool_position(comp, tool, (1, 2))  # doctest: +SKIP
    True
    """
    if comp.CurrentFrame is None:
        open_page("fusion")
    api.set_tool_position(comp, tool, pos)
    return True


def add_dctl_comp(
    comp: Any,
    dctl_path: str,
    option: dict[str, Any] | None = None,
    base_pos: list[float] | tuple[float, float] = (0, 0),
) -> Any:
    """Add and configure a Resolve DCTL Fusion tool.

    Parameters
    ----------
    comp
        Fusion Composition object.
    dctl_path
        Path relative to Resolve's LUT directory.
    option
        Optional DCTL parameter mapping.
    base_pos
        Flow-view position.

    Returns
    -------
    Any
        Configured DCTL tool.

    Examples
    --------
    >>> add_dctl_comp(comp, "TY_DCTL/draw_countdown_ramp.dctl")  # doctest: +SKIP
    """
    return api.add_dctl_tool(
        comp,
        dctl_path,
        lut_root=RESOLVE_LUT_PATH,
        options=option,
        position=base_pos,
    )


def add_transparent_background(comp: Any, pos: list[float] | tuple[float, float]) -> Any:
    """Create a transparent Fusion Background tool.

    Parameters
    ----------
    comp
        Fusion Composition object.
    pos
        Flow-view position.

    Returns
    -------
    Any
        Background tool.

    Examples
    --------
    >>> add_transparent_background(comp, (0, 0))  # doctest: +SKIP
    """
    return api.add_transparent_background(comp, pos)


def add_line_comp(
    comp: Any,
    rgba: list[float] | tuple[float, ...],
    width: float,
    height: float,
    angle: float = 0,
    pos: list[float] | tuple[float, float] = (0, 0),
    connect_fg: bool = True,
    center: dict[int, float] | None = None,
) -> Any:
    """Build the Countdown script's masked line tool group.

    Parameters
    ----------
    comp
        Fusion Composition object.
    rgba
        Line color.
    width
        Rectangle width.
    height
        Rectangle height.
    angle
        Rectangle angle.
    pos
        Base flow-view position.
    connect_fg
        Connect the line as foreground when True.
    center
        Optional Fusion center mapping.

    Returns
    -------
    Any
        Output Merge tool.

    Examples
    --------
    >>> add_line_comp(comp, [1, 1, 1, 1], 1, 0.01)  # doctest: +SKIP
    """
    center_value = (
        (center[1], center[2]) if center is not None else (0.5, 0.5)
    )
    return api.build_line(
        comp,
        rgba,
        width,
        height,
        angle=angle,
        position=pos,
        connect_as_foreground=connect_fg,
        center=center_value,
    )
