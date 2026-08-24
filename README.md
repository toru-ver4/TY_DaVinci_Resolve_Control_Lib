# TY_DaVinci_Resolve_Control_Lib

DaVinci Resolve 21.0.4をWindowsから制御するPython 3.12向けライブラリです。

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
- [Resolve 21.0.4 API対応表（開発者向け）](docs/api-reference.md)
- [移行・再設計計画（開発者向け）](docs/migration-plan.md)
