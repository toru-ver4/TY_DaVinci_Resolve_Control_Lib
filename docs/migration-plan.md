# TY_DaVinci_Resolve_Control_Lib 移行・再設計計画

この文書はライブラリ開発者向けの設計・移行記録です。制作での使い方は[利用ガイド](guide.md)、Project Settingsの自動化は[Resolve GUIと本ライブラリ定数の対応](project-settings.md)を参照してください。

この文書では、Resolve公式Scripting APIに**［Resolve API］**、本ライブラリ`ty_davinci_resolve`のPython APIに**［TY API］**を付けて区別します。例えば［Resolve API］`Project.SetSetting()`、［TY API］`ProjectSetting`です。ダブルクォートはPythonへ実際に渡す文字列にだけ使用します。

## 1. 目的

`sample_code/ty_lib` にある次の実装を出発点として、DaVinci Resolve 21.0.4 を Windows から制御する独立した Python パッケージを作る。

- `ty_davinci_control_lib_2.py`
- `ty_davinci_constants.py`

新パッケージは旧実装との後方互換性を持たせない。旧ファイルは `sample_code` 側に残し、新パッケージでは関数名、引数、戻り値、例外、モジュール分割を必要に応じて変更する。

公式 API の基準資料は `official_documents/21.0.4_Scripting/README.txt` とする。同文書が要求する Python は 3.6 以上の 64-bit 版であるため、初期保証環境には Python 3.12 64-bit を採用する（README.txt 16–20行）。

## 2. 対象範囲と保証環境

| 項目 | 方針 |
|---|---|
| OS | Windows のみ保証。macOS は可能な範囲で単体テスト可能な設計にするが、実機保証しない |
| DaVinci Resolve | 21.0.4 |
| Python | 3.12 64-bit |
| パッケージ形式 | `pyproject.toml` と `src` layout を使用 |
| 開発用インストール | `python -m pip install -e .` |
| 配布 | PyPI 公開は前提にせず、ローカルまたは Git URL から `pip install` |
| Git連携 | Git submodule は使用しない |
| 実機テスト | 専用プロジェクトの作成・削除、Resolve の終了・再起動を許可 |

初期の `requires-python` は `>=3.12,<3.13` とする。Python 3.13 は単体テストと Resolve 接続を実機確認した後、別の対応作業として追加する。

## 3. 設計原則

1. パッケージの import だけでは Resolve に接続しない。
2. `resolve` と `fusion` のモジュールグローバルを廃止し、接続状態を `ResolveSession` に保持する。
3. 公式 API の `False`、`None`、空リストなど、操作失敗を示す戻り値を検出したら独自例外を送出する。ライブラリ内で `sys.exit()` は呼ばない。
4. 公開関数の引数は呼び出し前に検証し、不正値なら Resolve を操作しない。
5. Resolve のリモートオブジェクトを過度に包み直さない。複数の公式 API 呼び出しを安全にまとめる処理、入力検証、エラー変換に価値がある箇所を公開 API にする。
6. 未ラップの公式 API を利用できるよう、`ResolveSession.resolve` と `ResolveSession.fusion` にはアクセス可能とする。
7. Python の公開関数には、プロジェクトの `AGENTS.md` に従った英語の NumPy style docstring を付ける。

## 4. パッケージ構成案

配布名を `ty-davinci-resolve-control`、import 名を `ty_davinci_resolve` とする。

```text
TY_DaVinci_Resolve_Control_Lib/
├── pyproject.toml
├── README.md
├── src/
│   └── ty_davinci_resolve/
│       ├── __init__.py
│       ├── connection.py
│       ├── errors.py
│       ├── constants.py
│       ├── project.py
│       ├── media.py
│       ├── timeline.py
│       ├── render.py
│       ├── fusion.py
│       └── timecode.py
├── tests/
│   ├── unit/
│   ├── integration/
│   │   └── test_countdown_regression.py
│   ├── countdown_regression/
│   │   └── create_countdown_v2.py
│   └── countdown_reference_data/
│       └── ref_data_1280x720.zip
├── examples/
└── official_documents/
```

- `connection.py`: API モジュール探索、接続、バージョン検査、終了、再起動
- `errors.py`: 接続・入力値・API操作失敗を区別する例外
- `constants.py`: ページ名、トラック種別など安定した値。環境依存のコーデック一覧は固定定数にせず公式 API から取得する
- `project.py`: プロジェクトのライフサイクルと設定
- `media.py`: Media Storage、Media Pool、Folder、MediaPoolItem 操作
- `timeline.py`: タイムライン、トラック、TimelineItem 操作
- `render.py`: レンダー能力照会、設定、ジョブ作成、待機、停止
- `fusion.py`: Composition と Tool の生成、接続、入力値設定
- `timecode.py`: Resolve に依存しないフレーム・タイムコード計算

大規模なクラス階層は作らず、`ResolveSession` と小さな関数群を基本とする。

## 5. 現行 API の移行方針

### 5.1 初期移植する機能

| 現行機能 | 新しい配置・方向性 |
|---|---|
| import時の接続、`get_project_manager()` | `ResolveSession.connect()` と `session.project_manager` に統合 |
| `reboot_resolve()` | `ResolveSession.restart()`。固定sleepではなく期限付き再接続を行う |
| project の作成・読込・保存・終了・削除 | `project.py` に整理し、名前と戻り値を統一 |
| project/timeline の設定、解像度取得 | 単項目操作と一括操作を分離。一括操作は最初の失敗で停止 |
| media の追加、連番読込 | `media.py` の単一インターフェースに整理し、パスとフレーム範囲を検証 |
| timeline の作成、clip追加、track item取得 | `timeline.py` に移動し、空の公式戻り値を安全に扱う |
| render format/codec/settings、実行待機 | `render.py` でジョブIDを追跡する方式に置換 |
| Fusion comp/tool の生成・接続・入力設定 | `fusion.py` に移動し、ミュータブルなデフォルト引数を廃止 |
| 秒・フレーム・タイムコード変換 | `timecode.py` の純粋関数にする。fpsを暗黙取得しない |
| RCM更新のページ切替 | Resolve 21.0.4 で再現確認できた場合のみ、明示的な workaround として残す |

現行 `_2` 利用箇所で実際に参照されている機能は、上表のプロジェクト設定、メディア追加、タイムライン追加、レンダー、Fusionノード操作にほぼ収まる。この利用実績を初期実装の優先順位に使うが、新パッケージの名前やシグネチャは旧 API に合わせない。

### 5.2 削除または再検討する機能

- `log_return_value`: `print` ベースのデバッグ機能は削除する。必要なら標準 `logging` を利用者側で設定できるようにする。
- `_create_dummy_video_relative_path()` とダミー動画依存: 公式の `Timeline.InsertFusionCompositionIntoTimeline()` をまず使用する。長さ指定が必要なユースケースだけ、独立した補助機能として実機検証する。
- render codec定数: Windows版Resolve Studio 21.0.4.5で観測した識別子を移植するが、可用性判定は`Project.GetRenderFormats()`と`Project.GetRenderCodecs()`の実行結果を常に優先する。
- `run_rendering_and_wait_until_finish()`: 現行実装は全ジョブ削除と完了待機の順序を再設計する。新実装では `AddRenderJob()` が返すジョブIDを保持し、`GetRenderJobStatus(jobId)` を監視して、そのジョブだけを扱う。
- `sec_to_frame_idx()`: プロジェクト状態を暗黙参照せず、fpsを明示引数にする。
- `make_videoMonitorFormat_str()`: 対応する解像度とfpsを明示的に検証し、命名を snake_case に直す。
- `add_line_comp()`、`add_rectangle_comp()` など用途特化ビルダー: 基本的なTool操作を先に実装した後、実利用を確認して第2段階で追加する。

### 5.2.1 旧定数の移植結果

旧`ty_davinci_constants.py`の全カテゴリを監査し、page、project設定値、color管理、clip property、generator、拡張子、codec、render設定を本ライブラリの公開Enum／定数へ移植した。旧名aliasは作らない。video monitor format 40定数は本ライブラリの`make_video_monitor_format()`で置換し、旧BT.2100 sampleはimmutableな`BT2100_PROJECT_SETTINGS`へ移行した。

公式Scripting README由来の値と、Windows版Resolve Studio 21.0.4.5の使い捨てprojectでResolve公式APIの`SetSetting()`成功かつreadback一致した値を区別する。ACES ODTは現行値の`nit`と`Rec.2100`を採用し、旧`nits`／`Rec.2020`値は残さない。`timelinePlaybackFrameRate`は適用用presetから除外する。Project／Timelineの両scopeで書き込みを拒否するためである。一方、本ライブラリではproject用`ProjectSetting`とは別に`TimelineSetting`を公開する。空timelineではcustom settings有効化後の`Timeline.SetSetting("timelineFrameRate", value)`がTimeline Settingsの「Timeline frame rate」を変更できるためである。

Project snapshotの未収録122キーのうち再設定／readback一致した115キーを追加し、本ライブラリの`ProjectSetting`を計151キーとする。解像度28寸法、render format 23件、runtime codec 196件も実機結果として定数化する。本ライブラリの`VideoQuality`は公式仕様とUIで一致した5名称とAutomatic整数値を維持し、codec依存bitrateは列挙しない。

Color processing mode `Custom`についてはUIの全ドロップダウンを監査し、Color
space 43件（Outputは39件）、Gamma 63件、Timeline working luminance 11件を
定数化する。Custom luminanceの数値範囲は実機境界検証済みの48–10,000 nitとする。
UIに存在してもAPIが拒否する値は、設定可能値と明確に区別する。

codecは旧識別子を`VideoCodec`へ移植するが、使用可能な組合せはOS、edition、hardware、format依存のため、`get_render_codecs()`によるruntime検証を必須方針とする。

### 5.3 現行便利関数の実装状況（全関数の漏れ監査）

旧ライブラリの全 `def` を、本ライブラリに実装済みの現行Python APIとP1/P2へ再度突き合わせた。後方互換用の旧名は作らず、複数の基本API呼び出しを安全にまとめるP1便利関数を新しい名前と契約で実装した。

#### 実装済み：旧関数名との対応

| 旧関数 | 本ライブラリに実装済みの現行Python API |
|---|---|
| `close_current_project()`、`delete_project()`、`create_project()`、`save_project()`、`load_project()`、`get_current_project()` | `close_project()`、`delete_project()`、`create_project()`、`save_project()`、`load_project()`、`get_current_project()` |
| `get_media_pool()`、`create_empty_timeline()` | `get_media_pool()`、`create_empty_timeline()` |
| `set_project_setting()`、`get_project_setting()`、`setup_project_settings()` | `set_setting()`、`get_setting()`、`set_settings()` |
| `add_seq_file_to_media_pool()`、`append_clip_to_timeline()` | `import_sequence()`、`append_clip()` |
| `sec_to_frame_idx()`、`timecode_to_frame_index()` | `seconds_to_frames()`、`timecode_to_frames()` |
| `get_timeline_items_in_track()` | `get_track_items()` |
| `set_render_format_codec_settings()`、`set_render_setting()` | `set_render_format_codec()`、`set_render_settings()` |
| `add_fusion_comp()`、`get_comp_tool_by_name()`、`add_comp_tool()` | `add_comp()`、`get_tool()`、`add_tool()` |
| `set_tool_input()`、`set_multiple_tool_input()`、`set_tool_position()` | `set_tool_input()`、`set_tool_inputs()`、`set_tool_position()` |

`log_return_value()`内の `wrapper()` はdecorator実装の内部関数であり、独立した公開APIとしては数えない。

#### P1：実装済みの便利関数

| 旧機能・用途 | 実装名・配置 | 方針 |
|---|---|---|
| `append_fusion_composition_to_timeline()` | `append_fusion_composition()` (`fusion.py`) | 長さ指定なしではnative `InsertFusionCompositionIntoTimeline()`を使用し、固定frame長ではtimelineの解像度・fpsからpackage同梱dummy mediaを自動選択する |
| `run_rendering_and_wait_until_finish()` | `render_current_settings()` (`render.py`) | render設定からjobを追加し、返されたjob IDだけを開始・待機する。完了後にそのjobを削除するかは明示引数にし、失敗時は削除しない |
| `get_current_page()`、`open_page()` | `get_current_page()`、`open_page()` (`connection.py`) | `Page` enumで検証し、失敗時は例外にする。Fusionの`CurrentFrame`有効化にも利用する |
| `get_current_timeline()`、`set_current_timecode()` | `get_current_timeline()`、`set_current_timecode()` (`timeline.py`) | project/timelineの存在とtimecode形式を操作前に検証し、既定では`GetCurrentTimecode()`で結果確認する。ResolveがTrueを返してもread-backが更新されない参照workflowでは`verify=False`を明示する |
| `get_project_resolution()` | `get_timeline_resolution()` (`project.py`) | width/height設定を取得し、正の整数tupleとして返す |
| `make_videoMonitorFormat_str()` | `make_video_monitor_format()` (`project.py`) | 1280/1920/2048/2560/3840/4096系の対応表とfpsを明示検証する。Resolveが受け付ける文字列生成だけを担当する |
| `set_timeline_setting()`、`set_timeline_settings()` | `get_timeline_setting()`、`set_timeline_setting()`、`set_timeline_settings()` (`timeline.py`) | `useCustomSettings`を含む一括設定をfail-fastで行う。29.97/59.94だけを無条件に成功扱いする旧例外処理は引き継がない |
| `add_file_to_media_pool(..., start_frame, end_frame)` | `import_media_storage_items()` (`media.py`) | `MediaStorage.AddItemListToMediaPool()`の`media/startFrame/endFrame`形式を追加し、通常file importとrange付きimportを区別する |
| `insert_generator_into_timeline()` | `insert_generator()` (`timeline.py`) | generator名を検証し、`None`を操作例外へ変換する。title/Fusion generator等への拡張は要求時に別関数とする |
| `delete_render_preset()`、`import_render_preset()` | `delete_render_preset()`、`import_render_preset()` (`render.py`) | preset fileの存在、preset名衝突、公式APIのBoolを検証する。既存presetの暗黙削除はしない |
| `refresh_lut_list()` | `refresh_lut_list()` (`project.py`) | DCTL/LUT追加後の明示的な更新として提供し、現在projectがない場合は操作しない |
| `connect_tool()`、`connect_mediaout()`、`connect_dctl()` | `connect_default_output()` (`fusion.py`) | `ConnectInput()`で名前指定できないdefault Output/Input接続を扱う。入力名が分かる場合は実装済み`connect_input()`を優先する |
| `connect_merge_tool()` | `connect_merge()` (`fusion.py`) | Background/Foregroundの少なくとも一方を必須とし、指定された入力だけを接続する |
| `set_tool_topleft_color()` | `set_background_color()` (`fusion.py`) | RGBAを4要素・有限値として検証し、4入力をread-back確認する |
| `add_dctl_comp()` | `add_dctl_tool()` (`fusion.py`) | LUT rootからの相対path、file存在、option mappingを事前検証してからDCTL Toolを作る |
| `is_font_available()` | `require_fusion_font()` (`fusion.py`) | family/styleをFusion FontManagerで検証し、Tool作成前に不足fontを明示する |
| `add_transparent_background()` | `add_transparent_background()` (`fusion.py`) | `add_tool()`と`set_background_color()`を組み合わせる小さなbuilderとして追加する |
| `add_line_comp()` | `build_line()` (`fusion.py`) | RectangleMask、Background、Mergeをまとめて構築する。位置、RGBA、幅、高さ、angle、foreground/background接続を検証する |
| `force_rcm_update_via_page_switch()` | `refresh_fusion_color_management()` (`fusion.py`) | Resolve 21.0.4で再現条件と効果を実機テストし、必要な場合だけversion限定workaroundとして追加する |

#### P2：実装済みの便利関数

| 旧機能・用途 | 実装名・配置 | 方針 |
|---|---|---|
| `add_rectangle_comp()` | `build_rectangle()` (`fusion.py`) | RectangleMask付きBackgroundを作り、`build_line()`とmask付きBackgroundの内部builderを共有する |
| `_get_font_list()` | `get_fusion_fonts()` (`fusion.py`) | 生のFontManager戻り値を公開せず、familyからstyle tupleへの読み取り専用mappingへ正規化する |
| page切替を伴うTool位置設定 | `set_tool_position(..., session=..., activate_fusion_page=True)` (`fusion.py`) | `Composition.CurrentFrame`が`None`の場合だけ、明示許可とsessionが揃っていればFusion pageへ切り替える |
| dummy videoの自動選択 | `append_fusion_composition()`、`select_fusion_duration_media()` (`fusion.py`) | resolution/fps別assetをpackageへ同梱し、timeline settingに対応するfilenameを厳密に選択する。明示pathでの上書きも可能 |

#### 新規候補にしない旧関数

- `log_return_value()`：廃止。標準`logging`を利用する。
- `_close_project()`、`_frame_index_to_timecode()`、`_create_dummy_video_relative_path()`：公開せず、必要な処理は本ライブラリの現行Python API内部または利用者指定assetへ置き換える。
- `get_project_manager()`、`get_media_storage()`：`ResolveSession.project_manager`、`ResolveSession.media_storage`で実装済み。
- project lifecycle、project setting、Media Pool取得、file/連番import、clip append、track item取得、render format/codec/settings、Fusion comp/tool/input/position、timecode変換：新しい公開APIで実装済み。
- `set_render_setting()`：実装済み`set_render_settings()`へ統合し、1項目専用aliasは作らない。
- `is_rendering_in_progress()`：global状態ではなくjob ID指定の`get_render_job_status()`を使う。
- `reboot_resolve()`：`ResolveSession.restart()`で実装済み。

## 6. 公式文書からの新規 API 候補

候補は `official_documents/21.0.4_Scripting/README.txt` の非deprecated APIを基準とする。すべてを薄くラップするのではなく、失敗検出、入力検証、複数操作の一貫性を提供できるものを採用する。

### 優先度 P0：初期リリースに含める

| 候補 | 公式API・根拠 | 用途 |
|---|---|---|
| 接続時の製品・版確認 | `Resolve.GetProductName()`, `GetVersion()`, `GetVersionString()`（91–93行） | 接続先が Resolve 21.0.4 かをfail-fastで確認 |
| 安全なアプリ終了 | `Resolve.Quit()`（101行） | OSの強制終了より先に公式終了APIを使用 |
| プロジェクト存在確認 | `ProjectManager.GetProjectListInCurrentFolder()`（133行） | create/load/delete前の検証と明確なエラー |
| プロジェクトの一覧・選択 | `Project.GetTimelineCount()`, `GetTimelineByIndex()`, `SetCurrentTimeline()`（163–166行） | タイムラインを名前またはindexで安全に取得 |
| レンダー能力照会 | `GetRenderFormats()`, `GetRenderCodecs()`, `GetCurrentRenderFormatAndCodec()`, `GetRenderResolutions()`（197–203行） | 環境依存のformat/codecを事前検証 |
| ジョブ単位のレンダー管理 | `AddRenderJob()`, `GetRenderJobList()`, `StartRendering(jobId)`, `StopRendering()`, `GetRenderJobStatus(jobId)`（172–189行） | 対象ジョブだけを開始・監視・停止し、他ジョブを消さない |
| Media Pool フォルダー取得 | `GetRootFolder()`, `GetCurrentFolder()`, `SetCurrentFolder()`（232、249–250行） | import先を暗黙のGUI選択状態に依存させない |
| trackの検証と操作 | `GetTrackCount()`, `GetTrackName()`, `SetTrackName()`, `GetItemListInTrack()`（372、399、416–417行） | track indexを操作前に検証し、テスト後の確認にも使う |
| playheadの取得 | `Timeline.GetCurrentTimecode()`（411行） | `SetCurrentTimecode()` の結果確認 |
| ネイティブFusion Composition挿入 | `Timeline.InsertFusionCompositionIntoTimeline()`（438行） | ダミー動画方式を使わない基本経路 |

### 優先度 P1：初期安定後に追加

| 候補 | 公式API・根拠 | 用途 |
|---|---|---|
| プロジェクトのバックアップ | `ImportProject()`, `ExportProject()`, `RestoreProject()`（141–143行） | 実機テスト前後の退避と復元にも利用可能 |
| Media Poolの整理 | `AddSubFolder()`, `DeleteFolders()`, `MoveClips()`, `MoveFolders()`（233、254–256行） | importワークフローをGUI状態から分離 |
| メディア再リンク | `RelinkClips()`, `UnlinkClips()`（260–261行） | ファイル移動後の復旧 |
| clip情報・設定 | `GetClipProperty()`, `SetClipProperty()`, `GetMetadata()`, `SetMetadata()`（305–308、332–334行） | color space等のset/get確認を共通化 |
| marker操作 | MediaPoolItem、Timeline、TimelineItem のmarker API（317–325、403–410、488–495行） | 同種APIの検証・エラー処理を共通化 |
| timeline複製・export | `DuplicateTimeline()`, `Timeline.Export()`（418、432行） | 破壊的変更前の複製、AAF/XML/OTIO等の出力 |
| timeline track管理 | `AddTrack()`, `DeleteTrack()`, enable/lock操作（372–397行） | テスト用timeline構築と通常の編集自動化 |
| thumbnail取得 | `GetCurrentClipThumbnailImage()`（414–415行） | 公式Example 6を基にbase64データを検証して返す |
| Fusion comp管理 | `GetFusionCompCount()`, `GetFusionCompByIndex/Name()`, import/export/rename/delete（473–476、502–507行） | compの生成確認と再利用 |
| LUT操作 | `Graph.SetLUT()`, `GetLUT()`（584–589行） | 現行DCTL/LUT用途を公式Color Graph側にも拡張 |
| テスト時の背景処理抑制 | `DisableBackgroundTasksForCurrentResolveSession()`（117行） | 実機テストの揺らぎを減らせるか検証 |

### 優先度 P2：要求が出たときに追加

- Gallery、ColorGroup、take、stereo、Fairlight、burn-in/layout/user-preference preset、database切替、cloud project関連。
- `CreateSubtitlesFromAudio()`、`GenerateSpeech()`、IntelliSearch、Slate解析、Motion Deblur等のStudio/AI機能。公式文書ではFree版、最小システム要件、追加パッケージの有無により `False` などを返すとされている（1021–1035行）ため、通常機能とテスト条件を分離する。
- Resolve 21で追加された `PerformAudioClassification()`、`RemoveMotionBlur()`、`AnalyzeForIntellisearch()`、`AnalyzeForSlate()`、`GenerateSpeech()` は新規API候補台帳には残すが、現行ライブラリの主用途から外れるため初期実装しない（CHANGELOG.txt「21.0 Beta」）。

deprecated欄（README.txt 1099行以降）およびunsupported欄（1140行以降）のAPIは新規ラッパーを作らない。

## 7. 公式文書を更新したときの API 棚卸し手順

Resolveの対応版を上げる際のGUI/API対応、設定snapshot、実機テスト、証拠、完了条件を含む手順は[Resolveバージョン更新時の検証手順](resolve-version-upgrade.md)に集約する。この節では公式APIの棚卸しだけを扱う。

次を実施する。

1. `official_documents/<version>_Scripting/` を追加し、旧版を削除しない。
2. 新旧 `CHANGELOG.txt` と `README.txt` のオブジェクト別メソッド一覧を比較する。
3. 追加・変更・deprecated・unsupported APIを一覧化する。
4. 既存ラッパーへの影響、利用価値、Free/Studio差、破壊性、実機テスト可否を評価する。
5. P0/P1/P2候補表を更新し、採用するAPIには公式文書の行または節を記録する。
6. 対応対象のResolveバージョンを接続時検査とパッケージ文書へ反映する。

## 8. テスト計画

### 8.1 単体テスト

Resolveを起動せず、Python 3.12で毎回実行できるようにする。

- timecode/frame変換の境界値と不正形式
- 解像度・fps・page・track type・index・パスの入力検証
- Fakeオブジェクトに正しい公式API名と引数を渡すこと
- 公式APIが `False`、`None`、空リストを返した場合の例外
- importしても `DaVinciResolveScript` のロードや接続を実行しないこと
- render job IDを保持し、他のジョブを削除しないこと
- float、dict、remote objectを含むFusion Tool入力値の照合

### 8.2 Windows実機テスト

`pytest` markerで通常テストから分離する。

- Resolve 21.0.4への接続とバージョン確認
- 専用プロジェクトのcreate/get/save/close/load/delete
- project/timeline設定のset/get。ただしResolve側で正規化される値は許容値を個別定義
- MediaPoolへの静止画・動画・連番追加と、返されたオブジェクトへのアクセス
- timeline作成、track作成、clip追加、取得、削除
- Fusion CompositionとToolの作成、接続、入力値、位置の確認
- 小さな素材を使ったrender job作成、状態監視、成果物確認、対象job削除
- `Quit()`、起動、期限付き再接続。再起動テストは最後に単独実行

テスト用プロジェクト名には専用prefixと実行IDを使い、その実行で作成した対象だけを削除する。既存プロジェクトや既存render jobを一括削除しない。

各テストファイルの冒頭には、`sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib` で実行することと、対応するコマンドをコメントで明記する。

```powershell
python -m pytest tests/unit
python -m pytest -m resolve_integration tests/integration
```

### 8.3 Countdown V2 画像回帰テスト

現行実装で最も複雑な利用例である `sample_code/2025/02_Countdown_V2/create_countdown_v2.py` を原本として、新パッケージの総合回帰テストを作る。原本は読み取り参照だけとし、一切変更しない。

新パッケージ対応版は、移行先リポジトリの `tests/countdown_regression/create_countdown_v2.py` にテスト専用の派生スクリプトとして作成する。原本との差分は、新パッケージへの移行、テスト可能化、`transfer_functions.py` 依存の除去に必要な範囲に限定する。

参照データは `tests/countdown_reference_data/ref_data_1280x720.zip` とする。事前確認時点の参照データは次の内容である。

- ZIP SHA-256: `490A48B91FE8ACD693C31253DAF263000D9F1AEB76DC6216F60049590296773D`
- 画像数: 384枚
- 画像仕様: 1280×720、RGB、各channel 16-bit、non-interlaced PNG
- 4条件: Gamma 2.4 / ST2084 と P3-D65 / Rec.2020 の組み合わせ
- 各条件: 96 frames

#### Countdownテスト用派生スクリプトの作成

`tests/countdown_regression/create_countdown_v2.py` には次の変更を反映する。

1. `ty_davinci_control_lib_2` と `ty_davinci_constants` を、新しい `ty_davinci_resolve` パッケージへ置換する。
2. 出力先を `F:\abuse\Countdown\temp_seq` に固定せず、関数引数またはCLI引数 `--output-dir` で指定可能にする。通常実行時のdefaultは既存値を維持してよいが、テストではpytestの一時directoryを渡す。
3. テスト対象の解像度、fps、gamut、gammaを引数で指定可能にし、モジュールをimportしただけでは処理を開始しない。
4. `ty_lib/transfer_functions.py` をimportしない。原本で使用しているのは `oetf_from_luminance(..., ST2084)` のみなので、派生スクリプト側にNumPyだけで動作する小さな `st2084_oetf_from_luminance()` を実装する。
5. ST 2084関数は、既存処理と同じく入力をcd/m²、出力を正規化code valueとし、0–10000 cd/m²の範囲を検証する。SMPTE ST 2084の定数を明記し、代表値の単体テストを追加する。
6. render完了前のjob削除を行わず、新ライブラリのjob ID単位の待機処理を使用する。
7. 使用する動画、音声、DCTL、font等のassetを開始前に検証し、不足があればレンダーを開始せずに失敗させる。

原本および `transfer_functions.py` のコードを無条件に同期させる構成にはしない。Countdownで必要なST 2084変換だけを派生スクリプトへ独立実装し、同モジュールと、その依存先である `colour` をCountdown回帰テストから除外する。

#### 比較方法

`tests/integration/test_countdown_regression.py` を追加し、次の順序で検査する。

1. 参照ZIPのSHA-256、entry数、重複entry、path traversalを検査する。
2. 空の一時directoryへCountdownの4条件をレンダーする。
3. 出力ファイル名の集合が参照ZIPと完全一致することを確認する。余分なPNGや欠落も失敗とする。
4. 参照・出力双方のPNGが1280×720、RGB、16-bitであることを確認する。
5. PNGを16-bit整数のRGB配列としてdecodeし、384枚すべてを同名ファイル同士で比較する。
6. shape、dtype、全channelの全画素値が完全一致することを確認する。許容差は設けず、1 code valueの差でも失敗とする。
7. 不一致時は最初のファイル名、座標、channel、期待値、実値、相違画素数を表示する。

PNGの圧縮方法、chunk順序、timestamp等は画としての出力に影響しないため、PNGファイル全体のbyte一致は要求しない。比較対象はdecode後の16-bit RGB sampleである。16-bit RGBを8-bitへ縮退させないdecoderをテスト用依存関係として選び、decoder自体のbit depth保持を小さな単体テストで確認する。

本テストには `resolve_integration` に加えて `countdown_regression` markerを付け、通常の単体テストでは実行しない。

```powershell
# Run from sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
python -m pytest -m countdown_regression tests/integration/test_countdown_regression.py
```

完全一致には、少なくともResolve 21.0.4、使用asset、DCTL、font、project/render設定が参照データ生成時と一致している必要がある。事前条件の差とライブラリの回帰を区別できるよう、これらをpreflight結果としてテスト出力へ記録する。

## 9. 実装フェーズ

### Phase 0: API契約の確定

- 公開名、例外、戻り値、対象APIを本計画に沿って確定
- 21.0.4公式文書の参照箇所を各機能のissue/checklistに記録

### Phase 1: パッケージ基盤

- `pyproject.toml`、`src` layout、README、pytest設定を作成
- `errors.py`、`connection.py`、バージョン検査を実装
- editable install、wheel build、import副作用なしを確認

### Phase 2: 純粋関数と基本操作

- `timecode.py`、定数、入力検証
- project、media、timelineのP0機能を移植
- Fakeを使った単体テストを先行して追加

### Phase 3: レンダーとFusion

- job ID単位のrender管理と実機テスト
- Fusion基本操作を移植
- ネイティブFusion Composition経路を検証し、ダミー動画方式の要否を決定

### Phase 4: P1公式APIと用途特化機能

- 5.3のP1便利関数を実装済み。固定長`append_fusion_composition()`、`render_current_settings()`、page/playhead/timeline setting、DCTL/transparent background/line builderを含む
- `build_rectangle()`、font一覧正規化、page切替付きTool位置設定、dummy media選択をP2として実装済み
- RCMページ切替workaroundを21.0.4で再評価
- 原本の `create_countdown_v2.py` は変更せず、`tests/countdown_regression/create_countdown_v2.py` に新パッケージ対応版を作り、384枚の16-bit RGB完全一致テストを追加

### Phase 5: Python 3.13評価

- 単体テスト、package install、`fusionscript.dll`ロード、Resolve接続、代表的な実機テストを3.13 64-bitで実行
- 合格後に `requires-python` を `>=3.12,<3.14` へ変更

## 10. 初期リリースの完了条件

- Python 3.12 64-bitでeditable installとGit URL installが可能
- import時にResolve未起動でも失敗しない
- Resolve 21.0.4以外への接続を明確なメッセージで拒否できる
- P0機能の単体テストが合格
- Windows + Resolve 21.0.4で主要な実機テストが合格
- Countdown V2が参照ZIPと同じ384枚を生成し、decode後の16-bit RGB値が全画素完全一致
- 既存プロジェクト、既存render job、GUIで選択中のMedia Pool Folderに暗黙依存しない
- READMEに最小の接続・プロジェクト作成・media追加・render例を掲載
- 実装したラッパーから21.0.4公式APIの根拠を追跡できる
