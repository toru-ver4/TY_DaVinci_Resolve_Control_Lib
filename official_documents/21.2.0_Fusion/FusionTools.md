**Fusion Tools Overview.** Fusion's tools by category. Each category below has its own section listing one line per tool on what it's for;
each tool's controls, script IDs and examples are in the Fusion Tool Reference, under the tool's name.

*Last Updated: 4 Oct 2026*

- **3D** (3D scenes: geometry, cameras, lights, materials, textures, Merge 3D and Renderer 3D): Alembic Mesh 3D, Ambient Light, Bender 3D, Blinn, BumpMap, Camera 3D, Catcher, Channel Boolean, CookTorrance, Cube 3D, CubeMap, Custom Vertex 3D, Directional Light, Displace 3D, Dome Light, Duplicate 3D, Extrude 3D, Falloff, Fast Noise Texture, FBX Exporter, FBX Mesh 3D, Fog 3D, Gradient, Image Plane 3D, Locator 3D, Material Merge, Merge 3D, OpenPBR, Override 3D, Phong, Point Light, PointCloud 3D, Projector 3D, Reflect, Relief Map, Renderer 3D, Replace Material 3D, Replace Normals 3D, Replicate 3D, Ribbon 3D, Shape 3D, SoftClip, SphereMap, Spherical Camera, Spot Light, Stereo Mix, Text 3D, Texture 2D, Texture Transform, Transform 3D, Triangulate 3D, UV Map 3D, Ward, Weld 3D
- **Blur** (blurs, glows and sharpening): Blur, Defocus, Directional Blur, Glow, Sharpen, Soft Glow, Unsharp Mask, VariBlur, Vector Motion Blur
- **Color** (colour correction, curves, channel maths and colour-space conversion (ACES, OCIO)): ACES Transform, Auto Gain, Brightness / Contrast, Channel Booleans, Chromatic Aberration Removal, Chromatic Adaptation, Color Corrector, Color Curves, Color Gain, Color Matrix, Color Space, Color Space Transform, Copy Aux, Film Look Creator, Gamut, Gamut Limiter, Gamut Mapping, Hue Curves, OCIO CDL Transform, OCIO ColorSpace, OCIO Display, OCIO File Transform, Set Canvas Color, White Balance
- **Composite** (layering and mixing images): Dissolve, Merge, MultiMerge
- **Deep Image** (compositing deep (per-sample depth) images): dColor Corrector, dCrop, Deep To Image, Deep To Points, dHoldout, dMerge, dRecolor, dResize, dTransform, Image To Deep
- **Deep Pixel** (effects driven by Z, position and normal channels): Ambient Occlusion, Depth Blur, Fog, Shader, Texture
- **Effect** (stylised effects: rays, trails, shadows, highlights, TV): Duplicate, Highlight, Hot Spot, Object Removal, Pseudo Color, Rays, Shadow, Trails, TV
- **Film** (film grain, noise removal and log conversion): Cineon Log, Film Grain, Grain, Light Trim, Remove Noise
- **Filter** (convolution filters, erode/dilate, relief and bump maps): Create Bump Map, Create Relief Map, Custom Filter, Erode / Dilate, Filter, Rank Filter
- **Flow** (organising the node tree): Note, Underlay
- **Generator** (creating images: text, backgrounds, noise and patterns): Background, DaySky, FastNoise, Mandelbrot, MultiText, OGrafLoader, Plasma, Text+
- **I/O** (getting media in and out (MediaIn/MediaOut in Resolve, Loader/Saver)): Loader, Media In, Media Out, Saver
- **Layer** (multi-layer (EXR/PSD) image handling): Layer Muxer, Layer Regex, Layer Remover, Swizzler
- **LUT** (applying and creating LUTs): File LUT, LUT Cube Analyzer, LUT Cube Apply, LUT Cube Creator
- **Mask** (shapes and rotoscoping for masks): Bitmap, BSpline, Ellipse, Mask Paint, MultiPoly, Polygon, Ranges, Rectangle, Triangle, Wand
- **Matte** (keying and matte handling): Alpha Divide, Alpha Multiply, Chroma Keyer, Clean Plate, Cryptomatte, Delta Keyer, Depth Map, Difference Keyer, Luma Keyer, Magic Mask, Matte Control, Relight, Ultra Keyer
- **Metadata** (image metadata and timecode): Copy Metadata, Set Metadata, Set Time Code
- **Miscellaneous** (time remapping, domain control, custom pixel maths and utilities): Auto Domain, Change Depth, Custom Tool, Fields, Frame Average, Keyframe Stretcher, RunCommand, Set Domain, Speed Warp, Switch, Time Speed, Time Stretcher, Wireless Link
- **Optical Flow** (motion vectors, retiming and frame repair): Optical Flow, Repair Frame, Smooth Motion, Tween, Vector Denoise, Vector Transform, Vector Warp
- **Paint** (paint strokes, clone and wire removal): Paint
- **Particles** (particle systems): pAvoid, pBounce, pChangeStyle, pCustom, pCustomForce, pDirectionalForce, pEmitter, pFlock, pFollow, pFriction, pGradientForce, pImageEmitter, pKill, pMerge, pPointForce, pRender, pSpawn, pTangentForce, pTurbulence, pVortex
- **Position** (tools driven by world-position passes): Volume Fog, Volume Mask, Z to WorldPos
- **Shape** (resolution-independent vector shapes for motion graphics): sBoolean, sBSpline, sChangeStyle, sDuplicate, sEllipse, sExpand, sGrid, sJitter, sMerge, sNGon, sOutline, sPolygon, sRectangle, sRender, sStar, sText, sTransform
- **Stereo** (stereoscopic 3D): Anaglyph, Combiner, Disparity, Disparity To Z, Global Align, New Eye, Splitter, Stereo Align, Z To Disparity
- **Tracking** (point, planar, surface and camera tracking): Camera Tracker, Planar Tracker, Surface Tracker, Tracker
- **Transform** (moving, scaling and cropping images): Camera Shake, Crop, DVE, Letterbox, Planar Transform, Resize, Scale, Transform
- **USD** (Universal Scene Description scenes): uCamera, uCatcher, uCylinder Light, uDisk Light, uDistant Light, uDome Light, uDuplicate, uExport, uImage Plane, uLoader, uMaterialX, uMerge, uNormal Map, uProjector, uRectangle Light, uRenderer, uReplace Material, uShader, uShape, uSphere Light, uSwitch, uTexture, uTexture Transform, uTransform, uVariant, uVisibility, uVolume
- **VR** (360° and immersive video): Immersive Patcher, LatLong Patcher, PanoMap, Spherical Stabilizer
- **Warp** (distortions and corner pinning): Coordinate Space, Corner Positioner, Dent, Displace, Drip, Grid Warp, Lens Distort, Perspective Positioner, Vector Distortion, Vortex
- **Krokodove: 3D** (Krokodove tools that modify 3D scenes): Align 3D, Connect 3D, Kill 3D, Mapped Duplicate 3D, Objectify 3D, Poly Play 3D
- **Krokodove: 3D Create** (Krokodove 3D geometry generators): Fold Create 3D, Heightfield Create 3D, Tube Create 3D
- **Krokodove: Image** (Krokodove image effects): Bounding Box, Color Map, Connect, Dither, Extend, Fragments, Grow, Grow Color, Microwaves, Pack, Painterly, Rasterize, Time Mapper, Worm
- **Krokodove: Image Color** (Krokodove colour tools): Invert, Match Color, Recolor, Replace Color, Threshold
- **Krokodove: Image Create** (Krokodove image generators): Blobs, Generate, Lines, Pattern, Shapes
- **Krokodove: Image Pixel** (Krokodove per-pixel effects): Average, Bevel, Channel Shifter, Clean Edges, Deflicker, Duplicate, Extrude, Noise, Plastic, Positioner, Push, Rest, Seamless, Seamless Loop, Sort
- **Krokodove: Image Position** (Krokodove position-pass tools): Contour
- **Krokodove: Image Vector** (Krokodove vector-field tools): Vector Visualization
- **Krokodove: Image Warp** (Krokodove distortion and transform tools): Bend, Directional Scale, Kaleidoscope, Mirror, Offset, Radial, Relative Transform, Segment Transform, Shear, Shuffle, Spherize, Stretch, Warped Transform
- **Krokodove: Region** (Krokodove 3D regions for limiting effects): rCube, rMerge, rModify, rNoise, rPlane, rSphere, rTransform
- **Krokodove: Shape** (Krokodove tools that modify Shape-tool vector shapes): sExtrude, sKill, sOffset, sResample, sRestyle, sRound, sSmooth, sTriangulate, sWriteOn, sZigZag
- **Krokodove: Shape Create** (Krokodove vector shape generators): sPrimitive Create, sSpiral Create, sTrace Create
- **Modifiers** (animation and linking attached to inputs: splines, paths, expressions, text modifiers): B-Spline, Beat, BezierSpline, BSpline, BSpline Path, Calculation, Character Level Styling, Color Switcher, CompName, CoordTransform 3D, Cubic Spline, Custom Poly, Expression, Fairlight Animator, Follower, Formula, From File, From Image, Gradient Color, Juggle, Keyframe Stretcher, MIDI Extractor, Natural Cubic Spline, Offset, Path, Probe, Random, Resolve Parameter, Shake, TextScramble, TextTimer, TimeCode, Track, Vector, Write, XY Path, Perturb, Publish, Switch

## 3D

Tools for building and rendering 3D scenes. Geometry, lights and cameras are combined in a Merge 3D, and a Renderer 3D
turns the scene into an image to merge with 2D work. Materials and textures connect to the geometry's material inputs.

*Scene and rendering:*

- **Merge 3D** (`Merge3D`) — Combines geometry, lights and cameras into one 3D scene. Every scene passes through one before rendering.
- **Renderer 3D** (`Renderer3D`) — Renders a 3D scene to a 2D image through a chosen camera, with the software, OpenGL or other renderers.
- **Camera 3D** (`Camera3D`) — A camera with focal length, film back and depth of field; also shows or projects an image plane.
- **Spherical Camera** (`SphericalCamera3D`) — A camera that sees the full sphere, rendered as a panorama such as lat-long, for 360° and VR output.
- **Transform 3D** (`Transform3D`) — Moves, rotates and scales everything connected to it, for grouping and hierarchical animation.
- **Override 3D** (`Override3D`) — Overrides visibility, lighting, shadow and matte settings for everything upstream.
- **Locator 3D** (`Locator3D`) — A marker at a point in the scene (not rendered by default) whose position and distance outputs can drive 2D tools.
- **PointCloud 3D** (`PointCloud3D`) — Displays a set of points, such as a camera track's, as crosses or dots for checking and reference.
- **Fog 3D** (`Fog3D`) — Depth-based fog in the 3D scene.
- **SoftClip** (`SoftClip`) — Fades objects out as they get near the camera.

*Geometry:*

- **Text 3D** (`Text3D`) — Extruded, bevelled 3D text with the layout and character transforms of Text+. The core of 3D titles.
- **Shape 3D** (`Shape3D`) — Basic primitives: plane, cube, sphere, cylinder, cone, torus and icosphere.
- **Image Plane 3D** (`ImagePlane3D`) — A flat card that shows an image or video in the 3D scene.
- **Cube 3D** (`Cube3D`) — A cube with a separate material or image on each face, or one Cube Map.
- **Extrude 3D** (`Extrude3D`) — Extrudes a 2D shape into a bevelled solid, with a classic or custom profile.
- **Ribbon 3D** (`Ribbon3D`) — Generates a band of subdivided lines between two points, for trails and light lines.

*Layout and geometry operations:*

- **Duplicate 3D** (`Duplicate3D`) — Makes a row or array of copies, each transformed from the last, with jitter and region limits.
- **Replicate 3D** (`Replicate3D`) — Copies geometry at every vertex or particle of a destination, aligned and coloured from it.
- **Displace 3D** (`Displace3D`) — Pushes vertices along their normals by the values of an image, for relief and surface noise.
- **Bender 3D** (`Bender3D`) — Bends, tapers, twists or shears geometry, measured against its own bounding box.
- **Custom Vertex 3D** (`CustomVertex3D`) — Moves and rewrites each vertex with expressions, optionally driven by images and curves.
- **Weld 3D** (`Weld3D`) — Joins vertices at the same position to close seams, or splits every face apart with Fracture.
- **Triangulate 3D** (`Triangulate3D`) — Splits every polygon of a mesh into triangles.
- **Replace Normals 3D** (`ReplaceNormals3D`) — Recomputes the normals and tangents of geometry, making it smooth or flat.
- **UV Map 3D** (`UVMap`) — Replaces texture coordinates with planar, spherical, cube or camera-projected ones.
- **Replace Material 3D** (`ReplaceMaterial3D`) — Replaces the material of the objects in a scene, per colour channel and by ID.

*Import and export:*

- **FBX Mesh 3D** (`SurfaceFBXMesh`) — Loads a mesh from an FBX file (or OBJ, 3DS, DAE or DXF) as a single object.
- **Alembic Mesh 3D** (`SurfaceAlembicMesh`) — Loads a baked mesh from an Alembic (.abc) file, with its animation played back as stored.
- **FBX Exporter** (`ExporterFBX`) — Writes the 3D scene to an FBX file or another scene format when it renders.

*Lights:*

- **Ambient Light** (`LightAmbient`) — A directionless light that lifts the whole scene evenly.
- **Directional Light** (`LightDirectional`) — Distant, sun-like light with a direction and optional soft shadows.
- **Point Light** (`LightPoint`) — Light from a point in all directions, with optional decay and shadows.
- **Spot Light** (`LightSpot`) — A cone of light with penumbra and dropoff, with optional shadows.
- **Dome Light** (`LightDome`) — Environment light from a lat-long sky or HDR image.
- **Projector 3D** (`LightProjector`) — Projects an image as light, ambient light, or a texture for a Catcher.

*Materials:*

- **Blinn** (`MtlBlinn`) — A basic illumination material with textures on diffuse and specular.
- **Phong** (`MtlPhong`) — A basic material with a sharp, polished-plastic highlight.
- **CookTorrance** (`MtlCookTorrance`) — A microfacet material for metals and shiny surfaces, with roughness and Fresnel.
- **OpenPBR** (`MtlPBRUber`) — A physically based uber material with metalness, coat, sheen, transmission and more.
- **Reflect** (`MtlReflect`) — Adds environment reflections and refraction to a surface.
- **Ward** (`MtlWard`) — A material with an anisotropic highlight that stretches along U or V.
- **Channel Boolean** (`MtlChanBool`) — Combines the channels of two materials with maths per channel.
- **Material Merge** (`MtlMerge3D`) — Layers one material over another with a blend amount.
- **Stereo Mix** (`MtlStereoMix3D`) — Assigns one material to the left eye and one to the right.

*Textures:*

- **Texture 2D** (`Texture2DOperator`) — Turns a 2D image into a texture with offset, scale and wrap.
- **Texture Transform** (`TextureTransformOperator`) — Translates, rotates and scales the UVW coordinates of a material.
- **Gradient** (`TexGradient`) — A procedural colour gradient in linear, radial and other shapes.
- **Fast Noise Texture** (`FastNoiseTexture3D`) — Resolution-independent procedural noise, in 2D (animated) or 3D (solid).
- **BumpMap** (`BumpMap`) — Turns a height or bump image into a bump material for surface detail.
- **Relief Map** (`ReliefMap`) — Height-based surface detail that can shadow itself.
- **CubeMap** (`CubeMap`) — An environment texture from six face images or a cross image.
- **SphereMap** (`SphereMap`) — Maps a 2:1 equirectangular image onto a sphere as a reflection environment.
- **Catcher** (`TexCatcher`) — Catches projections from a Projector 3D or Camera 3D as a texture.
- **Falloff** (`FalloffOperator`) — Blends two materials by the angle to the camera, for rim and two-tone looks.

## Blur

Tools that soften, glow, sharpen or blur an image, either everywhere or where a mask or a second image says.

- **Blur** (`Blur`) — Softens the image with a choice of blur filters, and separate X and Y sizes when Lock X/Y is off.
- **Defocus** (`Defocus`) — Simulates an out-of-focus lens, either a fast Gaussian or a Lens mode with aperture shapes and bloom.
- **Directional Blur** (`DirectionalBlur`) — Smears the image linearly, radially or as a zoom, for motion blur and light streaks.
- **Glow** (`Glow`) — Blooms the highlights, with a Threshold mode, per-channel colour scale and a glow pre-mask.
- **Soft Glow** (`SoftGlow`) — A diffuse, natural glow for haze, dreamy looks and skin, with threshold and gain.
- **Sharpen** (`Sharpen`) — Enhances detail with a convolution filter, overall or per channel.
- **Unsharp Mask** (`UnsharpMask`) — Sharpens only the edges, with a threshold to keep flat areas and noise unchanged.
- **VariBlur** (`VariBlur`) — A per-pixel blur whose amount is set by a second image, such as a gradient, a shape or a depth map.
- **Vector Motion Blur** (`VectorMotionBlur`) — Blurs each pixel along its own motion, from a motion-vector pass or optical flow.

## Color

Tools for colour correction, colour curves, channel maths and colour-space conversion, including ACES and OpenColorIO (OCIO).
The Color Corrector is the main grading tool; Color Gain and Brightness / Contrast do quicker, simpler adjustments.

- **ACES Transform** (`AcesTransform`) — Applies an ACES input and output device transform, for the chosen ACES version.
- **Auto Gain** (`AutoGain`) — Stretches the tonal range so the darkest and brightest pixels reach set Low and High values.
- **Brightness / Contrast** (`BrightnessContrast`) — Adjusts gain, lift, gamma, contrast, brightness and saturation, with a Low/High range remap.
- **Channel Booleans** (`ChannelBoolean`) — Combines and copies channels from a foreground into a background, with operations such as Copy, Add and Multiply.
- **Chromatic Aberration Removal** (`ChromaticAberrationRemoval`) — Corrects the colour fringing at lens edges, per channel, around a lens centre.
- **Chromatic Adaptation** (`ChromaticAdaptation`) — Changes the white point of an image from one illuminant (or colour temperature) to another.
- **Color Corrector** (`ColorCorrector`) — Full grading: colour, levels, histogram matching and colour suppression, per tonal range.
- **Color Curves** (`ColorCurves`) — Per-channel curves (Red, Green, Blue, Alpha) with an optional match to a reference image.
- **Color Gain** (`ColorGain`) — Gain, lift, gamma and saturation per channel, with balance and hue controls for highs, mids and darks.
- **Color Matrix** (`CustomColorMatrix`) — Applies a custom colour matrix to the channels, with an Invert option.
- **Color Space** (`ColorSpace`) — Converts the image to a colour model (HSV, YUV, HLS and others) and back, or to greyscale (B W).
- **Color Space Transform** (`ColorSpaceTransform`) — Converts between colour spaces and gammas with tone and gamut mapping, without a LUT.
- **Copy Aux** (`Dimension.CopyAux`) — Copies an auxiliary channel (Z, object ID, normals and others) to the colour channels, with remapping.
- **Film Look Creator** (`FilmLookCreator`) — A creative film look, with presets, grain, halation, bloom, vignette and gate weave.
- **Gamut** (`GamutConvert`) — Converts between colour gamuts (primaries) and removes or adds gamma curves.
- **Gamut Limiter** (`GamutLimiter`) — Limits the image to a smaller gamut, such as P3 or Rec.709, to meet a delivery specification.
- **Gamut Mapping** (`GamutMapping`) — Maps an image into a larger or smaller gamut with tone and saturation compression.
- **Hue Curves** (`HueCurves`) — Adjusts hue, saturation, luminance and channels with curves across the hue wheel, and suppresses colours.
- **OCIO CDL Transform** (`OCIOCDLTransform`) — Applies or exports an ASC CDL grade (slope, offset, power and saturation) through OCIO.
- **OCIO ColorSpace** (`OCIOColorSpace`) — Converts between the colour spaces of an OCIO configuration, with an optional look.
- **OCIO Display** (`OCIODisplay`) — Applies an OCIO display and view transform, to see an image as it looks on a display.
- **OCIO File Transform** (`OCIOFileTransform`) — Applies a LUT or transform file through OCIO, in either direction.
- **Set Canvas Color** (`SetCanvasColor`) — Sets the colour of the area outside the image's domain of definition.
- **White Balance** (`WhiteBalance`) — Removes a colour cast, from a picked neutral reference or a colour temperature.

## Composite

Tools that layer, mix and combine images.

- **Merge** (`Merge`) — Layers a foreground image over a background, with position, size and angle controls, blend
  modes (Screen, Multiply, Overlay…) and Porter-Duff operators. The workhorse of every comp.
- **MultiMerge** (`MultiMerge`) — Layers any number of foregrounds over a background in one node, each layer with its
  own Merge-style controls. Tidier than a chain of Merges.
- **Dissolve** (`Dissolve`) — Mixes or switches between two images: cross, additive, erode and random dissolves,
  alpha merges, luminance-map (gradient) wipes and SMPTE wipes.

## Deep Image

Deep image compositing. A deep image keeps several samples per pixel, each with a colour, alpha and depth, so objects that overlap in a pixel can be sorted in depth. These tools need Fusion Studio or DaVinci Resolve Studio. See Deep images (Common Controls) for how the pieces fit together.

- **Image To Deep** (`ImageToDeep`) — Gives a 2D image a depth, so it can be layered with deep images in dMerge.
- **Deep To Image** (`DeepToImage`) — Flattens a deep image into an ordinary 2D image, at the end of a deep chain.
- **Deep To Points** (`DeepToPoints`) — Turns a deep image into a 3D point cloud, to see its samples in depth.
- **dMerge** (`dMerge`) — Merges deep images by sorting their samples in depth. Foreground inputs are added as you connect them.
- **dHoldout** (`dHoldout`) — Cuts a deep image where a deep foreground is in front of it.
- **dCrop** (`dCrop`) — Crops a deep image to a depth range.
- **dResize** (`dResize`) — Resizes a deep image to a width and height in pixels.
- **dTransform** (`dTransform`) — Moves and scales a deep image in X and Y, and scales and shifts its depth.
- **dRecolor** (`dRecolor`) — Recolours the samples of a deep image with a 2D RGB image.
- **dColor Corrector** (`dColorCorrector`) — Grades a deep image at each depth, with the Color Corrector's controls.

## Deep Pixel

Effects that use the extra channels of a 3D render: Z (depth), Normals, UV and the object or material IDs. They work on a 2D image that carries these channels, typically from Renderer 3D. The Common Controls page describes the channels.

- **Ambient Occlusion** (`SSAO`) — Adds ambient occlusion (soft darkening in creases) from Z and Normals, or outputs it on its own.
- **Depth Blur** (`DepthBlur`) — Blurs by depth, for depth of field, or by a colour or matte channel.
- **Fog** (`Fog`) — Adds fog between the near and far depth planes of a render, optionally textured by a noise image.
- **Shader** (`Shader`) — Lights a render from its Normals, with ambient, diffuse, specular and reflection of an environment image.
- **Texture** (`Texture`) — Replaces the texture of rendered objects, using the UV channels.

## Effect

Stylised effects that give an image a particular look: repeated copies, feedback trails, shadows, light flares and rays,
old-TV distortion, false colour, and removal of a moving object. Most take one `Image` input and an Effect Mask, and have
the core Settings tab (Blend, channel and mask controls). Duplicate and Rays are built-in Fuses, which are documented from
their source and aren't created by script.

- **Duplicate** (`Fuse.Duplicate`) — A Fuse that makes a series of offset, scaled and time-shifted copies of the image, optionally along a path and with random jitter.
- **Highlight** (`Highlight`) — Finds hot spots in an image and adds star-like highlights with set rays, length and tint.
- **Hot Spot** (`HotSpot`) — Adds a lens flare, with a main spot and lens elements, optionally occluded by a matte.
- **Object Removal** (`ObjectRemoval`) — Removes a moving object from a shot by filling it from a clean plate of the background (analysis runs in the Fusion page).
- **Pseudo Color** (`PseudoColor`) — Recolours an image by passing each channel through a waveform, so colours sweep with frequency and phase.
- **Rays** (`Fuse.OCLRays`) — A Fuse that adds god rays radiating from a centre out of the bright areas of the image.
- **Shadow** (`Shadow`) — Casts a shadow from an image's alpha, offset and softened, or from a light with a depth map.
- **Trails** (`Trails`) — A 1970s-style feedback effect: each frame builds on the frames before, leaving trails behind moving objects.
- **TV** (`TV`) — Scan lines, roll, wobble and skew for an old-television picture, with scrolling noise bars.

## Film

Tools that emulate film: converting log footage to linear, adding and removing grain, and trimming exposure as a film scanner
or printer would. Film Grain is the tool to use for film grain; Grain is kept for older comps.

- **Cineon Log** (`CineonLog`) — Converts camera and film log formats (Cineon, Arri, BMD Film and others) to linear light, and back.
- **Film Grain** (`FilmGrain`) — Adds film grain modelled on film, with log processing, complexity, seed and per-channel control.
- **Grain** (`Grain`) — The older grain tool, with Power, per-channel difference and Spread curves. Kept for existing comps.
- **Light Trim** (`LightTrim`) — Adjusts exposure in film-scanner trim points (8 to a stop), per channel if required.
- **Remove Noise** (`RemoveNoise`) — Reduces noise and grain by softening and then restoring detail, in Color or Chroma method.

## Filter

Image filters: convolutions, relief and bump maps, and morphological and rank filters. Most work on the whole image, and the
Effect Mask limits them to an area.

- **Filter** (`Filter`) — Standard convolution filters: relief, emboss, defocus, Sobel and Laplacian edges, and noise or grain.
- **Custom Filter** (`CustomFilter`) — A user-defined convolution with a matrix of up to 7 x 7 whole-number weights, set in the Inspector.
- **Erode / Dilate** (`ErodeDilate`) — Shrinks or grows the image's bright or dark areas, for contracting and expanding mattes.
- **Rank Filter** (`RankFilter`) — Replaces each pixel with the value at a chosen rank among its neighbours: removes specks, or gives a painted look.
- **Create Bump Map** (`CreateBumpMap`) — Turns a grayscale height image into a bump map of surface normals, for BumpMap and Relight.
- **Create Relief Map** (`CreateReliefMap`) — Turns a height field into a relief map for the Relief Map tool.

## Flow

Tools that organise a comp rather than process images: sticky notes, underlays and wireless links.

- **Note** (`Note`) — A sticky note with text, placed in the node editor. It has no inputs or outputs.
- **Underlay** (`Underlay`) — A labelled area behind nodes, to group a section of the tree. It doesn't restrict connections.
- **Wireless Link** (`Fuse.Wireless`) — Passes an image through unchanged, so a distant node can be linked without a wire.

## Generator

Tools that create images from nothing: backgrounds, text, noise and patterns.

- **Text+** (`TextPlus`) — The main titling tool: styled text with per-character transforms, up to eight shading
  elements (fill, outline, shadow, border), and point, box, circle or path layouts. Animate it with Follower and
  other text modifiers.
- **MultiText** (`MultiText`) — Several independent text layers in one node, each with simplified Text+ styling
  (Fill, Outline and Shadow only; no character or word transforms). Good for multi-part titles and lower thirds.
- **Background** (`Background`) — Solid colour, or a horizontal, vertical, four-corner or shaped (linear, radial,
  angle…) gradient. Use it as a backdrop, a colour matte, a canvas to merge onto, or masked to fill shapes.
- **Fast Noise** (`FastNoise`) — Fast, animatable Perlin-style noise: clouds, smoke, fog, water, organic textures.
  It's also the usual source for driving Displace, gradient wipes and masks.
- **Plasma** (`Plasma`) — Smooth, swirling colour patterns built from overlapping circular waves. Useful for abstract
  backgrounds and as a map for distortion tools.
- **Day Sky** (`DaySky`) — An HDR map of daylight for a given location, date and time, used for lighting 3D
  scenes. It isn't a visible sky generator. Only northern and eastern locations can be set (latitude and longitude
  have a minimum of 0).
- **Mandelbrot** (`Mandel`) — Renders the Mandelbrot fractal, with zoom, iterations and colour controls.
- **OGraf Loader** (`OGrafLoader`) — Plays an OGraf HTML graphics template, with trim, time scale, looping and
  scheduled actions. *New: not covered in the Fusion 21 manual; documented from the tool and its source.*

## I/O

Getting media into and out of a comp. In DaVinci Resolve, clips come in and go out through MediaIn and MediaOut. Loader and
Saver are for file-based work, as in Fusion Studio.

- **Media In** (`MediaIn`) — Brings a timeline clip or a Media Pool clip into the comp. The usual start of every Resolve comp.
- **Media Out** (`MediaOut`) — The comp's output back to the timeline.
- **Loader** (`Loader`) — Reads a file or numbered sequence from disk, with trim, hold, loop and import settings. In Resolve it is for EXR files only.
- **Saver** (`Saver`) — Writes a file or numbered sequence to disk when the comp renders, in one of eight formats, with each format's own options.

## Layer

Multilayer images: a layer is a named group of channels inside a file, such as the passes of an EXR. These tools combine,
rename, filter and build layers.

- **Layer Muxer** (`LayerMuxer`) — Adds the layers of one multilayer image to another, and chooses the default layer.
- **Layer Regex** (`LayerRegex`) — Renames, keeps or removes layers by matching their names with a regular expression.
- **Layer Remover** (`LayerRemover`) — Removes checked layers from a multilayer image.
- **Swizzler** (`Swizzler`) — Builds new layers from channels taken from several images, for assembling passes into a multilayer file.

## LUT

Colour lookup tables: applying a LUT from a file, and building a 3D LUT from a graded test cube.

- **File LUT** (`FileLUT`) — Applies a LUT from a file on disk. Only the path is stored in the comp, so many comps can share one file.
- **LUT Cube Creator** (`Fuse.LUTCubeCreator`) — Generates a colour-cube test image to grade, as the first step of building a 3D LUT.
- **LUT Cube Analyzer** (`Fuse.LUTCubeAnalyzer`) — Writes a graded LUT Cube image to a 3D LUT file (ALUT3, CUBE or 3DL).
- **LUT Cube Apply** (`Fuse.LUTCubeApply`) — Applies a graded LUT Cube image to footage inside the comp, without writing a file.

## Mask

Tools that make single-channel masks for other tools' Effect Mask inputs, for shapes, rotoscoping and selecting by
colour or tone. Masks can be chained: a mask's own EffectMask input takes another mask, and its Paint Mode sets how the
two combine.

- **Polygon Mask** (`PolylineMask`) — A Bézier polyline mask for rotoscoping objects without a regular shape.
- **B-Spline Mask** (`BSplineMask`) — A smooth mask drawn with B-Spline points, which need fewer points than a polygon.
- **MultiPoly** (`MultiPoly`) — Several polygon and B-Spline shapes in one node, as a list of named layers.
- **Ellipse Mask** (`EllipseMask`) — A circle or ellipse, with width, height and angle.
- **Rectangle Mask** (`RectangleMask`) — A rectangle or rounded rectangle, with width, height and angle.
- **Triangle Mask** (`TriangleMask`) — A triangle set by its three corner points.
- **Bitmap Mask** (`BitmapMask`) — A mask made from one channel of an image, with threshold clipping.
- **Ranges Mask** (`RangesMask`) — A mask of the shadows, midtones or highlights of an image, set with a tonal curve.
- **Wand Mask** (`WandMask`) — A mask of the colour around a chosen point, like a magic wand.
- **Mask Paint** (`PaintMask`) — A mask painted freehand in the viewer, for fixing holes in a matte.

## Matte

Tools that make, refine and combine alpha channels: keyers for blue and green screens, tools that pull a matte from a
channel or a difference, clean plates for keying, and the tools that merge mattes together. Most keyers have the same
Matte tab (threshold, blur, contract/expand, gamma), the same solid and garbage mask inputs, and output a keyed image
for a Merge. Keyers are usually followed by a Matte Control to combine or choke the result.

- **Alpha Divide** (`AlphaDivide`) — Divides the colour by the alpha, to take an image with premultiplied alpha to straight colour for colour correction.
- **Alpha Multiply** (`AlphaMultiply`) — Multiplies the colour by the alpha, returning straight-colour work to premultiplied form.
- **Chroma Keyer** (`ChromaKeyer`) — Makes a matte from ranges of colour picked over a uniform screen, with spill suppression for the edges.
- **Clean Plate** (`CleanPLate`) — Builds an image of the screen with the subject removed, to feed the Delta Keyer's Clean input.
- **Cryptomatte** (`Cryptomatte`) — Decodes the Cryptomatte IDs in an EXR, to pick mattes for named objects or materials.
- **Delta Keyer** (`DeltaKeyer`) — The main blue and green screen keyer: screen colour pick, Pre-Matte, matte refinement, spill and fringe, and a Clean Plate input.
- **Depth Map** (`DepthMap`) — Makes an alpha from the distance of objects from the camera, for grading or blurring a depth band.
- **Difference Keyer** (`DifferenceKeyer`) — Makes a rough matte from the difference between a shot with the subject and a clean plate of the set.
- **Luma Keyer** (`LumaKeyer`) — Makes a matte from a range of one channel, usually luminance, and can key from the alpha or depth too.
- **Magic Mask** (`MagicMask`) — Tracks a mask for a person or object from points placed in the viewer, using the DaVinci AI Neural Engine.
- **Matte Control** (`MatteControl`) — Combines the alpha of one image with another, with add, subtract and choke, plus garbage and solid mattes and spill suppression.
- **Relight** (`Relight`) — Adds a light to a shot, reflected off a surface map the tool builds from the image.
- **Ultra Keyer** (`UltraKeyer`) — A two-stage blue and green screen keyer, with a Pre-Matte stage, for shots the Delta Keyer doesn't key cleanly.

## Metadata

Image metadata: the name and value pairs that travel with an image, and the timecode. These tools change the metadata of an image and leave its pixels as they are. They are Fuses that ship in Fusion's Blackmagic Fuses folder.

- **Copy Metadata** (`Fuse.FLS_CopyMetadata`) — Copies, merges, replaces or clears the metadata of an image.
- **Set Metadata** (`Fuse.SetMetaData`) — Adds, changes or removes a single custom name and value.
- **Set Time Code** (`Fuse.SetMetaDataTC`) — Writes a timecode into each frame's metadata, counted from a start value.

## Miscellaneous

Tools for retiming, depth, domains, interlaced video, switching and scripted expressions, plus a few utilities.

- **Time Speed** (`TimeSpeed`) — Changes a clip's speed by a fixed multiple, delays it, or reverses it. Speed can't be animated.
- **Time Stretcher** (`TimeStretcher`) — Retimes a clip with an animated curve, for speed ramps, holds and rewinds.
- **Speed Warp** (`SpeedWarp`) — AI-based retiming, for smooth slow motion of complex motion.
- **Frame Average** (`Fuse.FrameAverage`) — Averages a run of frames around each frame, for smoothing or a simple motion blur.
- **Keyframe Stretcher** (`KeyStretcher`) — Retimes keys to fit the length of the tool it feeds. Not run live.
- **Switch** (`Switch`) — Passes one of several image inputs, chosen by a number. For the modifier that switches a parameter, see Switch (modifier) in Modifiers.
- **Custom Tool** (`Custom`) — Per-pixel expressions for each channel, with setup and intermediate values, numbers, points and LUT curves.
- **Change Depth** (`ChangeDepth`) — Changes the processing bit depth, with dither when reducing it.
- **Fields** (`Fields`) — Strips, interpolates, de-interlaces or interlaces video fields.
- **Auto Domain** (`AutoDomain`) — Sets the domain of definition to the area with content, so later tools skip the rest.
- **Set Domain** (`SetDomain`) — Sets or offsets the domain of definition by hand.
- **Run Command** (`RunCommand`) — Runs an external program at the start, per frame, or at the end of a render.

## Optical Flow

Motion vectors, retiming and frame repair. Optical Flow measures how each pixel moves between frames and stores the motion in the Vector and BackVector channels, and the other tools here read those channels. Tween and Repair Frame calculate their own motion. The motion is calculated when frames are rendered, so these tools are not checked from a script.

- **Optical Flow** (`Dimension.OpticalFlow`) — Analyses a sequence and stores the motion vectors in the image's channels.
- **Tween** (`Dimension.Tween`) — Makes an in-between frame from two images, by warping them with optical flow.
- **Repair Frame** (`Dimension.RepairFrame`) — Fills dust, scratches and dropouts from the neighbouring frames.
- **Smooth Motion** (`Dimension.SmoothMotion`) — Smooths the chosen channels over time, using the motion of neighbouring frames.
- **Vector Denoise** (`VectorDenoise`) — Averages pixels over time along the motion, to reduce noise.
- **Vector Transform** (`VectorTransform`) — Resizes, rotates and attenuates the motion vectors.
- **Vector Warp** (`VectorWarp`) — Warps a still or texture with the motion of the shot, for tracking a painted element.

Vector Motion Blur (`VectorMotionBlur`), in the Blur category, reads the same vectors.

## Paint

Stroke-based painting. Strokes are drawn and edited in the viewer.

- **Paint** (`Paint`) — Brush strokes for cloning, wire and rig removal, and hand-painted masks and mattes. Strokes can't be created or edited from script: only the tool's connections can.

## Particles

Particle systems for motion graphics. A source (pEmitter, or pImageEmitter for a picture) makes particles, forces and limiters
change how they move or look, and pRender turns the particles into an image (2D) or 3D geometry. Every particle tool
except pRender takes and gives `Particles`, so a branch is a chain: source, then any number of forces, styles and limiters,
then pRender. A particle tool does nothing alone, and its result shows only once it reaches pRender. The shared controls
(Conditions, Region and Style tabs) are in Common Controls → Particle tools.

A typical chain is pEmitter → forces → pRender → Merge. pRender's OutputMode chooses the output: `"TwoD"` for an image,
`"ThreeD"` (the default) for geometry that goes to a Renderer 3D.

- **pEmitter** (`pEmitter`) — The main source: creates particles in a region, with lifespan, velocity, rotation and a visual style.
- **pImageEmitter** (`pImageEmitter`) — Makes one particle per pixel of an image, coloured from the image.
- **pRender** (`pRender`) — Ends a branch: renders the particles to an image (TwoD) or 3D geometry (ThreeD).
- **pDirectionalForce** (`pDirectionalForce`) — A constant push in one direction, such as gravity or wind.
- **pTurbulence** (`pTurbulence`) — Random, chaotic motion, with strength per axis and over the particle's life.
- **pVortex** (`pVortex`) — A swirl that draws particles round a centre.
- **pPointForce** (`pPointForce`) — Attracts or repels particles from a single point.
- **pTangentForce** (`pTangentForce`) — Pushes particles sideways, so they circulate around a centre.
- **pGradientForce** (`pGradientForce`) — Pushes particles along the alpha gradient of an image.
- **pFriction** (`pFriction`) — Slows particles in a region, and reduces their spin.
- **pFollow** (`pFollow`) — Makes particles spring toward a point that you can animate.
- **pFlock** (`pFlock`) — Flocking behaviour: particles follow, gather and keep apart from their neighbours.
- **pAvoid** (`pAvoid`) — Makes particles steer away from a region.
- **pBounce** (`pBounce`) — Bounces particles off a region, with elasticity, roughness and surface motion.
- **pKill** (`pKill`) — Removes particles that cross or enter its region.
- **pSpawn** (`pSpawn`) — Makes each particle create new particles of its own, for bursts and trails.
- **pChangeStyle** (`pChangeStyle`) — Changes the look of particles that meet its region, with a new style or set.
- **pCustom** (`pCustom`) — Sets particle position, velocity, colour and more from expressions you write.
- **pCustomForce** (`pCustomForce`) — Applies a force to particles from expressions you write.
- **pMerge** (`pMerge`) — Combines two particle streams into one.

## Position

Tools driven by world-position passes: images whose colour channels hold the XYZ position of each pixel in 3D space. They make volumes and masks that sit in the scene's space, rather than in the image's depth. The Z To WorldPos tool converts between a Z channel and a position pass.

- **Volume Fog** (`VolumeFog`) — Adds fog inside a sphere or cube placed in the scene's space, using the position pass.
- **Volume Mask** (`VolumeMask`) — Makes a mask from the objects inside a sphere or cube placed in the scene's space.
- **Z to WorldPos** (`ZtoWorldPos`) — Makes a world-position pass from a Z channel and a camera, or a Z channel from a position pass.

## Shape

Resolution-independent vector shapes. Shape tools pass a shape tree (`ShapeTree` output) to each other, and you
only see the result once it goes through **sRender**, which turns it into an image. A typical chain is a generator
(sRectangle, sEllipse…), then modifiers (sGrid, sDuplicate, sJitter…), then sMerge/sBoolean, then sRender, then Merge.

- **sRender** (`sRender`) — Converts a shape tree into an image at a chosen resolution. Every shape chain ends here.
- **sRectangle** (`sRectangle`) — Rectangle or rounded rectangle; filled or as an outline that can write on.
- **sEllipse** (`sEllipse`) — Circle or ellipse; filled or as an outline that can write on.
- **sNGon** (`sNGon`) — A regular polygon (triangle, hexagon, …) with a chosen number of sides.
- **sStar** (`sStar`) — A star with a chosen number of points and point depth.
- **sPolygon** (`sPolygon`) — A freely drawn Bézier shape or open line, with write-on. Its points are drawn in the
  viewer or set from a script.
- **sBSpline** (`sBSpline`) — The same as sPolygon, but drawn with B-spline curves.
- **sText** (`sText`) — Text as vector shapes, so it can be duplicated, gridded, jittered and combined with other
  shapes.
- **sMerge** (`sMerge`) — Combines any number of shape trees, keeping each one's own style.
- **sBoolean** (`sBoolean`) — Combines two shapes as a union, intersection, subtraction or XOR.
- **sTransform** (`sTransform`) — An extra transform (offset, size, rotation, pivot) on top of a shape's own,
  for building hierarchical animation.
- **sDuplicate** (`sDuplicate`) — Makes a series of copies of a shape, each offset in position, size, rotation,
  colour and time from the last, optionally along a path, with built-in random jitter.
- **sGrid** (`sGrid`) — Repeats a shape in rows and columns, with row and column offsets.
- **sJitter** (`sJitter`) — Randomises the position, size and rotation of each shape from sGrid or sDuplicate, or
  jitters the individual points of a shape. Can auto-animate.
- **sExpand** (`sExpand`) — Grows (dilates) or shrinks (erodes) a shape.
- **sOutline** (`sOutline`) — Turns shapes into outlines, with border width and style, and write-on.
- **sChangeStyle** (`sChangeStyle`) — Replaces the colour and style of everything upstream of it.

## Stereo

Stereoscopic 3D. Left and right eye images are combined, split, aligned, and turned into disparity or depth. Most of these tools need Fusion Studio or DaVinci Resolve Studio. Disparity is calculated when frames are rendered, so the Disparity-based tools are set up in the UI and not checked from a script.

- **Anaglyph** (`Anaglyph`) — Combines a left and right image into a coloured anaglyph, for viewing with glasses.
- **Combiner** (`Combiner`) — Stacks a left and right image side by side or one above the other, or as named layers.
- **Splitter** (`Splitter`) — Splits a stacked stereo image into its left and right eyes.
- **Disparity** (`Dimension.Disparity`) — Works out the shift between the eyes, for disparity-based tools.
- **Disparity To Z** (`Dimension.DisparityToZ`) — Calculates a Z channel from disparity, with a stereo camera.
- **Z To Disparity** (`Dimension.ZToDisparity`) — Calculates disparity from the Z channel of a CG stereo render.
- **Global Align** (`Dimension.GlobalAlign`) — Shifts and rotates one eye quickly, to correct large differences before disparity.
- **Stereo Align** (`Dimension.StereoAlign`) — Corrects vertical alignment, convergence and eye separation in one node.
- **New Eye** (`Dimension.NewEye`) — Builds a new eye between or beyond the two eyes, by interpolating with disparity.

## Tracking

Tools that follow motion through a clip. The Tracker follows points, and its paths can be used by other tools' controls
without a wire, or applied directly as a match move, stabilisation or corner pin. The Planar Tracker follows a flat
surface with its perspective, the Surface Tracker follows a deforming one, and the Camera Tracker solves the camera's 3D
motion. Tracking and solving run on the processed clip in the UI.

- **Camera Tracker** (`Dimension.CameraTracker`) — Tracks features through a shot and solves the camera's 3D motion and lens, for placing 3D elements into the plate.
- **Planar Tracker** (`Dimension.PlanarTracker`) — Tracks a flat surface with its perspective, for Steady, Corner Pin, Stabilize and Planar Transform (match move) work.
- **Surface Tracker** (`SurfaceTracker`) — Applies a graphic to a deforming surface, such as cloth or skin, by tracking a mesh placed over its folds.
- **Tracker** (`Tracker`) — The point tracker: follows up to several patterns, and applies the result as a match move, stabilisation, corner positioning or perspective positioning, or publishes its paths for other tools' controls.

## Transform

Tools that move, rotate, scale, crop, resize and reframe images. Transform, Camera Shake, DVE and Planar Transform keep the frame size; Crop, Letterbox, Resize and Scale change it.

- **Transform** (`Transform`) — Moves, rotates, scales, flips and stretches an image inside the same frame.
- **Camera Shake** (`CameraShake`) — Simulates handheld or mechanical camera shake, with deviation, speed and frequency controls.
- **Crop** (`Crop`) — Cuts out a rectangle, or offsets the image, in pixels, changing the resolution.
- **DVE** (`DVE`) — A 3D transform in the style of online effects systems: rotation about a pivot, Z move and perspective, with a pre-transform mask.
- **Letterbox** (`Letterbox`) — Fits a widescreen or film image into another frame size, with letterbox bars or pan-and-scan.
- **Planar Transform** (`Dimension.PlanarTransform`) — Moves an image to follow a plane tracked by a Planar Tracker.
- **Resize** (`BetterResize`) — Changes the frame to an exact width and height in pixels, optionally keeping the aspect.
- **Scale** (`Scale`) — Changes the frame by a multiplier, with separate X and Y sizes when Lock X/Y is off.

## USD

The USD tools build and render Universal Scene Description scenes. They are a separate system from the classic 3D tools:
they pass USD scenes (`USD` outputs), not 3D scenes, so a USD output doesn't connect to a Merge 3D or Renderer 3D. A typical
chain brings in geometry (uLoader, or uShape for a primitive), combines it in a uMerge with uCamera and the lights, renders
it with uRenderer, and merges the image over the video. Materials come from uShader, uMaterialX and uReplaceMaterial, and
textures from uTexture, uTextureTransform and uNormalMap. uSwitch and uVariant choose between alternatives.

- **uLoader** (`uLoader`) — Loads a USD scene from a `.usd`, `.usda`, `.usdc` or `.usdz` file, with its trim, time and loop controls.
- **uShape** (`uShape`) — A primitive (capsule, cone, cube, cylinder, icosphere, plane, sphere or torus) with its material.
- **uMerge** (`uMerge`) — Combines USD scenes, cameras, lights and other merges into one scene. Its transform moves the whole group.
- **uRenderer** (`uRenderer`) — Renders a USD scene to an image, with Storm, lighting, shadows and output passes.
- **uCamera** (`uCamera`) — A virtual camera with a real lens and film back, and an optional image plane and projection.
- **uCylinder Light** (`uCylinderLight`) — A tube light with length and radius.
- **uDisk Light** (`uDiskLight`) — A round, flat softbox-like light.
- **uDistant Light** (`uDistantLight`) — A directional, sun-like light with shadows.
- **uDome Light** (`uDomeLight`) — An environment light, lit by an image.
- **uRectangle Light** (`uRectLight`) — A flat rectangular panel light.
- **uSphere Light** (`uSphereLight`) — A local light from a sphere.
- **uProjector** (`uProjector`) — Projects an image onto the scene as light, or as a texture for uCatcher.
- **uCatcher** (`uCatcher`) — Catches a uProjector or uCamera texture projection on the geometry it is connected to.
- **uImage Plane** (`uImagePlane`) — A textured card in 3D space, from an image input or a file.
- **uDuplicate** (`uDuplicate`) — Copies a USD scene in rows and arrays, with jitter, along a path, and limited by a region.
- **uTransform** (`uTransform`) — Moves, turns and scales the chosen prims of a USD scene.
- **uVisibility** (`uVisibility`) — Shows or hides the chosen prims.
- **uVariant** (`uVariant`) — Chooses a variant set and variant from a USD asset.
- **uSwitch** (`uSwitch`) — Passes one of several sources through, chosen by a Source control.
- **uReplace Material** (`uReplaceMaterial`) — Assigns a new material (colour, texture or MaterialX) to chosen objects.
- **uMaterialX** (`uMaterialX`) — Loads a MaterialX `.mtlx` file as a material.
- **uShader** (`uShader`) — A USD or MaterialX surface, with texture sockets for each channel.
- **uTexture** (`uTexture`) — Loads an image as a texture, or takes one from a Fusion node.
- **uTexture Transform** (`uTextureTransform`) — Moves, turns and scales a texture before it reaches a shader.
- **uNormal Map** (`uNormalMap`) — Prepares a normal map for a shader's normal socket.
- **uExport** (`uExport`) — Writes the USD scene to a `.usd`, `.usda`, `.usdc` or `.usdz` file.
- **uVolume** (`uVolume`) — Brings in a VDB volume (smoke, fire, cloud) with density and emission controls.

## VR

360° and immersive video. These tools change the layout of a spherical image, patch sections of it, and stabilise it. They need Fusion Studio or DaVinci Resolve Studio.

- **Immersive Patcher** (`ImmersivePatcher`) — Converts a section of an immersive frame to flat 2D and back, for editing in a pair.
- **LatLong Patcher** (`LatLongPatcher`) — Extracts a section of a lat-long image as a flat square, and applies the edited square back over it.
- **PanoMap** (`PanoMap`) — Converts a spherical image between layouts, such as lat-long, cube map and VR180, and rotates it.
- **Spherical Stabilizer** (`SphericalStabilizer`) — Tracks the camera rotation through a 360° shot and cancels it.

## Warp

Tools that distort, bend, pin or reshape an image, from lens corrections and ripples to corner pinning and motion-driven warps.

- **Coordinate Space** (`CoordSpace`) — Converts between rectangular and polar coordinates, for tunnel and radial effects.
- **Corner Positioner** (`CornerPositioner`) — Pins the four corners of an image to any quadrilateral, in 2D or perspective.
- **Dent** (`Dent`) — A circular bulge, pinch or fish-eye dent in six filter styles.
- **Displace** (`Displace`) — Refracts an image using another image as a map: heat shimmer, water and bevelled glass.
- **Drip** (`Drip`) — A ripple across the image in several shapes, with amplitude, frequency and phase.
- **Grid Warp** (`GridWarp`) — Warps the image with a mesh of source and destination points, shaped in the viewer.
- **Lens Distort** (`LensDistort`) — Removes or restores lens distortion, with several lens models.
- **Perspective Positioner** (`PerspectivePositioner`) — Removes perspective from a skewed object, mapping its four corners to a flat image.
- **Vector Distortion** (`Distort`) — Moves each pixel by vector channels from the image or a second map, such as optical flow.
- **Vortex** (`Vortex`) — A swirling whirlpool with centre, size, angle and power.

## Krokodove: 3D

Tools that change a 3D scene from the Krokodove plug-in set. Each takes a scene (`DataType3D`) in its **SceneInput** and outputs a scene, so they fit between geometry and a Merge 3D, in the same way as the core 3D tools. Like the core tools, a chain ends at a **Renderer 3D**, which turns the scene into an image for a Merge over a video. The Krokodove 3D Create tools make new geometry; see that overview.

Most of these work on the individual parts of a scene: polygons, vertices, or whole objects. Several take a **Region** (see Krokodove: Region) that decides where the effect applies. Those that act over many parts also have a **Range**, a sweep that moves through the parts in an order, so the effect can spread across the object over time.

- **Align 3D** (`KD_Align3D`) — Moves a scene so its bounding box lines up with the origin, on each axis, from its minimum, middle or maximum face.
- **Connect 3D** (`KD_Connect3D`) — Draws links between the vertices of a scene: between every pair, in one chain, or along the polygon edges to make a wireframe.
- **Kill 3D** (`KD_Kill3D`) — Removes the polygons inside a region, and shrinks and fades those at its soft edges. Animate the Range to break an object up.
- **Mapped Duplicate 3D** (`KD_MappedDuplicate3D`) — Makes a grid of copies of a scene, each with its own offset, rotation, scale, time and chance of appearing, set by numbers or by images. Its output is `Data3D`.
- **Objectify 3D** (`KD_Objectify3D`) — Moves and fades whole objects, or the elements inside them, in proportion to a region.
- **Poly Play 3D** (`KD_PolyPlay3D`) — Offsets, rotates, scales, extrudes and recolours each polygon in its own frame, where a region and range select them.

**Use for:** motion-graphics scenes built from geometry: breaking up or reassembling a title, wireframes and cages, grids of copies, and objects that move or fade inside a region. For VFX work, these pair with Camera 3D and Image Plane 3D, or with a Camera Tracker scene, so that an effect can be placed in the plate's space.

Each operator lists its own controls in its section. The shared 3D tabs of the core tools (Transform, Controls and Material) are described in Common Controls → 3D objects. These operators have their own equivalents, not those tabs.

## Krokodove: 3D Create

Geometry generators from the Krokodove plug-in set. Each makes a new 3D surface from its own controls, not from the geometry of its input, and outputs a scene (`DataType3D`). Their **SceneInput** is optional, as on Cube 3D, so a generator can be used alone or with a scene already connected. A **MaterialInput** takes a material; unconnected, the basic material on the Material tab is used. Like the other 3D tools, a generator's output goes to a Merge 3D and then a Renderer 3D.

All three share the same 3D controls (Transform, with its `Transform3DOp` IDs, and the Controls tab's visibility, lighting, matte and blend settings). Their surfaces can be animated with the Range, Grow and Fold controls, as the sections describe.

- **Fold Create 3D** (`KD_FoldCreate3D`) — A sheet divided into strips that fold over one another, in Parallel, Zig Zag, or Mapped by an image. Grow Out unfolds it.
- **Heightfield Create 3D** (`KD_HeightfieldCreate3D`) — A grid of squares or bars whose heights come from images, for reliefs and bar charts.
- **Tube Create 3D** (`KD_TubeCreate3D`) — A polygon or star profile swept along a smooth path through a set of points, with taper, twist and a range that draws it on.

**Use for:** origami and paper reveals (Fold), landscapes and bar charts from pictures (Heightfield), and pipes, cables and curved ribbons (Tube). The results are ordinary 3D surfaces, so they can be lit, shadowed and then passed through a Krokodove 3D operator, such as Poly Play 3D or Kill 3D, to be broken up.

## Krokodove: Image

Krokodove image tools that process a picture: they distort, extend, fill, break up, or re-pixel the image, or
trace it into a new form. Most take one `Image` input and an Effect Mask. Connect and Worm draw their own line
art and use the image only for the pen (see their sections).

- **Bounding Box** (`KD_BoundingBox`) — Fills the rectangle that encloses the area where a channel reaches a threshold.
- **Color Map** (`KD_ColorMap`) — Places a map into the colour regions of the image, from manual or automatic colours.
- **Connect** (`KD_Connect`) — Draws a line through a list of points, straight or smoothly curved.
- **Dither** (`KD_Dither`) — Reduces the bits per channel and adds dither noise to avoid banding.
- **Extend** (`KD_Extend`) — Repeats the edge pixels along a horizontal or vertical line, creating streaks.
- **Fragments** (`KD_Fragments`) — Breaks the image into pieces that can fade in and out over time.
- **Grow** (`KD_Grow`) — Grows or removes the image from one or more seed points.
- **Grow Color** (`KD_GrowColor`) — Fills transparent areas by extending the colour at the edges.
- **Microwaves** (`KD_Microwaves`) — Adds radiating light beams from a centre point.
- **Pack** (`KD_Pack`) — Packs many small shapes into a channel's area, coloured solid, from the image, or from a shape input.
- **Painterly** (`KD_Painterly`) — Gives the image a painted look by choosing colours within a brush area.
- **Rasterize** (`KD_Rasterize`) — Converts the image into a half-tone pattern of shapes sized by brightness.
- **Time Mapper** (`KD_TimeMapper`) — Shows a different moment of a sequence at each pixel, set by a time map image.
- **Worm** (`KD_Worm`) — Draws a path of straight and curved segments, with a write-on and repeats.

## Krokodove: Image Color

Krokodove colour tools. They change the colour of an image: inverting, matching tones, thresholding,
or replacing specific colours.

- **Invert** (`KD_Invert`) — Inverts the colour, luminance or hue of the image.
- **Match Color** (`KD_MatchColor`) — Changes the shadows, midtones and highlights to match chosen source and destination colours.
- **Recolor** (`KD_Recolor`) — Replaces up to 63 uniform colours with other colours.
- **Replace Color** (`KD_ReplaceColor`) — Replaces a range of colours around a source colour with a destination colour.
- **Threshold** (`KD_Threshold`) — Clips each channel at a threshold, with softness, repeats and ping-pong.

## Krokodove: Image Create

Krokodove generators. They take no image input and create a picture from scratch: noise, blobs, line and shape
patterns, and tiled patterns. Most work well as sources for other tools, or as textures and backgrounds.

- **Blobs** (`KD_Blobs`) — Draws soft, merging round blobs at positions you set.
- **Generate** (`KD_Generate`) — Creates procedural noise (Perlin, Worley, fluid, plasma and others), with animation.
- **Lines** (`KD_Lines`) — Draws sets of lines that interpolate between a first and a last line set.
- **Pattern** (`KD_Pattern`) — Fills the frame with a repeating triangle, grid or honeycomb pattern.
- **Shapes** (`KD_Shapes`) — Draws sets of concentric circles or squares that interpolate between a first and a last set.

## Krokodove: Image Pixel

Krokodove image tools that work on the pixels of a picture. They combine frames over time, add a bevel, plastic sheen
or extrusion, shift and duplicate colour channels, tile or sort the pixel values, and make the edges of a frame join up.
Most take one `Image` input and an Effect Mask, and they have the core Settings tab (Blend, channel and mask controls).
Tools that move the picture around on a warp grid are in Krokodove: Image Warp.

- **Average** (`KD_Average`) — Blends several consecutive frames into one image, with frame count and step controls.
- **Bevel** (`KD_Bevel`) — Adds a raised, lit edge inside the image's alpha, with an optional shaped profile.
- **Channel Shifter** (`KD_ChannelShifter`) — Offsets, blurs and scales five sets of colour channels so they separate.
- **Clean Edges** (`KD_CleanEdges`) — Replaces a band of pixels along each edge with repeated pixels or a solid colour.
- **Deflicker** (`KD_Deflicker`) — Matches each frame's brightness to a reference to remove flicker.
- **Duplicate (Krokodove)** (`KD_Duplicate`) — Makes many copies of the image, placed by two shapes that can morph between them.
- **Extrude (Krokodove)** (`KD_Extrude`) — Extrudes the edges of the image into a shaded solid behind it.
- **Noise (Krokodove)** (`KD_Noise`) — Adds random noise, in colour or position, with an optional colour palette.
- **Plastic** (`KD_Plastic`) — Lays a glossy plastic sheen over the image from its luminance, lit from a point or direction.
- **Positioner** (`KD_Positioner`) — Pins the image to destination points, one to four pairs, as a corner-pin.
- **Push** (`KD_Push`) — Slides the image across the frame, filling the gap from a second input.
- **Rest** (`KD_Rest`) — Settles the image's pixels onto a floor line, column by column.
- **Seamless** (`KD_Seamless`) — Blends the opposite edges of the image so that it tiles without a seam.
- **Seamless Loop** (`KD_SeamlessLoop`) — Cross-fades the end of a clip into its start so that it loops without a jump.
- **Sort** (`KD_Sort`) — Orders the pixels of each row or column by colour value, over a range of time.

## Krokodove: Image Position

Krokodove tools that find the position of edges in an image.

- **Contour** (`KD_Contour`) — Draws an anti-aliased outline around the edges of the image.

## Krokodove: Image Vector

Krokodove tools for motion vectors. They need an image that carries velocity data, and show that data on the frame.

- **Vector Visualization** (`KD_VectorVisualization`) — Draws arrows showing motion direction and speed from the image's vectors.

## Krokodove: Image Warp

Krokodove image tools that distort the picture by moving its pixels. They bend, stretch, shear, mirror, fold, push and
spherize the image, or rearrange it in tiles and segments. Most take an `Image` input, an optional Warp Mask that limits
or varies the warp, and an Effect Mask; their shared Render controls are under Common Controls → Krokodove tools.

- **Bend** (`KD_Bend`) — Bends the image along a curve, set by three points or by a centre, radius and angles.
- **Directional Scale** (`KD_DirectionalScale`) — Stretches or squashes the image along a chosen axis.
- **Kaleidoscope (Krokodove)** (`KD_Kaleidoscope`) — Folds the image into a repeating pattern of segments around a centre.
- **Mirror (Krokodove)** (`KD_Mirror`) — Reflects one side of the image across a line, with a Mirror All option.
- **Offset (Krokodove)** (`KD_Offset`) — Displaces each pixel by an amount read from a Deformation map's channels.
- **Radial** (`KD_Radial`) — Pushes the image outward from, or pulls it inward towards, a centre point.
- **Relative Transform** (`KD_RelativeTransform`) — Transforms the image around its own content, found from its bounding box or its weighted pixels.
- **Segment Transform** (`KD_SegmentTransform`) — Cuts the frame into segments and rotates and scales each one about its own centre.
- **Shear** (`KD_Shear`) — Slants the image along a dividing axis, by value or by angle.
- **Shuffle** (`KD_Shuffle`) — Cuts the frame into a grid of tiles and slides or swaps them.
- **Spherize** (`KD_Spherize`) — Bulges or pinches a region (band, circle or rectangle) to give a lens or sphere look.
- **Stretch** (`KD_Stretch`) — Stretches the part of the image between two points to fill a new span.
- **Warped Transform** (`KD_Transform`) — A position, angle and size transform that can be limited by a warp mask.

## Krokodove: Region

Regions are 3D volumes used by other Krokodove tools. A region doesn't make an image. It is a field that gives every point in a 3D scene a value from 0 (outside) to 1 (inside), with soft edges where the values are between. A 3D Krokodove tool, such as **Kill3D**, multiplies its effect by that value at each object's position, so the effect applies only inside the region.

Regions are built in a chain. A generator creates a basic volume, and the modifier tools combine, move and reshape it:

- **Generators** make a volume from nothing: **rCube** (a box), **rSphere** (a sphere), **rPlane** (a half-space on one side of a plane) and **rNoise** (a patchy 3D noise field).
- **Modifiers** take a region as input and return a new one: **rMerge** combines two regions (union, intersect, add, subtract or exclusive), **rModify** changes its brightness, contrast and edge, and **rTransform** moves, rotates and scales it.

The output of the last region in the chain is connected to the **Region** input of the 3D tool. Each region tool has an Invert control that swaps inside and outside. Regions are not rendered, so there is nothing to see until a 3D tool uses them. They work in the 3D scene's units: a default rCube runs from −1 to 1 on each axis, and a default rSphere has radius 1.

- **rCube** (`KD_Region3DCube`) — A box region, with softness on each axis.
- **rSphere** (`KD_Region3DSphere`) — A spherical region, with a soft edge set by Softness X.
- **rPlane** (`KD_Region3DPlane`) — A half-space on the side that the plane's +Z axis points to, with a soft transition set by Softness Z.
- **rNoise** (`KD_Region3DNoise`) — A patchy region from a 3D noise field, with brightness and contrast.
- **rMerge** (`KD_Region3DMerge`) — Combines two regions with a set operation.
- **rModify** (`KD_Region3DModify`) — Adjusts brightness, contrast and the edge of a region. Its Use Shape control has no effect in the current source.
- **rTransform** (`KD_Region3DTransform`) — Moves, rotates and scales a region.

The 3D Krokodove tools with a Region input are Kill3D, Objectify3D, PolyPlay3D, VertexPlay3D and Tool3D. Two region types exist in the source but are not registered in this build: an image region and a shape region.

## Krokodove: Shape

Shape tools from the Krokodove plug-in set. They extend the core Shape toolset: they take a shape tree (`ShapeTree`) and pass one on, so they fit into any chain built from sRectangle, sStar or sText. Like the core shapes, a chain ends at **sRender**, which turns the shapes into an image. The tools are grouped here by what they do: editing the path, and changing the style.

Several are motion-graphics tools in their own right: **sWriteOn** draws a path on, **sZigZag** and **sRound** change the edges, and **sSmooth** and **sOffset** reshape and repeat outlines.

- **sWriteOn** (`KD_ShapeWriteOn`) — Shows only part of each outline, set by a range along its length. Animate the range to write on, or Shift to move a visible piece along the path.
- **sZigZag** (`KD_ShapeZigZag`) — Turns each straight segment into a zigzag, with a step count and an offset that sets its amplitude.
- **sRound** (`KD_ShapeRound`) — Rounds the corners that fall within an angle range, with a radius limited by the neighbouring edges.
- **sSmooth** (`KD_ShapeSmooth`) — Turns straight segments into smooth curves through the same points, from straight lines to full smoothing.
- **sOffset** (`KD_ShapeOffset`) — Makes a set of outline copies at steps away from the shape, outwards, inwards or both ways.
- **sResample** (`KD_ShapeResample`) — Re-spaces the points of a path at a set distance, to prepare it for sZigZag.
- **sKill** (`KD_ShapeKill`) — Removes the segments that fail a direction or length test, which breaks the path into pieces.
- **sExtrude** (`KD_ShapeExtrude`) — Gives a shape depth by sweeping its outline along a direction.
- **sTriangulate** (`KD_ShapeTriangulate`) — Splits a filled shape into triangles.
- **sRestyle** (`KD_ShapeRestyle`) — Gives shapes a new style from one node, either replacing or adding to the existing style.

## Krokodove: Shape Create

Shape generators from the Krokodove plug-in set. They have no shape input: each one creates a shape from its own controls, or from an image, and outputs a shape tree (`ShapeTree`). Like the core shape generators, they need a **sRender** after them to be seen, and they can be passed through any Krokodove or core shape modifier first, such as sRound, sOffset or sWriteOn.

- **sPrimitive Create** (`KD_ShapePrimitiveCreate`) — Creates a cross, a regular polygon, a rectangle or a star, sized by Size X and Y with a Steps count.
- **sSpiral Create** (`KD_ShapeSpiralCreate`) — Creates an open spiral that winds from one radius to another over a range of angles.
- **sTrace Create** (`KD_ShapeTraceCreate`) — Traces the outline of an image's chosen channel at a threshold, turning a picture or matte into a shape.

## Modifiers

Modifiers animate, generate or link the value of an input, rather than processing images. They aren't added with
`AddTool`: attach one with `tool.AddModifier('Input', 'ModifierID')` or `tool.Input = comp.BezierSpline()`, reach its
controls with `tool.Input.GetConnectedOutput().GetTool()`, and read the result per frame with `tool.Input[frame]`.
Families (Perturb, Publish, Switch) are attached by member ID, such as `PerturbPoint`.

*Animation curves:*

- **BezierSpline** (`BezierSpline`) — The default keyframe curve for a number, with a value and Bézier handles at each key, for smooth, eased or sharp animation.
- **B-Spline** (`NURBSpline`) — A smoothed number curve that doesn't pass through its keys, softer than a Bézier, with weights per key.
- **Cubic Spline** (`CubicSpline`) — A number curve that passes through every key, with smooth curves between them.
- **Natural Cubic Spline** (`NaturalCubicSpline`) — A number curve through its keys with a natural cubic fit, with automatic handles.
- **BSpline** (`BSpline`) — The B-spline shape type used by B-spline shapes; not a number modifier (use B-Spline to animate a value).
- **Keyframe Stretcher** (`KeyStretcherMod`) — Stretches an animation's keys to a new frame range, so a template keeps its shape when trimmed.

*Motion paths and positions:*

- **Path** (`PolyPath`) — A motion path for a position, with a Displacement spline that sets the speed along it.
- **BSpline Path** (`BSplinePath`) — A motion path for a position, smoothed by a B-spline rather than passing through its points.
- **XY Path** (`XYPath`) — A position animated by separate X and Y curves, so each axis can be eased on its own.
- **Offset** (`Offset`) — Combines two positions (sum, difference, average, max, min and more) to give a position, an angle or a distance.
- **Vector** (`Vector`) — A point at a set distance and angle from an origin, for orbiting a position around a centre.
- **Track** (`TrackerModifier`) — Tracks one pattern in a source image and drives one input from it, without a Tracker node.
- **CoordTransform 3D** (`CoordTransform3D`) — Reads a 3D object's position as numbers, to drive 2D or 3D controls from the scene.

*Procedural values, maths and linking:*

- **Perturb** (`Perturb*`) — Smooth random jitter for a number, point, polyline, mesh or gradient, added on top of existing animation.
- **Shake** (`Shake`) — Semi-random motion of a position or value between a minimum and maximum, with smoothing.
- **Random** (`KD_NumberRandom`) — A seeded random number between Minimum and Maximum, changing every frame or held for a set number of frames, for jitter and flicker.
- **Beat** (`KD_NumberBeat`) — A repeating attack, decay, sustain and release envelope, set to beats of a frame count or a tempo, for pulsing a number in time with music.
- **Expression** (`Expression`) — Evaluates a formula over time and up to nine number and point inputs, for links and oscillation; also covers SetExpression on any input.
- **Calculation** (`Calculation`) — Combines two numbers with one operation (add, multiply, average and more), for quick maths on an input.
- **Publish** (`Publish*`) — Publishes one value that other inputs can link to, for one control shared by many inputs.
- **Switch (modifier)** (`Switch*`) — Chooses one of several values by a Source index, for switching between presets; one member for each data type.
- **Probe** (`Probe`) — Drives a number from the colour or luminance of a pixel or rectangle in an image.
- **Custom Poly** (`CustomPoly`) — Builds a polyline from X and Y formulas over a number of points, for shapes that follow a formula.

*Text:*

- **Follower** (`StyledTextFollower`) — Animates one character's keyed values and passes the timing on to the rest of the text by Order and Delay, for per-character titles.
- **Character Level Styling** (`StyledTextCLS`) — Changes the style of selected characters only, for highlighting words or letters in a Text+.
- **TextScramble** (`TextScramble`) — Scrambles a line of text by a randomness amount, settling to the text as randomness drops, for decode and glitch reveals.
- **TextTimer** (`TextTimer`) — Shows a countdown, a timer or the clock as text, for slates and on-screen timers.
- **TimeCode** (`TimeCode`) — Shows the frame as a timecode string, with a frame rate and start offset, for on-screen timecode.
- **CompName** (`CompName`) — Outputs the composition name as text, for slates that should match the comp.
- **Formula** (`KD_TextFormula`) — Writes numbers, points and text inputs into a line of text by placeholder (`n1`, `p1x`, `t1`), for live readouts.
- **From File** (`KD_TextFromFile`) — Supplies one line of text per frame from a file or a text box, timed by hold frames or start frames, for captions and lists.
- **Juggle** (`KD_TextJuggle`) — Scrambles the characters of a line by an amount, with spaces optionally kept in place, for scrambled text reveals.
- **Write** (`KD_TextWrite`) — Types out a line as a fraction, with an optional cursor and prefix, for typewriter effects.

*Colour and gradients:*

- **From Image** (`GradientFromImage`) — Samples a line across an image and makes a gradient from its colours, for matching a graphic to a plate.
- **Gradient Color** (`GradientColorModifier`) — Reads a gradient at an offset and outputs its colour as four numbers, for animating a colour from a gradient.
- **Color Switcher** (`KD_NumberColorSwitchboard`) — Eight palettes of eight colours; picks one by a Set number and outputs its colours as numbers, for switching or cycling a colour scheme.

*Audio and Resolve:*

- **MIDI Extractor** (`MIDI`) — Reads a MIDI file's notes, beats or controllers as a number over time, for music-driven animation.
- **Fairlight Animator** (`FairlightAnimator`) — Drives a number from a Fairlight audio analysis in Resolve, for sound-reactive graphics.
- **Resolve Parameter** (`ResolveParameter`) — Reads a Resolve parameter such as a transition's progress as a number, for driving graphics with the edit.
