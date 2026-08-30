# Resolve 21.0.4 API対応表

このページはライブラリの保守・拡張を行う開発者向けです。通常の制作自動化は[利用ガイド](guide.md)、Resolve画面から設定項目を探す場合は[Resolve GUIと本ライブラリ定数の対応](project-settings.md)を参照してください。

この文書では、Resolve公式Scripting APIに**［Resolve API］**、本ライブラリ`ty_davinci_resolve`のPython APIに**［TY API］**を付けて区別します。例えば［Resolve API］`Project.SetSetting()`、［TY API］`set_settings()`です。`"timelineFrameRate"`のようなダブルクォート付きの表記は、Resolve公式APIへ実際に渡す文字列です。

実装の基準資料は `official_documents/21.0.4_Scripting/README.txt` です。行番号はリポジトリに保存した21.0.4版を基準にしています。

| ［TY API］モジュール | ［TY API］公開Python API | ［Resolve API］公式Scripting API | 公式文書 |
|---|---|---|---|
| `connection.py` | `ResolveSession.connect()` | `scriptapp("Resolve")`, `GetProductName()`, `GetVersion()`, `GetVersionString()`, `Fusion()` | 67–93行 |
| `connection.py` | `ResolveSession.quit()` | `Resolve.Quit()` | 101行 |
| `connection.py` | `ResolveSession.restart()` | `Resolve.Quit()`後にWindows上でResolveを再起動し、version確認付きで再接続 | 101行 |
| `connection.py` | `get_current_page()`, `open_page()` | `Resolve.GetCurrentPage()`, `OpenPage()` | 89–90行 |
| `project.py` | project一覧・作成・読込・保存・終了・削除 | `ProjectManager.GetProjectListInCurrentFolder()`, `CreateProject()`, `LoadProject()`, `SaveProject()`, `CloseProject()`, `DeleteProject()` | 123–143行 |
| `project.py` | setting、timeline取得・選択 | `Project.Get/SetSetting()`, `GetTimelineCount()`, `GetTimelineByIndex()`, `SetCurrentTimeline()` | 162–203行 |
| `project.py` | resolution取得、LUT更新 | `Project.GetSetting()`, `RefreshLUTList()` | 195、204行 |
| `media.py` | folder取得・選択、file・連番import | `MediaPool.GetRootFolder()`, `GetCurrentFolder()`, `SetCurrentFolder()`, `ImportMedia()` | 231–265行 |
| `media.py` | `import_media_storage_items()` | `MediaStorage.AddItemListToMediaPool()` | 225–227行 |
| `timeline.py` | track検証・取得・名称、clip追加 | `Timeline.GetTrackCount()`, `GetItemListInTrack()`, `GetTrackName()`, `SetTrackName()`, `MediaPool.AppendToTimeline()` | 236–238、372–417行 |
| `timeline.py` | native Fusion Composition挿入 | `Timeline.InsertFusionCompositionIntoTimeline()` | 438行 |
| `timeline.py` | current timeline、playhead、timeline setting、generator | `Project.GetCurrentTimeline()`, `Timeline.Get/SetCurrentTimecode()`, `Get/SetSetting()`, `InsertGeneratorIntoTimeline()` | 165、411–412、434–436行 |
| `render.py` | format・codec・解像度照会 | `GetRenderFormats()`, `GetRenderCodecs()`, `GetRenderResolutions()` | 197–203行 |
| `render.py` | job ID単位の追加・開始・監視・削除 | `AddRenderJob()`, `StartRendering(jobId)`, `GetRenderJobStatus(jobId)`, `DeleteRenderJob(jobId)` | 172–189行 |
| `render.py` | render preset import・削除 | `Resolve.ImportRenderPreset()`, `Project.GetRenderPresetList()`, `DeleteRenderPreset()` | 102、177、186行 |
| `fusion.py` | native/固定長Fusion Composition追加 | `InsertFusionCompositionIntoTimeline()`, `GetFusionCompByIndex()`, `AddFusionComp()`と明示dummy media fallback | 438、473–474、502行 |

`fusion.py` の `Composition.AddTool()`、`Tool.ConnectInput()`、`SetInput()`、`GetInput()`、`FlowView.SetPos()` は、Resolve 21.0.4 Scripting READMEのオブジェクト一覧には掲載されていないResolve内蔵Fusion APIです。これらは実機テストとCountdown回帰テストで検証し、未検証の薄いラッパーは追加しません。

`FusionTool`と`FusionResolveFxTool`は、Fusion 8 Scripting Guideの`Fusion.GetRegSummary(CT_Tool, False)`および`Registry.GetAttrs()`に従い、Resolve Studio 21.0.4.5の実機Registryから取得したRegIDです。Blackmagic提供の通常ToolとResolve FXを分離し、第三者提供の追加Fuse/OFXやKrokodoveの内部Toolなどinstall環境に依存する項目は収録していません。一覧の再調査には`tests/integration/probe_fusion_tool_registry.py`を使用します。

`refresh_fusion_color_management()`はFusion pageからEdit pageへ切り替えるResolve 21.0.4向けworkaroundです。0.1秒待機では連続して作成した3つ目のCompositionから16-bit出力差が発生しましたが、0.5秒待機では4条件・384枚が参照画像と完全一致したため、既定値を0.5秒としています。この待機時間は公式仕様ではなく、Windows版Resolve Studio 21.0.4.5の実機結果です。

P2の`build_rectangle()`、`get_fusion_fonts()`、page切替付き`set_tool_position()`もResolve内蔵Fusion APIを使用します。固定長`append_fusion_composition()`はTimeline settingから解像度とfpsを取得し、package同梱の`dummy_video_{width}x{height}_{fps}P.mp4`を自動選択します。`select_fusion_duration_media()`は、任意directoryのmediaを明示選択する用途にも使用できます。

## Project lifecycleの完了待機

Resolve 21.0.4ではproject lifecycle APIが成功を返しても、内部の状態遷移が完了していない場合があります。実機ログでは`LoadProject()`の処理完了後、current projectの切替までさらに約0.27秒を要し、返されたremote objectへ直ちにアクセスした際にResolveが異常終了しました。

`create_project()`、`save_project()`、`close_project()`、`load_project()`、`delete_project()`は、API呼出し後に静穏時間を置き、観測可能な操作では低頻度pollingで状態遷移を確認します。既定値は`DEFAULT_PROJECT_LIFECYCLE_TIMING`、環境に応じた値は`ProjectLifecycleTiming`を各関数の`timing=`へ渡せます。特に`load_project()`は、返されたremote objectには触れず1.5秒待ってから、`GetCurrentProject()`で安定したobjectを取得して返します。

反復検証は次のコマンドで実行します。各反復は別processで実行され、45秒を超える停止も失敗として検出します。

```powershell
python tests/stress/project_lifecycle_stress.py --iterations 20
```

## 定数の根拠と実機検証

Resolve公式APIの`Project.GetSetting()`／`Project.SetSetting()`の調査方法、`superScale`、frame rate、render setting値は、同梱の[公式Scripting README](../official_documents/21.0.4_Scripting/README.txt) 679–711行、832–864行を根拠にしています。Windows版Resolve Studio 21.0.4.5から取得した158個の設定キーのうち151個を、本ライブラリの`ProjectSetting`クラスへ定数として収録しました。151は収録数であり、全項目の書き込みを保証する数ではありません。例えば`timelinePlaybackFrameRate`は読み取り専用で、`colorSpaceOutputGamutMapping`はGUIとの対応を特定できていません。codec／format、Super Scale strength、deck formatに関する残り7個は、同値の書き戻しも拒否されたため収録していません。

Project scopeでは、`timelineFrameRate`をproject作成直後に設定できます。`timelinePlaybackFrameRate`は値を読み取れますが、`Project.SetSetting()`による変更は拒否されました。

本ライブラリでは、timeline用の設定キーを`TimelineSetting`クラスとしてproject用の`ProjectSetting`とは分けて公開します。ProjectとTimelineで変更できる設定が異なるためです。Timeline scopeでは、空timelineの`useCustomSettings`を`1`にした後、Resolve公式APIの`Timeline.SetSetting("timelineFrameRate", value)`でTimeline Settingsの「Timeline frame rate」を変更できます。25 fpsを設定した実機試験では、timelineの`timelineFrameRate`だけが25.0へ変わり、projectの`timelineFrameRate`と`timelinePlaybackFrameRate`は24のままでした。`Timeline.SetSetting("timelinePlaybackFrameRate", value)`はcustom settingsの前後とも拒否されました。

Windows操作でProject／Deliverの全リストを確認し、本ライブラリの`ResolutionValue`へ28寸法、`PlaybackFrameRate`へ19値を収録しました。Deliver UIではvideo format 19件を確認しました。本ライブラリの`FrameRate`は同じUIの19値に、公式Scripting READMEで規定されたDrop Frame値`29.97 DF`／`59.94 DF`を加えた21件です。Drop Frame値の設定は成功しますが、readbackは数値部分の`timelineFrameRate`と`timelineDropFrameTimecode=1`に分離されます。Resolve公式APIの`GetRenderFormats()`はvideo以外を含む23識別子を返し、本ライブラリの`RenderFormat`はこちらを完全収録します。UIに表示された`HEIF`はこの実機の`GetRenderFormats()`には返らずAPI識別子を確認できないため、推測して追加していません。format別`GetRenderCodecs()`の和集合は196識別子で、すべて本ライブラリの`VideoCodec`に収録しました。さらに旧移植値3件を残すためEnum総数は199件です。利用可能な組合せは実行環境依存なので、固定Enumだけで可否を判断してはいけません。

`VideoQuality`はDeliver UIと公式Scripting README 846–850行で`Least`、`Low`、`Medium`、`High`、`Best`の5件を確認しました。Automaticは整数`0`、正整数はcodec別bitrateであり、追加の固定Enum値ではありません。

本ライブラリの定数クラス`ColorSpace`、`Gamma`、`ColorSpaceGamma`、`WorkingLuminanceMode`、`AcesInputTransform`、`AcesOutputTransform`は、使い捨てprojectで設定間に0.35秒置き、API成功値とreadbackを確認した値だけを公開します。旧ACES ODTは`nits`→`nit`、`Rec.2020`→`Rec.2100`の現行値へ変更しました。Resolve 21.0.4.5が旧値を拒否するためです。`DaVinci Wide Gamut`、`Alexa Wide Gamut`、`ACES AP0/AP1`、`Sony S-Log3`、`HDR 400`なども本ライブラリの公開Enumへ含めません。これらも実機試験で拒否されました。

Custom 条件は`colorScienceMode=davinciYRGBColorManagedv2`、
`rcmPresetMode=Custom`、`separateColorSpaceAndGamma=1`です。Resolve Studio
21.0.4.5のUI全件調査とAPI readbackにより、Input／Timeline color space 43件、
Output color space 39件（`OUTPUT_COLOR_SPACES`）、3種のGamma各63件、Timeline
working luminance 11件を確認しました。Custom luminance の数値境界は48–10,000
nitです。`colorSpaceOutputGamutMapping`はsnapshotに存在しますが、UI表示値のうち
APIで設定できたのは`None`だけでした。この設定キーは、GUIの`Limit output gamut to`
には対応しません。GUIを`P3-D65`と`Output color space`の間で変更しても、158-key
snapshotに差がなかったためです。White point adaptation は158-key snapshotに
推測した定数は公開していません。対応keyを特定できていないためです。

UI/API表記差は`P3 DCI`→`P3-DCI`、`SMPTE C`→`SMPTE-C`、`YUV`→`Y'UV`、
`AstroDesign A Log`→`AstroDesign A-Log`、`DJI D Log`→`DJI D-Log`、
`Leica L Log`→`Leica L-Log`、`Nikon N Log`→`Nikon N-Log`、
`S Log2`→`S-Log2`です。Inputの`Same as Timeline`はUIには存在しますが、
`SetSetting()`では拒否されます。

旧定数カテゴリとの対応は次のとおりです。

| 旧カテゴリ | 本ライブラリの現行Python API |
|---|---|
| page、project key/toggle、resolution、fps、SDI、data level | `Page`、`ProjectSetting`、`SettingToggle`、`ResolutionValue`、`FrameRate`／`PlaybackFrameRate`、`SDIConfiguration`、`VideoDataLevel` |
| color science、gamut、gamma、ACES、luminance | `ColorScienceMode`、`ColorSpace`、`Gamma`、`ColorSpaceGamma`、`AcesOutputTransform`、`WorkingLuminanceMode` |
| clip property、generator、拡張子、codec | `ClipProperty`、`GeneratorName`、`RenderFormat`、`STILL_SEQUENCE_FORMATS`、`VideoCodec` |
| render setting | `UniqueFilenameStyle`、`VIDEO_QUALITY_AUTOMATIC`／`VideoQuality`、`AudioCodec`、`AudioBitDepth`、`AudioSampleRate` |
| monitor format 40定数、BT.2100 sample | `make_video_monitor_format()`、`BT2100_PROJECT_SETTINGS` |

固定codec値は利用可能性を保証しません。`get_render_codecs()`の実機結果でformatごとに検証します。

非対応方針は次のとおりです。

- deprecated APIは `README.txt` 1099行以降を参照し、新規ラッパーを作りません。
- index指定の旧render APIなどunsupported APIは `README.txt` 1140行以降を参照し、job ID APIを使用します。
- Resolveの版、OS、edition、hardwareで変化するformat・codec一覧は、固定一覧ではなく実機の照会結果を検証に使用します。
