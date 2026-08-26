# Resolveバージョン更新時の検証手順

この文書は、本ライブラリの対応対象を新しいDaVinci Resolveへ更新するときに使う開発者向けチェックリストです。GUI名とAPIキー名が似ているという理由だけで対応付けず、作品制作の自動化に使えることを実機で確認してから公開します。

現在の基準環境はWindows版DaVinci Resolve Studio 21.0.4.5／Python 3.12です。この環境での利用方法は[GUIと定数の対応](project-settings.md)、実装根拠は[API対応表](api-reference.md)を参照してください。

## 最初に残す情報

更新作業を始める前に、次を検証記録へ残します。

- Resolveの完全なバージョン、Free／Studio、OS
- Pythonのバージョン
- 使用した公式Scripting README／CHANGELOGの版
- 検証日時
- GPU、I/O機器、codecなど、結果に影響した可能性がある環境情報
- 更新前後の［Resolve API］`Project.GetSetting()`の全snapshot

検証にはPythonだけを使用します。Luaを使わざるを得ない場合は、実行前にユーザーの許可を得ます。既存作品は使用せず、固有名を付けた使い捨てprojectを作成し、成功・失敗にかかわらず最後に削除します。

## 対応関係を採用する条件

GUI項目とAPI設定キーは、名前や値が似ているだけでは対応済みと判定しません。対応表へ確認済みとして掲載できるのは、次のいずれかを満たす場合だけです。

1. Resolve公式資料に対応関係が明記されている。
2. GUIで調査対象の1項目だけを変更し、変更前後の全snapshotから対応キーの変化を確認した。
3. Pythonで値を設定し、APIの再取得値、GUI表示、projectを開き直した後の保持状態まで確認した。

結果は次の4種類に分類します。

| 状態 | 意味 | 文書での扱い |
|---|---|---|
| `verified_bidirectional` | Pythonから変更でき、API再取得値とGUI表示の両方が一致する | 自動設定可能として掲載する |
| `verified_gui_to_api` | GUI変更に連動するAPIキーを確認したが、Pythonからの変更は未確認 | 書き込み未確認と明記する |
| `query_only` | APIから現在値は取得できるが、Pythonから変更できない | 読み取り専用として掲載する |
| `unmapped` | GUIに項目があるが、対応するAPIキーを特定できない | 既存定数へ割り当てず、GUI操作が必要と案内する |

推測段階の値は［TY API］の公開Enumへ追加しません。`SetSetting()`が`True`を返すだけでも採用せず、少なくとも待機後のreadback一致を必要とします。

## 更新作業の順序

### 1. 公式APIの差分を調べる

1. `official_documents/<version>_Scripting/`へ新しい公式文書を追加し、旧版を残す。
2. 新旧のScripting READMEとCHANGELOGを比較する。
3. 追加、変更、deprecated、unsupportedになったAPIを記録する。
4. ［TY API］ラッパー、定数、対応バージョン検査への影響を整理する。

### 2. 設定キーの全体像を比較する

空の使い捨てprojectで［Resolve API］`Project.GetSetting()`を引数なしで実行し、全設定を保存します。前バージョンのsnapshotと比較し、追加・削除・初期値変更を分類します。

基準環境では158個のキーを取得し、そのうち151個を［TY API］`ProjectSetting`へ収録しました。残る7個は読み取れても同値の書き戻しが拒否されたため未収録です。151は収録数であり、全項目があらゆる状態で書き込めるという意味ではありません。読み取り専用やGUIとの対応を特定できていないキーは、個別に区別します。新バージョンでは、この個数を正解として固定せず、改めて取得結果から判断します。

### 3. GUIの状態を切り替えて観察する

ResolveのGUIは親設定によって表示項目や選択肢が変わります。初期画面だけを調べず、少なくともColor Managementでは次の状態を個別に確認します。

- DaVinci YRGB
- DaVinci YRGB Color Managed＋Automatic color managementオン
- DaVinci YRGB Color Managed＋Automatic color managementオフ
- Automatic color managementオフ＋既定プリセット
- Automatic color managementオフ＋Custom
- ACEScc
- ACEScct

各状態について、GUIのpage／section／label、表示条件、選択肢、APIキー、［TY API］定数、根拠を記録します。全状態の総当たりが過大になる場合は、まず表示を変える親設定ごとに状態を分け、その中で各項目を一つずつ変更します。

### 4. GUIからAPIへの対応を検証する

GUI項目ごとに次を行います。

1. `Project.GetSetting()`の全項目を変更前snapshotとして保存する。
2. GUIでは調査対象の項目だけを変更して保存する。
3. 全項目を変更後snapshotとして保存する。
4. キー集合と値を機械的に比較する。
5. 想定したキーだけが変わったか確認する。

予想したキーだけを読んではいけません。全snapshotに差分がなければ、名前の似た既存キーを割り当てず`unmapped`とします。

実例として、Resolve 21.0.4.5の［Resolve GUI］`Limit output gamut to`を`P3-D65`から`Output color space`へ変更しても、158個の設定値に差分はありませんでした。名前が似た［Resolve API］設定キー`"colorSpaceOutputGamutMapping"`も`"None"`のままだったため、［TY API］`ProjectSetting.OUTPUT_GAMUT_MAPPING`をこのGUI項目へ対応付けてはいけません。

### 5. PythonからGUIへの対応を検証する

候補値ごとに次を確認します。

1. `SetSetting()`の戻り値が`True`である。
2. Resolveの処理待ちを入れる。
3. `GetSetting()`のreadbackが設定値と一致する。数値の正規化がある場合は個別に許容する。
4. GUI表示が意図した項目だけ変わっている。
5. projectを保存して開き直しても保持される。

設定順やprojectの状態にも注意します。フレームレートのようにproject作成直後または空timelineでのみ変更できる値は、その前提条件もテストと利用者向け文書に残します。

### 6. 定数・台帳・文書を更新する

- 安定して書き込みとreadbackができた値だけを`src/ty_davinci_resolve/constants.py`へ追加する。
- GUI確認状況を[`project-setting-gui-coverage.json`](project-setting-gui-coverage.json)へ反映する。
- 制作者の判断に必要な情報を[GUIと定数の対応](project-settings.md)へ反映する。
- 実装上の根拠や制約を[API対応表](api-reference.md)へ反映する。
- READMEと[ドキュメント一覧](index.md)から新しい資料へ到達できることを確認する。

現在のGUI確認台帳は「本文に掲載済み」と「継続調査中」の2分類です。将来、台帳を上記4状態へ拡張する場合は、各記録にResolve版、GUI表示条件、検証方法、証拠ファイルを持たせ、既存項目を根拠なく一括変換しません。

## 実行するテスト

最初に単体テスト、その後にResolve実機テストを実行します。各テストはリポジトリのrootで実行します。

```powershell
python -m pytest tests/unit
python -m pytest -m resolve_integration tests/integration/test_setting_constants.py -q
python -m pytest -m resolve_integration tests/integration/test_timeline_frame_rate_settings.py -q
```

詳細な候補値の調査には、正式テストとは分けて次のPython probeを使用します。

```powershell
python tests/integration/probe_project_setting_values.py
python tests/integration/probe_timeline_playback_frame_rate.py
```

設定関連の変更後は、project lifecycle、MediaPool、timeline、Fusion、renderの実機テストも実行します。出力画へ影響する変更ではCountdown画像回帰を実行します。再起動テストはほかの実機テストの最後に単独で行います。具体的な全体計画は[移行・再設計計画](migration-plan.md#8-テスト計画)を参照してください。

## 自動テストで守ること

少なくとも次を機械的に検査します。

- ［TY API］`ProjectSetting`の全定数がGUI確認台帳のいずれかに分類されている。
- 「GUI対応を本文に掲載済み」の定数が本文に存在する。
- 対応表に書かれた定数が`constants.py`に存在する。
- 将来4状態へ移行した後は、`unmapped`のGUI項目にTY定数が割り当てられていない。
- 将来4状態へ移行した後は、`verified_*`の記録に検証環境と証拠がある。
- 同じGUI項目へ複数のAPIキーが根拠なく割り当てられていない。
- Markdownのローカルリンクが切れていない。

対応表を将来構造化データから自動生成する場合は、Markdownを直接編集せず、台帳を唯一の情報源にします。生成後の差分が残っていればテストを失敗させます。

## 21.0.4.5から引き継ぐ重点確認項目

次は、これまでの調査で単純な名前対応が成立しなかった項目です。Resolve更新時には、以前の結論をそのまま流用せず、特に優先して再検証します。

| 対象 | 21.0.4.5での確認結果 | 更新時の確認点 |
|---|---|---|
| ProjectのTimeline frame rate | project作成直後ならPythonから設定可能 | 素材やtimeline作成後の制限も再確認する |
| ProjectのPlayback frame rate | APIで取得できるが、Pythonからの変更は拒否された | `query_only`のままか確認する |
| 個別timelineのTimeline frame rate | 空timelineでcustom settingsを有効にすると設定可能 | 設定順と再生結果を確認する |
| 個別timelineのPlayback frame rate | GUIに独立項目がなく、APIからの変更も拒否された | 新GUIまたは新APIが追加されていないか確認する |
| Automatic color management | オン／オフで表示項目と設定の意味が変わる | 両状態を別々に観察する |
| RCM preset mode | Automatic color managementオフ時のプリセット／Customを確認する必要がある | 全プリセットとCustom時の追加項目を確認する |
| Input／Timeline／Output color space | Outputだけは選択可能な値の集合が異なる | GUI選択肢と`OUTPUT_COLOR_SPACES`を再比較する |
| Limit output gamut to | 全158-key snapshotに変化がなく、対応APIキー不明 | `unmapped`のままか全snapshotで確認する |

現在の正式な実機テストは`tests/integration/test_setting_constants.py`と`tests/integration/test_timeline_frame_rate_settings.py`、候補値調査は`tests/integration/probe_project_setting_values.py`、フレームレートの詳細調査は`tests/integration/probe_timeline_playback_frame_rate.py`に分けています。GUI掲載漏れは`tests/unit/test_project_setting_gui_coverage.py`で検査します。

## 完了条件

- 新旧公式APIの差分が記録されている。
- 全設定snapshotの追加・削除・初期値変更が分類されている。
- GUI対応が、名前の類似ではなく変更前後の証拠に基づいている。
- 公開定数はPythonからの書き込みとreadbackを確認済みである。
- query-only／unmapped／環境依存の項目が、設定可能な項目と区別されている。
- 単体テスト、対象となる実機テスト、必要な画像回帰が成功している。
- 使い捨てprojectと調査用成果物が残っていない。
- 対応バージョン、利用者向け文書、開発者向け根拠、READMEの導線が更新されている。
