"""Small helpers for Resolve-hosted Fusion compositions and tools."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from decimal import Decimal, InvalidOperation
import math
from pathlib import Path
import time
from types import MappingProxyType
from typing import Any

from .connection import ResolveSession, open_page
from .constants import Page, SUPPORTED_RESOLVE_VERSION
from .errors import ResolveOperationError, ResolveValidationError
from .media import import_files
from .timeline import (
    MediaType,
    append_clip,
    get_timeline_setting,
    insert_fusion_composition,
)


PACKAGED_DURATION_MEDIA_DIRECTORY = (
    Path(__file__).resolve().parent / "assets" / "duration_media"
)


def add_comp(timeline_item: Any) -> Any:
    """Add a Fusion composition to a timeline item.

    Parameters
    ----------
    timeline_item
        Resolve TimelineItem remote object.

    Returns
    -------
    Any
        Fusion Composition remote object.

    Examples
    --------
    >>> add_comp(timeline_item)  # doctest: +SKIP
    """
    if timeline_item is None:
        raise ResolveValidationError("timeline_item must not be None.")
    comp = timeline_item.AddFusionComp()
    if comp is None:
        raise ResolveOperationError("TimelineItem.AddFusionComp", comp)
    return comp


def get_tool(comp: Any, name: str) -> Any:
    """Find a Fusion tool by its instance name.

    Parameters
    ----------
    comp
        Fusion Composition remote object.
    name
        Tool instance name, such as ``MediaOut1``.

    Returns
    -------
    Any
        Fusion Tool remote object.

    Examples
    --------
    >>> get_tool(comp, "MediaOut1")  # doctest: +SKIP
    """
    if not isinstance(name, str) or not name:
        raise ResolveValidationError("name must be a non-empty string.")
    tools = comp.GetToolList()
    if not isinstance(tools, dict):
        raise ResolveOperationError("Composition.GetToolList", tools)
    for tool in tools.values():
        if getattr(tool, "Name", None) == name:
            return tool
    raise ResolveOperationError(
        "Composition.GetToolList", tools, f"Fusion tool was not found: {name!r}."
    )


def add_tool(
    comp: Any,
    tool_type: str,
    position: Sequence[float] = (0.0, 0.0),
) -> Any:
    """Add a Fusion tool at a flow-view position.

    Parameters
    ----------
    comp
        Fusion Composition remote object.
    tool_type
        Fusion tool type, such as ``Background`` or ``Merge``.
    position
        Two-element flow-view position.

    Returns
    -------
    Any
        Created Fusion Tool remote object.

    Examples
    --------
    >>> add_tool(comp, "Background", (1, 2))  # doctest: +SKIP
    """
    if not isinstance(tool_type, str) or not tool_type:
        raise ResolveValidationError("tool_type must be a non-empty string.")
    if len(position) != 2 or not all(
        isinstance(value, (int, float)) and math.isfinite(value) for value in position
    ):
        raise ResolveValidationError("position must contain two finite numbers.")
    tool = comp.AddTool(tool_type, position[0], position[1])
    if tool is None:
        raise ResolveOperationError("Composition.AddTool", tool)
    return tool


def connect_input(target: Any, input_name: str, source: Any) -> None:
    """Connect a source tool to a named target input.

    Parameters
    ----------
    target
        Target Fusion Tool remote object.
    input_name
        Target input name.
    source
        Source Fusion Tool remote object.

    Returns
    -------
    None

    Examples
    --------
    >>> connect_input(media_out, "Input", background)  # doctest: +SKIP
    """
    if not isinstance(input_name, str) or not input_name:
        raise ResolveValidationError("input_name must be a non-empty string.")
    if target is None or source is None:
        raise ResolveValidationError("target and source must not be None.")
    result = target.ConnectInput(input_name, source)
    if result is not True:
        raise ResolveOperationError("Tool.ConnectInput", result)


def connect_default_output(source: Any, target: Any) -> None:
    """Connect a source's default output to a target's default input.

    Parameters
    ----------
    source
        Source Fusion Tool remote object.
    target
        Target Fusion Tool remote object.

    Returns
    -------
    None

    Examples
    --------
    >>> connect_default_output(background, merge)  # doctest: +SKIP
    """
    if source is None or target is None:
        raise ResolveValidationError("source and target must not be None.")
    try:
        result = target.Input.ConnectTo(source.Output)
    except AttributeError as error:
        raise ResolveValidationError("source and target must expose default Output and Input connectors.") from error
    if result is not True:
        raise ResolveOperationError("Input.ConnectTo", result)


def connect_merge(
    merge: Any,
    *,
    background: Any | None = None,
    foreground: Any | None = None,
) -> None:
    """Connect the supplied inputs to a Fusion Merge tool.

    Parameters
    ----------
    merge
        Target Merge Tool remote object.
    background
        Optional background source.
    foreground
        Optional foreground source.

    Returns
    -------
    None

    Examples
    --------
    >>> connect_merge(merge, foreground=title)  # doctest: +SKIP
    """
    if background is None and foreground is None:
        raise ResolveValidationError("background or foreground must be provided.")
    if background is not None:
        connect_input(merge, "Background", background)
    if foreground is not None:
        connect_input(merge, "Foreground", foreground)


def set_tool_input(
    tool: Any,
    name: str,
    value: Any,
    *,
    tolerance: float = 1e-6,
) -> None:
    """Set and verify a Fusion tool input value.

    Parameters
    ----------
    tool
        Fusion Tool remote object.
    name
        Input name.
    value
        Input value accepted by Fusion.
    tolerance
        Absolute verification tolerance for floating-point values.

    Returns
    -------
    None

    Notes
    -----
    BlackmagicFusion remote objects are accepted without equality comparison.

    Examples
    --------
    >>> set_tool_input(background, "TopLeftRed", 0.18)  # doctest: +SKIP
    """
    if not isinstance(name, str) or not name:
        raise ResolveValidationError("name must be a non-empty string.")
    if not isinstance(tolerance, (int, float)) or tolerance < 0:
        raise ResolveValidationError("tolerance must be non-negative.")
    tool.SetInput(name, value)
    actual = tool.GetInput(name)
    is_remote = (
        type(value).__module__ == "BlackmagicFusion"
        or type(value).__name__ == "PyRemoteObject"
    )
    if is_remote:
        return
    if isinstance(value, float):
        matches = isinstance(actual, (int, float)) and math.isclose(
            value, actual, rel_tol=0.0, abs_tol=tolerance
        )
    else:
        matches = value == actual
    if not matches:
        raise ResolveOperationError(
            "Tool.SetInput",
            actual,
            f"Fusion input {name!r} verification failed: "
            f"expected {value!r}, got {actual!r}.",
        )


def set_tool_inputs(tool: Any, values: Mapping[str, Any]) -> None:
    """Set and verify multiple Fusion tool inputs in mapping order.

    Parameters
    ----------
    tool
        Fusion Tool remote object.
    values
        Non-empty mapping of input names to values.

    Returns
    -------
    None

    Notes
    -----
    Processing stops at the first failed verification.

    Examples
    --------
    >>> set_tool_inputs(background, {"TopLeftRed": 0.18})  # doctest: +SKIP
    """
    if not isinstance(values, Mapping) or not values:
        raise ResolveValidationError("values must be a non-empty mapping.")
    for name, value in values.items():
        set_tool_input(tool, name, value)


def set_tool_position(
    comp: Any,
    tool: Any,
    position: Sequence[float],
    *,
    tolerance: float = 0.1,
    session: ResolveSession | None = None,
    activate_fusion_page: bool = False,
) -> None:
    """Set and verify a Fusion tool's flow-view position.

    Parameters
    ----------
    comp
        Fusion Composition remote object.
    tool
        Fusion Tool remote object.
    position
        Two-element flow-view position.
    tolerance
        Absolute position verification tolerance.
    session
        Resolve session used only when Fusion page activation is required.
    activate_fusion_page
        Allow switching to the Fusion page when ``CurrentFrame`` is unavailable.

    Returns
    -------
    None

    Examples
    --------
    >>> set_tool_position(comp, background, (1, 2))  # doctest: +SKIP
    """
    if len(position) != 2 or not all(
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        for value in position
    ):
        raise ResolveValidationError("position must contain two finite numbers.")
    if (
        isinstance(tolerance, bool)
        or not isinstance(tolerance, (int, float))
        or not math.isfinite(tolerance)
        or tolerance < 0
    ):
        raise ResolveValidationError("tolerance must be a non-negative finite number.")
    if not isinstance(activate_fusion_page, bool):
        raise ResolveValidationError("activate_fusion_page must be a bool.")
    current_frame = comp.CurrentFrame
    if current_frame is None:
        if not activate_fusion_page:
            raise ResolveOperationError(
                "Composition.CurrentFrame",
                current_frame,
                "Fusion CurrentFrame is unavailable; pass a session and "
                "activate_fusion_page=True to permit a page switch.",
            )
        if not isinstance(session, ResolveSession):
            raise ResolveValidationError(
                "session is required when activate_fusion_page is True."
            )
        open_page(session, Page.FUSION)
        current_frame = comp.CurrentFrame
        if current_frame is None:
            raise ResolveOperationError(
                "Composition.CurrentFrame",
                current_frame,
                "Fusion CurrentFrame remained unavailable after opening the Fusion page.",
            )
    flow = current_frame.FlowView
    flow.SetPos(tool, position[0], position[1])
    actual = tuple(flow.GetPosTable(tool).values())
    if len(actual) < 2 or not all(
        math.isclose(float(expected), float(observed), rel_tol=0.0, abs_tol=tolerance)
        for expected, observed in zip(position, actual)
    ):
        raise ResolveOperationError(
            "FlowView.SetPos",
            actual,
            f"Fusion tool position verification failed: expected {tuple(position)!r}, "
            f"got {actual!r}.",
        )


def set_background_color(tool: Any, rgba: Sequence[float]) -> None:
    """Set and verify a Fusion Background tool's RGBA color.

    Parameters
    ----------
    tool
        Fusion Background Tool remote object.
    rgba
        Four finite red, green, blue, and alpha values.

    Returns
    -------
    None

    Examples
    --------
    >>> set_background_color(background, (0.0, 0.0, 0.0, 1.0))  # doctest: +SKIP
    """
    if len(rgba) != 4 or not all(isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) for value in rgba):
        raise ResolveValidationError("rgba must contain four finite numbers.")
    values = {f"TopLeft{channel}": value for channel, value in zip(("Red", "Green", "Blue", "Alpha"), rgba)}
    set_tool_inputs(tool, values)


def get_fusion_fonts(fusion: Any) -> Mapping[str, tuple[str, ...]]:
    """Return Fusion fonts as an immutable normalized mapping.

    Parameters
    ----------
    fusion
        Fusion application remote object.

    Returns
    -------
    Mapping of str to tuple of str
        Read-only family-to-style mapping sorted by family and style.

    Examples
    --------
    >>> fonts = get_fusion_fonts(session.fusion)  # doctest: +SKIP
    >>> fonts["Noto Sans"]  # doctest: +SKIP
    ('Regular',)
    """
    try:
        raw_fonts = fusion.FontManager.GetFontList()
    except AttributeError as error:
        raise ResolveOperationError(
            "Fusion.FontManager.GetFontList", None
        ) from error
    if not isinstance(raw_fonts, Mapping):
        raise ResolveOperationError("Fusion.FontManager.GetFontList", raw_fonts)
    normalized: dict[str, tuple[str, ...]] = {}
    for family, raw_styles in raw_fonts.items():
        if not isinstance(family, str) or not family:
            raise ResolveOperationError(
                "Fusion.FontManager.GetFontList",
                raw_fonts,
                f"Fusion returned an invalid font family: {family!r}.",
            )
        if isinstance(raw_styles, Mapping):
            styles = tuple(raw_styles.keys())
        elif isinstance(raw_styles, Sequence) and not isinstance(
            raw_styles, (str, bytes)
        ):
            styles = tuple(raw_styles)
        else:
            raise ResolveOperationError(
                "Fusion.FontManager.GetFontList",
                raw_fonts,
                f"Fusion returned invalid styles for {family!r}: {raw_styles!r}.",
            )
        if not styles or not all(isinstance(style, str) and style for style in styles):
            raise ResolveOperationError(
                "Fusion.FontManager.GetFontList",
                raw_fonts,
                f"Fusion returned invalid styles for {family!r}: {styles!r}.",
            )
        normalized[family] = tuple(sorted(set(styles)))
    return MappingProxyType(dict(sorted(normalized.items())))


def require_fusion_font(fusion: Any, family: str, style: str) -> None:
    """Require a Fusion font family and style before tool creation.

    Parameters
    ----------
    fusion
        Fusion application remote object.
    family
        Font family name.
    style
        Font style name.

    Returns
    -------
    None

    Examples
    --------
    >>> require_fusion_font(session.fusion, "Noto Sans", "Regular")  # doctest: +SKIP
    """
    if not isinstance(family, str) or not family.strip() or not isinstance(style, str) or not style.strip():
        raise ResolveValidationError("family and style must be non-empty strings.")
    fonts = get_fusion_fonts(fusion)
    if family not in fonts or style not in fonts[family]:
        raise ResolveValidationError(f"Required Fusion font is unavailable: {family} {style}.")


def add_dctl_tool(
    comp: Any,
    dctl_path: str | Path,
    *,
    lut_root: str | Path,
    options: Mapping[str, Any] | None = None,
    position: Sequence[float] = (0.0, 0.0),
) -> Any:
    """Add and configure a Resolve DCTL Fusion tool.

    Parameters
    ----------
    comp
        Fusion Composition remote object.
    dctl_path
        DCTL path relative to ``lut_root``.
    lut_root
        Resolve LUT root directory.
    options
        Optional DCTL input mapping.
    position
        Two-element flow-view position.

    Returns
    -------
    Any
        Configured DCTL Tool remote object.

    Examples
    --------
    >>> add_dctl_tool(comp, "TY_DCTL/example.dctl", lut_root="C:/ProgramData/Resolve/LUT")  # doctest: +SKIP
    """
    relative_path = Path(dctl_path)
    root = Path(lut_root).expanduser()
    if relative_path.is_absolute() or not relative_path.parts or ".." in relative_path.parts:
        raise ResolveValidationError("dctl_path must be a path below lut_root.")
    if not root.is_absolute() or not root.is_dir():
        raise ResolveValidationError(f"LUT root does not exist: {root}.")
    target = root / relative_path
    if not target.is_file():
        raise ResolveValidationError(f"DCTL file does not exist: {target}.")
    if options is not None and not isinstance(options, Mapping):
        raise ResolveValidationError("options must be a mapping or None.")
    tool = add_tool(comp, "ofx.com.blackmagicdesign.resolvefx.DCTL", position)
    values: dict[str, Any] = {"DCTLs": str(relative_path), "reloadDCTLButton": 1.0}
    if options:
        values.update(options)
    set_tool_inputs(tool, values)
    return tool


def add_transparent_background(
    comp: Any,
    position: Sequence[float] = (0.0, 0.0),
) -> Any:
    """Add a fully transparent Fusion Background tool.

    Parameters
    ----------
    comp
        Fusion Composition remote object.
    position
        Two-element flow-view position.

    Returns
    -------
    Any
        Created Background Tool remote object.

    Examples
    --------
    >>> add_transparent_background(comp, (0, 0))  # doctest: +SKIP
    """
    tool = add_tool(comp, "Background", position)
    set_background_color(tool, (0.0, 0.0, 0.0, 0.0))
    return tool


def _build_masked_background(
    comp: Any,
    rgba: Sequence[float],
    mask_inputs: Mapping[str, Any],
    *,
    mask_position: Sequence[float],
    background_position: Sequence[float],
) -> Any:
    mask = add_tool(comp, "RectangleMask", mask_position)
    background = add_tool(comp, "Background", background_position)
    set_tool_inputs(mask, mask_inputs)
    set_background_color(background, rgba)
    set_tool_input(background, "EffectMask", mask)
    return background


def build_rectangle(
    comp: Any,
    rgba: Sequence[float] = (1.0, 1.0, 1.0, 1.0),
    *,
    center: Sequence[float] = (0.5, 0.5),
    width: float = 0.1,
    height: float = 0.1,
    position: Sequence[float] = (0.0, 0.0),
) -> Any:
    """Build a masked Fusion Background representing a rectangle.

    Parameters
    ----------
    comp
        Fusion Composition remote object.
    rgba
        Four finite rectangle color values.
    center
        Two finite normalized center coordinates.
    width
        Positive RectangleMask width.
    height
        Positive RectangleMask height.
    position
        Background flow-view position; the mask is placed one row above it.

    Returns
    -------
    Any
        Created Background Tool remote object.

    Examples
    --------
    >>> build_rectangle(comp, width=0.2, height=0.1)  # doctest: +SKIP
    """
    for value, name in ((width, "width"), (height, "height")):
        if (
            isinstance(value, bool)
            or not isinstance(value, (int, float))
            or not math.isfinite(value)
            or value <= 0
        ):
            raise ResolveValidationError(
                f"{name} must be a positive finite number."
            )
    if len(center) != 2 or not all(
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        for value in center
    ):
        raise ResolveValidationError("center must contain two finite numbers.")
    if len(position) != 2 or not all(
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        for value in position
    ):
        raise ResolveValidationError("position must contain two finite numbers.")
    x, y = position
    return _build_masked_background(
        comp,
        rgba,
        {
            "Center": {1: center[0], 2: center[1], 3: 0.0},
            "Width": width,
            "Height": height,
        },
        mask_position=(x, y - 1),
        background_position=(x, y),
    )


def build_line(
    comp: Any,
    rgba: Sequence[float],
    width: float,
    height: float,
    *,
    angle: float = 0.0,
    position: Sequence[float] = (0.0, 0.0),
    connect_as_foreground: bool = True,
    center: Sequence[float] = (0.5, 0.5),
) -> Any:
    """Build a masked Background and Merge representing a line.

    Parameters
    ----------
    comp
        Fusion Composition remote object.
    rgba
        Four finite line color values.
    width
        Positive RectangleMask width.
    height
        Positive RectangleMask height.
    angle
        Finite RectangleMask angle.
    position
        Base flow-view position.
    connect_as_foreground
        Connect the line to Foreground instead of Background.
    center
        Two finite normalized center coordinates.

    Returns
    -------
    Any
        Created Merge Tool remote object.

    Examples
    --------
    >>> build_line(comp, (1, 1, 1, 1), 1.0, 0.01)  # doctest: +SKIP
    """
    for value, name in ((width, "width"), (height, "height")):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0:
            raise ResolveValidationError(f"{name} must be a positive finite number.")
    if isinstance(angle, bool) or not isinstance(angle, (int, float)) or not math.isfinite(angle):
        raise ResolveValidationError("angle must be a finite number.")
    if not isinstance(connect_as_foreground, bool):
        raise ResolveValidationError("connect_as_foreground must be a bool.")
    if len(center) != 2 or not all(isinstance(value, (int, float)) and math.isfinite(value) for value in center):
        raise ResolveValidationError("center must contain two finite numbers.")
    if len(position) != 2:
        raise ResolveValidationError("position must contain two numbers.")
    x, y = position
    foreground = _build_masked_background(
        comp,
        rgba,
        {
            "Width": width,
            "Height": height,
            "Angle": angle,
            "Center": {1: center[0], 2: center[1], 3: 0.0},
        },
        mask_position=(x, y - 2),
        background_position=(x, y - 1),
    )
    merge = add_tool(comp, "Merge", (x, y))
    if connect_as_foreground:
        connect_merge(merge, foreground=foreground)
    else:
        connect_merge(merge, background=foreground)
    return merge


def select_fusion_duration_media(
    directory: str | Path,
    width: int,
    height: int,
    frame_rate: int | float | str,
    *,
    prefix: str = "dummy_video",
    extension: str = ".mp4",
) -> Path:
    """Select caller-owned dummy media by resolution and frame rate.

    Parameters
    ----------
    directory
        Absolute directory containing duration media files.
    width
        Positive frame width.
    height
        Positive frame height.
    frame_rate
        Positive finite frame rate used in the filename.
    prefix
        Filename prefix without path separators.
    extension
        Filename extension including the leading dot.

    Returns
    -------
    pathlib.Path
        Existing absolute media path.

    Notes
    -----
    The expected filename is
    ``{prefix}_{width}x{height}_{frame_rate}P{extension}``.

    Examples
    --------
    >>> select_fusion_duration_media(Path("C:/media"), 1280, 720, 23.976)  # doctest: +SKIP
    WindowsPath('C:/media/dummy_video_1280x720_23.976P.mp4')
    """
    root = Path(directory).expanduser()
    if not root.is_absolute() or not root.is_dir():
        raise ResolveValidationError(
            f"duration media directory does not exist: {root}."
        )
    for value, name in ((width, "width"), (height, "height")):
        if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
            raise ResolveValidationError(f"{name} must be a positive integer.")
    if (
        not isinstance(prefix, str)
        or not prefix
        or Path(prefix).name != prefix
        or not isinstance(extension, str)
        or not extension.startswith(".")
        or Path(extension).name != extension
    ):
        raise ResolveValidationError(
            "prefix and extension must be filename components."
        )
    try:
        rate = Decimal(str(frame_rate))
    except (InvalidOperation, ValueError) as error:
        raise ResolveValidationError(
            "frame_rate must be a positive finite number."
        ) from error
    if not rate.is_finite() or rate <= 0:
        raise ResolveValidationError(
            "frame_rate must be a positive finite number."
        )
    rate_text = format(rate.normalize(), "f")
    candidate = root / f"{prefix}_{width}x{height}_{rate_text}P{extension}"
    if not candidate.is_file():
        raise ResolveValidationError(
            f"Fusion duration media does not exist: {candidate}."
        )
    return candidate


def get_packaged_fusion_duration_media(
    width: int,
    height: int,
    frame_rate: int | float | str,
) -> Path:
    """Return packaged dummy media for a timeline format.

    Parameters
    ----------
    width
        Positive frame width.
    height
        Positive frame height.
    frame_rate
        Positive finite frame rate used in the filename.

    Returns
    -------
    pathlib.Path
        Existing absolute path inside the installed package.

    Examples
    --------
    >>> get_packaged_fusion_duration_media(1280, 720, 23.976).name
    'dummy_video_1280x720_23.976P.mp4'
    """
    return select_fusion_duration_media(
        PACKAGED_DURATION_MEDIA_DIRECTORY,
        width,
        height,
        frame_rate,
    )


def append_fusion_composition(
    timeline: Any,
    *,
    duration_frames: int | None = None,
    record_frame: int | float | None = None,
    media_pool: Any | None = None,
    dummy_media: str | Path | None = None,
) -> tuple[Any, Any]:
    """Append a native or explicitly sized Fusion composition.

    Parameters
    ----------
    timeline
        Current Resolve Timeline remote object.
    duration_frames
        Fixed duration requested for the dummy-media route. Omit to use native insertion.
    record_frame
        Optional destination frame for the dummy-media route.
    media_pool
        Media Pool required for fixed-duration insertion.
    dummy_media
        Optional media override for fixed-duration insertion. When omitted,
        packaged media is selected from the timeline resolution and frame rate.

    Returns
    -------
    tuple of Any
        Inserted TimelineItem and its Fusion Composition.

    Notes
    -----
    Resolve 21.0.4 cannot set the native Fusion Composition duration. The
    fixed-duration route reproduces the tested dummy-media workaround and
    removes ``MediaIn1`` after adding the composition. Packaged files cover the
    supported resolution and frame-rate combinations.

    Examples
    --------
    >>> item, comp = append_fusion_composition(timeline)  # doctest: +SKIP
    """
    if duration_frames is None:
        if record_frame is not None or media_pool is not None or dummy_media is not None:
            raise ResolveValidationError("duration_frames is required when fixed-duration arguments are supplied.")
        item = insert_fusion_composition(timeline)
        count = item.GetFusionCompCount()
        if not isinstance(count, int) or count < 1:
            raise ResolveOperationError("TimelineItem.GetFusionCompCount", count)
        comp = item.GetFusionCompByIndex(1)
        if comp is None:
            raise ResolveOperationError("TimelineItem.GetFusionCompByIndex", comp)
        return item, comp
    if isinstance(duration_frames, bool) or not isinstance(duration_frames, int) or duration_frames <= 0:
        raise ResolveValidationError("duration_frames must be a positive integer.")
    if media_pool is None:
        raise ResolveValidationError(
            "media_pool is required for fixed-duration insertion."
        )
    if dummy_media is None:
        try:
            width = int(get_timeline_setting(timeline, "timelineResolutionWidth"))
            height = int(get_timeline_setting(timeline, "timelineResolutionHeight"))
        except ValueError as error:
            raise ResolveOperationError(
                "Timeline.GetSetting",
                None,
                "Timeline resolution settings must be integers.",
            ) from error
        frame_rate = get_timeline_setting(timeline, "timelineFrameRate")
        dummy_media = get_packaged_fusion_duration_media(width, height, frame_rate)
    clip = import_files(media_pool, [dummy_media])[0]
    item = append_clip(media_pool, clip, record_frame=record_frame, start_frame=0, end_frame=duration_frames, media_type=MediaType.VIDEO_ONLY)
    comp = add_comp(item)
    media_in = get_tool(comp, "MediaIn1")
    result = media_in.Delete()
    if result is False:
        raise ResolveOperationError("Tool.Delete", result)
    return item, comp


def refresh_fusion_color_management(
    session: ResolveSession,
    *,
    delay: float = 0.1,
) -> None:
    """Apply the Resolve 21.0.4 Fusion-page RCM refresh workaround.

    Parameters
    ----------
    session
        Connected Resolve 21.0.4 session.
    delay
        Positive page-transition delay in seconds.

    Returns
    -------
    None

    Notes
    -----
    This intentionally leaves Resolve on the Edit page.

    Examples
    --------
    >>> refresh_fusion_color_management(session)  # doctest: +SKIP
    """
    if tuple(session.version[:3]) != SUPPORTED_RESOLVE_VERSION:
        raise ResolveValidationError("The Fusion RCM workaround is limited to Resolve 21.0.4.")
    if isinstance(delay, bool) or not isinstance(delay, (int, float)) or not math.isfinite(delay) or delay <= 0:
        raise ResolveValidationError("delay must be a positive finite number.")
    open_page(session, Page.FUSION)
    time.sleep(delay)
    open_page(session, Page.EDIT)
