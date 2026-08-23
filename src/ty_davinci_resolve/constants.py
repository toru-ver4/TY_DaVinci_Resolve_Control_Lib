"""Stable values used by the DaVinci Resolve scripting API."""

from enum import IntEnum, StrEnum
from types import MappingProxyType


class Page(StrEnum):
    """DaVinci Resolve page names documented by Resolve 21.0.4."""

    MEDIA = "media"
    PHOTO = "photo"
    CUT = "cut"
    EDIT = "edit"
    FUSION = "fusion"
    COLOR = "color"
    FAIRLIGHT = "fairlight"
    DELIVER = "deliver"


class TrackType(StrEnum):
    """Timeline track types documented by Resolve 21.0.4."""

    VIDEO = "video"
    AUDIO = "audio"
    SUBTITLE = "subtitle"


class ProjectSetting(StrEnum):
    """Project setting keys observed in a Resolve 21.0.4 snapshot.

    Notes
    -----
    Snapshot presence does not guarantee that ``SetSetting`` accepts a value.
    """

    TIMELINE_RESOLUTION_WIDTH = "timelineResolutionWidth"
    TIMELINE_RESOLUTION_HEIGHT = "timelineResolutionHeight"
    TIMELINE_PLAYBACK_FRAME_RATE = "timelinePlaybackFrameRate"
    TIMELINE_FRAME_RATE = "timelineFrameRate"
    TIMELINE_SAMPLE_RATE = "timelineSampleRate"
    VIDEO_MONITOR_FORMAT = "videoMonitorFormat"
    VIDEO_MONITOR_USE_444_SDI = "videoMonitorUse444SDI"
    VIDEO_MONITOR_SDI_CONFIGURATION = "videoMonitorSDIConfiguration"
    VIDEO_MONITOR_USE_HDR_OVER_HDMI = "videoMonitorUseHDROverHDMI"
    VIDEO_DATA_LEVELS = "videoDataLevels"
    COLOR_SCIENCE_MODE = "colorScienceMode"
    RCM_PRESET_MODE = "rcmPresetMode"
    AUTO_COLOR_MANAGEMENT = "isAutoColorManage"
    SEPARATE_COLOR_SPACE_AND_GAMMA = "separateColorSpaceAndGamma"
    COLOR_SPACE_INPUT = "colorSpaceInput"
    COLOR_SPACE_INPUT_GAMMA = "colorSpaceInputGamma"
    COLOR_SPACE_TIMELINE = "colorSpaceTimeline"
    COLOR_SPACE_TIMELINE_GAMMA = "colorSpaceTimelineGamma"
    COLOR_SPACE_OUTPUT = "colorSpaceOutput"
    COLOR_SPACE_OUTPUT_GAMMA = "colorSpaceOutputGamma"
    COLOR_ACES_IDT = "colorAcesIDT"
    COLOR_ACES_ODT = "colorAcesODT"
    COLOR_ACES_GAMUT_COMPRESS_TYPE = "colorAcesGamutCompressType"
    TIMELINE_WORKING_LUMINANCE = "timelineWorkingLuminance"
    TIMELINE_WORKING_LUMINANCE_MODE = "timelineWorkingLuminanceMode"
    INPUT_DRT = "inputDRT"
    OUTPUT_DRT = "outputDRT"
    OUTPUT_GAMUT_MAPPING = "colorSpaceOutputGamutMapping"
    USE_INVERSE_DRT = "useInverseDRT"
    USE_COLOR_SPACE_AWARE_GRADING_TOOLS = "useColorSpaceAwareGradingTools"
    IMAGE_RESIZING_GAMMA = "imageResizingGamma"
    DISABLE_FUSION_TONE_MAPPING = "disableFusionToneMapping"
    GRAPHICS_WHITE_LEVEL = "graphicsWhiteLevel"
    HDR_MASTERING_LUMINANCE_MAX = "hdrMasteringLuminanceMax"
    HDR_MASTERING_ON = "hdrMasteringOn"
    SUPER_SCALE = "superScale"
    AUDIO_CAPTURE_NUM_CHANNELS = "audioCaptureNumChannels"
    AUDIO_OUTPUT_HAS_TIMECODE = "audioOutputHasTimecode"
    AUDIO_PLAYOUT_NUM_CHANNELS = "audioPlayoutNumChannels"
    CLOUD_PROJECT_MEDIA_LOCATION = "cloudProjectMediaLocation"
    COLOR_ACES_NODE_LUT_PROCESSING_SPACE = "colorAcesNodeLUTProcessingSpace"
    COLOR_GALLERY_STILLS_LOCATION = "colorGalleryStillsLocation"
    COLOR_GALLERY_STILLS_NAMING_CUSTOM_PATTERN = (
        "colorGalleryStillsNamingCustomPattern"
    )
    COLOR_GALLERY_STILLS_NAMING_ENABLED = "colorGalleryStillsNamingEnabled"
    COLOR_GALLERY_STILLS_NAMING_PATTERN = "colorGalleryStillsNamingPattern"
    COLOR_GALLERY_STILLS_NAMING_WITH_STILL_NUMBER = (
        "colorGalleryStillsNamingWithStillNumber"
    )
    COLOR_KEYFRAME_DYNAMICS_END_PROFILE = "colorKeyframeDynamicsEndProfile"
    COLOR_KEYFRAME_DYNAMICS_START_PROFILE = (
        "colorKeyframeDynamicsStartProfile"
    )
    COLOR_LUMINANCE_MIXER_DEFAULT_ZERO = "colorLuminanceMixerDefaultZero"
    COLOR_SPACE_OUTPUT_GAMUT_SATURATION_KNEE = (
        "colorSpaceOutputGamutSaturationKnee"
    )
    COLOR_SPACE_OUTPUT_GAMUT_SATURATION_MAX = (
        "colorSpaceOutputGamutSaturationMax"
    )
    COLOR_SPACE_OUTPUT_TONE_LUMINANCE_MAX = (
        "colorSpaceOutputToneLuminanceMax"
    )
    COLOR_SPACE_OUTPUT_TONE_MAPPING = "colorSpaceOutputToneMapping"
    COLOR_USE_BGR_PIXEL_ORDER_FOR_DPX = "colorUseBGRPixelOrderForDPX"
    COLOR_USE_CONTRAST_S_CURVE = "colorUseContrastSCurve"
    COLOR_USE_LEGACY_LOG_GRADES = "colorUseLegacyLogGrades"
    COLOR_USE_LOCAL_VERSIONS_AS_DEFAULT = "colorUseLocalVersionsAsDefault"
    COLOR_USE_STEREO_CONVERGENCE_FOR_EFFECTS = (
        "colorUseStereoConvergenceForEffects"
    )
    COLOR_VERSION_1_NAME = "colorVersion1Name"
    COLOR_VERSION_2_NAME = "colorVersion2Name"
    COLOR_VERSION_3_NAME = "colorVersion3Name"
    COLOR_VERSION_4_NAME = "colorVersion4Name"
    COLOR_VERSION_5_NAME = "colorVersion5Name"
    COLOR_VERSION_6_NAME = "colorVersion6Name"
    COLOR_VERSION_7_NAME = "colorVersion7Name"
    COLOR_VERSION_8_NAME = "colorVersion8Name"
    COLOR_VERSION_9_NAME = "colorVersion9Name"
    COLOR_VERSION_10_NAME = "colorVersion10Name"
    HDR10_PLUS_CONTROLS_ON = "hdr10PlusControlsOn"
    HDR_DOLBY_ANALYSIS_TUNING = "hdrDolbyAnalysisTuning"
    HDR_DOLBY_CONTROLS_ON = "hdrDolbyControlsOn"
    HDR_DOLBY_MASTER_DISPLAY = "hdrDolbyMasterDisplay"
    HDR_DOLBY_VERSION = "hdrDolbyVersion"
    IMAGE_DEINTERLACE_QUALITY = "imageDeinterlaceQuality"
    IMAGE_ENABLE_FIELD_PROCESSING = "imageEnableFieldProcessing"
    IMAGE_MOTION_ESTIMATION_MODE = "imageMotionEstimationMode"
    IMAGE_MOTION_ESTIMATION_RANGE = "imageMotionEstimationRange"
    IMAGE_RESIZE_MODE = "imageResizeMode"
    IMAGE_RETIME_INTERPOLATION = "imageRetimeInterpolation"
    INPUT_DRT_SAT_ROLLOFF_LIMIT = "inputDRTSatRolloffLimit"
    INPUT_DRT_SAT_ROLLOFF_START = "inputDRTSatRolloffStart"
    LIMIT_AUDIO_METER_ALIGN_LEVEL = "limitAudioMeterAlignLevel"
    LIMIT_AUDIO_METER_DISPLAY_MODE = "limitAudioMeterDisplayMode"
    LIMIT_AUDIO_METER_HIGH_LEVEL = "limitAudioMeterHighLevel"
    LIMIT_AUDIO_METER_LUFS = "limitAudioMeterLUFS"
    LIMIT_AUDIO_METER_LOUDNESS_SCALE = "limitAudioMeterLoudnessScale"
    LIMIT_AUDIO_METER_LOW_LEVEL = "limitAudioMeterLowLevel"
    LIMIT_BROADCAST_SAFE_LEVELS = "limitBroadcastSafeLevels"
    LIMIT_BROADCAST_SAFE_ON = "limitBroadcastSafeOn"
    LIMIT_SUBTITLE_CPL = "limitSubtitleCPL"
    LIMIT_SUBTITLE_CAPTION_DURATION_SEC = "limitSubtitleCaptionDurationSec"
    NODE_STACK_LAYERS = "nodeStackLayers"
    OUTPUT_DRT_SAT_ROLLOFF_LIMIT = "outputDRTSatRolloffLimit"
    OUTPUT_DRT_SAT_ROLLOFF_START = "outputDRTSatRolloffStart"
    PERF_AUTO_RENDER_CACHE_AFTER_TIME = "perfAutoRenderCacheAfterTime"
    PERF_AUTO_RENDER_CACHE_COMPOSITE = "perfAutoRenderCacheComposite"
    PERF_AUTO_RENDER_CACHE_ENABLE = "perfAutoRenderCacheEnable"
    PERF_AUTO_RENDER_CACHE_FU_EFFECT = "perfAutoRenderCacheFuEffect"
    PERF_AUTO_RENDER_CACHE_TRANSITION = "perfAutoRenderCacheTransition"
    PERF_CACHE_CLIPS_LOCATION = "perfCacheClipsLocation"
    PERF_OPTIMISED_MEDIA_ON = "perfOptimisedMediaOn"
    PERF_OPTIMIZED_RESOLUTION_RATIO = "perfOptimizedResolutionRatio"
    PERF_PROXY_MEDIA_MODE = "perfProxyMediaMode"
    PERF_PROXY_RESOLUTION_RATIO = "perfProxyResolutionRatio"
    PERF_RENDER_CACHE_MODE = "perfRenderCacheMode"
    PROJECT_MEDIA_LOCATION = "projectMediaLocation"
    SPEAKER_DETECTION = "speakerDetection"
    SUPER_SCALE_NOISE_REDUCTION = "superScaleNoiseReduction"
    SUPER_SCALE_SHARPNESS = "superScaleSharpness"
    TIMELINE_DROP_FRAME_TIMECODE = "timelineDropFrameTimecode"
    TIMELINE_FRAME_RATE_MISMATCH_BEHAVIOR = (
        "timelineFrameRateMismatchBehavior"
    )
    TIMELINE_INPUT_RES_MISMATCH_BEHAVIOR = (
        "timelineInputResMismatchBehavior"
    )
    TIMELINE_INPUT_RES_MISMATCH_CUSTOM_PRESET = (
        "timelineInputResMismatchCustomPreset"
    )
    TIMELINE_INPUT_RES_MISMATCH_USE_CUSTOM_PRESET = (
        "timelineInputResMismatchUseCustomPreset"
    )
    TIMELINE_INTERLACE_PROCESSING = "timelineInterlaceProcessing"
    TIMELINE_OUTPUT_PIXEL_ASPECT_RATIO = "timelineOutputPixelAspectRatio"
    TIMELINE_OUTPUT_RES_MATCH_TIMELINE_RES = (
        "timelineOutputResMatchTimelineRes"
    )
    TIMELINE_OUTPUT_RES_MISMATCH_BEHAVIOR = (
        "timelineOutputResMismatchBehavior"
    )
    TIMELINE_OUTPUT_RES_MISMATCH_CUSTOM_PRESET = (
        "timelineOutputResMismatchCustomPreset"
    )
    TIMELINE_OUTPUT_RES_MISMATCH_USE_CUSTOM_PRESET = (
        "timelineOutputResMismatchUseCustomPreset"
    )
    TIMELINE_OUTPUT_RESOLUTION_HEIGHT = "timelineOutputResolutionHeight"
    TIMELINE_OUTPUT_RESOLUTION_WIDTH = "timelineOutputResolutionWidth"
    TIMELINE_PIXEL_ASPECT_RATIO = "timelinePixelAspectRatio"
    TIMELINE_SAVE_THUMBS_IN_PROJECT = "timelineSaveThumbsInProject"
    TRANSCRIPTION_LANGUAGE = "transcriptionLanguage"
    USE_CA_TRANSFORM = "useCATransform"
    VIDEO_CAPTURE_INGEST_HANDLES = "videoCaptureIngestHandles"
    VIDEO_CAPTURE_MODE = "videoCaptureMode"
    VIDEO_DATA_LEVELS_RETAIN_SUBBLACK_AND_SUPER_WHITE_DATA = (
        "videoDataLevelsRetainSubblockAndSuperWhiteData"
    )
    VIDEO_DECK_ADD_32_PULLDOWN = "videoDeckAdd32Pulldown"
    VIDEO_DECK_BIT_DEPTH = "videoDeckBitDepth"
    VIDEO_DECK_NON_AUTO_EDIT_FRAMES = "videoDeckNonAutoEditFrames"
    VIDEO_DECK_OUTPUT_SYNC_SOURCE = "videoDeckOutputSyncSource"
    VIDEO_DECK_PREROLL_SEC = "videoDeckPrerollSec"
    VIDEO_DECK_SDI_CONFIGURATION = "videoDeckSDIConfiguration"
    VIDEO_DECK_USE_444_SDI = "videoDeckUse444SDI"
    VIDEO_DECK_USE_AUDIO_EDIT = "videoDeckUseAudoEdit"
    VIDEO_DECK_USE_STEREO_SDI = "videoDeckUseStereoSDI"
    VIDEO_MONITOR_BIT_DEPTH = "videoMonitorBitDepth"
    VIDEO_MONITOR_MATRIX_OVERRIDE_FOR_422_SDI = (
        "videoMonitorMatrixOverrideFor422SDI"
    )
    VIDEO_MONITOR_SCALING = "videoMonitorScaling"
    VIDEO_MONITOR_USE_LEVEL_A = "videoMonitorUseLevelA"
    VIDEO_MONITOR_USE_MATRIX_OVERRIDE_FOR_422_SDI = (
        "videoMonitorUseMatrixOverrideFor422SDI"
    )
    VIDEO_MONITOR_USE_STEREO_SDI = "videoMonitorUseStereoSDI"
    VIDEO_PLAYOUT_AUDIO_FRAMES_OFFSET = "videoPlayoutAudioFramesOffset"
    VIDEO_PLAYOUT_BATCH_HEAD_DURATION = "videoPlayoutBatchHeadDuration"
    VIDEO_PLAYOUT_BATCH_TAIL_DURATION = "videoPlayoutBatchTailDuration"
    VIDEO_PLAYOUT_LTC_FRAMES_OFFSET = "videoPlayoutLTCFramesOffset"
    VIDEO_PLAYOUT_MODE = "videoPlayoutMode"
    VIDEO_PLAYOUT_SHOW_LTC = "videoPlayoutShowLTC"
    VIDEO_PLAYOUT_SHOW_SOURCE_TIMECODE = "videoPlayoutShowSourceTimecode"


class SettingToggle(StrEnum):
    """String booleans accepted by Project settings."""

    DISABLED = "0"
    ENABLED = "1"


class ResolutionValue(StrEnum):
    """Common resolution dimensions accepted as setting values."""

    PX_480 = "480"
    PX_486 = "486"
    PX_576 = "576"
    PX_720 = "720"
    PX_858 = "858"
    PX_1152 = "1152"
    PX_1080 = "1080"
    PX_1280 = "1280"
    PX_1332 = "1332"
    PX_1440 = "1440"
    PX_1556 = "1556"
    PX_1716 = "1716"
    PX_1828 = "1828"
    PX_1920 = "1920"
    PX_1998 = "1998"
    PX_2048 = "2048"
    PX_2160 = "2160"
    PX_2560 = "2560"
    PX_2664 = "2664"
    PX_3072 = "3072"
    PX_3112 = "3112"
    PX_3654 = "3654"
    PX_3656 = "3656"
    PX_3840 = "3840"
    PX_3996 = "3996"
    PX_4096 = "4096"
    PX_4320 = "4320"
    PX_7680 = "7680"


class FrameRate(StrEnum):
    """Complete timeline frame-rate values for Resolve 21.0.4."""

    FPS_16 = "16"
    FPS_18 = "18"
    FPS_23_976 = "23.976"
    FPS_24 = "24"
    FPS_25 = "25"
    FPS_29_97 = "29.97"
    FPS_30 = "30"
    FPS_47_952 = "47.952"
    FPS_48 = "48"
    FPS_50 = "50"
    FPS_59_94 = "59.94"
    FPS_60 = "60"
    FPS_72 = "72"
    FPS_90 = "90"
    FPS_95_904 = "95.904"
    FPS_96 = "96"
    FPS_100 = "100"
    FPS_119_88 = "119.88"
    FPS_120 = "120"
    FPS_29_97_DF = "29.97 DF"
    FPS_59_94_DF = "59.94 DF"


class PlaybackFrameRate(StrEnum):
    """Frame-rate values shown by Resolve 21.0.4 Project Settings."""

    FPS_16 = "16"
    FPS_18 = "18"
    FPS_23_976 = "23.976"
    FPS_24 = "24"
    FPS_25 = "25"
    FPS_29_97 = "29.97"
    FPS_30 = "30"
    FPS_47_952 = "47.952"
    FPS_48 = "48"
    FPS_50 = "50"
    FPS_59_94 = "59.94"
    FPS_60 = "60"
    FPS_72 = "72"
    FPS_90 = "90"
    FPS_95_904 = "95.904"
    FPS_96 = "96"
    FPS_100 = "100"
    FPS_119_88 = "119.88"
    FPS_120 = "120"


class SDIConfiguration(StrEnum):
    """SDI link configurations observed in Resolve 21.0.4."""

    NONE = "none"
    SINGLE_LINK = "single_link"
    DUAL_LINK = "dual_link"


class VideoDataLevel(StrEnum):
    """Project and render video data levels."""

    VIDEO = "Video"
    FULL = "Full"


class ColorScienceMode(StrEnum):
    """Project color-science modes accepted by Resolve 21.0.4."""

    DAVINCI_YRGB = "davinciYRGB"
    DAVINCI_YRGB_COLOR_MANAGED = "davinciYRGBColorManagedv2"
    ACES_CC = "acescc"
    ACES_CCT = "acescct"


class ProjectPresetMode(StrEnum):
    """Project color-management preset modes."""

    CUSTOM = "Custom"


class ColorSpace(StrEnum):
    """Complete Custom-mode gamut list verified by Resolve 21.0.4."""

    ACES_AP0 = "ACES (AP0)"
    ACES_AP1 = "ACES (AP1)"
    ADOBE_RGB = "Adobe RGB"
    APPLE_LOG_2 = "Apple Log 2"
    ARRI_WIDE_GAMUT_3 = "ARRI Wide Gamut 3"
    ARRI_WIDE_GAMUT_4 = "ARRI Wide Gamut 4"
    ASTRODESIGN = "AstroDesign"
    BLACKMAGIC_4_6K_FILM_GEN_1 = "Blackmagic Design 4.6K Film Gen 1"
    BLACKMAGIC_4_6K_FILM_GEN_3 = "Blackmagic Design 4.6K Film Gen 3"
    BLACKMAGIC_4K_FILM_GEN_1 = "Blackmagic Design 4K Film Gen 1"
    BLACKMAGIC_4K_FILM_GEN_3 = "Blackmagic Design 4K Film Gen 3"
    BLACKMAGIC_FILM_GEN_1 = "Blackmagic Design Film Gen 1"
    BLACKMAGIC_POCKET_4K_FILM_GEN_4 = (
        "Blackmagic Design Pocket 4K Film Gen 4"
    )
    BLACKMAGIC_VIDEO_GAMUT_GEN_4 = "Blackmagic Design Video Gamut Gen 4"
    BLACKMAGIC_VIDEO_GEN_5 = "Blackmagic Design Video Gen 5"
    BLACKMAGIC_WIDE_GAMUT_GEN_4_5 = (
        "Blackmagic Design Wide Gamut Gen 4 / 5"
    )
    CANON_CINEMA_GAMUT = "Canon Cinema Gamut"
    DAVINCI_WG = "DaVinci WG"
    DCI_XYZ = "DCI XYZ"
    DJI_D_GAMUT = "DJI D-Gamut"
    DRAGONCOLOR = "DRAGONcolor"
    DRAGONCOLOR2 = "DRAGONcolor2"
    FUJIFILM_F_GAMUT_C = "Fujifilm F-Gamut C"
    HSL = "HSL"
    HSV = "HSV"
    LAB_CIE = "Lab (CIE)"
    P3_D60 = "P3-D60"
    P3_D65 = "P3-D65"
    P3_DCI = "P3-DCI"
    PANASONIC_V_GAMUT = "Panasonic V-Gamut"
    REC_709 = "Rec.709"
    REC_2020 = "Rec.2020"
    RED_COLOR_2 = "REDcolor2"
    RED_COLOR_3 = "REDcolor3"
    RED_COLOR_4 = "REDcolor4"
    RED_WIDE_GAMUT_RGB = "REDWideGamutRGB"
    SMPTE_C = "SMPTE-C"
    SONY_S_GAMUT = "Sony S-Gamut"
    SONY_S_GAMUT3 = "Sony S-Gamut3"
    SONY_S_GAMUT3_CINE = "Sony S-Gamut3.Cine"
    SRGB = "sRGB"
    XYZ_CIE = "XYZ (CIE)"
    YUV = "Y'UV"


class InputColorSpaceMode(StrEnum):
    """Input-only UI labels in Custom mode (not accepted by SetSetting)."""

    SAME_AS_TIMELINE = "Same as Timeline"


# Output color space omits the four working/model spaces that Resolve exposes
# only in the Input and Timeline dropdowns.
OUTPUT_COLOR_SPACES = tuple(
    value
    for value in ColorSpace
    if value
    not in {
        ColorSpace.HSL,
        ColorSpace.HSV,
        ColorSpace.LAB_CIE,
        ColorSpace.YUV,
    }
)


class Gamma(StrEnum):
    """Complete Custom-mode gamma list verified by Resolve 21.0.4."""

    ACES_CC = "ACEScc"
    ACES_CCT = "ACEScct"
    ADOBE_RGB = "Adobe RGB"
    APPLE_LOG = "Apple Log"
    ARIB_STD_B67_HLG = "ARIB STD-B67 HLG"
    ARRI_LOG_C3 = "ARRI LogC3"
    ARRI_LOG_C4 = "ARRI LogC4"
    ASTRODESIGN_A_LOG = "AstroDesign A-Log"
    BLACKMAGIC_4_6K_FILM = "Blackmagic Design 4.6K Film"
    BLACKMAGIC_4K_FILM = "Blackmagic Design 4K Film"
    BLACKMAGIC_BROADCAST_FILM_GEN_4 = (
        "Blackmagic Design Broadcast Film Gen 4"
    )
    BLACKMAGIC_EXTENDED_VIDEO_GEN_4 = (
        "Blackmagic Design Extended Video Gen 4"
    )
    BLACKMAGIC_EXTENDED_VIDEO_GEN_5 = (
        "Blackmagic Design Extended Video Gen 5"
    )
    BLACKMAGIC_FILM = "Blackmagic Design Film"
    BLACKMAGIC_FILM_GEN_5 = "Blackmagic Design Film Gen 5"
    BLACKMAGIC_POCKET_4K_FILM_GEN_4 = (
        "Blackmagic Design Pocket 4K Film Gen 4"
    )
    BLACKMAGIC_POCKET_6K_FILM_GEN_4 = (
        "Blackmagic Design Pocket 6K Film Gen 4"
    )
    BLACKMAGIC_VIDEO = "Blackmagic Design Video"
    BLACKMAGIC_VIDEO_GEN_3 = "Blackmagic Design Video Gen 3"
    BLACKMAGIC_VIDEO_GEN_4 = "Blackmagic Design Video Gen 4"
    BLACKMAGIC_VIDEO_GEN_5 = "Blackmagic Design Video Gen 5"
    CANON_LOG = "Canon Log"
    CANON_LOG_2 = "Canon Log 2"
    CANON_LOG_3 = "Canon Log 3"
    CINEON_FILM_LOG = "Cineon Film Log"
    DAVINCI_INTERMEDIATE = "DaVinci Intermediate"
    DCI = "DCI"
    DJI_D_LOG = "DJI D-Log"
    FUJIFILM_F_LOG = "Fujifilm F-Log"
    FUJIFILM_F_LOG2 = "Fujifilm F-Log2"
    GAMMA_2_2 = "Gamma 2.2"
    GAMMA_2_4 = "Gamma 2.4"
    GAMMA_2_5 = "Gamma 2.5"
    GAMMA_2_6 = "Gamma 2.6"
    INSTA360_I_LOG = "Insta360 I-Log"
    LEICA_L_LOG = "Leica L-Log"
    LINEAR = "Linear"
    NIKON_N_LOG = "Nikon N-Log"
    PANASONIC_V_LOG = "Panasonic V-Log"
    REC_709 = "Rec.709"
    REC_709_A = "Rec.709-A"
    REC_2100_HLG = "Rec.2100 HLG"
    REC_2100_HLG_SCENE = "Rec.2100 HLG (Scene)"
    REC_2100_ST2084 = "Rec.2100 ST2084"
    REC_2100_ST2084_SCENE = "Rec.2100 ST2084 (Scene)"
    RED_LOG3G10 = "RED Log3G10"
    RED_GAMMA_3 = "REDgamma3"
    RED_GAMMA_4 = "REDgamma4"
    RED_LOG_FILM = "REDlogFilm"
    SAMSUNG_LOG = "Samsung Log"
    SONY_S_LOG = "S-Log"
    SONY_S_LOG2 = "S-Log2"
    SONY_S_LOG3 = "S-Log3"
    SRGB = "sRGB"
    ST2084 = "ST2084"
    ST2084_300_NIT = "ST2084 300 nit"
    ST2084_500_NIT = "ST2084 500 nit"
    ST2084_800_NIT = "ST2084 800 nit"
    ST2084_1000_NIT = "ST2084 1000 nit"
    ST2084_2000_NIT = "ST2084 2000 nit"
    ST2084_3000_NIT = "ST2084 3000 nit"
    ST2084_4000_NIT = "ST2084 4000 nit"
    STOPS_18_PERCENT_GRAY = "Stops (18% Gray)"


class ColorSpaceGamma(StrEnum):
    """Combined color-space and gamma values verified by readback."""

    REC_709_A = "Rec.709-A"
    REC_709_SCENE = "Rec.709 (Scene)"
    REC_709_GAMMA_2_2 = "Rec.709 Gamma 2.2"
    REC_709_GAMMA_2_4 = "Rec.709 Gamma 2.4"
    LINEAR = "Linear"
    DAVINCI_WIDE_GAMUT_INTERMEDIATE = "DaVinci WG/Intermediate"


class AcesInputTransform(StrEnum):
    """Stable ACES input-transform values."""

    NONE = "No Input Transform"


class AcesOutputTransform(StrEnum):
    """ACES output transforms verified by Resolve 21.0.4 readback."""

    NONE = "No Output Transform"
    P3_D65_ST2084_108_NIT = "P3-D65 ST2084 (108 nit)"
    P3_D65_ST2084_1000_NIT = "P3-D65 ST2084 (1000 nit)"
    P3_D65_ST2084_4000_NIT = "P3-D65 ST2084 (4000 nit)"
    REC_2100_ST2084_1000_NIT = "Rec.2100 ST2084 (1000 nit)"


class WorkingLuminanceMode(StrEnum):
    """Complete Timeline working luminance list in Custom processing mode."""

    SDR_100 = "SDR 100"
    HDR_500 = "HDR 500"
    HDR_1000 = "HDR 1000"
    HDR_2000 = "HDR 2000"
    HDR_4000 = "HDR 4000"
    SDR_ER_100_200 = "SDR ER 100/200"
    HDR_ER_1000_2000 = "HDR ER 1000/2000"
    HDR_ER_1000_4000 = "HDR ER 1000/4000"
    HDR_ER_1000_10000 = "HDR ER 1000/10000"
    HDR_ER_4000_10000 = "HDR ER 4000/10000"
    CUSTOM = "Custom"


TIMELINE_WORKING_LUMINANCE_MIN_NITS = 48
TIMELINE_WORKING_LUMINANCE_MAX_NITS = 10_000


class ResizeTransformation(StrEnum):
    """Resize-transformation working spaces verified by Resolve 21.0.4."""

    TIMELINE = "Timeline"
    LOG = "Log"
    LINEAR = "Linear"
    LINEAR_TONE_MAPPED = "Linear - Tone Mapped"
    GAMMA = "Gamma"
    GAMMA_TONE_MAPPED = "Gamma - Tone Mapped"


class DynamicRangeTransform(StrEnum):
    """Input and output DRT values verified by Resolve 21.0.4 readback."""

    NONE = "None"
    SIMPLE = "Simple"
    LUMINANCE_MAPPING = "Luminance Mapping"
    DAVINCI = "DaVinci"
    SATURATION_PRESERVING = "Saturation Preserving"


class ClipProperty(StrEnum):
    """Media Pool clip property names migrated from the legacy library."""

    INPUT_COLOR_SPACE = "Input Color Space"
    INPUT_GAMMA = "Input Gamma"


class GeneratorName(StrEnum):
    """Common Resolve generator names."""

    SOLID_COLOR = "Solid Color"
    WINDOW = "Window"


class RenderFormat(StrEnum):
    """Render format identifiers reported by Resolve Studio 21.0.4.5."""

    AVI = "avi"
    BRAW = "braw"
    CINEON = "cin"
    DCP = "dcp"
    QUICKTIME = "mov"
    MP4 = "mp4"
    EXR = "exr"
    DPX = "dpx"
    TIFF = "tif"
    PNG = "png"
    GIF = "gif"
    HLS = "m3u8"
    IMF = "imf"
    JPEG = "jpg"
    JPEG_2000 = "j2c"
    MJ2 = "mj2"
    MKV = "mkv"
    MTS = "mts"
    MXF_OP_ATOM = "mxf"
    MXF_OP1A = "mxf_op1a"
    PANASONIC_AVC = "pavc"
    WAVE = "wav"
    WEBP = "webp"


class VideoCodec(StrEnum):
    """Common codec identifiers to validate against the current Resolve host."""

    PRORES_422 = "ProRes422"
    PRORES_422_HQ = "ProRes422HQ"
    PRORES_422_LT = "ProRes422LT"
    PRORES_422_PROXY = "ProRes422P"
    PRORES_4444 = "ProRes4444"
    PRORES_4444_XQ = "ProRes4444XQ"
    DNXHR_444_10 = "DNxHR444_10"
    DNXHR_444_12 = "DNxHR444_12"
    DNXHR_HQ = "DNxHRHQ"
    DNXHR_HQX_10 = "DNxHRHQX_10"
    DNXHR_HQX_12 = "DNxHRHQX_12"
    H264 = "H264"
    H264_NVIDIA = "H264_NVIDIA"
    H265 = "H265"
    H265_NVIDIA = "H265_NVIDIA"
    RGB_8 = "RGB8"
    RGB_8_LZW = "RGB8LZW"
    RGB_10 = "RGB10"
    RGB_12 = "RGB12"
    RGB_16 = "RGB16"
    RGB_16_LZW = "RGB16LZW"
    XYZ_16 = "XYZ16"
    XYZ_16_LZW = "XYZ16LZW"
    RGB_FLOAT = "RGBFloat"
    RGB_FLOAT_DWAA = "RGBFloatDWAA"
    RGB_FLOAT_DWAB = "RGBFloatDWAB"
    RGB_FLOAT_PIZ = "RGBFloatPIZ"
    RGB_FLOAT_RLE = "RGBFloatRLE"
    RGB_FLOAT_ZIP = "RGBFloatZIP"
    RGB_HALF = "RGBHalf"
    RGB_HALF_DWAA = "RGBHalfDWAA"
    RGB_HALF_DWAB = "RGBHalfDWAB"
    RGB_HALF_PIZ = "RGBHalfPIZ"
    RGB_HALF_RLE = "RGBHalfRLE"
    RGB_HALF_ZIP = "RGBHalfZIP"
    APV_YUV422_10 = "APVYUV422_10"
    ARGB_8 = "ARGB8"
    AV1_YUV420_10_NVIDIA = "AV1YUV420_10_NVIDIA"
    AV1_YUV420_8_NVIDIA = "AV1YUV420_8_NVIDIA"
    ANIMATED_GIF = "Animated_GIF"
    ANIMATED_WEBP = "Animated_WEBP"
    BGRA_8 = "BGRA8"
    DNX_HD_1080I_100 = "DNxHD1080i100"
    DNX_HD_1080I_145 = "DNxHD1080i145"
    DNX_HD_1080I_220 = "DNxHD1080i220"
    DNX_HD_1080I_220_10 = "DNxHD1080i220_10"
    DNX_HD_1080P_100 = "DNxHD1080p100"
    DNX_HD_1080P_145 = "DNxHD1080p145"
    DNX_HD_1080P_220 = "DNxHD1080p220"
    DNX_HD_1080P_220_10 = "DNxHD1080p220_10"
    DNX_HD_1080P_36 = "DNxHD1080p36"
    DNX_HD_1080P_444_10 = "DNxHD1080p440"
    DNX_HD_720P_100 = "DNxHD720p100"
    DNX_HD_720P_145 = "DNxHD720p145"
    DNX_HD_720P_220 = "DNxHD720p220"
    DNX_HD_720P_220_10 = "DNxHD720p220_10"
    DNX_HD_THIN_RASTER_1080I_145 = "DNxHDTR1080i145"
    DNX_HR_LB = "DNxHRLB"
    DNX_HR_SQ = "DNxHRSQ"
    DNX_UNCOMP_RGB_10 = "DNxUncomp_RGB_10"
    DNX_UNCOMP_RGB_12 = "DNxUncomp_RGB_12"
    DNX_UNCOMP_RGB_8 = "DNxUncomp_RGB_8"
    DNX_UNCOMP_RGB_FLOAT = "DNxUncomp_RGB_Float"
    DNX_UNCOMP_RGB_HALF = "DNxUncomp_RGB_Half"
    DNX_UNCOMP_YUV422_10 = "DNxUncomp_YUV422_10"
    DNX_UNCOMP_YUV422_12 = "DNxUncomp_YUV422_12"
    DNX_UNCOMP_YUV422_8 = "DNxUncomp_YUV422_8"
    DNX_UNCOMP_YUV422_FLOAT = "DNxUncomp_YUV422_Float"
    DNX_UNCOMP_YUV422_HALF = "DNxUncomp_YUV422_Half"
    FFV1_INTRA_RGBA_16 = "FFV1IntraRGBA_16"
    FFV1_INTRA_RGBA_8 = "FFV1IntraRGBA_8"
    FFV1_INTRA_YUV422_10 = "FFV1IntraYUV422_10"
    FFV1_INTRA_YUV422_8 = "FFV1IntraYUV422_8"
    FFV1_RGBA_16 = "FFV1RGBA_16"
    FFV1_RGBA_8 = "FFV1RGBA_8"
    FFV1_YUV420_10 = "FFV1YUV420_10"
    FFV1_YUV420_8 = "FFV1YUV420_8"
    FFV1_YUV422_10 = "FFV1YUV422_10"
    FFV1_YUV422_12 = "FFV1YUV422_12"
    FFV1_YUV422_8 = "FFV1YUV422_8"
    GV_HQ_1280X1080 = "GVHQ1280x1080"
    GV_HQ_1280X720 = "GVHQ1280x720"
    GV_HQ_1280X960 = "GVHQ1280x960"
    GV_HQ_1440X1080 = "GVHQ1440x1080"
    GV_HQ_1920X1080 = "GVHQ1920x1080"
    GV_HQ_720X480 = "GVHQ720x480"
    GV_HQ_720X486 = "GVHQ720x486"
    GV_HQ_720X576 = "GVHQ720x576"
    GV_HQX = "GVHQX"
    GOPRO_RGB_16 = "GoProRGB16"
    GOPRO_YUV_10 = "GoProYUV10"
    GRAY_8 = "Gray8"
    H264_AMD = "H264_AMD"
    H265_AMD = "H265_AMD"
    KAKADU_JPEG_2000_2K_DCI = "KJP2K_2KDCI"
    KAKADU_JPEG_2000_2K_DCI_FLAT = "KJP2K_2KDCI_Flat"
    KAKADU_JPEG_2000_2K_DCI_SCOPE = "KJP2K_2KDCI_Scope"
    KAKADU_JPEG_2000_4K_DCI = "KJP2K_4KDCI"
    KAKADU_JPEG_2000_4K_DCI_FLAT = "KJP2K_4KDCI_Flat"
    KAKADU_JPEG_2000_4K_DCI_SCOPE = "KJP2K_4KDCI_Scope"
    KAKADU_JPEG_2000_DCI = "KJP2K_DCI"
    KAKADU_JPEG_2000_DCI_FLAT = "KJP2K_DCI_Flat"
    KAKADU_JPEG_2000_DCI_SCOPE = "KJP2K_DCI_Scope"
    KAKADU_JPEG_2000_DOLBY_VISION_2K = "KJP2K_DV_2K"
    KAKADU_JPEG_2000_DOLBY_VISION_4K = "KJP2K_DV_4K"
    KAKADU_JPEG_2000_DOLBY_VISION_HD = "KJP2K_DV_HD"
    KAKADU_JPEG_2000_DOLBY_VISION_UHD = "KJP2K_DV_UHD"
    KAKADU_JPEG_2000_RGB = "KJP2K_RGB"
    KAKADU_JPEG_2000_RGB_10 = "KJP2K_RGB10"
    KAKADU_JPEG_2000_RGB_12 = "KJP2K_RGB12"
    KAKADU_JPEG_2000_RGB_8 = "KJP2K_RGB8"
    KAKADU_JPEG_2000_RGB_2K = "KJP2K_RGB_2K"
    KAKADU_JPEG_2000_RGB_4K = "KJP2K_RGB_4K"
    KAKADU_JPEG_2000_RGB_HD = "KJP2K_RGB_HD"
    KAKADU_JPEG_2000_RGB_UHD = "KJP2K_RGB_UHD"
    KAKADU_JPEG_2000_YUV422_10 = "KJP2K_YUV422_10"
    KAKADU_JPEG_2000_YUV422_12 = "KJP2K_YUV422_12"
    KAKADU_JPEG_2000_YUV422_2K = "KJP2K_YUV422_2K"
    KAKADU_JPEG_2000_YUV422_8 = "KJP2K_YUV422_8"
    KAKADU_JPEG_2000_YUV422_HD = "KJP2K_YUV422_HD"
    KAKADU_JPEG_2000_YUV422_UHD = "KJP2K_YUV422_UHD"
    KAKADU_JPEG_2000_YUV444_10 = "KJP2K_YUV444_10"
    KAKADU_JPEG_2000_YUV444_12 = "KJP2K_YUV444_12"
    KAKADU_JPEG_2000_YUV444_8 = "KJP2K_YUV444_8"
    KAKADU_JPEG_2000_4K_GENERIC_DCI = "KJP4K_DCI"
    KAKADU_JPEG_2000_4K_GENERIC_DCI_FLAT = "KJP4K_DCI_Flat"
    KAKADU_JPEG_2000_4K_GENERIC_DCI_SCOPE = "KJP4K_DCI_Scope"
    KAKADU_JPEG_2000_IMF_RGB = "KJPIMF_RGB"
    KAKADU_JPEG_2000_IMF_XYZ = "KJPIMF_XYZ"
    KAKADU_JPEG_2000_IMF_YUV422 = "KJPIMF_YUV422"
    MPEG2_422 = "MPEG2_422"
    MPEG2_MAIN = "MPEG2_Main"
    MPEG4_VIDEO = "MPEG4"
    NTSC_AVID_8 = "NTSCAvid8"
    PAL_AVID_8 = "PALAvid8"
    PHOTO_JPEG_YUV420 = "PJPEG"
    PHOTO_JPEG_YUV422 = "PJPEGYUV422"
    PHOTO_JPEG_YUV444 = "PJPEGYUV444"
    PANASONIC_AVC_INTRA_1080_C100 = "PanasonicAVCIntra_1080_C100"
    PANASONIC_AVC_INTRA_1080_C200 = "PanasonicAVCIntra_1080_C200"
    PANASONIC_AVC_INTRA_1080_C50 = "PanasonicAVCIntra_1080_C50"
    PANASONIC_AVC_INTRA_2K_C100 = "PanasonicAVCIntra_2k_C100"
    PANASONIC_AVC_INTRA_4K_C100 = "PanasonicAVCIntra_4k_C100"
    PANASONIC_AVC_INTRA_720P_C100 = "PanasonicAVCIntra_720p_C100"
    PANASONIC_AVC_INTRA_720P_C200 = "PanasonicAVCIntra_720p_C200"
    PANASONIC_AVC_INTRA_720P_C50 = "PanasonicAVCIntra_720p_C50"
    PANASONIC_AVC_INTRA_8K = "PanasonicAVCIntra_8k"
    PANASONIC_AVC_INTRA_QFHD_C100 = "PanasonicAVCIntra_qfhd_C100"
    PANASONIC_P2_AVC_INTRA_1080_C100 = "PanasonicP2AVCIntra_1080_C100"
    PANASONIC_P2_AVC_INTRA_1080_C50 = "PanasonicP2AVCIntra_1080_C50"
    RGB_1080I_AVID_10_A = "RGB1080iAvid10A"
    RGB_1080P_AVID_10_A = "RGB1080pAvid10A"
    RGBA_8 = "RGBA8"
    RGB_FLOAT_ZIP1 = "RGBFloatZIP1"
    RGB_HALF_ZIP1 = "RGBHalfZIP1"
    SONY_XAVC_INTRA_CBG_100_1280X720 = "SonyXAVCIC100_1280x720"
    SONY_XAVC_INTRA_CBG_100_1920X1080 = "SonyXAVCIC100_1920x1080"
    SONY_XAVC_INTRA_CBG_100_2048X1080 = "SonyXAVCIC100_2048x1080"
    SONY_XAVC_INTRA_CBG_300_3840X2160 = "SonyXAVCIC300_3840x2160"
    SONY_XAVC_INTRA_CBG_300_4096X2160 = "SonyXAVCIC300_4096x2160"
    SONY_XAVC_INTRA_CBG_480_3840X2160 = "SonyXAVCIC480_3840x2160"
    SONY_XAVC_INTRA_CBG_480_4096X2160 = "SonyXAVCIC480_4096x2160"
    SONY_XAVC_INTRA_CBG_50_1440X1080 = "SonyXAVCIC50_1440x1080"
    SONY_XAVC_INTRA_VBR_100_2048X1080 = "SonyXAVCIV100_2048x1080"
    SONY_XAVC_INTRA_VBR_300_3840X2160 = "SonyXAVCIV300_3840x2160"
    SONY_XAVC_INTRA_VBR_300_4096X2160 = "SonyXAVCIV300_4096x2160"
    SONY_XAVC_INTRA_VBR_480_3840X2160 = "SonyXAVCIV480_3840x2160"
    SONY_XAVC_INTRA_VBR_480_4096X2160 = "SonyXAVCIV480_4096x2160"
    SONY_XAVC_LONG_10BIT_100_3840X2160 = "SonyXAVC_10bit_LONG_100_3840x2160"
    SONY_XAVC_LONG_10BIT_140_3840X2160 = "SonyXAVC_10bit_LONG_140_3840x2160"
    SONY_XAVC_LONG_10BIT_200_3840X2160 = "SonyXAVC_10bit_LONG_200_3840x2160"
    SONY_XAVC_LONG_10BIT_25_1920X1080 = "SonyXAVC_10bit_LONG_25_1920x1080"
    SONY_XAVC_LONG_10BIT_35_1920X1080 = "SonyXAVC_10bit_LONG_35_1920x1080"
    SONY_XAVC_LONG_10BIT_50_1280X720 = "SonyXAVC_10bit_LONG_50_1280x720"
    SONY_XAVC_LONG_10BIT_50_1920X1080 = "SonyXAVC_10bit_LONG_50_1920x1080"
    SONY_XAVC_LONG_8BIT_100_3840X2160 = "SonyXAVC_8bit_LONG_100_3840x2160"
    SONY_XAVC_LONG_8BIT_150_3840X2160 = "SonyXAVC_8bit_LONG_150_3840x2160"
    SONY_XAVC_LONG_8BIT_60_3840X2160 = "SonyXAVC_8bit_LONG_60_3840x2160"
    SONY_XAVC_S_LONG_8BIT_100A_3840X2160 = (
        "SonyXAVC_S_8bit_LONG_100A_3840x2160"
    )
    SONY_XAVC_S_LONG_8BIT_100_3840X2160 = (
        "SonyXAVC_S_8bit_LONG_100_3840x2160"
    )
    SONY_XAVC_S_LONG_8BIT_150_3840X2160 = (
        "SonyXAVC_S_8bit_LONG_150_3840x2160"
    )
    SONY_XAVC_S_LONG_8BIT_50_1920X1080 = (
        "SonyXAVC_S_8bit_LONG_50_1920x1080"
    )
    SONY_XAVC_S_LONG_8BIT_60A_3840X2160 = (
        "SonyXAVC_S_8bit_LONG_60A_3840x2160"
    )
    SONY_XAVC_S_LONG_8BIT_60_3840X2160 = (
        "SonyXAVC_S_8bit_LONG_60_3840x2160"
    )
    XDCAM_MPEG2 = "XDMPEG2"
    XDCAM_MPEG2_TAPE = "XDMPEG2_TAPE"
    YUV_1080I_AVID_8 = "YUV1080iAvid8"
    YUV420_8 = "YUV420_8"
    YUV422_10 = "YUV422_10"
    YUV422_8 = "YUV422_8"
    YUV444_8 = "YUV444_8"
    EASY_DCP_2K_DCI = "easyDCP2KDCI"
    EASY_DCP_2K_DCI_FLAT = "easyDCP2KDCI_Flat"
    EASY_DCP_2K_DCI_SCOPE = "easyDCP2KDCI_Scope"
    EASY_DCP_4K_DCI = "easyDCP4KDCI"
    EASY_DCP_4K_DCI_FLAT = "easyDCP4KDCI_Flat"
    EASY_DCP_4K_DCI_SCOPE = "easyDCP4KDCI_Scope"
    EASY_DCP_RGB = "easyDCP_RGB"
    EASY_DCP_YUV422 = "easyDCP_YUV422"


class UniqueFilenameStyle(IntEnum):
    """Render collision filename styles documented by Resolve 21.0.4."""

    PREFIX = 0
    SUFFIX = 1


class VideoQuality(StrEnum):
    """Named render quality levels documented by Resolve 21.0.4."""

    LEAST = "Least"
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    BEST = "Best"


VIDEO_QUALITY_AUTOMATIC = 0


class AudioCodec(StrEnum):
    """Common render audio codec identifiers."""

    LINEAR_PCM = "lpcm"
    AAC = "aac"
    MP3 = "mp3"


class AudioBitDepth(IntEnum):
    """Common render audio bit depths."""

    BIT_16 = 16
    BIT_24 = 24


class AudioSampleRate(IntEnum):
    """Common render audio sample rates."""

    HZ_44100 = 44100
    HZ_48000 = 48000


class SuperScale(IntEnum):
    """Project Super Scale values documented by Resolve 21.0.4."""

    AUTO = 0
    OFF = 1
    X2 = 2
    X3 = 3
    X4 = 4


class PixelAspectRatio(StrEnum):
    """Render pixel aspect ratios documented by Resolve 21.0.4."""

    SD_16_9 = "16_9"
    SD_4_3 = "4_3"
    SQUARE = "square"
    CINEMASCOPE = "cinemascope"


class AlphaMode(IntEnum):
    """Render alpha modes documented by Resolve 21.0.4."""

    PREMULTIPLIED = 0
    STRAIGHT = 1


class SubtitleFormat(StrEnum):
    """Render subtitle formats documented by Resolve 21.0.4."""

    BURN_IN = "BurnIn"
    EMBEDDED_CAPTIONS = "EmbeddedCaptions"
    SEPARATE_FILE = "SeparateFile"


STILL_SEQUENCE_FORMATS = frozenset(
    {RenderFormat.EXR, RenderFormat.DPX, RenderFormat.TIFF, RenderFormat.PNG}
)


BT2100_PROJECT_SETTINGS = MappingProxyType(
    {
        ProjectSetting.TIMELINE_RESOLUTION_WIDTH: ResolutionValue.PX_1920,
        ProjectSetting.TIMELINE_RESOLUTION_HEIGHT: ResolutionValue.PX_1080,
        ProjectSetting.TIMELINE_FRAME_RATE: FrameRate.FPS_24,
        ProjectSetting.VIDEO_MONITOR_FORMAT: "HD 1080p 24",
        ProjectSetting.VIDEO_MONITOR_USE_444_SDI: SettingToggle.DISABLED,
        ProjectSetting.VIDEO_MONITOR_SDI_CONFIGURATION: (
            SDIConfiguration.SINGLE_LINK
        ),
        ProjectSetting.VIDEO_DATA_LEVELS: VideoDataLevel.VIDEO,
        ProjectSetting.VIDEO_MONITOR_USE_HDR_OVER_HDMI: SettingToggle.ENABLED,
        ProjectSetting.COLOR_SCIENCE_MODE: (
            ColorScienceMode.DAVINCI_YRGB_COLOR_MANAGED
        ),
        ProjectSetting.RCM_PRESET_MODE: ProjectPresetMode.CUSTOM,
        ProjectSetting.SEPARATE_COLOR_SPACE_AND_GAMMA: SettingToggle.ENABLED,
        ProjectSetting.COLOR_SPACE_INPUT: ColorSpace.REC_2020,
        ProjectSetting.COLOR_SPACE_INPUT_GAMMA: Gamma.ST2084,
        ProjectSetting.COLOR_SPACE_TIMELINE: ColorSpace.REC_2020,
        ProjectSetting.COLOR_SPACE_TIMELINE_GAMMA: Gamma.ST2084,
        ProjectSetting.COLOR_SPACE_OUTPUT: ColorSpace.REC_2020,
        ProjectSetting.COLOR_SPACE_OUTPUT_GAMMA: Gamma.ST2084,
        ProjectSetting.TIMELINE_WORKING_LUMINANCE: "10000",
        ProjectSetting.TIMELINE_WORKING_LUMINANCE_MODE: (
            WorkingLuminanceMode.CUSTOM
        ),
        ProjectSetting.INPUT_DRT: DynamicRangeTransform.NONE,
        ProjectSetting.OUTPUT_DRT: DynamicRangeTransform.NONE,
        ProjectSetting.HDR_MASTERING_LUMINANCE_MAX: "1000",
        ProjectSetting.HDR_MASTERING_ON: SettingToggle.ENABLED,
    }
)


SUPPORTED_RESOLVE_VERSION = (21, 0, 4)
