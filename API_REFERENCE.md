# Resolve 21.0.4 API対応表

実装の基準資料は `official_documents/21.0.4_Scripting/README.txt` です。行番号はリポジトリに保存した21.0.4版を基準にしています。

| 新モジュール | 主な公開API | Resolve公式API | 公式文書 |
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

P2の`build_rectangle()`、`get_fusion_fonts()`、page切替付き`set_tool_position()`もResolve内蔵Fusion APIを使用します。固定長`append_fusion_composition()`はTimeline settingから解像度とfpsを取得し、package同梱の`dummy_video_{width}x{height}_{fps}P.mp4`を自動選択します。`select_fusion_duration_media()`は、任意directoryのmediaを明示選択する用途にも使用できます。

## Project lifecycleの完了待機

Resolve 21.0.4ではproject lifecycle APIが成功を返しても、内部の状態遷移が完了していない場合があります。実機ログでは`LoadProject()`の処理完了後、current projectの切替までさらに約0.27秒を要し、返されたremote objectへ直ちにアクセスした際にResolveが異常終了しました。

`create_project()`、`save_project()`、`close_project()`、`load_project()`、`delete_project()`は、API呼出し後に静穏時間を置き、観測可能な操作では低頻度pollingで状態遷移を確認します。既定値は`DEFAULT_PROJECT_LIFECYCLE_TIMING`、環境に応じた値は`ProjectLifecycleTiming`を各関数の`timing=`へ渡せます。特に`load_project()`は、返されたremote objectには触れず1.5秒待ってから、`GetCurrentProject()`で安定したobjectを取得して返します。

反復検証は次のコマンドで実行します。各反復は別processで実行され、45秒を超える停止も失敗として検出します。

```powershell
python tests/stress/project_lifecycle_stress.py --iterations 20
```

## 定数の根拠と実機検証

`Project.GetSetting()`／`SetSetting()`の調査方法、`superScale`、frame rate、render setting値は、同梱の公式Scripting README 679–711行、832–864行を根拠にしています。Windows版Resolve Studio 21.0.4.5の新規projectで取得した158-key snapshotを既存36キーと照合し、未収録122キーのうち現在値の`SetSetting()`成功とreadback一致を確認した115キーを追加しました。拒否された7キー（codec／format、Super Scale strength、deck format）は除外し、`ProjectSetting`は計151キーです。なお既存キーの`timelinePlaybackFrameRate`はquery可能ですがread-onlyで、`"24"`と旧値`"24.0"`の双方が拒否されました。

Windows操作でProject／Deliverの全リストを確認し、`ResolutionValue` 28寸法、`PlaybackFrameRate` 19値、Deliver UIのvideo format 19件を確認しました。`FrameRate`は同じUIの19値に、公式Scripting READMEで規定されたDrop Frame値`29.97 DF`／`59.94 DF`を加えた21件です。Drop Frame値の設定は成功しますが、readbackは数値部分の`timelineFrameRate`と`timelineDropFrameTimecode=1`に分離されます。APIの`GetRenderFormats()`はvideo以外を含む23識別子を返し、`RenderFormat`はこちらを完全収録します。UIに表示された`HEIF`はこの実機の`GetRenderFormats()`には返らずAPI識別子を確認できないため、推測して追加していません。format別`GetRenderCodecs()`の和集合は196識別子で、すべて`VideoCodec`に収録しました。さらに旧移植値3件を残すためEnum総数は199件です。利用可能な組合せは実行環境依存なので、固定Enumだけで可否を判断してはいけません。

`VideoQuality`はDeliver UIと公式Scripting README 846–850行で`Least`、`Low`、`Medium`、`High`、`Best`の5件を確認しました。Automaticは整数`0`、正整数はcodec別bitrateであり、追加の固定Enum値ではありません。

`ColorSpace`、`Gamma`、`ColorSpaceGamma`、`WorkingLuminanceMode`、`AcesInputTransform`、`AcesOutputTransform`は、使い捨てprojectで設定間に0.35秒置き、API成功値とreadbackを確認した値だけを公開します。旧ACES ODTはResolve 21.0.4.5で拒否されたため、`nits`→`nit`、`Rec.2020`→`Rec.2100`の現行値へ変更しました。rejectされた`DaVinci Wide Gamut`、`Alexa Wide Gamut`、`ACES AP0/AP1`、`Sony S-Log3`、`HDR 400`などは公開Enumへ含めません。

Custom 条件は`colorScienceMode=davinciYRGBColorManagedv2`、
`rcmPresetMode=Custom`、`separateColorSpaceAndGamma=1`です。Resolve Studio
21.0.4.5のUI全件調査とAPI readbackにより、Input／Timeline color space 43件、
Output color space 39件（`OUTPUT_COLOR_SPACES`）、3種のGamma各63件、Timeline
working luminance 11件を確認しました。Custom luminance の数値境界は48–10,000
nitです。`colorSpaceOutputGamutMapping`はsnapshotに存在しますが、UI表示値のうち
APIで設定できたのは`None`だけでした。White point adaptation は158-key snapshotに
対応keyを特定できていないため、推測した定数を公開していません。

UI/API表記差は`P3 DCI`→`P3-DCI`、`SMPTE C`→`SMPTE-C`、`YUV`→`Y'UV`、
`AstroDesign A Log`→`AstroDesign A-Log`、`DJI D Log`→`DJI D-Log`、
`Leica L Log`→`Leica L-Log`、`Nikon N Log`→`Nikon N-Log`、
`S Log2`→`S-Log2`です。Inputの`Same as Timeline`はUIには存在しますが、
`SetSetting()`では拒否されます。

旧定数カテゴリとの対応は次のとおりです。

| 旧カテゴリ | 新API |
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
