"""Stable values used by the DaVinci Resolve scripting API."""

from enum import StrEnum


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


class RenderFormat(StrEnum):
    """Common render format identifiers accepted by Resolve."""

    QUICKTIME = "mov"
    MP4 = "mp4"
    EXR = "exr"
    DPX = "dpx"
    TIFF = "tif"
    PNG = "png"


class VideoCodec(StrEnum):
    """Common codec identifiers to validate against the current Resolve host."""

    PRORES_4444 = "ProRes4444"
    PRORES_4444_XQ = "ProRes4444XQ"
    H264 = "H264"
    H265 = "H265"


SUPPORTED_RESOLVE_VERSION = (21, 0, 4)

