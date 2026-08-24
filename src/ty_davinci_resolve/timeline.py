"""Timeline creation, selection, track, and clip helpers."""

from __future__ import annotations

from collections.abc import Mapping
from enum import IntEnum
import re
from typing import Any

from .constants import TimelineSetting, TrackType
from .errors import ResolveOperationError, ResolveValidationError


class MediaType(IntEnum):
    """Media types accepted by ``MediaPool.AppendToTimeline``."""

    VIDEO_ONLY = 1
    AUDIO_ONLY = 2


def _track_type_value(track_type: TrackType | str) -> str:
    try:
        return TrackType(track_type).value
    except (TypeError, ValueError) as error:
        raise ResolveValidationError(f"Invalid track type: {track_type!r}.") from error


def create_empty_timeline(media_pool: Any, name: str) -> Any:
    """Create an empty timeline.

    Parameters
    ----------
    media_pool
        Resolve MediaPool remote object.
    name
        New timeline name.

    Returns
    -------
    Any
        Created Resolve Timeline remote object.

    Examples
    --------
    >>> create_empty_timeline(media_pool, "Main")  # doctest: +SKIP
    """
    if not isinstance(name, str) or not name.strip():
        raise ResolveValidationError("name must be a non-empty string.")
    timeline = media_pool.CreateEmptyTimeline(name)
    if timeline is None:
        raise ResolveOperationError("MediaPool.CreateEmptyTimeline", timeline)
    return timeline


def get_current_timeline(project: Any) -> Any:
    """Return the project's currently loaded timeline.

    Parameters
    ----------
    project
        Resolve Project remote object.

    Returns
    -------
    Any
        Current Resolve Timeline remote object.

    Examples
    --------
    >>> get_current_timeline(project)  # doctest: +SKIP
    """
    timeline = project.GetCurrentTimeline()
    if timeline is None:
        raise ResolveOperationError("Project.GetCurrentTimeline", timeline, "No timeline is currently loaded.")
    return timeline


def append_clip(
    media_pool: Any,
    clip: Any,
    *,
    record_frame: int | float | None = None,
    start_frame: int | float | None = None,
    end_frame: int | float | None = None,
    media_type: MediaType | int | None = None,
    track_index: int = 1,
) -> Any:
    """Append one Media Pool clip to the current timeline.

    Parameters
    ----------
    media_pool
        Resolve MediaPool remote object.
    clip
        Resolve MediaPoolItem remote object.
    record_frame
        Optional destination frame.
    start_frame
        Optional inclusive source start frame.
    end_frame
        Optional inclusive source end frame.
    media_type
        Optional video-only or audio-only selector.
    track_index
        One-based target track index.

    Returns
    -------
    Any
        Appended Resolve TimelineItem remote object.

    Examples
    --------
    >>> append_clip(media_pool, clip, track_index=1)  # doctest: +SKIP
    """
    if clip is None:
        raise ResolveValidationError("clip must not be None.")
    if isinstance(track_index, bool) or not isinstance(track_index, int) or track_index < 1:
        raise ResolveValidationError("track_index must be a positive integer.")
    if (start_frame is None) != (end_frame is None):
        raise ResolveValidationError(
            "start_frame and end_frame must be provided together."
        )
    if start_frame is not None and start_frame > end_frame:
        raise ResolveValidationError("start_frame must not exceed end_frame.")
    clip_info: dict[str, Any] = {
        "mediaPoolItem": clip,
        "trackIndex": track_index,
    }
    if record_frame is not None:
        clip_info["recordFrame"] = record_frame
    if start_frame is not None:
        clip_info["startFrame"] = start_frame
        clip_info["endFrame"] = end_frame
    if media_type is not None:
        try:
            clip_info["mediaType"] = MediaType(media_type).value
        except ValueError as error:
            raise ResolveValidationError(f"Invalid media_type: {media_type!r}.") from error
    result = media_pool.AppendToTimeline([clip_info])
    if not result or result[0] is None:
        raise ResolveOperationError("MediaPool.AppendToTimeline", result)
    return result[0]


def get_track_items(
    timeline: Any,
    track_type: TrackType | str,
    track_index: int,
) -> tuple[Any, ...]:
    """Return all items in a validated timeline track.

    Parameters
    ----------
    timeline
        Resolve Timeline remote object.
    track_type
        Video, audio, or subtitle track type.
    track_index
        One-based track index.

    Returns
    -------
    tuple of Any
        Timeline items, possibly empty.

    Examples
    --------
    >>> get_track_items(timeline, TrackType.VIDEO, 1)  # doctest: +SKIP
    """
    track_value = _track_type_value(track_type)
    count = timeline.GetTrackCount(track_value)
    if not isinstance(count, int) or count < 0:
        raise ResolveOperationError("Timeline.GetTrackCount", count)
    if isinstance(track_index, bool) or not isinstance(track_index, int) or not 1 <= track_index <= count:
        raise ResolveValidationError(
            f"track_index must be between 1 and {count}, got {track_index!r}."
        )
    result = timeline.GetItemListInTrack(track_value, track_index)
    if result is None:
        raise ResolveOperationError("Timeline.GetItemListInTrack", result)
    return tuple(result)


def get_track_name(
    timeline: Any,
    track_type: TrackType | str,
    track_index: int,
) -> str:
    """Return the name of a validated timeline track.

    Parameters
    ----------
    timeline
        Resolve Timeline remote object.
    track_type
        Video, audio, or subtitle track type.
    track_index
        One-based track index.

    Returns
    -------
    str
        Track name.

    Examples
    --------
    >>> get_track_name(timeline, "video", 1)  # doctest: +SKIP
    'Video 1'
    """
    get_track_items(timeline, track_type, track_index)
    result = timeline.GetTrackName(_track_type_value(track_type), track_index)
    if not isinstance(result, str):
        raise ResolveOperationError("Timeline.GetTrackName", result)
    return result


def set_track_name(
    timeline: Any,
    track_type: TrackType | str,
    track_index: int,
    name: str,
) -> None:
    """Set the name of a validated timeline track.

    Parameters
    ----------
    timeline
        Resolve Timeline remote object.
    track_type
        Video, audio, or subtitle track type.
    track_index
        One-based track index.
    name
        New non-empty track name.

    Returns
    -------
    None

    Examples
    --------
    >>> set_track_name(timeline, "video", 1, "Main")  # doctest: +SKIP
    """
    if not isinstance(name, str) or not name.strip():
        raise ResolveValidationError("name must be a non-empty string.")
    get_track_items(timeline, track_type, track_index)
    result = timeline.SetTrackName(_track_type_value(track_type), track_index, name)
    if result is not True:
        raise ResolveOperationError("Timeline.SetTrackName", result)


def insert_fusion_composition(timeline: Any) -> Any:
    """Insert a native Fusion Composition at the playhead.

    Parameters
    ----------
    timeline
        Resolve Timeline remote object.

    Returns
    -------
    Any
        Inserted Resolve TimelineItem remote object.

    Examples
    --------
    >>> insert_fusion_composition(timeline)  # doctest: +SKIP
    """
    item = timeline.InsertFusionCompositionIntoTimeline()
    if item is None:
        raise ResolveOperationError(
            "Timeline.InsertFusionCompositionIntoTimeline", item
        )
    return item


def set_current_timecode(
    timeline: Any,
    timecode: str,
    *,
    verify: bool = True,
) -> None:
    """Set and verify the current timeline playhead timecode.

    Parameters
    ----------
    timeline
        Resolve Timeline remote object.
    timecode
        Non-drop timecode in ``HH:MM:SS:FF`` form.
    verify
        Verify the playhead using ``GetCurrentTimecode()`` after setting it.

    Returns
    -------
    None

    Examples
    --------
    >>> set_current_timecode(timeline, "01:00:00:00")  # doctest: +SKIP
    """
    if not isinstance(timecode, str) or re.fullmatch(r"\d{2}:\d{2}:\d{2}:\d{2}", timecode) is None:
        raise ResolveValidationError("timecode must use HH:MM:SS:FF form.")
    if not isinstance(verify, bool):
        raise ResolveValidationError("verify must be a bool.")
    result = timeline.SetCurrentTimecode(timecode)
    if result is not True:
        raise ResolveOperationError("Timeline.SetCurrentTimecode", result)
    if not verify:
        return
    actual = timeline.GetCurrentTimecode()
    if actual != timecode:
        raise ResolveOperationError("Timeline.GetCurrentTimecode", actual, f"Playhead verification failed: expected {timecode!r}, got {actual!r}.")


def get_timeline_setting(timeline: Any, name: str) -> str:
    """Return one timeline setting.

    Parameters
    ----------
    timeline
        Resolve Timeline remote object.
    name
        Non-empty setting name.

    Returns
    -------
    str
        Setting value reported by Resolve.

    Examples
    --------
    >>> get_timeline_setting(timeline, "timelineFrameRate")  # doctest: +SKIP
    '24'
    """
    if not isinstance(name, str) or not name.strip():
        raise ResolveValidationError("name must be a non-empty string.")
    result = timeline.GetSetting(name)
    if result is None:
        raise ResolveOperationError("Timeline.GetSetting", result)
    return str(result)


def set_timeline_setting(timeline: Any, name: str, value: str) -> None:
    """Set one timeline setting and fail on rejection.

    Parameters
    ----------
    timeline
        Resolve Timeline remote object.
    name
        Non-empty setting name.
    value
        Non-empty setting value.

    Returns
    -------
    None

    Examples
    --------
    >>> set_timeline_setting(timeline, "useCustomSettings", "1")  # doctest: +SKIP
    """
    if not isinstance(name, str) or not name.strip():
        raise ResolveValidationError("name must be a non-empty string.")
    if not isinstance(value, str) or not value.strip():
        raise ResolveValidationError("value must be a non-empty string.")
    result = timeline.SetSetting(name, value)
    if result is not True:
        raise ResolveOperationError("Timeline.SetSetting", result, f"Timeline rejected setting {name!r}.")


def set_timeline_settings(
    timeline: Any,
    settings: Mapping[str, str],
    *,
    enable_custom_settings: bool = True,
) -> None:
    """Set timeline settings in mapping order.

    Parameters
    ----------
    timeline
        Resolve Timeline remote object.
    settings
        Non-empty setting mapping.
    enable_custom_settings
        Set ``useCustomSettings`` to ``1`` before other settings.

    Returns
    -------
    None

    Notes
    -----
    All argument values are validated before Resolve is mutated. API rejection
    stops processing immediately.

    Examples
    --------
    >>> set_timeline_settings(timeline, {"timelineResolutionWidth": "1280"})  # doctest: +SKIP
    """
    if not isinstance(settings, Mapping) or not settings:
        raise ResolveValidationError("settings must be a non-empty mapping.")
    for name, value in settings.items():
        if not isinstance(name, str) or not name.strip() or not isinstance(value, str) or not value.strip():
            raise ResolveValidationError("setting names and values must be non-empty strings.")
    if not isinstance(enable_custom_settings, bool):
        raise ResolveValidationError("enable_custom_settings must be a bool.")
    if enable_custom_settings and TimelineSetting.USE_CUSTOM_SETTINGS not in settings:
        set_timeline_setting(timeline, TimelineSetting.USE_CUSTOM_SETTINGS, "1")
    for name, value in settings.items():
        set_timeline_setting(timeline, name, value)


def insert_generator(timeline: Any, name: str) -> Any:
    """Insert a standard generator at the playhead.

    Parameters
    ----------
    timeline
        Resolve Timeline remote object.
    name
        Generator name displayed by Resolve.

    Returns
    -------
    Any
        Inserted TimelineItem remote object.

    Examples
    --------
    >>> insert_generator(timeline, "Solid Color")  # doctest: +SKIP
    """
    if not isinstance(name, str) or not name.strip():
        raise ResolveValidationError("name must be a non-empty string.")
    item = timeline.InsertGeneratorIntoTimeline(name)
    if item is None:
        raise ResolveOperationError("Timeline.InsertGeneratorIntoTimeline", item)
    return item
