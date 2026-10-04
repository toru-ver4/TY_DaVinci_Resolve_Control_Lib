# TY_DaVinci_Resolve_Control_Lib

DaVinci Resolve 21.0.4／21.1.0をWindowsから制御するPython 3.13（64-bit）向けライブラリです。

現在の実機検証はStudio 21.1.0.17です。21.0.4への接続は維持しますが、今回の変更をPython 3.13＋21.0.4実機では再検証していません。[21.1検証記録](docs/resolve-21.1-verification.md)に公式API差分、GUI/API対応、保存時の制限、画像比較をまとめています。旧版のraw全設定snapshotがないため、新旧の設定キー・初期値比較は未確認です。

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
- [Resolveバージョン更新時の検証手順（開発者向け）](docs/resolve-version-upgrade.md)
- [移行・再設計計画（開発者向け）](docs/migration-plan.md)
