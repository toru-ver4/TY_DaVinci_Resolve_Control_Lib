"""Typing facade for Resolve-hosted Fusion helpers."""

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any, Literal, overload

from .connection import ResolveSession
from .fusion_tool_constants import FusionModifier, FusionResolveFxTool, FusionTool
from .fusion_tool_types import *

PACKAGED_DURATION_MEDIA_DIRECTORY: Path

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.ACES_TRANSFORM],
    position: Sequence[float] = ...,
) -> ACESTransformTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.ALPHA_DIVIDE],
    position: Sequence[float] = ...,
) -> AlphaDivideTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.ALPHA_MULTIPLY],
    position: Sequence[float] = ...,
) -> AlphaMultiplyTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.ANAGLYPH],
    position: Sequence[float] = ...,
) -> AnaglyphTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.AUTO_DOMAIN],
    position: Sequence[float] = ...,
) -> AutoDomainTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.AUTO_GAIN],
    position: Sequence[float] = ...,
) -> AutoGainTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.BACKGROUND],
    position: Sequence[float] = ...,
) -> BackgroundTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.BENDER_3D],
    position: Sequence[float] = ...,
) -> Bender3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.BETTER_RESIZE],
    position: Sequence[float] = ...,
) -> BetterResizeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.BITMAP_MASK],
    position: Sequence[float] = ...,
) -> BitmapMaskTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.BLUR],
    position: Sequence[float] = ...,
) -> BlurTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.BRIGHTNESS_CONTRAST],
    position: Sequence[float] = ...,
) -> BrightnessContrastTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.BUMP_MAP],
    position: Sequence[float] = ...,
) -> BumpMapTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.B_SPLINE_MASK],
    position: Sequence[float] = ...,
) -> BSplineMaskTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CAMERA_3D],
    position: Sequence[float] = ...,
) -> Camera3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CAMERA_SHAKE],
    position: Sequence[float] = ...,
) -> CameraShakeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CHANGE_DEPTH],
    position: Sequence[float] = ...,
) -> ChangeDepthTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CHANNEL_BOOLEAN],
    position: Sequence[float] = ...,
) -> ChannelBooleanTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CHROMATIC_ABERRATION_REMOVAL],
    position: Sequence[float] = ...,
) -> ChromaticAberrationRemovalTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CHROMATIC_ADAPTATION],
    position: Sequence[float] = ...,
) -> ChromaticAdaptationTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CHROMA_KEYER],
    position: Sequence[float] = ...,
) -> ChromaKeyerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CINEON_LOG],
    position: Sequence[float] = ...,
) -> CineonLogTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CLEAN_PLATE],
    position: Sequence[float] = ...,
) -> CleanPlateTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.COLOR_CORRECTOR],
    position: Sequence[float] = ...,
) -> ColorCorrectorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.COLOR_CURVES],
    position: Sequence[float] = ...,
) -> ColorCurvesTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.COLOR_GAIN],
    position: Sequence[float] = ...,
) -> ColorGainTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.COLOR_SPACE],
    position: Sequence[float] = ...,
) -> ColorSpaceTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.COLOR_SPACE_TRANSFORM],
    position: Sequence[float] = ...,
) -> ColorSpaceTransformTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.COMBINER],
    position: Sequence[float] = ...,
) -> CombinerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.COORD_SPACE],
    position: Sequence[float] = ...,
) -> CoordSpaceTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CORNER_POSITIONER],
    position: Sequence[float] = ...,
) -> CornerPositionerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CREATE_BUMP_MAP],
    position: Sequence[float] = ...,
) -> CreateBumpMapTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CREATE_RELIEF_MAP],
    position: Sequence[float] = ...,
) -> CreateReliefMapTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CROP],
    position: Sequence[float] = ...,
) -> CropTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CRYPTOMATTE],
    position: Sequence[float] = ...,
) -> CryptomatteTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CUBE_3D],
    position: Sequence[float] = ...,
) -> Cube3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CUBE_MAP],
    position: Sequence[float] = ...,
) -> CubeMapTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CUSTOM],
    position: Sequence[float] = ...,
) -> CustomTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CUSTOM_COLOR_MATRIX],
    position: Sequence[float] = ...,
) -> CustomColorMatrixTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CUSTOM_FILTER],
    position: Sequence[float] = ...,
) -> CustomFilterTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.CUSTOM_VERTEX_3D],
    position: Sequence[float] = ...,
) -> CustomVertex3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DAY_SKY],
    position: Sequence[float] = ...,
) -> DaySkyTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DEEP_TO_IMAGE],
    position: Sequence[float] = ...,
) -> DeepToImageTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DEEP_TO_POINTS],
    position: Sequence[float] = ...,
) -> DeepToPointsTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DEFOCUS],
    position: Sequence[float] = ...,
) -> DefocusTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DELTA_KEYER],
    position: Sequence[float] = ...,
) -> DeltaKeyerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DENT],
    position: Sequence[float] = ...,
) -> DentTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DEPTH_BLUR],
    position: Sequence[float] = ...,
) -> DepthBlurTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DEPTH_MAP],
    position: Sequence[float] = ...,
) -> DepthMapTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIFFERENCE_KEYER],
    position: Sequence[float] = ...,
) -> DifferenceKeyerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIMENSION_CAMERA_TRACKER],
    position: Sequence[float] = ...,
) -> DimensionCameraTrackerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIMENSION_COPY_AUX],
    position: Sequence[float] = ...,
) -> DimensionCopyAuxTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIMENSION_DISPARITY],
    position: Sequence[float] = ...,
) -> DimensionDisparityTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIMENSION_DISPARITY_TO_Z],
    position: Sequence[float] = ...,
) -> DimensionDisparityToZTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIMENSION_GLOBAL_ALIGN],
    position: Sequence[float] = ...,
) -> DimensionGlobalAlignTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIMENSION_NEW_EYE],
    position: Sequence[float] = ...,
) -> DimensionNewEyeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIMENSION_OPTICAL_FLOW],
    position: Sequence[float] = ...,
) -> DimensionOpticalFlowTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIMENSION_PLANAR_TRACKER],
    position: Sequence[float] = ...,
) -> DimensionPlanarTrackerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIMENSION_PLANAR_TRANSFORM],
    position: Sequence[float] = ...,
) -> DimensionPlanarTransformTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIMENSION_REPAIR_FRAME],
    position: Sequence[float] = ...,
) -> DimensionRepairFrameTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIMENSION_SMOOTH_MOTION],
    position: Sequence[float] = ...,
) -> DimensionSmoothMotionTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIMENSION_STEREO_ALIGN],
    position: Sequence[float] = ...,
) -> DimensionStereoAlignTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIMENSION_TWEEN],
    position: Sequence[float] = ...,
) -> DimensionTweenTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIMENSION_Z_TO_DISPARITY],
    position: Sequence[float] = ...,
) -> DimensionZToDisparityTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DIRECTIONAL_BLUR],
    position: Sequence[float] = ...,
) -> DirectionalBlurTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DISPLACE],
    position: Sequence[float] = ...,
) -> DisplaceTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DISPLACE_3D],
    position: Sequence[float] = ...,
) -> Displace3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DISSOLVE],
    position: Sequence[float] = ...,
) -> DissolveTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DISTORT],
    position: Sequence[float] = ...,
) -> DistortTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DRIP],
    position: Sequence[float] = ...,
) -> DripTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DUPLICATE_3D],
    position: Sequence[float] = ...,
) -> Duplicate3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.DVE],
    position: Sequence[float] = ...,
) -> DVETool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.D_COLOR_CORRECTOR],
    position: Sequence[float] = ...,
) -> DColorCorrectorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.D_CROP],
    position: Sequence[float] = ...,
) -> DCropTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.D_HOLDOUT],
    position: Sequence[float] = ...,
) -> DHoldoutTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.D_MERGE],
    position: Sequence[float] = ...,
) -> DMergeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.D_RECOLOR],
    position: Sequence[float] = ...,
) -> DRecolorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.D_RESIZE],
    position: Sequence[float] = ...,
) -> DResizeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.D_TRANSFORM],
    position: Sequence[float] = ...,
) -> DTransformTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.ELLIPSE_MASK],
    position: Sequence[float] = ...,
) -> EllipseMaskTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.ERODE_DILATE],
    position: Sequence[float] = ...,
) -> ErodeDilateTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.EXPORTER_FBX],
    position: Sequence[float] = ...,
) -> ExporterFBXTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.EXTRUDE_3D],
    position: Sequence[float] = ...,
) -> Extrude3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FALLOFF_OPERATOR],
    position: Sequence[float] = ...,
) -> FalloffOperatorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FAST_NOISE],
    position: Sequence[float] = ...,
) -> FastNoiseTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FAST_NOISE_TEXTURE_3D],
    position: Sequence[float] = ...,
) -> FastNoiseTexture3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FIELDS],
    position: Sequence[float] = ...,
) -> FieldsTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FILE_LUT],
    position: Sequence[float] = ...,
) -> FileLUTTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FILM_GRAIN],
    position: Sequence[float] = ...,
) -> FilmGrainTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FILM_LOOK_CREATOR],
    position: Sequence[float] = ...,
) -> FilmLookCreatorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FILTER],
    position: Sequence[float] = ...,
) -> FilterTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FOG],
    position: Sequence[float] = ...,
) -> FogTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FOG_3D],
    position: Sequence[float] = ...,
) -> Fog3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FUSE_DUPLICATE],
    position: Sequence[float] = ...,
) -> FuseDuplicateTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FUSE_FLS_COPY_METADATA],
    position: Sequence[float] = ...,
) -> FuseFlsCopyMetadataTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FUSE_FRAME_AVERAGE],
    position: Sequence[float] = ...,
) -> FuseFrameAverageTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FUSE_LUT_CUBE_ANALYZER],
    position: Sequence[float] = ...,
) -> FuseLUTCubeAnalyzerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FUSE_LUT_CUBE_APPLY],
    position: Sequence[float] = ...,
) -> FuseLUTCubeApplyTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FUSE_LUT_CUBE_CREATOR],
    position: Sequence[float] = ...,
) -> FuseLUTCubeCreatorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FUSE_OCL_RAYS],
    position: Sequence[float] = ...,
) -> FuseOclRaysTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FUSE_SET_META_DATA],
    position: Sequence[float] = ...,
) -> FuseSetMetaDataTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FUSE_SET_META_DATA_TC],
    position: Sequence[float] = ...,
) -> FuseSetMetaDataTcTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.FUSE_WIRELESS],
    position: Sequence[float] = ...,
) -> FuseWirelessTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.GAMUT_CONVERT],
    position: Sequence[float] = ...,
) -> GamutConvertTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.GAMUT_LIMITER],
    position: Sequence[float] = ...,
) -> GamutLimiterTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.GAMUT_MAPPING],
    position: Sequence[float] = ...,
) -> GamutMappingTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.GLOW],
    position: Sequence[float] = ...,
) -> GlowTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.GRAIN],
    position: Sequence[float] = ...,
) -> GrainTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.GRID_WARP],
    position: Sequence[float] = ...,
) -> GridWarpTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.HIGHLIGHT],
    position: Sequence[float] = ...,
) -> HighlightTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.HOT_SPOT],
    position: Sequence[float] = ...,
) -> HotSpotTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.HUE_CURVES],
    position: Sequence[float] = ...,
) -> HueCurvesTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.IMAGE_PLANE_3D],
    position: Sequence[float] = ...,
) -> ImagePlane3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.IMAGE_TO_DEEP],
    position: Sequence[float] = ...,
) -> ImageToDeepTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.IMMERSIVE_PATCHER],
    position: Sequence[float] = ...,
) -> ImmersivePatcherTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.KEY_STRETCHER],
    position: Sequence[float] = ...,
) -> KeyStretcherTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LAT_LONG_PATCHER],
    position: Sequence[float] = ...,
) -> LatLongPatcherTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LAYER_MUXER],
    position: Sequence[float] = ...,
) -> LayerMuxerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LAYER_REGEX],
    position: Sequence[float] = ...,
) -> LayerRegexTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LAYER_REMOVER],
    position: Sequence[float] = ...,
) -> LayerRemoverTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LENS_DISTORT],
    position: Sequence[float] = ...,
) -> LensDistortTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LETTERBOX],
    position: Sequence[float] = ...,
) -> LetterboxTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LIGHT_AMBIENT],
    position: Sequence[float] = ...,
) -> LightAmbientTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LIGHT_DIRECTIONAL],
    position: Sequence[float] = ...,
) -> LightDirectionalTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LIGHT_DOME],
    position: Sequence[float] = ...,
) -> LightDomeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LIGHT_POINT],
    position: Sequence[float] = ...,
) -> LightPointTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LIGHT_PROJECTOR],
    position: Sequence[float] = ...,
) -> LightProjectorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LIGHT_SPOT],
    position: Sequence[float] = ...,
) -> LightSpotTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LIGHT_TRIM],
    position: Sequence[float] = ...,
) -> LightTrimTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LOADER],
    position: Sequence[float] = ...,
) -> LoaderTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LOCATOR_3D],
    position: Sequence[float] = ...,
) -> Locator3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.LUMA_KEYER],
    position: Sequence[float] = ...,
) -> LumaKeyerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MAGIC_MASK],
    position: Sequence[float] = ...,
) -> MagicMaskTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MANDEL],
    position: Sequence[float] = ...,
) -> MandelTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MATTE_CONTROL],
    position: Sequence[float] = ...,
) -> MatteControlTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MEDIA_IN],
    position: Sequence[float] = ...,
) -> MediaInTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MEDIA_OUT],
    position: Sequence[float] = ...,
) -> MediaOutTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MERGE],
    position: Sequence[float] = ...,
) -> MergeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MERGE_3D],
    position: Sequence[float] = ...,
) -> Merge3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MTL_BLINN],
    position: Sequence[float] = ...,
) -> MtlBlinnTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MTL_CHAN_BOOL],
    position: Sequence[float] = ...,
) -> MtlChanBoolTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MTL_COOK_TORRANCE],
    position: Sequence[float] = ...,
) -> MtlCookTorranceTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MTL_MERGE_3D],
    position: Sequence[float] = ...,
) -> MtlMerge3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MTL_PHONG],
    position: Sequence[float] = ...,
) -> MtlPhongTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MTL_REFLECT],
    position: Sequence[float] = ...,
) -> MtlReflectTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MTL_STEREO_MIX_3D],
    position: Sequence[float] = ...,
) -> MtlStereoMix3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MTL_WARD],
    position: Sequence[float] = ...,
) -> MtlWardTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MULTI_MERGE],
    position: Sequence[float] = ...,
) -> MultiMergeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MULTI_POLY],
    position: Sequence[float] = ...,
) -> MultiPolyTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.MULTI_TEXT],
    position: Sequence[float] = ...,
) -> MultiTextTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.NOTE],
    position: Sequence[float] = ...,
) -> NoteTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.OBJECT_REMOVAL],
    position: Sequence[float] = ...,
) -> ObjectRemovalTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.OCIO_CDL_TRANSFORM],
    position: Sequence[float] = ...,
) -> OCIOCDLTransformTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.OCIO_COLOR_SPACE],
    position: Sequence[float] = ...,
) -> OCIOColorSpaceTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.OCIO_DISPLAY],
    position: Sequence[float] = ...,
) -> OCIODisplayTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.OCIO_FILE_TRANSFORM],
    position: Sequence[float] = ...,
) -> OCIOFileTransformTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.OVERRIDE_3D],
    position: Sequence[float] = ...,
) -> Override3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.O_GRAF_LOADER],
    position: Sequence[float] = ...,
) -> OGrafLoaderTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.PAINT],
    position: Sequence[float] = ...,
) -> PaintTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.PAINT_MASK],
    position: Sequence[float] = ...,
) -> PaintMaskTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.PANO_MAP],
    position: Sequence[float] = ...,
) -> PanoMapTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.PERSPECTIVE_POSITIONER],
    position: Sequence[float] = ...,
) -> PerspectivePositionerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.PLASMA],
    position: Sequence[float] = ...,
) -> PlasmaTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.POINT_CLOUD_3D],
    position: Sequence[float] = ...,
) -> PointCloud3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.POLYLINE_MASK],
    position: Sequence[float] = ...,
) -> PolylineMaskTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.PSEUDO_COLOR],
    position: Sequence[float] = ...,
) -> PseudoColorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_AVOID],
    position: Sequence[float] = ...,
) -> PAvoidTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_BOUNCE],
    position: Sequence[float] = ...,
) -> PBounceTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_CHANGE_STYLE],
    position: Sequence[float] = ...,
) -> PChangeStyleTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_CUSTOM],
    position: Sequence[float] = ...,
) -> PCustomTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_CUSTOM_FORCE],
    position: Sequence[float] = ...,
) -> PCustomForceTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_DIRECTIONAL_FORCE],
    position: Sequence[float] = ...,
) -> PDirectionalForceTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_EMITTER],
    position: Sequence[float] = ...,
) -> PEmitterTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_FLOCK],
    position: Sequence[float] = ...,
) -> PFlockTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_FOLLOW],
    position: Sequence[float] = ...,
) -> PFollowTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_FRICTION],
    position: Sequence[float] = ...,
) -> PFrictionTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_GRADIENT_FORCE],
    position: Sequence[float] = ...,
) -> PGradientForceTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_IMAGE_EMITTER],
    position: Sequence[float] = ...,
) -> PImageEmitterTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_KILL],
    position: Sequence[float] = ...,
) -> PKillTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_MERGE],
    position: Sequence[float] = ...,
) -> PMergeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_POINT_FORCE],
    position: Sequence[float] = ...,
) -> PPointForceTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_RENDER],
    position: Sequence[float] = ...,
) -> PRenderTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_SPAWN],
    position: Sequence[float] = ...,
) -> PSpawnTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_TANGENT_FORCE],
    position: Sequence[float] = ...,
) -> PTangentForceTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_TURBULENCE],
    position: Sequence[float] = ...,
) -> PTurbulenceTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.P_VORTEX],
    position: Sequence[float] = ...,
) -> PVortexTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.RANGES_MASK],
    position: Sequence[float] = ...,
) -> RangesMaskTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.RANK_FILTER],
    position: Sequence[float] = ...,
) -> RankFilterTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.RECTANGLE_MASK],
    position: Sequence[float] = ...,
) -> RectangleMaskTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.RELIEF_MAP],
    position: Sequence[float] = ...,
) -> ReliefMapTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.RELIGHT],
    position: Sequence[float] = ...,
) -> RelightTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.REMOVE_NOISE],
    position: Sequence[float] = ...,
) -> RemoveNoiseTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.RENDERER_3D],
    position: Sequence[float] = ...,
) -> Renderer3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.REPLACE_MATERIAL_3D],
    position: Sequence[float] = ...,
) -> ReplaceMaterial3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.REPLACE_NORMALS_3D],
    position: Sequence[float] = ...,
) -> ReplaceNormals3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.REPLICATE_3D],
    position: Sequence[float] = ...,
) -> Replicate3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.RIBBON_3D],
    position: Sequence[float] = ...,
) -> Ribbon3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.RUN_COMMAND],
    position: Sequence[float] = ...,
) -> RunCommandTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SAVER],
    position: Sequence[float] = ...,
) -> SaverTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SCALE],
    position: Sequence[float] = ...,
) -> ScaleTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SET_CANVAS_COLOR],
    position: Sequence[float] = ...,
) -> SetCanvasColorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SET_DOMAIN],
    position: Sequence[float] = ...,
) -> SetDomainTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SHADER],
    position: Sequence[float] = ...,
) -> ShaderTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SHADOW],
    position: Sequence[float] = ...,
) -> ShadowTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SHAPE_3D],
    position: Sequence[float] = ...,
) -> Shape3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SHARPEN],
    position: Sequence[float] = ...,
) -> SharpenTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SOFT_CLIP],
    position: Sequence[float] = ...,
) -> SoftClipTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SOFT_GLOW],
    position: Sequence[float] = ...,
) -> SoftGlowTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SPEED_WARP],
    position: Sequence[float] = ...,
) -> SpeedWarpTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SPHERE_MAP],
    position: Sequence[float] = ...,
) -> SphereMapTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SPHERICAL_CAMERA_3D],
    position: Sequence[float] = ...,
) -> SphericalCamera3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SPHERICAL_STABILIZER],
    position: Sequence[float] = ...,
) -> SphericalStabilizerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SPLITTER],
    position: Sequence[float] = ...,
) -> SplitterTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SSAO],
    position: Sequence[float] = ...,
) -> SSAOTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SURFACE_ALEMBIC_MESH],
    position: Sequence[float] = ...,
) -> SurfaceAlembicMeshTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SURFACE_FBX_MESH],
    position: Sequence[float] = ...,
) -> SurfaceFBXMeshTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SURFACE_TRACKER],
    position: Sequence[float] = ...,
) -> SurfaceTrackerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SWITCH],
    position: Sequence[float] = ...,
) -> SwitchTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.SWIZZLER],
    position: Sequence[float] = ...,
) -> SwizzlerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_BOOLEAN],
    position: Sequence[float] = ...,
) -> SBooleanTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_B_SPLINE],
    position: Sequence[float] = ...,
) -> SBSplineTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_CHANGE_STYLE],
    position: Sequence[float] = ...,
) -> SChangeStyleTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_DUPLICATE],
    position: Sequence[float] = ...,
) -> SDuplicateTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_ELLIPSE],
    position: Sequence[float] = ...,
) -> SEllipseTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_EXPAND],
    position: Sequence[float] = ...,
) -> SExpandTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_GRID],
    position: Sequence[float] = ...,
) -> SGridTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_JITTER],
    position: Sequence[float] = ...,
) -> SJitterTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_MERGE],
    position: Sequence[float] = ...,
) -> SMergeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_N_GON],
    position: Sequence[float] = ...,
) -> SNGonTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_OUTLINE],
    position: Sequence[float] = ...,
) -> SOutlineTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_POLYGON],
    position: Sequence[float] = ...,
) -> SPolygonTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_RECTANGLE],
    position: Sequence[float] = ...,
) -> SRectangleTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_RENDER],
    position: Sequence[float] = ...,
) -> SRenderTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_STAR],
    position: Sequence[float] = ...,
) -> SStarTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_TEXT],
    position: Sequence[float] = ...,
) -> STextTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.S_TRANSFORM],
    position: Sequence[float] = ...,
) -> STransformTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TEXTURE],
    position: Sequence[float] = ...,
) -> TextureTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TEXTURE_2D_OPERATOR],
    position: Sequence[float] = ...,
) -> Texture2DOperatorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TEXTURE_TRANSFORM_OPERATOR],
    position: Sequence[float] = ...,
) -> TextureTransformOperatorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TEXT_3D],
    position: Sequence[float] = ...,
) -> Text3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TEXT_PLUS],
    position: Sequence[float] = ...,
) -> TextPlusTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TEX_CATCHER],
    position: Sequence[float] = ...,
) -> TexCatcherTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TEX_GRADIENT],
    position: Sequence[float] = ...,
) -> TexGradientTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TIME_SPEED],
    position: Sequence[float] = ...,
) -> TimeSpeedTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TIME_STRETCHER],
    position: Sequence[float] = ...,
) -> TimeStretcherTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TRACKER],
    position: Sequence[float] = ...,
) -> TrackerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TRAILS],
    position: Sequence[float] = ...,
) -> TrailsTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TRANSFORM],
    position: Sequence[float] = ...,
) -> TransformTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TRANSFORM_3D],
    position: Sequence[float] = ...,
) -> Transform3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TRIANGLE_MASK],
    position: Sequence[float] = ...,
) -> TriangleMaskTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TRIANGULATE_3D],
    position: Sequence[float] = ...,
) -> Triangulate3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.TV],
    position: Sequence[float] = ...,
) -> TVTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.ULTRA_KEYER],
    position: Sequence[float] = ...,
) -> UltraKeyerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.UNDERLAY],
    position: Sequence[float] = ...,
) -> UnderlayTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.UNSHARP_MASK],
    position: Sequence[float] = ...,
) -> UnsharpMaskTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.UV_MAP],
    position: Sequence[float] = ...,
) -> UVMapTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_CAMERA],
    position: Sequence[float] = ...,
) -> UCameraTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_CATCHER],
    position: Sequence[float] = ...,
) -> UCatcherTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_CYLINDER_LIGHT],
    position: Sequence[float] = ...,
) -> UCylinderLightTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_DISK_LIGHT],
    position: Sequence[float] = ...,
) -> UDiskLightTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_DISTANT_LIGHT],
    position: Sequence[float] = ...,
) -> UDistantLightTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_DOME_LIGHT],
    position: Sequence[float] = ...,
) -> UDomeLightTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_DUPLICATE],
    position: Sequence[float] = ...,
) -> UDuplicateTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_EXPORT],
    position: Sequence[float] = ...,
) -> UExportTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_IMAGE_PLANE],
    position: Sequence[float] = ...,
) -> UImagePlaneTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_LOADER],
    position: Sequence[float] = ...,
) -> ULoaderTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_MATERIAL_X],
    position: Sequence[float] = ...,
) -> UMaterialXTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_MERGE],
    position: Sequence[float] = ...,
) -> UMergeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_NORMAL_MAP],
    position: Sequence[float] = ...,
) -> UNormalMapTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_PROJECTOR],
    position: Sequence[float] = ...,
) -> UProjectorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_RECT_LIGHT],
    position: Sequence[float] = ...,
) -> URectLightTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_RENDERER],
    position: Sequence[float] = ...,
) -> URendererTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_REPLACE_MATERIAL],
    position: Sequence[float] = ...,
) -> UReplaceMaterialTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_SHADER],
    position: Sequence[float] = ...,
) -> UShaderTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_SHAPE],
    position: Sequence[float] = ...,
) -> UShapeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_SPHERE_LIGHT],
    position: Sequence[float] = ...,
) -> USphereLightTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_SWITCH],
    position: Sequence[float] = ...,
) -> USwitchTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_TEXTURE],
    position: Sequence[float] = ...,
) -> UTextureTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_TEXTURE_TRANSFORM],
    position: Sequence[float] = ...,
) -> UTextureTransformTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_TRANSFORM],
    position: Sequence[float] = ...,
) -> UTransformTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_VARIANT],
    position: Sequence[float] = ...,
) -> UVariantTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_VISIBILITY],
    position: Sequence[float] = ...,
) -> UVisibilityTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.U_VOLUME],
    position: Sequence[float] = ...,
) -> UVolumeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.VARI_BLUR],
    position: Sequence[float] = ...,
) -> VariBlurTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.VECTOR_DENOISE],
    position: Sequence[float] = ...,
) -> VectorDenoiseTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.VECTOR_MOTION_BLUR],
    position: Sequence[float] = ...,
) -> VectorMotionBlurTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.VECTOR_TRANSFORM],
    position: Sequence[float] = ...,
) -> VectorTransformTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.VECTOR_WARP],
    position: Sequence[float] = ...,
) -> VectorWarpTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.VOLUME_FOG],
    position: Sequence[float] = ...,
) -> VolumeFogTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.VOLUME_MASK],
    position: Sequence[float] = ...,
) -> VolumeMaskTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.VORTEX],
    position: Sequence[float] = ...,
) -> VortexTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.WAND_MASK],
    position: Sequence[float] = ...,
) -> WandMaskTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.WELD_3D],
    position: Sequence[float] = ...,
) -> Weld3DTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.WHITE_BALANCE],
    position: Sequence[float] = ...,
) -> WhiteBalanceTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.XY_PATH],
    position: Sequence[float] = ...,
) -> XYPathTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionTool.ZTO_WORLD_POS],
    position: Sequence[float] = ...,
) -> ZtoWorldPosTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.ABSTRACTION],
    position: Sequence[float] = ...,
) -> ResolveFxAbstractionTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.ANALOG_DAMAGE],
    position: Sequence[float] = ...,
) -> ResolveFxAnalogDamageTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.APERTURE_DIFFRACTION],
    position: Sequence[float] = ...,
) -> ResolveFxApertureDiffractionTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.BEAUTY],
    position: Sequence[float] = ...,
) -> ResolveFxBeautyTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.BLANKING_FILL],
    position: Sequence[float] = ...,
) -> ResolveFxBlankingFillTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.BLEMISH_REMOVAL],
    position: Sequence[float] = ...,
) -> ResolveFxBlemishRemovalTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.BOX_BLUR],
    position: Sequence[float] = ...,
) -> ResolveFxBoxBlurTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.BURN_AWAY],
    position: Sequence[float] = ...,
) -> ResolveFxBurnAwayTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.CAMERA_SHAKE],
    position: Sequence[float] = ...,
) -> ResolveFxCameraShakeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.CINEMATIC_HAZE],
    position: Sequence[float] = ...,
) -> ResolveFxCinematicHazeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.CINE_FOCUS],
    position: Sequence[float] = ...,
) -> ResolveFxCineFocusTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.COLOR_COMPRESSOR],
    position: Sequence[float] = ...,
) -> ResolveFxColorCompressorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.COLOR_GENERATOR_PLUGIN],
    position: Sequence[float] = ...,
) -> ResolveFxColorGeneratorPluginTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.COLOR_PALETTE],
    position: Sequence[float] = ...,
) -> ResolveFxColorPaletteTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.COLOR_TONE_DIFFUSER],
    position: Sequence[float] = ...,
) -> ResolveFxColorToneDiffuserTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.CONTRAST_POP],
    position: Sequence[float] = ...,
) -> ResolveFxContrastPopTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.DCTL],
    position: Sequence[float] = ...,
) -> ResolveFxDCTLTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.DEAD_PIXEL_FIXER_V2],
    position: Sequence[float] = ...,
) -> ResolveFxDeadPixelFixerV2Tool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.DEBAND],
    position: Sequence[float] = ...,
) -> ResolveFxDebandTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.DEFLICKER],
    position: Sequence[float] = ...,
) -> ResolveFxDeflickerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.DEHAZE],
    position: Sequence[float] = ...,
) -> ResolveFxDehazeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.DENT],
    position: Sequence[float] = ...,
) -> ResolveFxDentTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.DESPILL_PLUGIN],
    position: Sequence[float] = ...,
) -> ResolveFxDespillPluginTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.DETAIL_RECOVERY],
    position: Sequence[float] = ...,
) -> ResolveFxDetailRecoveryTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.DIRECTIONAL_BLUR],
    position: Sequence[float] = ...,
) -> ResolveFxDirectionalBlurTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.DROP_SHADOW],
    position: Sequence[float] = ...,
) -> ResolveFxDropShadowTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.DUST_BUSTER_V2],
    position: Sequence[float] = ...,
) -> ResolveFxDustBusterV2Tool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.EDGE_DETECT],
    position: Sequence[float] = ...,
) -> ResolveFxEdgeDetectTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.EMBOSS],
    position: Sequence[float] = ...,
) -> ResolveFxEmbossTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.FALSE_COLOR],
    position: Sequence[float] = ...,
) -> ResolveFxFalseColorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.FILM_DAMAGE],
    position: Sequence[float] = ...,
) -> ResolveFxFilmDamageTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.FILM_GRAIN],
    position: Sequence[float] = ...,
) -> ResolveFxFilmGrainTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.FILM_LOOK],
    position: Sequence[float] = ...,
) -> ResolveFxFilmLookTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.FLICKER_ADDITION],
    position: Sequence[float] = ...,
) -> ResolveFxFlickerAdditionTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.FRAME_REPLACER],
    position: Sequence[float] = ...,
) -> ResolveFxFrameReplacerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.GAUSSIAN_BLUR],
    position: Sequence[float] = ...,
) -> ResolveFxGaussianBlurTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.GLOW],
    position: Sequence[float] = ...,
) -> ResolveFxGlowTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.GRID],
    position: Sequence[float] = ...,
) -> ResolveFxGridTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.HALATION_PLUGIN],
    position: Sequence[float] = ...,
) -> ResolveFxHalationPluginTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.INVERT_COLOR],
    position: Sequence[float] = ...,
) -> ResolveFxInvertColorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.JPEG_DAMAGE],
    position: Sequence[float] = ...,
) -> ResolveFxJpegDamageTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.LENS_BLUR],
    position: Sequence[float] = ...,
) -> ResolveFxLensBlurTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.LENS_DISTORTION],
    position: Sequence[float] = ...,
) -> ResolveFxLensDistortionTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.LENS_FLARE_V2],
    position: Sequence[float] = ...,
) -> ResolveFxLensFlareV2Tool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.LENS_REFLECTIONS],
    position: Sequence[float] = ...,
) -> ResolveFxLensReflectionsTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.LIGHTRAY],
    position: Sequence[float] = ...,
) -> ResolveFxLightrayTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.MIRROR],
    position: Sequence[float] = ...,
) -> ResolveFxMirrorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.MOSAIC_BLUR],
    position: Sequence[float] = ...,
) -> ResolveFxMosaicBlurTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.MOTION_BLUR],
    position: Sequence[float] = ...,
) -> ResolveFxMotionBlurTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.MOTION_TRAILS],
    position: Sequence[float] = ...,
) -> ResolveFxMotionTrailsTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.NOISE_REDUCTION],
    position: Sequence[float] = ...,
) -> ResolveFxNoiseReductionTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.NVIDIA_RTXHDR],
    position: Sequence[float] = ...,
) -> ResolveFxNvidiaRTXHDRTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.OFXHSL_KEYER],
    position: Sequence[float] = ...,
) -> ResolveFxOfxhslKeyerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.OFX_3D_KEYER_V2],
    position: Sequence[float] = ...,
) -> ResolveFxOFX3DKeyerV2Tool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.OFX_LUMA_KEYER],
    position: Sequence[float] = ...,
) -> ResolveFxOFXLumaKeyerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.PATCH_REPLACER],
    position: Sequence[float] = ...,
) -> ResolveFxPatchReplacerTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.PICTURE_IN_PICTURE],
    position: Sequence[float] = ...,
) -> ResolveFxPictureInPictureTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.PRISM_BLUR],
    position: Sequence[float] = ...,
) -> ResolveFxPrismBlurTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.RADIAL_BLUR],
    position: Sequence[float] = ...,
) -> ResolveFxRadialBlurTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.RELIGHT],
    position: Sequence[float] = ...,
) -> ResolveFxRelightTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.RIPPLE],
    position: Sequence[float] = ...,
) -> ResolveFxRippleTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.SCANLINE_V2],
    position: Sequence[float] = ...,
) -> ResolveFxScanlineV2Tool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.SHARPEN],
    position: Sequence[float] = ...,
) -> ResolveFxSharpenTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.SHARPEN_EDGE_PLUGIN],
    position: Sequence[float] = ...,
) -> ResolveFxSharpenEdgePluginTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.SHRINK_AND_GROW],
    position: Sequence[float] = ...,
) -> ResolveFxShrinkAndGrowTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.SKETCH],
    position: Sequence[float] = ...,
) -> ResolveFxSketchTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.SMEAR],
    position: Sequence[float] = ...,
) -> ResolveFxSmearTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.SOFT_SHARPEN_SKIN],
    position: Sequence[float] = ...,
) -> ResolveFxSoftSharpenSkinTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.SPLIT_TONE],
    position: Sequence[float] = ...,
) -> ResolveFxSplitToneTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.STOP_MOTION],
    position: Sequence[float] = ...,
) -> ResolveFxStopMotionTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.STYLIZE],
    position: Sequence[float] = ...,
) -> ResolveFxStylizeTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.TEXTURE_POP],
    position: Sequence[float] = ...,
) -> ResolveFxTexturePopTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.TILT_SHIFT_BLUR],
    position: Sequence[float] = ...,
) -> ResolveFxTiltShiftBlurTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.TRANSFORM],
    position: Sequence[float] = ...,
) -> ResolveFxTransformTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.ULTRA_SHARPEN],
    position: Sequence[float] = ...,
) -> ResolveFxUltraSharpenTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.VIDEO_COLLAGE],
    position: Sequence[float] = ...,
) -> ResolveFxVideoCollageTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.VIDEO_RESTORATION],
    position: Sequence[float] = ...,
) -> ResolveFxVideoRestorationTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.VIGNETTE],
    position: Sequence[float] = ...,
) -> ResolveFxVignetteTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.VORTEX],
    position: Sequence[float] = ...,
) -> ResolveFxVortexTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.WARPER],
    position: Sequence[float] = ...,
) -> ResolveFxWarperTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.WATERCOLOR],
    position: Sequence[float] = ...,
) -> ResolveFxWatercolorTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.WAVINESS],
    position: Sequence[float] = ...,
) -> ResolveFxWavinessTool: ...

@overload
def add_tool(
    comp: Any,
    tool_type: Literal[FusionResolveFxTool.ZOOM_BLUR],
    position: Sequence[float] = ...,
) -> ResolveFxZoomBlurTool: ...

def add_tool(
    comp: Any,
    tool_type: str,
    position: Sequence[float] = ...,
) -> FusionToolProtocol: ...

@overload
def add_modifier(
    comp: Any,
    modifier_type: Literal[FusionModifier.BEZIER_SPLINE],
) -> BezierSplineTool: ...

@overload
def add_modifier(
    comp: Any,
    modifier_type: Literal[FusionModifier.B_SPLINE_PATH],
) -> BSplinePathTool: ...

@overload
def add_modifier(
    comp: Any,
    modifier_type: Literal[FusionModifier.EXPRESSION],
) -> ExpressionTool: ...

@overload
def add_modifier(
    comp: Any,
    modifier_type: Literal[FusionModifier.OFFSET],
) -> OffsetTool: ...

@overload
def add_modifier(
    comp: Any,
    modifier_type: Literal[FusionModifier.PATH],
) -> PathTool: ...

@overload
def add_modifier(
    comp: Any,
    modifier_type: Literal[FusionModifier.PERTURB_NUMBER],
) -> PerturbNumberTool: ...

@overload
def add_modifier(
    comp: Any,
    modifier_type: Literal[FusionModifier.PERTURB_POINT],
) -> PerturbPointTool: ...

@overload
def add_modifier(
    comp: Any,
    modifier_type: Literal[FusionModifier.POLY_PATH],
) -> PolyPathTool: ...

@overload
def add_modifier(
    comp: Any,
    modifier_type: Literal[FusionModifier.SHAKE],
) -> ShakeTool: ...

@overload
def add_modifier(
    comp: Any,
    modifier_type: Literal[FusionModifier.TRACKER_MODIFIER],
) -> TrackerModifierTool: ...

@overload
def add_modifier(
    comp: Any,
    modifier_type: Literal[FusionModifier.XY_PATH],
) -> XYPathTool: ...

def add_modifier(
    comp: Any,
    modifier_type: str,
) -> FusionToolProtocol: ...

def add_comp(timeline_item: Any) -> FusionCompositionProtocol:
    ...


def get_tool(comp: Any, name: str) -> FusionToolProtocol:
    ...


def connect_input(target: Any, input_name: str, source: Any) -> None:
    ...


def connect_default_output(source: Any, target: Any) -> None:
    ...


def connect_merge(merge: Any, *, background: Any | None=None, foreground: Any | None=None) -> None:
    ...


def set_tool_input(tool: Any, name: str, value: Any, *, tolerance: float=1e-06) -> None:
    ...


def set_tool_inputs(tool: Any, values: Mapping[str, Any]) -> None:
    ...


def set_tool_position(comp: Any, tool: Any, position: Sequence[float], *, tolerance: float=0.1, session: ResolveSession | None=None, activate_fusion_page: bool=False) -> None:
    ...


def set_background_color(tool: Any, rgba: Sequence[float]) -> None:
    ...


def get_fusion_fonts(fusion: Any) -> Mapping[str, tuple[str, ...]]:
    ...


def require_fusion_font(fusion: Any, family: str, style: str) -> None:
    ...


def add_dctl_tool(comp: Any, dctl_path: str | Path, *, lut_root: str | Path, options: Mapping[str, Any] | None=None, position: Sequence[float]=(0.0, 0.0)) -> Any:
    ...


def add_transparent_background(comp: Any, position: Sequence[float]=(0.0, 0.0)) -> Any:
    ...


def build_rectangle(comp: Any, rgba: Sequence[float]=(1.0, 1.0, 1.0, 1.0), *, center: Sequence[float]=(0.5, 0.5), width: float=0.1, height: float=0.1, position: Sequence[float]=(0.0, 0.0)) -> Any:
    ...


def build_line(comp: Any, rgba: Sequence[float], width: float, height: float, *, angle: float=0.0, position: Sequence[float]=(0.0, 0.0), connect_as_foreground: bool=True, center: Sequence[float]=(0.5, 0.5)) -> Any:
    ...


def select_fusion_duration_media(directory: str | Path, width: int, height: int, frame_rate: int | float | str, *, prefix: str='dummy_video', extension: str='.mp4') -> Path:
    ...


def get_packaged_fusion_duration_media(width: int, height: int, frame_rate: int | float | str) -> Path:
    ...


def append_fusion_composition(timeline: Any, *, duration_frames: int | None=None, record_frame: int | float | None=None, media_pool: Any | None=None, dummy_media: str | Path | None=None) -> tuple[Any, FusionCompositionProtocol]:
    ...


def refresh_fusion_color_management(session: ResolveSession, *, delay: float=0.5) -> None:
    ...
