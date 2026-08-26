# Resolve GUIと本ライブラリ定数の対応

このページは、納品仕様や制作テンプレートに合わせてProject SettingsをPythonから自動設定したい人向けの対応表です。Resolveの画面で見える項目から、コードで指定する設定名と値を探せます。

## 名前の読み方

- **［Resolve GUI］** 「Project Settings」や「Timeline frame rate」は、Resolveの画面に表示される名前です。
- **［Resolve API］** `Project.SetSetting()`や設定キー`"timelineFrameRate"`は、Resolve公式Scripting APIの名前です。
- **［TY API］** `ProjectSetting`、`TimelineSetting`、`FrameRate`、`set_settings()`は、本ライブラリ`ty_davinci_resolve`からimportして使うPythonの名前です。Resolveの画面に表示される名称ではありません。

本文と表では、名前だけで所属を判断しにくい場合にこのタグを付けます。ダブルクォートは実際にPythonへ渡す文字列だけに使用します。

## 自動設定するときの基本方針

解像度、フレームレート、カラーマネージメントなど、作品全体の前提になる項目は、空のprojectを作成した直後に設定してください。素材のimportやtimelineの作成後は、作品の時間軸や既存clipへ影響するため、Resolveが変更を受け付けない項目があります。

フレームレートに関係するAPIキーは、Projectと個別timelineに2種類ずつ、次の4つがあります。ただし、4つすべてをPythonから変更できるわけではありません。

| ［Resolve GUI］対象 | ［Resolve GUI］画面項目 | 制作上の役割 | ［TY API］からの変更 |
|---|---|---|---|
| Project | Timeline frame rate | 新しく作るtimelineの基準となるフレームレート | ［TY API］`ProjectSetting.TIMELINE_FRAME_RATE`で設定可能。project作成直後に設定する |
| Project | Playback frame rate | Project Settingsで指定する再生フレームレート | 変更不可。［TY API］`ProjectSetting.TIMELINE_PLAYBACK_FRAME_RATE`で現在値の確認だけが可能 |
| 個別timeline | Timeline frame rate | そのtimelineを編集・再生するフレームレート | ［TY API］`TimelineSetting.TIMELINE_FRAME_RATE`で設定可能。空timelineに設定する |
| 個別timeline | Playback frame rate | 個別timelineには独立した設定項目がない | 設定不要。GUIにも選択項目がなく、［Resolve API］`Timeline.SetSetting()`からも変更できない |

作品を狙ったフレームレートで作るときは、まずProjectの「Timeline frame rate」を設定してください。特定のtimelineだけ別のフレームレートにする場合は、そのtimelineの「Timeline frame rate」を設定します。個別timelineはこの値で再生されるため、「Playback frame rate」を追加で設定する必要はありません。

一方、Projectの「Playback frame rate」を「Timeline frame rate」と異なる値にしたい場合、［Resolve API］`Project.SetSetting()`では変更できず、［TY API］からも自動化できません。必要な場合はProject SettingsのGUIで設定してください（Resolve Studio 21.0.4.5で確認）。

```python
from ty_davinci_resolve import (
    FrameRate,
    ProjectSetting,
    TimelineSetting,
    create_empty_timeline,
    get_media_pool,
    set_settings,
    set_timeline_settings,
)

# 新しく作るtimelineの既定値を24 fpsにする
set_settings(
    project,
    {ProjectSetting.TIMELINE_FRAME_RATE: FrameRate.FPS_24},
)

# この空timelineだけを25 fpsにする
timeline = create_empty_timeline(get_media_pool(project), "25 fps Timeline")
set_timeline_settings(
    timeline,
    {TimelineSetting.TIMELINE_FRAME_RATE: FrameRate.FPS_25},
)
```

［TY API］`set_timeline_settings()`は、最初に［Resolve API］設定キー`"useCustomSettings"`へ`"1"`を設定してから、指定されたtimeline設定を適用します。どちらの一括設定関数も、Resolveが設定を拒否した時点で例外を出して停止します。

## 対象環境と収録範囲

この文書はWindows版DaVinci Resolve Studio 21.0.4.5を対象とします。APIの基準資料は同梱の[Resolve 21.0.4 Scripting README](../official_documents/21.0.4_Scripting/README.txt)です（679–711行）。

［TY API］`ProjectSetting`クラスには、調査対象158個のうち151個の設定キーを定数として収録しています。151は収録数であり、すべてをPythonから変更できるという意味ではありません。読み取り専用やGUIとの対応を特定できていないキーは、この文書で個別に区別します。［TY API］`ProjectSetting`はResolveの画面名ではなく、設定キーの入力間違いを防ぐために本ライブラリが用意したPythonクラスです。

次の7個の設定キーは、［TY API］`ProjectSetting`には収録していません。自動設定には使用できないためです。［Resolve API］`Project.GetSetting()`で現在値を読み取ることはできますが、［Resolve API］`Project.SetSetting()`へ同じ値を書き戻してもResolveに拒否されます。

- `perfOptimisedCodec`
- `perfRenderCacheCodec`
- `superScaleNoiseReductionStrength`
- `superScaleSharpnessStrength`
- `videoCaptureCodec`
- `videoCaptureFormat`
- `videoDeckFormat`

## GUIと定数の対応

表中の「根拠」は次を表します。

- 公式: Resolve 21.0.4 Scripting READMEに値または設定方法が明記されている。
- GUI: Windows版Resolve Studio 21.0.4.5のProject Settingsで表示を確認した。
- 設定確認: 使い捨てprojectで値を設定し、Resolveから同じ値を読み取れることを確認した。

| ［Resolve GUI］Project Settingsの場所 | ［Resolve GUI］項目 | ［TY API］`ProjectSetting`定数 | ［TY API］値定数 | 根拠 |
|---|---|---|---|---|
| Master Settings > Timeline Format | Timeline resolution | `TIMELINE_RESOLUTION_WIDTH`, `TIMELINE_RESOLUTION_HEIGHT` | `ResolutionValue`（例: `"1920"`, `"1080"`） | GUI、設定確認 |
| Master Settings > Timeline Format | Timeline frame rate | `TIMELINE_FRAME_RATE` | `FrameRate`（例: `"24"`, `"29.97 DF"`） | 公式、GUI、設定確認 |
| Master Settings > Timeline Format | Playback frame rate | `ProjectSetting.TIMELINE_PLAYBACK_FRAME_RATE` | `PlaybackFrameRate`（現在値の確認用） | GUI、Project APIで変更不可 |
| Master Settings > Timeline Format | Pixel aspect ratio | `TIMELINE_PIXEL_ASPECT_RATIO` | `PixelAspectRatio`（例: `"square"`） | 公式、GUI |
| Master Settings > Video Monitoring | Video format | `VIDEO_MONITOR_FORMAT` | `make_video_monitor_format()`（例: `"HD 1080p 24"`） | GUI、設定確認 |
| Master Settings > Video Monitoring | SDI configuration | `VIDEO_MONITOR_SDI_CONFIGURATION` | `SDIConfiguration`（例: `"dual_link"`） | GUI、設定確認 |
| Master Settings > Video Monitoring | Bit depth | `VIDEO_MONITOR_BIT_DEPTH` | `VideoBitDepth`（`"8"`, `"10"`） | GUI、設定確認 |
| Master Settings > Video Monitoring | Data levels | `VIDEO_DATA_LEVELS` | `VideoDataLevel`（`"Video"`, `"Full"`） | GUI、設定確認 |
| Master Settings > Optimized Media and Render Cache | Optimized media resolution | `PERF_OPTIMIZED_RESOLUTION_RATIO` | `OptimizedMediaResolution` | GUI、設定確認 |
| Master Settings > Optimized Media and Render Cache | Proxy media resolution | `PERF_PROXY_RESOLUTION_RATIO` | `ProxyResolution` | GUI、設定確認 |
| Master Settings > Optimized Media and Render Cache | Proxy media usage | `PERF_PROXY_MEDIA_MODE` | `ProxyMediaMode` | GUI、設定確認 |
| Master Settings > Optimized Media and Render Cache | Render cache | `PERF_RENDER_CACHE_MODE` | `RenderCacheMode` | GUI、設定確認 |
| Master Settings > Frame Interpolation | Retime process | `IMAGE_RETIME_INTERPOLATION` | `RetimeInterpolation` | GUI、設定確認 |
| Master Settings > Frame Interpolation | Motion estimation mode | `IMAGE_MOTION_ESTIMATION_MODE` | `MotionEstimationMode` | GUI、設定確認 |
| Master Settings > Frame Interpolation | Motion range | `IMAGE_MOTION_ESTIMATION_RANGE` | `MotionEstimationRange` | GUI、設定確認 |
| Image Scaling | Resize filter | `IMAGE_RESIZE_MODE` | `ImageResizeMode` | GUI、設定確認 |
| Image Scaling | Super Scale | `SUPER_SCALE` | `SuperScale`（整数`0`–`4`） | 公式、GUI、設定確認 |
| Image Scaling | Super Scale sharpness / noise reduction | `SUPER_SCALE_SHARPNESS`, `SUPER_SCALE_NOISE_REDUCTION` | `SuperScaleDetail` | GUI、設定確認 |
| Color Management | Color science | `COLOR_SCIENCE_MODE` | `ColorScienceMode` | GUI、設定確認 |
| Color Management | Automatic color management | `AUTO_COLOR_MANAGEMENT` | `SettingToggle`（`DISABLED="0"`, `ENABLED="1"`） | GUI、設定確認 |
| Color Management | Color processing mode | `RCM_PRESET_MODE` | `ProjectPresetMode` | GUI、設定確認 |
| Color Management | Use separate color space and gamma | `SEPARATE_COLOR_SPACE_AND_GAMMA` | `SettingToggle` | GUI、設定確認 |
| Color Management | Input / Timeline / Output color space | `COLOR_SPACE_INPUT`, `COLOR_SPACE_TIMELINE`, `COLOR_SPACE_OUTPUT` | Input／Timeline: `ColorSpace`。Output: `OUTPUT_COLOR_SPACES`に含まれる`ColorSpace`の要素 | GUI、設定確認 |
| Color Management | Input / Timeline / Output gamma | `COLOR_SPACE_INPUT_GAMMA`, `COLOR_SPACE_TIMELINE_GAMMA`, `COLOR_SPACE_OUTPUT_GAMMA` | `Gamma` | GUI、設定確認 |
| Color Management | Combined color space and gamma | `COLOR_SPACE_TIMELINE` | `ColorSpaceGamma` | GUI、設定確認 |
| Color Management | Timeline working luminance | `TIMELINE_WORKING_LUMINANCE_MODE`, `TIMELINE_WORKING_LUMINANCE` | `WorkingLuminanceMode`, 48–10,000 nit | GUI、設定確認 |
| Color Management | Input / Output DRT | `INPUT_DRT`, `OUTPUT_DRT` | `DynamicRangeTransform` | GUI、設定確認 |
| Color Management | Use inverse DRT for SDR to HDR conversion | `USE_INVERSE_DRT` | `SettingToggle` | GUI、設定確認 |
| Color Management | Use color space aware grading tools | `USE_COLOR_SPACE_AWARE_GRADING_TOOLS` | `SettingToggle` | GUI、設定確認 |
| Color Management | Apply resize transformations in | `IMAGE_RESIZING_GAMMA` | `ResizeTransformation` | GUI、設定確認 |
| Color Management | Disable tone mapping for Fusion conversions | `DISABLE_FUSION_TONE_MAPPING` | `SettingToggle` | GUI、設定確認 |
| Color Management | Graphics white level | `GRAPHICS_WHITE_LEVEL` | nit値を表す文字列 | GUI、設定確認 |
| Color Management > ACES | ACES IDT / ODT | `COLOR_ACES_IDT`, `COLOR_ACES_ODT` | `AcesInputTransform`, `AcesOutputTransform` | GUI、設定確認 |
| Color Management > ACES | Apply ACES reference gamut compress | `COLOR_ACES_GAMUT_COMPRESS_TYPE` | Resolveへ渡す文字列 | GUI、設定確認 |
| Color Management > ACES | Process node LUTs in | `COLOR_ACES_NODE_LUT_PROCESSING_SPACE` | Resolveへ渡す文字列 | GUI、設定確認 |
| Fairlight | Audio capture / playout channels | `AUDIO_CAPTURE_NUM_CHANNELS`, `AUDIO_PLAYOUT_NUM_CHANNELS` | `AudioChannelCount` | GUI、設定確認 |
| Fairlight | Loudness scale | `LIMIT_AUDIO_METER_LOUDNESS_SCALE` | `AudioMeterLoudnessScale` | GUI、設定確認 |
| Color | Broadcast safe levels | `LIMIT_BROADCAST_SAFE_LEVELS` | `BroadcastSafeLevel` | GUI、設定確認 |
| Color | Node stack layers | `NODE_STACK_LAYERS` | `NodeStackLayerCount` | GUI、設定確認 |

Output color spaceには、［TY API］`OUTPUT_COLOR_SPACES`に含まれる［TY API］`ColorSpace`の要素を1つ指定します。`OUTPUT_COLOR_SPACES`はOutputで選択できる39個の色空間をまとめたタプルであり、タプル自体を設定値として渡すものではありません。

```python
{
    ProjectSetting.COLOR_SPACE_OUTPUT: ColorSpace.REC_2020,
}
```

［Resolve GUI］`Limit output gamut to`はPythonから自動設定できません。納品先の色域に制限する必要がある場合は、Project SettingsのGUIで設定してください。GUIを`P3-D65`と`Output color space`の間で変更しても、［Resolve API］`Project.GetSetting()`が返す158個の設定値には差がなく、対応する設定キーは見つかりませんでした（Resolve Studio 21.0.4.5で確認）。

名前が似ている［TY API］`ProjectSetting.OUTPUT_GAMUT_MAPPING`は、このGUI項目には対応しません。これは［Resolve API］設定キー`"colorSpaceOutputGamutMapping"`を表す定数ですが、上記のGUI変更後も値は`"None"`のままでした。制作設定の自動化には使用せず、GUI上の対応項目が特定できていない内部的な設定キーとして扱ってください。

`Color processing mode`は、［Resolve GUI］Color scienceを`DaVinci YRGB Color Managed`にし、`Automatic color management`をオフにしたときに表示されます。制作方式をResolveのプリセットから選ぶ場合は［TY API］`ProjectPresetMode`を指定してください。`CUSTOM`を選ぶと、Input／Timeline／Output color space、Timeline working luminance、DRTなどを個別に決められます。

自動管理をオンにした場合は、GUIの`Color processing mode`がSDR／HDRの簡易選択へ変わります。この状態は［TY API］`RCM_PRESET_MODE`の10個のプリセットとは別です。細かな色管理を自動化する場合は、先に`AUTO_COLOR_MANAGEMENT=DISABLED`を設定してから`RCM_PRESET_MODE`を設定してください。

### Color scienceのGUI表示とAPI値

GUIラベルと`Project.SetSetting("colorScienceMode", value)`へ渡す文字列は一致しません。

| GUI表示 | `ColorScienceMode` | API value |
|---|---|---|
| DaVinci YRGB | `DAVINCI_YRGB` | `davinciYRGB` |
| DaVinci YRGB Color Managed | `DAVINCI_YRGB_COLOR_MANAGED` | `davinciYRGBColorManagedv2` |
| ACEScc | `ACES_CC` | `acescc` |
| ACEScct | `ACES_CCT` | `acescct` |

### 本ライブラリで指定できる定数値

本ライブラリの各定数クラスには、Resolve Studio 21.0.4.5で実際に設定でき、その後に同じ値を読み取れた値だけを収録しています。文字列を直接書くより、ここにある定数を使う方が綴りや大文字・小文字の間違いを防げます。

| 本ライブラリの定数クラス | Resolveへ渡すことを確認した値 |
|---|---|
| `AudioChannelCount` | `2`, `4`, `6`, `8`, `16` |
| `DeinterlaceQuality` | `normal`, `high` |
| `MotionEstimationMode` | `standardFaster`, `standardBetter`, `enhancedFaster`, `enhancedBetter` |
| `MotionEstimationRange` | `small`, `medium` |
| `ImageResizeMode` | `sharper`, `smoother`, `bicubic`, `bilinear` |
| `RetimeInterpolation` | `nearest`, `frameBlend`, `opticalFlow` |
| `AudioMeterLoudnessScale` | `ebu_9_scale`, `ebu_18_scale` |
| `BroadcastSafeLevel` | `0_100`, `10_110`, `20_120` |
| `NodeStackLayerCount` | `1`, `2`, `3`, `4` |
| `OptimizedMediaResolution` | `auto`, `original`, `half`, `quarter` |
| `ProxyMediaMode` | `0`, `1`, `2` |
| `ProxyResolution` | `original`, `half`, `quarter` |
| `RenderCacheMode` | `none`, `smart`, `user` |
| `SuperScaleDetail` | `Low`, `Medium`, `High` |
| `FrameRateMismatchBehavior` | `resolve`, `none` |
| `VideoBitDepth` | `8`, `10` |
| `SDIConfiguration` | `none`, `single_link`, `dual_link`, `quad_link`（項目により使用可能値が異なる） |
| `ProjectPresetMode` | `SDR Rec.2020`, `SDR Rec.2020 (P3-D65 limited)`, `SDR P3-D60 Cinema`, `HDR DaVinci Wide Gamut Intermediate`, `HDR Rec.2020 Intermediate`, `HDR Rec.2020 HLG`, `HDR Rec.2020 HLG (P3-D65 limited)`, `HDR Rec.2020 PQ`, `HDR Rec.2020 PQ (P3-D65 limited)`, `Custom` |

Resolve画面に選択肢が表示されても、Pythonから同じ値を設定できるとは限りません。自動化で使えなかった候補は定数へ追加していません。

## 開発者向け：GUI対応表の確認漏れを防ぐ

確認状況は[`project-setting-gui-coverage.json`](project-setting-gui-coverage.json)で管理します。［TY API］`ProjectSetting`の全定数を「GUI対応を本文に掲載済み」または「GUI対応を継続調査中」のどちらかへ明示的に分類します。定数を追加したのに分類し忘れた場合や、掲載済みの定数が本文から消えた場合は、単体テストが失敗します。

Resolve更新時に確認するGUI状態、名前による誤対応を防ぐ判定基準、変更前後の全snapshot比較、テストと完了条件は[Resolveバージョン更新時の検証手順](resolve-version-upgrade.md)にまとめています。

## 開発者向け：設定値の再検証

Resolveの更新後に設定の互換性を調べ直す場合は、Pythonの`tests/integration/test_setting_constants.py`を使用します。このテストはProject Settingsのキーと候補値を実際に設定し、設定後の値を確認して、使い捨てprojectを削除します。ProjectとTimelineのフレームレート適用範囲は`test_timeline_frame_rate_settings.py`、詳細な調査出力が必要な場合は`probe_timeline_playback_frame_rate.py`で確認できます。

実施順序と判定基準は[Resolveバージョン更新時の検証手順](resolve-version-upgrade.md)を参照してください。
