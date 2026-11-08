# TY_DaVinci_Resolve_Control_Lib

DaVinci Resolve 21.0.4／21.1.0／21.1.2／21.2.0をWindowsから制御するPython 3.13（64-bit）向けライブラリです。

現在の実機検証はStudio 21.2.0.5です。[21.2.0検証記録](docs/resolve-21.2.0-verification.md)に公式API差分、全設定比較、Playback frame rateの変更と実機テストをまとめています。旧対応版への接続を維持します。旧版実機は今回再検証していません。

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
- [Fusion公式資料の精査と修正](docs/fusion-documentation-review.md)
- [Resolve 21.1調査・検証記録](docs/resolve-21.1-verification.md)
- [Resolve 21.1.2調査・検証記録](docs/resolve-21.1.2-verification.md)
- [Resolveバージョン更新時の検証手順（開発者向け）](docs/resolve-version-upgrade.md)
- [移行・再設計計画（開発者向け）](docs/migration-plan.md)
