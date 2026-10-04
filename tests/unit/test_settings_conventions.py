# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: .venv313/Scripts/python.exe -m pytest tests/unit/test_settings_conventions.py -q

from types import SimpleNamespace

import pytest

from ty_davinci_resolve import (
    ResolveOperationError, get_project_setting, get_timeline_setting,
    set_project_settings, set_timeline_setting,
)


def test_canonical_project_and_timeline_settings_do_not_call_legacy() -> None:
    calls = []
    target = SimpleNamespace(
        GetSettings=lambda: {"timelineFrameRate": 24.0},
        SetSettings=lambda values: calls.append(values) or True,
        GetSetting=lambda *args: pytest.fail("legacy getter called"),
        SetSetting=lambda *args: pytest.fail("legacy setter called"),
    )
    assert get_project_setting(target, "timelineFrameRate") == "24.0"
    assert get_timeline_setting(target, "timelineFrameRate") == "24.0"
    set_project_settings(target, {"timelineFrameRate": "25", "superScale": 2})
    set_timeline_setting(target, "timelineFrameRate", "30")
    assert calls == [{"timelineFrameRate": "25"}, {"superScale": 2}, {"timelineFrameRate": "30"}]


def test_canonical_rejection_stops_ordered_settings_without_legacy_retry() -> None:
    calls = []
    target = SimpleNamespace(
        SetSettings=lambda values: calls.append(values) or False,
        SetSetting=lambda *args: pytest.fail("rejected write retried"),
    )
    with pytest.raises(ResolveOperationError, match="SetSettings"):
        set_project_settings(target, {"bad": "1", "later": "2"})
    assert calls == [{"bad": "1"}]


@pytest.mark.parametrize("snapshot", [None, {}, {"timelineFrameRate": None}])
def test_canonical_invalid_readback_is_an_error(snapshot) -> None:
    target = SimpleNamespace(GetSettings=lambda: snapshot)
    with pytest.raises(ResolveOperationError, match="GetSettings"):
        get_project_setting(target, "timelineFrameRate")
