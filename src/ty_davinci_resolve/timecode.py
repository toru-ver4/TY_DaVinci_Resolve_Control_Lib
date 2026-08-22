"""Resolve-independent frame and non-drop-frame timecode conversion."""

from __future__ import annotations

import math

from .errors import ResolveValidationError


def _nominal_fps(fps: float) -> int:
    if isinstance(fps, bool) or not isinstance(fps, (int, float)):
        raise ResolveValidationError("fps must be a positive finite number.")
    if not math.isfinite(fps) or fps <= 0:
        raise ResolveValidationError("fps must be a positive finite number.")
    return round(fps)


def seconds_to_frames(seconds: float, fps: float) -> int:
    """Convert non-negative seconds to the nearest frame index.

    Parameters
    ----------
    seconds
        Non-negative duration in seconds.
    fps
        Playback frame rate.

    Returns
    -------
    int
        Nearest zero-based frame index.

    Examples
    --------
    >>> seconds_to_frames(2.0, 23.976)
    48
    """
    if isinstance(seconds, bool) or not isinstance(seconds, (int, float)):
        raise ResolveValidationError("seconds must be a non-negative finite number.")
    if not math.isfinite(seconds) or seconds < 0:
        raise ResolveValidationError("seconds must be a non-negative finite number.")
    _nominal_fps(fps)
    return round(seconds * fps)


def frames_to_timecode(frame_index: int, fps: float) -> str:
    """Convert a frame index to non-drop-frame timecode.

    Parameters
    ----------
    frame_index
        Non-negative frame index.
    fps
        Playback frame rate. Its nearest integer is the timecode base.

    Returns
    -------
    str
        Timecode in ``HH:MM:SS:FF`` form.

    Notes
    -----
    This function does not implement drop-frame timecode.

    Examples
    --------
    >>> frames_to_timecode(24, 24)
    '00:00:01:00'
    """
    if isinstance(frame_index, bool) or not isinstance(frame_index, int) or frame_index < 0:
        raise ResolveValidationError("frame_index must be a non-negative integer.")
    base = _nominal_fps(fps)
    seconds, frames = divmod(frame_index, base)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{frames:02d}"


def timecode_to_frames(timecode: str, fps: float) -> int:
    """Convert non-drop-frame timecode to a frame index.

    Parameters
    ----------
    timecode
        Timecode in ``HH:MM:SS:FF`` form.
    fps
        Playback frame rate. Its nearest integer is the timecode base.

    Returns
    -------
    int
        Zero-based frame index.

    Notes
    -----
    This function does not implement drop-frame timecode.

    Examples
    --------
    >>> timecode_to_frames("01:00:00:00", 24)
    86400
    """
    if not isinstance(timecode, str):
        raise ResolveValidationError("timecode must be a string.")
    parts = timecode.split(":")
    if len(parts) != 4 or any(not part.isdigit() for part in parts):
        raise ResolveValidationError("timecode must use HH:MM:SS:FF format.")
    hours, minutes, seconds, frames = (int(part) for part in parts)
    base = _nominal_fps(fps)
    if minutes >= 60 or seconds >= 60 or frames >= base:
        raise ResolveValidationError(f"Invalid timecode field: {timecode!r}.")
    return ((hours * 60 + minutes) * 60 + seconds) * base + frames
