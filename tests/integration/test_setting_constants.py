# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest -m resolve_integration tests/integration/test_setting_constants.py -q

from __future__ import annotations

import time
from enum import IntEnum, StrEnum
from uuid import uuid4

import pytest

from ty_davinci_resolve import (
    BT2100_PROJECT_SETTINGS,
    AcesInputTransform,
    AcesOutputTransform,
    ColorScienceMode,
    ColorSpace,
    ColorSpaceGamma,
    DynamicRangeTransform,
    FrameRate,
    Gamma,
    OUTPUT_COLOR_SPACES,
    PlaybackFrameRate,
    ProjectPresetMode,
    ProjectSetting,
    RenderFormat,
    ResolveSession,
    ResizeTransformation,
    SettingToggle,
    SuperScale,
    VideoCodec,
    WorkingLuminanceMode,
    TIMELINE_WORKING_LUMINANCE_MAX_NITS,
    TIMELINE_WORKING_LUMINANCE_MIN_NITS,
    close_project,
    create_project,
    delete_project,
    list_projects,
    load_project,
    set_settings,
)


def _setting_matches(actual: object, expected: str | int) -> bool:
    """Compare a setting while allowing Resolve numeric normalization.

    Parameters
    ----------
    actual
        Value returned by Resolve.
    expected
        Value sent to Resolve.

    Returns
    -------
    bool
        Whether the values are exactly equal or numerically equivalent.

    Examples
    --------
    >>> _setting_matches(24.0, "24")
    True
    """
    if actual == expected:
        return True
    try:
        return float(actual) == float(expected)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return False


def _assert_setting(
    project: object,
    key: ProjectSetting,
    value: StrEnum | IntEnum,
) -> None:
    """Set one enum value and verify exact Resolve readback.

    Parameters
    ----------
    project
        Disposable Resolve Project remote object.
    key
        Verified project setting key.
    value
        Candidate string enum value.

    Returns
    -------
    None

    Examples
    --------
    >>> _assert_setting(project, ProjectSetting.COLOR_SPACE_TIMELINE, ColorSpace.P3_D65)  # doctest: +SKIP
    """
    assert project.SetSetting(key, value) is True
    time.sleep(0.35)
    actual = project.GetSetting(key)
    assert _setting_matches(actual, value)


@pytest.mark.resolve_integration
def test_project_setting_constants_on_resolve_21_0_4() -> None:
    session = ResolveSession.connect()
    manager = session.project_manager
    original = manager.GetCurrentProject()
    original_name = original.GetName() if original is not None else None
    original_names = list_projects(session)
    project_name = f"TY_CONSTANTS_{uuid4().hex}"

    try:
        project = create_project(session, project_name)
        snapshot = project.GetSetting()
        assert isinstance(snapshot, dict)
        assert set(ProjectSetting).issubset(snapshot)

        drop_frame_rates = {
            FrameRate.FPS_29_97_DF,
            FrameRate.FPS_59_94_DF,
        }
        for value in set(FrameRate) - drop_frame_rates:
            _assert_setting(project, ProjectSetting.TIMELINE_FRAME_RATE, value)
        for value in drop_frame_rates:
            assert project.SetSetting(
                ProjectSetting.TIMELINE_FRAME_RATE,
                value,
            ) is True
            time.sleep(0.35)
            assert _setting_matches(
                project.GetSetting(ProjectSetting.TIMELINE_FRAME_RATE),
                value.removesuffix(" DF"),
            )
            assert project.GetSetting(
                ProjectSetting.TIMELINE_DROP_FRAME_TIMECODE
            ) == SettingToggle.ENABLED

        for value in PlaybackFrameRate:
            _assert_setting(project, ProjectSetting.TIMELINE_FRAME_RATE, value)

        render_formats = project.GetRenderFormats()
        assert set(render_formats.values()) == set(RenderFormat)
        runtime_codecs = {
            codec
            for format_id in render_formats.values()
            for codec in project.GetRenderCodecs(format_id).values()
        }
        assert runtime_codecs.issubset(set(VideoCodec))

        set_settings(project, BT2100_PROJECT_SETTINGS, settle_delay=0.35)
        for key, value in BT2100_PROJECT_SETTINGS.items():
            assert _setting_matches(project.GetSetting(key), value)

        _assert_setting(
            project,
            ProjectSetting.COLOR_SCIENCE_MODE,
            ColorScienceMode.DAVINCI_YRGB_COLOR_MANAGED,
        )
        for value in ProjectPresetMode:
            _assert_setting(project, ProjectSetting.RCM_PRESET_MODE, value)
        _assert_setting(
            project,
            ProjectSetting.RCM_PRESET_MODE,
            ProjectPresetMode.CUSTOM,
        )
        _assert_setting(
            project,
            ProjectSetting.SEPARATE_COLOR_SPACE_AND_GAMMA,
            SettingToggle.ENABLED,
        )
        for key in (
            ProjectSetting.COLOR_SPACE_INPUT,
            ProjectSetting.COLOR_SPACE_TIMELINE,
        ):
            for value in ColorSpace:
                _assert_setting(project, key, value)
        for value in OUTPUT_COLOR_SPACES:
            _assert_setting(project, ProjectSetting.COLOR_SPACE_OUTPUT, value)
        for key in (
            ProjectSetting.COLOR_SPACE_INPUT_GAMMA,
            ProjectSetting.COLOR_SPACE_TIMELINE_GAMMA,
            ProjectSetting.COLOR_SPACE_OUTPUT_GAMMA,
        ):
            for value in Gamma:
                _assert_setting(project, key, value)
        _assert_setting(
            project,
            ProjectSetting.SEPARATE_COLOR_SPACE_AND_GAMMA,
            SettingToggle.DISABLED,
        )
        for value in ColorSpaceGamma:
            _assert_setting(project, ProjectSetting.COLOR_SPACE_TIMELINE, value)
        _assert_setting(
            project,
            ProjectSetting.SEPARATE_COLOR_SPACE_AND_GAMMA,
            SettingToggle.ENABLED,
        )
        for value in WorkingLuminanceMode:
            _assert_setting(
                project,
                ProjectSetting.TIMELINE_WORKING_LUMINANCE_MODE,
                value,
            )
        _assert_setting(
            project,
            ProjectSetting.TIMELINE_WORKING_LUMINANCE_MODE,
            WorkingLuminanceMode.CUSTOM,
        )
        for value in (
            TIMELINE_WORKING_LUMINANCE_MIN_NITS,
            TIMELINE_WORKING_LUMINANCE_MAX_NITS,
        ):
            assert project.SetSetting(
                ProjectSetting.TIMELINE_WORKING_LUMINANCE,
                str(value),
            ) is True
            time.sleep(0.35)
            assert _setting_matches(
                project.GetSetting(ProjectSetting.TIMELINE_WORKING_LUMINANCE),
                value,
            )
        for value in ResizeTransformation:
            _assert_setting(
                project,
                ProjectSetting.IMAGE_RESIZING_GAMMA,
                value,
            )
        for key in (ProjectSetting.INPUT_DRT, ProjectSetting.OUTPUT_DRT):
            for value in DynamicRangeTransform:
                _assert_setting(project, key, value)
        _assert_setting(
            project,
            ProjectSetting.COLOR_SCIENCE_MODE,
            ColorScienceMode.ACES_CCT,
        )
        for value in AcesInputTransform:
            _assert_setting(project, ProjectSetting.COLOR_ACES_IDT, value)
        for value in AcesOutputTransform:
            _assert_setting(project, ProjectSetting.COLOR_ACES_ODT, value)
        for value in SuperScale:
            _assert_setting(project, ProjectSetting.SUPER_SCALE, value)
    finally:
        current = manager.GetCurrentProject()
        if current is not None and current.GetName() == project_name:
            close_project(session, current)
        if project_name in list_projects(session):
            delete_project(session, project_name)
        if original_name and original_name in original_names:
            load_project(session, original_name)
