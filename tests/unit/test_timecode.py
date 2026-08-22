# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_timecode.py -q

import pytest

from ty_davinci_resolve import (
    ResolveValidationError,
    frames_to_timecode,
    seconds_to_frames,
    timecode_to_frames,
)


def test_seconds_to_frames_uses_actual_rate() -> None:
    assert seconds_to_frames(2, 23.976) == 48


@pytest.mark.parametrize(
    ("frame_index", "fps", "expected"),
    [(0, 24, "00:00:00:00"), (24, 24, "00:00:01:00"), (86423, 24, "01:00:00:23")],
)
def test_frames_to_timecode(frame_index: int, fps: float, expected: str) -> None:
    assert frames_to_timecode(frame_index, fps) == expected


def test_timecode_round_trip() -> None:
    frame_index = timecode_to_frames("01:02:03:12", 24)
    assert frames_to_timecode(frame_index, 24) == "01:02:03:12"


@pytest.mark.parametrize(
    "timecode",
    ["00:00", "00:60:00:00", "00:00:60:00", "00:00:00:24", "x:00:00:00"],
)
def test_invalid_timecode_is_rejected(timecode: str) -> None:
    with pytest.raises(ResolveValidationError):
        timecode_to_frames(timecode, 24)


def test_negative_frame_is_rejected() -> None:
    with pytest.raises(ResolveValidationError):
        frames_to_timecode(-1, 24)
