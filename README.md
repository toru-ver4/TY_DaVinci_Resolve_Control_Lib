# TY_DaVinci_Resolve_Control_Lib

DaVinci Resolve 21.0.4／21.1.0／21.1.2をWindowsから制御するPython 3.13（64-bit）向けライブラリです。

現在の実機検証はStudio 21.1.2.10です。[21.1.2検証記録](docs/resolve-21.1.2-verification.md)に公式API差分、21.1.0からの全設定比較、実機テストと画像比較をまとめています。21.0.4／21.1.0への接続は維持しますが、今回の変更後に旧版実機では再検証していません。過去のGUI/API対応と制限は[21.1.0検証記録](docs/resolve-21.1-verification.md)に版を区別して残しています。

```powershell
python -m pip install -e .
```

```python
import ty_davinci_resolve as tdr

session = tdr.ResolveSession.connect()
project = tdr.create_project(session, "Automation Test")
```

制作の自動化を始める場合は利用ガイドを、Resolve画面の設定を本ライブラリのPython定数へ置き換える場合はGUI対応表を参照してください。

- [ドキュメント一覧](docs/index.md)
- [利用ガイド](docs/guide.md)
- [Resolve GUIと本ライブラリ定数の対応](docs/project-settings.md)
- [Resolve API対応表（開発者向け）](docs/api-reference.md)
- [Resolve 21.1調査・検証記録](docs/resolve-21.1-verification.md)
- [Resolve 21.1.2調査・検証記録](docs/resolve-21.1.2-verification.md)
- [Resolveバージョン更新時の検証手順（開発者向け）](docs/resolve-version-upgrade.md)
- [移行・再設計計画（開発者向け）](docs/migration-plan.md)
