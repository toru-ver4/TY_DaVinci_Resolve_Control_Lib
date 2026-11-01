# Resolve 21.1.2調査・検証記録

2026-11-01、Windows／Python 3.13.16（64-bit）／DaVinci Resolve Studio
21.1.2.10で検証しました。接続を通常の制限環境で一度試して失敗したため、
AGENTS.mdの許可に従って制限外で実機検証しています。

## 公式資料とAPI差分

同梱の[README](../official_documents/21.1.2_Scripting/README.md)、
[CHANGELOG](../official_documents/21.1.2_Scripting/CHANGELOG.md)（22 Oct 2026）、
[型定義](../official_documents/21.1.2_Scripting/DaVinciResolveScript.pyi)、接続モジュールは、
インストール先の同名ファイルとbyte単位で一致します。
[21.1.0からの構造化差分](verification/21.1.2.10/api-diff.json)は公式`.pyi`をASTで読み、
全overload、引数・戻り値、TypedDictのfield、Enum定義と基底クラスを比較しています。
型定義の省略を実行時APIの削除と断定しません。

```powershell
.venv313/Scripts/python.exe tests/integration/probe_resolve_21_1_2.py api
.venv313/Scripts/python.exe tests/integration/probe_resolve_21_1_2.py live
```

メソッドは102件追加、既存5件のシグネチャに差があり、型定義からのメソッド削除はありません。
READMEのDeprecated／Unsupported節は21.1.0から変更ありません。

| 対象 | 公式資料の変更 | 本ライブラリへの影響 |
|---|---|---|
| 21.1.1の非同期化 | TranscribeAudio、AnalyzeForSlate、CreateSubtitlesFromAudio、DetectSceneCuts、SmartReframe、RenderWithQuickExportが非blocking化。Projectに6種類のstatus取得APIを追加 | 本ライブラリの既存ラッパーは未使用。直接使用する場合は戻り値だけで完了と判断せず、対応するGet…StatusでJobStatus／Errorを確認する |
| Timeline custom設定 | 21.1.1でuseCustomSettings切替時のproject設定保持を修正 | 独立したtimeline設定とproject設定を実機で再検証する |
| Photo Album | Project／MediaPoolのalbum操作、PhotoAlbum、PhotoAlbumItem、photo用render／quick export設定を追加 | 新機能。既存のvideo制作APIへ混在させず、公式オブジェクト経由で利用する。専用ラッパーと実機保証は今回追加しない |
| Effect、編集、音声 | Effect取得・追加・削除・並べ替え、属性copy、clip位置／offset、gap削除、timeline enabled、silence削除、audio level解析を追加 | 既存ラッパーに変更不要。新機能の実機保証は別途必要 |
| ExportFrame／親folder／metadata | Timeline／TimelineItem／MediaPoolItemのframe export、parent folder照会、SetTranscription等を追加 | 既存ラッパー未使用 |
| Graph.ApplyGradeFromDRX | applyToAllLayers、keyframeModeのoptional引数を追加。node label／color APIも追加 | 既存ラッパー未使用 |
| MediaPool.CreateEmptyTimeline | optional timecodeとnullable戻り値を追加 | 既存の名前のみの呼び出しは維持できる。Noneは既存の例外処理で停止する |
| MediaPool.AddSubFolder | 戻り値をFolderからFolderまたはNoneへ明確化 | 既存ラッパー未使用 |
| Project.GenerateSpeech | optional timecodeとnullable戻り値を追加 | 21.1.0のREADME／型定義間のtimecode不一致を解消。既存ラッパー未使用 |
| Resolve.GetKeyframeMode | 戻り値注釈をintからKeyframeModeへ変更。21.1.2では全pageから使用可能 | 既存ラッパー未使用 |
| 設定辞書 | ProjectSettingsとAutoCaptionSettingsにtranscriptionExtendedLanguageSupport追加。RenderJobInfoにphoto用fieldとnullableなvideo fieldを追加。TimelineItemPropertiesにtransition関連4 field追加 | 巨大な公式型定義はpackageへ複製せず、必要なproject設定定数を実機確認して追加する |

対応バージョンは21.0.4／21.1.0／21.1.2を明示列挙します。未検証の21.1.1や将来のpatchを
自動許可しません。旧版実機で今回の変更を再検証していません。

## 設定・呼び出し形式・GUI

[環境](verification/21.1.2.10/environment.json)、[GPU](verification/21.1.2.10/gpu.json)、
[空projectの全159設定](verification/21.1.2.10/project-default-settings.json)、
[旧158設定との差分](verification/21.1.2.10/setting-comparison.json)を保存しました。
新旧のraw snapshotを比較し、追加は`transcriptionExtendedLanguageSupport`の1キー
（初期値`"0"`）、削除と既存設定の初期値変更はありませんでした。
この結果は同一環境での観測であり、すべてのユーザー設定・presetに同じ初期値を保証しません。
新snapshotではGetSettingsと旧GetSettingの全件が一致しています。

［TY API］`ProjectSetting.TRANSCRIPTION_EXTENDED_LANGUAGE_SUPPORT`を追加し、公開キーは152個です。
[拡張言語設定の全snapshot](verification/21.1.2.10/transcription-extended-language.json)では
`"0"`の設定・readback・保存後保持が成功しました。`"1"`はFalseを返し、全設定に変化が
ありませんでした。公式型定義は有効化に拡張言語モデルが必要と明記しています。
この環境では有効化できず、モデル導入後の動作は未検証です。GUIとの対応は未確認として
台帳のpending_gui_reviewに追加し、旧版に存在する定数として扱いません。

[ImportMedia形式の比較](verification/21.1.2.10/import-conventions.json)では通常MP4の
FilePath辞書が再び0件、旧pathリストが1件成功しました。制作側の旧形式を維持し、
拒否時の自動fallbackは追加しません。
[全format／codec](verification/21.1.2.10/render-formats-codecs.json)では23 format、
codec和集合200識別子となり、すべて既存Enumに含まれます。新codec追加は不要でした。

[Fusion registry比較](verification/21.1.2.10/fusion-registry-comparison.json)では、
既存Enumに対してOpenPBRの`MtlPBRUber`だけが未収録でした。
［TY API］`FusionTool.MTL_PBR_UBER`を追加し、native Toolは297、Modifierは11、
Resolve FXは83となります。これはこの版での実機観測であり、OpenPBRがResolveのどの版で
初めて導入されたかは断定しません。旧版での新定数の使用可否は未検証です。
[入力生成の結果](verification/21.1.2.10/fusion-typing-summary.json)では全391登録のTool作成に
失敗はなく、入力補完用の`fusion.pyi`／`fusion_tool_types.pyi`を再生成しました。
[入力名差分](verification/21.1.2.10/fusion-input-diff.json)は51 class、149入力追加、10入力削除です。
削除された10個はOGrafLoaderのCustomAction0〜9で、新しいplay／stop action等の入力を
取得しています。型定義は21.1.2で取得した入力名の補完用であり、全入力を旧版にも保証する
ものではありません。大文字・小文字だけが異なる入力名の生成順も固定しました。

[frame rate制限](verification/21.1.2.10/frame-rate-constraints.json)は従来どおりで、
空custom timelineの整数24／25／30／50／60は成功、小数23.976／29.97／59.94と
clip追加後の変更は拒否されました。projectのframe rateは、全timelineがcustomという
今回の条件で素材追加後も変更可能でした。OutputのSame as Timelineは成功、Inputは拒否です。
[保存形式の比較](verification/21.1.2.10/settings-persistence-conventions.json)では、
SetSetting／SetSettingsの両方で、Customからプリセット名だけを設定しても保存後にCustomへ
戻り、Automaticオンも保存後オフへ戻りました。SDR Rec.709とHDR DaVinci Wide Gamut
Intermediateの両方で確認しています。制作設定はCustomで関連する値を明示してください。

21.1.0.17のsnapshotとGUI証拠はそのまま保持しています。旧GUI対応表は21.1.0以前の
観測であり、21.1.2でGUIを再観測したという扱いへ一括変更していません。

## 自動テストと配布確認

| 検証 | 結果 |
|---|---|
| 単体テスト | 98件成功 |
| 設定・project lifecycle・timeline・Fusionの実機テスト | 6件成功（199.83秒） |
| Countdown画像回帰 | 4条件・384枚、16-bit RGB全sample完全一致（152.18秒） |
| Fusion色管理refreshを無効にした比較 | 384枚中196枚に差。従来のpage切替と0.5秒待機を維持 |
| project lifecycle stress | 20回成功。元のprojectとproject一覧の復元を確認 |
| Resolve終了・再起動・再接続 | 単独実行で1件成功（34.06秒）。元のprojectとEdit pageへ復元 |
| wheel／sdist build | uvの既存cacheを用いてofflineで成功 |
| wheel install | 独立Python 3.13環境でimport、21.1.2対応、152設定、297 Tool、OpenPBR入力補完、py.typedと48媒体assetを確認 |

画像マスターは変更していません。既存のpage切替・待機を含む通常経路で一致しています。
[refresh無効時の差分](verification/21.1.2.10/fusion-without-refresh.json)により、
21.1.2でもこの回避処理が必要であることを確認しました。
[20回の反復検証](verification/21.1.2.10/lifecycle-stress.json)では、全projectを削除した後に
元の保存済みprojectを開き直し、project一覧も実行前と一致することを確認しました。
[再起動の記録](verification/21.1.2.10/restart.json)でも21.1.2.10へ再接続し、元のprojectと
project一覧の復元を確認しました。通常回帰の生成PNG384枚は比較成功後に削除しました。
集約した結果と配布物のhashは[validation.json](verification/21.1.2.10/validation.json)に保存しています。
単体テストの一時領域には作業フォルダー内の一意な`.pytest-tmp/upgrade-2112-*`を使用しました。

## 再実行

ライブラリ直下のPython 3.13環境から実行します。Resolveを変更する処理は同時実行しません。
使い捨てprojectは各処理のfinallyで削除し、元の保存済みprojectへ戻します。

```powershell
.venv313/Scripts/python.exe -m pytest tests/unit -q
.venv313/Scripts/python.exe -m pytest tests/integration -m "not resolve_restart" -q
.venv313/Scripts/python.exe tests/integration/probe_frame_rate_constraints.py
.venv313/Scripts/python.exe tests/integration/probe_settings_persistence.py
.venv313/Scripts/python.exe tests/integration/probe_fusion_color_management.py
.venv313/Scripts/python.exe tests/stress/project_lifecycle_stress.py --iterations 20
.venv313/Scripts/python.exe -m pytest tests/integration/test_restart.py -q
```

画像比較は承認済み21.1.0用マスターを使用し、16-bit RGB全sampleの完全一致で判定します。
マスター、フォント、DCTLの置換は行いません。今回のfontとDCTLのhashは
[render-environment.json](verification/21.1.2.10/render-environment.json)に保存しています。
SDI／I/O機器出力、Free版、他OS、新規Photo／AI機能の実行は保証範囲外です。
