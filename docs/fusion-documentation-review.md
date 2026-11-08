# Fusion公式資料の精査と修正

2026-11-08、Resolve Studio 21.2.0.5／Windows／Python 3.13.16で確認しました。
[FusionTools.md](../official_documents/21.2.0_Fusion/FusionTools.md)と
[FusionToolReference.md](../official_documents/21.2.0_Fusion/FusionToolReference.md)は、どちらも本文の更新日が4 Oct 2026です。
両ファイルはインストール先`Developer/Fusion/`とbyte単位で一致しました。
[照合結果・SHA-256・入力比較](verification/21.2.0.5/fusion-documentation-audit.json)を保存しています。
旧版Fusion資料を保存していなかったため、以下の発見を21.2.0で初めて導入された動作とは断定しません。

## 調査範囲

Overviewの分類とReference全418 Tool節のIDを調査し、現行の公開Enum、生成済み入力属性、
Fusionラッパーの呼び出し、Conventions／Common Controls、使用中Toolの記述を照合しました。
全Toolの全機能や公式例を実行した検証ではありません。Lua例、モデル導入、外部packageの取得は実行していません。

native ToolとModifierの公開IDは重複を除いて307個、そのうち304個にReferenceの完全一致見出しがあります。
残る`Path`は実機で確認済みの互換ID、`PerturbNumber`／`PerturbPoint`は`Perturb*`節の型別memberです。
文書側の未収録114見出しにはKrokodove、追加Modifier、`Publish*`／`Switch*`等のfamilyを含みます。
公開Enumは実機Registryで確認した範囲を維持し、文書のfamily名をAddTool IDとして追加しません。
Resolve FXの別APIと混同しません。

明示的なID列を持つControl表も生成済みのTool属性と照合しました。101 Tool節で属性名としての差が
ありましたが、すべてドット付きID、番号付きtemplate、予約済みメソッド名に分類できました。
例えば`Transform3DOp.Translate.X`は`tool['Transform3DOp.Translate.X']`で指定します。
`ElementShape`*n*や`DynParamNum`*n*は文書の表記どおりでは固定入力名ではありません。
Trackerの`Delete`ボタンは`tool.Delete()`メソッドと衝突するため属性として生成せず、必要ならitem構文を使います。
Common Controlsや状態によって現れる入力は、Tool初期状態のdumpだけで網羅したと扱いません。

## 修正した点

| 対象 | 発見と修正 |
|---|---|
| `connect_default_output()` | `target.Input.ConnectTo(source.Output)`は端子名を固定していた。RectangleMaskの出力は`Mask`で、旧処理が実機で失敗することを再現。`FindMainOutput(1)`／`FindMainInput(1)`で既定端子を取得して接続する。端子がなければ接続操作の前に例外で停止する |
| `set_fusion_tool_input()`のPoint | `[x, y]`と`{1: x, 2: y}`は正常に設定できても読戻しが`{1: x, 2: y, 3: 0.0}`になり、旧コードが誤ってエラーにしていた。数値Pointの形式を正規化し、各軸を指定toleranceで検証する。座標の不一致は引き続きエラー |
| remote値の検証 | 旧コードはremote objectを渡すと無条件に検証を省略していた。入力IDの存在を設定前に確認し、設定後は値または接続先outputの存在を確認する。未評価のImage／Maskでは`GetInput()`がNoneでも接続自体は正常なので、値がNoneという理由だけでは失敗にしない |
| 共通Protocolと生成器 | `GetInput`とframe引数、`GetOutputList`、`FindMainInput`／`FindMainOutput`、item構文、Inputの属性・接続照会を型定義へ追加。`SetInput`の戻り値はboolと断定しない。既存Tool別入力属性は維持する |

端子の型が適合しない場合の失敗や、値の設定拒否は例外で停止します。自動fallbackは追加していません。
remote値の厳密な同一性、FuID／fontの意味的な正当性、最終画像の成功をsetterだけで保証するものではありません。

## 今回変更しなかった点と制作時の注意

- **AddToolと自動接続**：公式Conventionsは、表示中compでは自動接続・自動Mergeが起き、座標指定時には抑止flagが無視されることがあると説明しています。一方、今回の使い捨てTimelineの表示中compでは、選択Toolと座標を指定しても再現しませんでした。作成ラッパーへの選択解除や全API形式の変更は採用していません。更新時は非表示compだけでなく、表示中comp・選択状態・ユーザー設定を分けて再確認します。
- **保存済みTool default**：`AddTool`はユーザーの保存済みdefaultを使い、`comp.ID()`は組込みdefaultを使うとの記載があります。既存作品の見た目への影響を避けるため作成形式を一括置換せず、制作に必要な入力を明示します。
- **値の型とrender**：Number comboはindex、FuID comboは文字列です。無効なFuIDやfontは読戻しが一致してもrenderに失敗することがあります。sliderのsoft rangeをhard limitと同一視しません。一般setterへ全Tool固有の値検査や毎回のrenderを組み込む変更は行いません。
- **animation**：PointはPolyPath／XYPath、NumberはBezierSplineなどのModifierを接続してからframeを指定します。初期keyframe、既存expression、既存animationを通常の値代入で消せると仮定しません。専用animationラッパーの追加は今回の範囲外です。
- **特殊値**：Gradient／BSplinePolyline等は専用constructorを使い、Polylineとは区別します。汎用のdict比較を全データ型へ拡張していません。
- **Loader／settings**：LoaderはAuto Clip Browseによるmodalを避けるためlocked compで扱います。外部PythonのSaveSettingsはmodule-level OrderedDictが必要との注意がありますが、現行ラッパーはSaveSettings／Pasteを使用していないため新しいimportや回避処理は追加していません。

## 検証

ライブラリ直下の既存Python 3.13環境で実行します。実機処理は同時実行しません。

```powershell
.venv313/Scripts/python.exe tests/integration/probe_fusion_documentation.py
.venv313/Scripts/python.exe -m pytest tests/unit -q
.venv313/Scripts/python.exe -m pytest tests/integration/test_fusion_document_conventions.py tests/integration/test_p1_resolve_workflow.py tests/integration/test_p2_resolve_workflow.py -q
.venv313/Scripts/python.exe -m pytest tests/integration/test_countdown_regression.py -q
```

単体テスト109件、対象の実機テスト3件が成功しました。
Countdown画像回帰も4条件・384枚の16-bit RGB全sampleが既存マスターと完全一致しました（164.34秒）。
マスター、font、DCTLは変更していません。
画像比較後の一時PNG384枚は削除しました。wheel／sdistのoffline buildも成功し、
[検証結果・配布物hash](verification/21.2.0.5/fusion-documentation-validation.json)を保存しています。
[実機証拠](verification/21.2.0.5/fusion-document-conventions.json)にはMask出力の接続、
Pointの各形式のreadback、remote接続、存在しない入力の拒否、非表示compの閉鎖を記録しています。
通常環境からの接続失敗後はAGENTS.mdの許可に従って制限外で確認しました。旧対応版の実機再検証は行っていません。
