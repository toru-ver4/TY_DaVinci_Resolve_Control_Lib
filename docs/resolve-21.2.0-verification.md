# Resolve 21.2.0調査・検証記録

2026-11-08、Windows／Python 3.13.16（64-bit）／DaVinci Resolve Studio 21.2.0.5で検証しました。通常環境からの接続が失敗したため、AGENTS.mdの許可に従って制限外で実機検証しました。

## 公式APIの差分

同梱の[README](../official_documents/21.2.0_Scripting/README.md)、[CHANGELOG](../official_documents/21.2.0_Scripting/CHANGELOG.md)（4 Nov 2026）、[型定義](../official_documents/21.2.0_Scripting/DaVinciResolveScript.pyi)、接続モジュールをインストール先とbyte単位で照合しました。[環境・SHA-256](verification/21.2.0.5/environment.json)を保存しています。

[21.1.2とのAST差分](verification/21.2.0.5/api-diff.json)は13 class、メソッド18件追加、既存メソッドのシグネチャ変更・型定義からの削除はありません。新しい型にはサムネイル出力設定・結果とExtrasのpackage情報があります。READMEのDeprecated／Unsupported節には変更ありません。

| 対象 | 変更と本ライブラリへの影響 |
|---|---|
| Project設定 | Playback frame rateの書き込みに対応。Timeline frame rate変更はPlaybackも更新。既存setterで利用可能 |
| Extras | GetExtrasPackages／InstallExtrasPackage／UninstallExtrasPackage追加。モデル等の自動導入は行わない |
| サムネイル | Timeline／TimelineItem／MediaPoolItem／PhotoAlbumにExportThumbnails追加 |
| frame export | ROI・JPEG品質指定、結果の寸法field追加 |
| 色補正・grade参照 | TimelineItem／PhotoAlbumItemにAuto Color操作とGetCDL、GraphにGetNodeEnabled追加 |

新規APIの専用ラッパーと実行保証は今回追加していません。対応版を21.0.4／21.1.0／21.1.2／21.2.0に明示列挙し、他のpatchは自動許可しません。旧版実機での再検証は行っていません。

## 設定と保存後保持

[空projectの全設定](verification/21.2.0.5/project-default-settings.json)は159個です。[21.1.2との差分](verification/21.2.0.5/setting-comparison.json)では追加・削除・初期値変更はありません。GetSettingsと旧GetSettingの全件は一致し、公開ProjectSettingは152個を維持します。初期値はこの環境での観測です。

[Playback frame rateの全snapshot](verification/21.2.0.5/playback-frame-rate.json)では、SetSetting／SetSettingsそれぞれでTimelineを24、Playbackだけを25、Timelineを30へ変更しました。各段階でreadbackと保存・再読込後保持を確認しています。Timeline変更時はPlaybackも24／30へ更新されました。異なるPlayback値はTimeline設定の後に指定してください。公式CHANGELOGにGUIとの連動が明記されていますが、今回GUIの全項目を再観測したという意味ではありません。旧GUI台帳は変更していません。

[ImportMedia](verification/21.2.0.5/import-conventions.json)はFilePath辞書が0件、旧pathリストが1件で、制作側の呼び出し形式を維持します。[拡張言語モデル設定](verification/21.2.0.5/transcription-extended-language.json)は無効値の設定・保存保持が成功し、有効化は拒否され全設定に変化がありません。モデルの追加取得は行っていません。

[フレームレート制約](verification/21.2.0.5/frame-rate-constraints.json)は従来どおりで、空custom timelineの整数24／25／30／50／60は成功、小数23.976／29.97／59.94とclip追加後の変更は拒否されました。全timelineがcustomという条件ではproject frame rateを素材追加後にも変更できました。OutputのSame as Timelineは成功、Inputは拒否です。[設定保存](verification/21.2.0.5/settings-persistence-conventions.json)では、両setter形式ともプリセット名のみの変更が再読込でCustomへ戻り、Automaticオンもオフへ戻りました。制作条件はCustomで関連設定を明示してください。

[Fusion registry](verification/21.2.0.5/fusion-registry-comparison.json)はTool 297／Modifier 11／Resolve FX 83で増減・ID変更はありません。[入力型生成](verification/21.2.0.5/fusion-typing-summary.json)では全391登録の作成が成功しました。[入力差分](verification/21.2.0.5/fusion-input-diff.json)はOGrafLoaderの動的入力120件追加、削除なしです。`fusion_tool_types.pyi`へ反映しました。入力補完は21.2.0での観測であり、旧版の同じ入力を保証しません。

## 自動検証と配布

単体テスト99件、再起動以外の実機テスト7件（314.09秒）が成功しました。実機テストにはCountdownの4条件・384枚の16-bit RGB全sample完全一致を含みます。Fusion色管理のpage切替・待機は維持しています。

project作成・保存・再読込・削除の反復検証は20回成功しました（153.88秒）。Resolve終了・再起動・再接続の単独テストも1件成功しました（24.23秒）。画像比較後の生成PNG384枚は削除しました。起動時は未保存のUntitled Projectで、保存済み作品の復元対象はありませんでした。[最終project監査](verification/21.2.0.5/final-project-audit.json)に、今回の作成物と確認できない既存の調査用projectを残したことを記録しています。

wheel／sdistのoffline buildが成功しました。独立Python 3.13環境へ最終wheelをインストールし、import、21.2.0許可、OGraf追加入力、py.typed、48媒体assetを確認しました。[GPU環境](verification/21.2.0.5/gpu.json)と[最終配布物のSHA-256](verification/21.2.0.5/distribution.json)も保存しています。

## 再実行

ライブラリ直下の既存Python 3.13環境から実行します。Resolve操作は同時実行しません。probeと実機テストは固有名の使い捨てprojectを作成し、finallyで削除します。

```powershell
.venv313/Scripts/python.exe tests/integration/probe_resolve_21_2_0.py api
.venv313/Scripts/python.exe tests/integration/probe_resolve_21_2_0.py live
.venv313/Scripts/python.exe -m pytest tests/unit -q
.venv313/Scripts/python.exe -m pytest tests/integration -m "not resolve_restart" -q
.venv313/Scripts/python.exe -m pytest tests/integration/test_restart.py -q
```

画像マスターは承認済み21.1.0用を使用し、16-bit RGB全sampleの完全一致で判定します。マスター、フォント、DCTLは置換しません。Free版・他OS・I/O機器・新規AI機能は実機検証の範囲外です。
