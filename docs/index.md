# ドキュメント

- [利用ガイド](guide.md): project作成、制作条件の設定、素材・Fusion・renderの自動化
- [Resolve GUIと本ライブラリ定数の対応](project-settings.md): Resolve画面の各項目をPythonから設定する方法と注意点
- [Resolve API対応表](api-reference.md): 開発者向けの実装根拠とResolve公式APIの対応
- [Resolve 21.1調査・検証記録](resolve-21.1-verification.md): 公式API差分、全snapshot、GUI証拠、保存時の制限、画像比較と未確認事項
- [Resolveバージョン更新時の検証手順](resolve-version-upgrade.md): 更新時のGUI/API再調査、証拠の残し方、テスト、完了条件
- [移行・再設計計画](migration-plan.md): 開発者向けの設計原則、対象範囲、実装状況

## 名前の読み方

各文書では、名前の直前に次のタグを付けて所属を区別します。

- **［Resolve GUI］**: ［Resolve GUI］「Timeline frame rate」のように、DaVinci Resolveの画面に表示される名前を表す。
- **［Resolve API］**: ［Resolve API］`Project.SetSetting()`のように、Resolve公式Scripting APIのクラス、メソッド、設定キーを表す。
- **［TY API］**: ［TY API］`ProjectSetting`、［TY API］`set_project_settings()`のように、本ライブラリ`ty_davinci_resolve`が提供するクラス、定数、関数を表す。

バッククォートはPythonの識別子、ダブルクォートは`"timelineFrameRate"`のような実際の文字列を表すために使用し、APIの所属を区別する目的では使用しません。コードブロック内では実行可能なコードを優先し、タグは説明文や表に付けます。
