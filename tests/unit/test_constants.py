# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_constants.py -q

from __future__ import annotations

from types import MappingProxyType

import pytest

from ty_davinci_resolve import (
    BT2100_PROJECT_SETTINGS,
    STILL_SEQUENCE_FORMATS,
    VIDEO_QUALITY_AUTOMATIC,
    AcesOutputTransform,
    AlphaMode,
    AudioBitDepth,
    AudioChannelCount,
    AudioCodec,
    AudioMeterLoudnessScale,
    AudioSampleRate,
    BroadcastSafeLevel,
    ClipProperty,
    ColorScienceMode,
    ColorSpace,
    ColorSpaceGamma,
    DynamicRangeTransform,
    DeinterlaceQuality,
    FrameRate,
    FrameRateMismatchBehavior,
    Gamma,
    GeneratorName,
    ImageResizeMode,
    InputColorSpaceMode,
    MotionEstimationMode,
    MotionEstimationRange,
    NodeStackLayerCount,
    OptimizedMediaResolution,
    OUTPUT_COLOR_SPACES,
    PlaybackFrameRate,
    PixelAspectRatio,
    ProjectSetting,
    ProxyMediaMode,
    ProxyResolution,
    ProjectPresetMode,
    RenderFormat,
    ResolutionValue,
    ResizeTransformation,
    RenderCacheMode,
    RetimeInterpolation,
    SDIConfiguration,
    SettingToggle,
    SubtitleFormat,
    SuperScale,
    SuperScaleDetail,
    TimelineSetting,
    UniqueFilenameStyle,
    VideoCodec,
    VideoBitDepth,
    VideoDataLevel,
    VideoQuality,
    WorkingLuminanceMode,
    TIMELINE_WORKING_LUMINANCE_MAX_NITS,
    TIMELINE_WORKING_LUMINANCE_MIN_NITS,
    set_settings,
)


def test_legacy_project_values_are_migrated() -> None:
    assert SettingToggle.ENABLED == "1"
    assert SettingToggle.DISABLED == "0"
    assert ResolutionValue.PX_1280 == "1280"
    assert ResolutionValue.PX_2160 == "2160"
    assert FrameRate.FPS_23_976 == "23.976"
    assert FrameRate.FPS_59_94 == "59.94"
    assert PlaybackFrameRate.FPS_24 == "24"
    assert TimelineSetting.USE_CUSTOM_SETTINGS == "useCustomSettings"
    assert TimelineSetting.TIMELINE_FRAME_RATE == "timelineFrameRate"
    assert TimelineSetting.TIMELINE_PLAYBACK_FRAME_RATE == "timelinePlaybackFrameRate"
    assert SDIConfiguration.SINGLE_LINK == "single_link"
    assert VideoDataLevel.VIDEO == "Video"
    assert VideoDataLevel.FULL == "Full"
    assert ColorScienceMode.DAVINCI_YRGB == "davinciYRGB"
    assert ColorScienceMode.ACES_CCT == "acescct"
    assert len(ProjectPresetMode) == 10
    assert ProjectPresetMode.SDR_REC_2020 == "SDR Rec.2020"
    assert ProjectPresetMode.HDR_REC_2020_PQ_P3_D65_LIMITED == (
        "HDR Rec.2020 PQ (P3-D65 limited)"
    )
    assert ProjectPresetMode.CUSTOM == "Custom"
    assert ColorSpace.P3_D65 == "P3-D65"
    assert ColorSpace.REC_2020 == "Rec.2020"
    assert Gamma.ST2084 == "ST2084"
    assert Gamma.GAMMA_2_4 == "Gamma 2.4"
    assert Gamma.GAMMA_2_5 == "Gamma 2.5"
    assert Gamma.ST2084_1000_NIT == "ST2084 1000 nit"
    assert ColorSpaceGamma.REC_709_SCENE == "Rec.709 (Scene)"
    assert ClipProperty.INPUT_COLOR_SPACE == "Input Color Space"
    assert GeneratorName.SOLID_COLOR == "Solid Color"


def test_legacy_render_values_are_migrated() -> None:
    assert VideoCodec.PRORES_422_HQ == "ProRes422HQ"
    assert VideoCodec.PRORES_4444_XQ == "ProRes4444XQ"
    assert VideoCodec.DNXHR_HQX_12 == "DNxHRHQX_12"
    assert VideoCodec.RGB_FLOAT_DWAA == "RGBFloatDWAA"
    assert UniqueFilenameStyle.PREFIX == 0
    assert VIDEO_QUALITY_AUTOMATIC == 0
    assert VideoQuality.BEST == "Best"
    assert AudioCodec.LINEAR_PCM == "lpcm"
    assert AudioBitDepth.BIT_24 == 24
    assert AudioSampleRate.HZ_48000 == 48000
    assert STILL_SEQUENCE_FORMATS == {
        RenderFormat.EXR,
        RenderFormat.DPX,
        RenderFormat.TIFF,
        RenderFormat.PNG,
    }


def test_new_official_and_readback_values_are_defined() -> None:
    assert len(FrameRate) == 21
    assert len(ProjectSetting) == 151
    assert len(ResolutionValue) == 28
    assert len(PlaybackFrameRate) == 19
    assert len(TimelineSetting) == 6
    assert len(RenderFormat) == 23
    assert len(VideoCodec) == 199
    assert len(VideoQuality) == 5
    assert FrameRate.FPS_29_97_DF == "29.97 DF"
    assert SuperScale.X4 == 4
    assert PixelAspectRatio.CINEMASCOPE == "cinemascope"
    assert AlphaMode.STRAIGHT == 1
    assert SubtitleFormat.SEPARATE_FILE == "SeparateFile"
    assert ColorSpace.ARRI_WIDE_GAMUT_4 == "ARRI Wide Gamut 4"
    assert Gamma.DAVINCI_INTERMEDIATE == "DaVinci Intermediate"
    assert WorkingLuminanceMode.HDR_4000 == "HDR 4000"
    assert DynamicRangeTransform.LUMINANCE_MAPPING == "Luminance Mapping"
    assert DynamicRangeTransform.SATURATION_PRESERVING == "Saturation Preserving"
    assert len(ColorSpace) == 43
    assert len(OUTPUT_COLOR_SPACES) == 39
    assert ColorSpace.HSL not in OUTPUT_COLOR_SPACES
    assert ColorSpace.HSV not in OUTPUT_COLOR_SPACES
    assert ColorSpace.LAB_CIE not in OUTPUT_COLOR_SPACES
    assert ColorSpace.YUV not in OUTPUT_COLOR_SPACES
    assert ColorSpace.YUV == "Y'UV"
    assert ColorSpace.SMPTE_C == "SMPTE-C"
    assert InputColorSpaceMode.SAME_AS_TIMELINE == "Same as Timeline"
    assert len(Gamma) == 63
    assert Gamma.ARIB_STD_B67_HLG == "ARIB STD-B67 HLG"
    assert Gamma.SONY_S_LOG2 == "S-Log2"
    assert len(WorkingLuminanceMode) == 11
    assert WorkingLuminanceMode.HDR_ER_1000_10000 == "HDR ER 1000/10000"
    assert TIMELINE_WORKING_LUMINANCE_MIN_NITS == 48
    assert TIMELINE_WORKING_LUMINANCE_MAX_NITS == 10_000
    assert ResizeTransformation.GAMMA_TONE_MAPPED == "Gamma - Tone Mapped"
    assert AcesOutputTransform.P3_D65_ST2084_1000_NIT == (
        "P3-D65 ST2084 (1000 nit)"
    )
    assert AudioChannelCount.CHANNELS_16 == "16"
    assert DeinterlaceQuality.HIGH == "high"
    assert MotionEstimationMode.ENHANCED_BETTER == "enhancedBetter"
    assert MotionEstimationRange.MEDIUM == "medium"
    assert ImageResizeMode.BICUBIC == "bicubic"
    assert RetimeInterpolation.OPTICAL_FLOW == "opticalFlow"
    assert AudioMeterLoudnessScale.EBU_18 == "ebu_18_scale"
    assert BroadcastSafeLevel.RANGE_10_110 == "10_110"
    assert NodeStackLayerCount.LAYERS_4 == "4"
    assert OptimizedMediaResolution.QUARTER == "quarter"
    assert ProxyMediaMode.WHEN_SOURCE_UNAVAILABLE == "2"
    assert ProxyResolution.HALF == "half"
    assert RenderCacheMode.USER == "user"
    assert SuperScaleDetail.HIGH == "High"
    assert FrameRateMismatchBehavior.NONE == "none"
    assert VideoBitDepth.BIT_10 == "10"
    assert SDIConfiguration.QUAD_LINK == "quad_link"


def test_setting_enums_can_be_passed_directly() -> None:
    calls: list[tuple[str, str | int]] = []

    class Project:
        def SetSetting(self, name: str, value: str | int) -> bool:
            calls.append((name, value))
            return True

    set_settings(
        Project(),
        {
            ProjectSetting.COLOR_SPACE_TIMELINE: ColorSpace.P3_D65,
            ProjectSetting.COLOR_SPACE_TIMELINE_GAMMA: Gamma.ST2084,
            ProjectSetting.SUPER_SCALE: SuperScale.X4,
        },
    )

    assert calls == [
        ("colorSpaceTimeline", "P3-D65"),
        ("colorSpaceTimelineGamma", "ST2084"),
        ("superScale", SuperScale.X4),
    ]


def test_bt2100_preset_is_immutable() -> None:
    assert isinstance(BT2100_PROJECT_SETTINGS, MappingProxyType)
    assert BT2100_PROJECT_SETTINGS[ProjectSetting.COLOR_SPACE_OUTPUT] == (
        ColorSpace.REC_2020
    )
    with pytest.raises(TypeError):
        BT2100_PROJECT_SETTINGS[ProjectSetting.HDR_MASTERING_ON] = (  # type: ignore[index]
            SettingToggle.DISABLED
        )


def test_bt2100_preset_can_be_passed_directly() -> None:
    calls: list[tuple[str, str | int]] = []

    class Project:
        def SetSetting(self, name: str, value: str | int) -> bool:
            calls.append((name, value))
            return True

    set_settings(Project(), BT2100_PROJECT_SETTINGS)

    assert calls == [
        (str(name), value) for name, value in BT2100_PROJECT_SETTINGS.items()
    ]
