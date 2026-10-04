# Resolve 21.1調査・検証記録

2026-10-04、Windows 11 Pro 64-bit／Python 3.13.16／DaVinci Resolve Studio
21.1.0.17で調査しました。開始時の独立リポジトリはcleanで、Python 3.13移行は
`41a1191`にコミット済みでした。この更新ではコミットを作成していません。

環境の根拠は[environment.json](verification/21.1.0.17/environment.json)、
[GPU](verification/21.1.0.17/gpu.json)、[OS](verification/21.1.0.17/os.json)です。
Resolve FontManagerが報告するWindowsユーザーフォントの実ファイルをhashしました。
Noto Sans Regular／Bold、Noto Sans Mono Blackのhashは承認済み21.1マスターの記録と
一致します。インストール済みDCTL 3ファイルも制作元とhash一致しました。
フォント・DCTL・画像マスターは置換していません。I/O機器経由のSDI出力は未検証です。

## 公式資料の比較

旧[README](../official_documents/21.0.4_Scripting/README.txt)／
[CHANGELOG](../official_documents/21.0.4_Scripting/CHANGELOG.txt)と、新
[README](../official_documents/21.1.0_Scripting/README.md)（31 Aug 2026）、
[CHANGELOG](../official_documents/21.1.0_Scripting/CHANGELOG.md)（1 Sep 2026）、
[型定義](../official_documents/21.1.0_Scripting/DaVinciResolveScript.pyi)を照合しました。
README本文の配置変更はAPI削除と扱っていません。

[シグネチャ台帳](verification/21.1.0.17/api-signatures.json)はオブジェクト・メソッド単位で
旧呼び出し形式と新しい正式シグネチャを保存しています。
`python tests/integration/probe_official_api_diff.py`で再生成できます。
`absent_from_stub`は「型定義に掲載なし」であり、削除を意味しません。
旧資料の引数のoptional指定・型・戻り値の説明は本文も参照する必要があります。
特に旧`InsertAudioToCurrentTrackAtPlayhead`のシグネチャ行は途中で切れているため、
新API追加ではなく、新型定義による引数の明確化として扱います。

| 分類 | 21.1での差分 | 既存ラッパーへの影響・対応 |
|---|---|---|
| 変更・非推奨形式 | Project／Timelineの`GetSetting`→`GetSettings()`、`SetSetting`→`SetSettings(dict)` | 新形式を優先。1キーずつ順序を維持して設定し、拒否で停止。新メソッド不在時だけ旧形式を使う |
| 変更・非推奨形式 | `ImportMedia`の通常パスリスト→`ImportClipInfo`辞書リスト | **実機制約あり**。通常MP4は新形式で`None`、旧形式で成功。通常ファイルの旧形式を維持。画像連番は既存の辞書形式 |
| 変更・非推奨形式 | `AddItemListToMediaPool`の通常パスリスト→`MediaStorageItemInfo`辞書リスト | パスだけでも`{"media": path}`に変更。ソース範囲付きの既存形式は維持 |
| 正式形式への修正 | `StartRendering(jobIds: list[str], isInteractiveMode=False)` | 単一IDも`[job_id]`で渡す。indexは使わない |
| 非推奨形式 | `AppendToTimeline`、`CreateTimelineFromClips`のオブジェクトリスト→辞書リスト | Appendは既に辞書形式。CreateTimelineFromClipsは未使用 |
| 変更・非推奨形式 | TimelineItemの`GetProperty`／`SetProperty`→`GetProperties`／`SetProperties` | ライブラリ本体に旧形式の使用なし。新setterは辞書全体を事前検証し、全適用または全拒否 |
| 非推奨形式 | MediaPoolItemの`SetMetadata`／`SetThirdPartyMetadata`は辞書、`GetMetadata`／`GetClipProperty`は全件取得してindex | ラッパー未使用。getterの旧optional引数は型定義に残るがREADMEは非推奨と明記 |
| 新たに非推奨のメソッド | Projectの`GetPresetList`／`SetPreset` | 未使用。新ProjectSettingsPreset群への移行対象 |
| 追加 | ResolveのKeyboardPreset一覧・現在値・読込・削除・import/export、ProjectのProjectSettingsPreset一覧・適用・保存・更新・削除・import/export | 任意の新機能。既存機能の移行には不要 |
| 追加 | Projectの`UpdateRenderPreset`、`SetQuickExportEnabledForRenderPreset`、音声render formats/codecs | 既存video render照会・render preset処理とは別機能。未ラッパー化 |
| 追加 | `CreateMulticamClip`、`AutoAlignClips`、`PerformMulticamSmartSwitch`、`FlattenMulticam` | 任意の新機能、未使用 |
| 追加 | TimelineItemのtype、transition、speed、fades、output blanking、Timelineのoutput blanking | 任意の新機能、未使用 |
| 追加 | 音声normalize modes／level、MediaPoolItemの`SetAudioMapping`、TimelineItemの`SetSourceAudioChannelMapping`、`GetTranscription` | 任意の新機能、未使用 |
| 引数変更 | Folder／MediaPoolItemの`TranscribeAudio(..., transcribeAsNestedClip=False)`、MediaPoolItemの`ClearTranscription(clearNestedClipTranscription=False)` | optional引数追加。未使用 |
| 追加・型の明確化 | TimelineItemPropertiesのnative audio・enabled states等の辞書型 | 公開ラッパー未使用。旧property記述だけから削除や動作保証を判断しない |
| 追加 | MediaStorage clone開始・停止・状態・設定 | 任意の新機能、未使用 |
| 追加 | Resolveの`ValidateDCTL`／`EncryptDCTL` | 既存のFusion DCTL tool作成は別API。今回の配置・暗号化・置換は行わない |
| 追加 | Resolveのcurrent Project／Timeline／MediaPool／Gallery、`SetHighPriority`、`IsStudio`、ProjectManagerの`GetProjectLastModifiedTime` | 既存manager経由の取得を維持。優先度は変更しない |
| 戻り値の資料差 | `Resolve.Quit`は旧READMEでNone、新型定義でbool | `quit()`は戻り値を使わず、restartは終了・再接続を観測する既存方式を維持 |
| 資料間の不一致 | `GenerateSpeech`は新型定義でSpeechSettingsのみ、READMEではtimecodeを含む旧記載 | 未使用。正式引数の実機確認は未実施。どちらかだけを根拠に保証しない |
| 実行環境 | Python 2廃止、内蔵Python 3.14追加 | 外部Python 3.13の本ライブラリとは別。内蔵Pythonへ移行・依存追加はしない |

既存deprecatedメソッド（ProjectManagerの旧dict一覧、ProjectのGetPresets／GetRenderJobs／
GetRenderPresets、MediaStorageの旧dict一覧／AddItemsToMediaPool、FolderのGetClips／
GetSubFolders、MediaPoolItemのGetFlags、TimelineのGetItemsInTrack、TimelineItemの
GetFusionCompNames／GetFlags／GetVersionNames／GetNumNodes／SetLUT／GetLUT／GetNodeLabel）
は新READMEにも残り、ライブラリ本体では使用していません。

Unsupportedは旧版と同じrender job index群、`videoMonitorUseRec601For422SDI`の置換、
`perfProxyMediaOn`の置換、FCPXML 1.3〜1.7 exportです。新たな非対応APIとしては数えません。
新型定義から旧setting/property形式が省かれていても、READMEはdeprecatedとして残しています。

通常ImportMediaの制約は[実機比較](verification/21.1.0.17/import-conventions.json)、
MediaStorageの形式は[実機比較](verification/21.1.0.17/storage-conventions.json)を参照してください。
失敗した新形式を自動再試行する実装は追加していません。

型定義はASTで静的に読み、正式メソッド・引数・戻り値・設定辞書の根拠に使用しています。
実行時モジュールとしてロードしません。remote objectの既存`Any`注釈は維持し、
21.1専用の巨大な型定義をpackageへ複製したり、21.0.4にもその型を保証したりしません。
公開APIの引数・戻り値は従来の型を維持します。

## 全設定snapshot

[新規の空projectの158キー](verification/21.1.0.17/project-default-settings.json)は
`GetSettings()`で取得し、同じprojectの`GetSetting()`全件と一致しました。
158キーは公式`ProjectSettings`型のキー集合と完全一致します。公開ProjectSettingは151キーです。
残る7キーの一覧と比較状態は[setting-comparison.json](verification/21.1.0.17/setting-comparison.json)に記録しました。

旧版のraw全snapshotはリポジトリの保存記録に見つかりませんでした。旧文書に158キーとの
記録があるだけではキー集合や初期値の一致を保証できません。**追加キー・削除キー・初期値変更の
新旧比較はすべて`comparison_unverified`**です。新旧とも158という数だけから「変更なし」とは判定しません。
フォルダー設定等の初期値はユーザーの環境・既定presetにも依存します。

[公開151キーの同値書き戻し](verification/21.1.0.17/public-key-writeback.json)では、新
`SetSettings`で148件が成功しreadback一致、Playbackと初期状態の空Timeline／Output gammaは
拒否されました。gammaはCustom＋Separate条件で候補Enumの書き込みを別途検証します。
同値書き戻し成功は全候補・GUI対応・保存後保持の保証ではありません。

## GUI・API検証

各変更の全snapshotと画面証拠は[検証ディレクトリ](verification/21.1.0.17/)、
分類は[GUI台帳](project-setting-gui-coverage.json)を参照してください。
台帳の旧版の本文掲載分類は保持し、21.1で確認した項目だけを版付き観測として追加します。
旧版で本文に載っていたという理由で21.1のGUI確認済みにはしません。

- RCMをGUIで選ぶとAutomaticがオンになり、処理モードはSDR、outputはSDR Rec.709表示になります。
  GUIでAutomaticだけをオフにするとプリセット選択が現れます。親設定変更は複数キーへ波及します。
- CustomではInput／Timeline／Output、working luminance、DRT、Limit output gamut to等が現れます。
  Separateオンでガンマの独立選択が現れ、combined color spaceはgamut単体へ正規化されます。
- [全10プリセットのGUI差分](verification/21.1.0.17/gui-preset-differences.json)を、
  Automaticオフの同一空projectで、処理モードだけを1項目ずつ変えて取得しました。
  Customは別の全snapshotと画面を保存しています。GUIの親変更はTimeline color space、
  DRT、working luminance、graphics white等の関連値も適用します。
  APIは全11ラベルの設定・直後readbackが成功しましたが、名前だけのSDR Rec.709設定は
  [再読込でCustomへ戻りました](verification/21.1.0.17/preset-sdr709-reload.json)。
  GUIで設定したSDR Rec.709とHDR PQ P3は再読込後も保持されました。
- Customから[APIでAutomaticをオン](verification/21.1.0.17/api-automatic-on.json)にすると
  readbackは1ですが、[再読込で0へ戻りました](verification/21.1.0.17/api-automatic-on-reload.json)。
  Automatic／presetは`verified_gui_to_api`として、Pythonの保存後保持の制限を明記します。
  [旧・新呼び出し比較](verification/21.1.0.17/settings-persistence-conventions.json)では、
  新規Custom projectごとにSDR Rec.709、HDR Wide Gamut、Automaticオンを単独設定しました。
  旧`SetSetting`と新`SetSettings`の双方で同じ保存後の戻りを観測したため、今回の形式変更に
  よる差とは確認されませんでした。これは当該Custom条件の結果であり、全初期条件の保証ではありません。
- [SeparateオンのGUI全gamut候補](verification/21.1.0.17/gui-gamut-options.json)は
  Input／Timeline各45件、Output41件です。InputとOutputにはさらにSame as Timelineが表示されます。
  OutputはHSL／HSV／Lab／YUVを省きます。DJI D-Gamut2／Vivo Wide Gamutを発見し、
  Python設定・readback・[再読込](verification/21.1.0.17/api-new-gamuts-reload.json)・
  [GUI](verification/21.1.0.17/api-new-gamuts-reloaded.jpg)を確認してEnumに追加しました。
  これらを旧版から追加されたGUI値と断定せず、旧Enumに未収録の21.1観測値として扱います。
  SeparateオフのInput combined menuも先頭から末尾まで画面を保存しました。
  API値とGUI表記は一部異なり、GUIラベルをそのまま公開Enumへ複写しません。
  特殊値`"Same as Timeline"`はInputでは新APIも拒否しましたが、Outputでは設定・readback・
  [保存後保持](verification/21.1.0.17/output-same-as-timeline.json)・
  [GUI一致](verification/21.1.0.17/output-same-as-timeline-reloaded.jpg)を確認しました。
  これはgamut値ではないため`OUTPUT_COLOR_SPACES`の41件とは別の文字列候補です。
- PythonでInput=P3-D65、Timeline=Rec.2020、Output=P3-D65を1キーずつ設定し、
  readback、保存・再読込後の保持、GUIの該当3欄を確認しました。
  未指定の空gammaは再読込でGamma 2.4へ補完されました。全snapshotの差分を残しています。
- ACESccはPython設定・readback・保存・再読込・GUIを確認しました。
  ACEScc→ACEScctはGUIのcolor scienceだけを変え、全snapshotを保存しました。
  親変更ではgamut compressやcolor aware gradingの既定値も変わり得ます。
- Project timeline frame rateはPythonで25へ設定して保存・再読込・GUI一致を確認しました。
  Playbackは新SetSettingsでも拒否されます。GUIだけで30へ変更し、API取得値と再読込後保持を確認しました。
  Pythonのtimeline frame rate変更だけではPlaybackが自動で同じ値になることを保証しません。
- 個別Timelineは空の状態でcustom settingsを有効にし、Pythonで30へ設定してreadback・保存・再読込・
  GUIを確認しました。GUIだけで25へ変更した全snapshotも保存しています。
  Timeline Settingsには独立したPlayback欄がなく、そのAPI書き込みも拒否されました。
- [新APIのframe rate制限](verification/21.1.0.17/frame-rate-constraints.json)では、
  空custom timelineの整数24／25／30／50／60は成功、小数23.976／29.97／59.94は拒否でした。
  clipを追加したtimelineのfps変更も拒否されました。全timelineがcustom設定の今回のprojectは
  空timeline存在時・素材import後ともproject fps変更が成功し、custom timelineのfpsは別に保持されました。
  素材存在だけを一律のproject fpsロック条件として扱いません。
- Limit output gamut toをGUIだけでOutput color space→P3-D65へ変更して保存しても158キーに差分は
  ありません。`colorSpaceOutputGamutMapping`はNoneのままです。21.1でも`unmapped`、GUI操作が必要です。

## 互換性と画像マスター

接続対象は21.0.4／21.1.0です。今回の実機検証は21.1.0.17のみです。
21.0.4の新Python環境・今回の変更後の実機互換性は未再検証です。
新SDR_REC_709定数の根拠も21.1実機です。

## Fusion回避処理の比較

通常の回避処理ありでは、4条件・384枚が承認済み21.1マスターと全16-bit RGB sampleで
完全一致しました。同じ環境・同じ4条件で`refresh_fusion_color_management`だけを無効に
した[比較](verification/21.1.0.17/fusion-without-refresh.json)では196/384枚に差がありました。
したがって21.1でも処理を維持します。0.5秒は実機で採用した待機値であり公式仕様ではありません。
比較probeは差分を観測結果として記録し、API／render失敗はエラーで停止します。
無効時の比較画像・使い捨てprojectはfinallyで削除します。マスターは更新していません。

承認済み21.1マスターへの回帰一致と、旧21.0.4マスターとの描画互換性は別の判断です。
旧ZIPは保持し、今回の変更で旧版との描画完全一致は保証しません。

## 検証結果と完了範囲

[実行結果](verification/21.1.0.17/test-results.json)に最終コマンドと件数を保存しました。
単体97件、実機7件、分離した再起動1件の計105件が成功しています。実機試験は
許可されたサンドボックス外実行です。新定数も正式SetSettings形式で設定・readbackを確認しました。
lifecycleの作成・保存・再読込・削除は20/20回成功しました。
wheel／sdistをoffline buildし、一時directoryへのwheel install、import、正式settings呼び出しを
確認しました。新`_settings.py`が両配布物に入り、cacheが混入しないことも確認しました。
現在の`.venv313`のeditable環境で単体・実機検証を行っています。

| 更新手順の完了条件 | 今回の結果 |
|---|---|
| 新旧公式API差分 | owner・メソッド・シグネチャ台帳、変更・非推奨・非対応・追加機能の影響を記録済み |
| 全設定snapshotの比較分類 | 21.1の158キーを取得済み。旧raw snapshot不足により追加・削除・初期値変更はすべて比較未確認と分類 |
| GUI対応の証拠 | 親状態、全プリセット＋Custom、ACES、色空間、両scopeのfps、Limit output gamutを調査。全snapshot・差分・画面を保存 |
| 公開定数の設定/readback | 新形式のEnum候補検証成功。同値書き戻し151件の個別結果と状態依存の拒否も保存 |
| query-only／unmapped／制限の区別 | 版付き台帳へ4状態を追加。旧掲載履歴は保持。preset／Automaticの保存制約、ImportMedia新形式の実機制約も記録 |
| テスト・必要な画像回帰 | 105件成功、4条件384枚は承認済み21.1マスターと完全一致。Fusion回避処理なしとの差も比較済み |
| 片付け | 今回の使い捨てproject、一時PNG、pytest directory、wheel install先、比較用build出力を削除。監査証拠はこの文書から参照するため保持 |
| 対応版・利用者文書・導線 | GUI対応、API根拠、更新手順、README、一覧を更新。21.0.4未再検証を明記 |

21.1環境で可能な調査・正常系検証と必要な実装更新は実施しました。旧版の完全なsnapshot比較、
Python 3.13＋21.0.4での実機互換性、旧マスターとの描画完全一致は確認できていません。
これらを確認済みとして全面的な互換性保証はしません。テスト成功だけで新旧の差がないとも判断しません。

後続候補は`2026/06_DaVinci_Resolve_API_Test_V3/api_sapmle.py`の見直しです。
今回のライブラリ更新の範囲には含めていません。
