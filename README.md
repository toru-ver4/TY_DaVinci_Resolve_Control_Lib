# TY_DaVinci_Resolve_Control_Lib

DaVinci Resolve 21.0.4をPythonから制御するためのライブラリです。

現在は再設計中のpre-alpha版です。Windows、Python 3.12 64-bitのみを動作保証対象とします。

## インストール

開発時はリポジトリ直下でeditable installします。

```powershell
python -m pip install -e .
```

テスト用依存関係も導入する場合は次のようにします。

```powershell
python -m pip install -e ".[test]"
```

Countdown回帰テスト用のNumPyと16-bit PNG decoderも導入する場合は次のようにします。

```powershell
python -m pip install -e ".[test,countdown]"
```

Gitリポジトリから直接インストールすることもできます。

```powershell
python -m pip install "git+https://github.com/toru-ver4/TY_DaVinci_Resolve_Control_Lib.git"
```

## 接続

パッケージをimportしただけではDaVinci Resolveへ接続しません。Resolveを起動してから明示的に接続します。

```python
from ty_davinci_resolve import ResolveSession

session = ResolveSession.connect()
print(session.product_name)
print(session.version_string)
```

標準では接続先がResolve 21.0.4であることを検査します。未起動、APIのロード失敗、バージョン不一致は例外になります。

## 基本操作

プロジェクトの作成と設定は、明示的なsessionを渡して行います。公式APIが失敗値を返した場合は例外になります。

```python
from ty_davinci_resolve import ResolveSession, create_project, set_settings

session = ResolveSession.connect()
project = create_project(session, "Automation Test")
set_settings(
    project,
    {
        "timelineResolutionWidth": "1280",
        "timelineResolutionHeight": "720",
        "timelineFrameRate": "23.976",
    },
)
```

メディアは、import先のMedia Poolを明示して追加します。

```python
from pathlib import Path

from ty_davinci_resolve import get_media_pool, import_files

media_pool = get_media_pool(project)
clips = import_files(media_pool, [Path(r"C:\media\clip.mov")])
```

## P1便利関数

固定長のFusion Compositionは、呼出側が解像度・fpsに合うdummy mediaを明示して追加します。長さを省略した場合はResolve 21.0.4公式のnative挿入を使用します。

```python
from pathlib import Path

from ty_davinci_resolve import (
    append_fusion_composition,
    get_current_timeline,
    get_media_pool,
)

timeline = get_current_timeline(project)
item, comp = append_fusion_composition(
    timeline,
    duration_frames=24,
    record_frame=86400,
    media_pool=get_media_pool(project),
    dummy_media=Path(r"C:\media\dummy_video_1280x720_24P.mp4"),
)
```

そのほか、page/playhead/timeline設定、Media Storage range import、generator挿入、render一括実行、render preset、DCTL・font検証・Fusion builderをトップレベルAPIから利用できます。render一括実行は、この呼出しが作成したjob IDだけを操作します。

```python
from ty_davinci_resolve import Page, open_page, render_current_settings

open_page(session, Page.EDIT)
status = render_current_settings(
    project,
    delete_completed_job=True,
)
```

render formatとcodecは現在のResolveから取得した一覧で検証します。例えばProRes 4444 XQは次のように指定します。

```python
from ty_davinci_resolve import (
    RenderFormat,
    VideoCodec,
    add_render_job,
    delete_render_job,
    set_render_format_codec,
    set_render_settings,
    start_render_job,
    wait_for_render_job,
)

set_render_format_codec(
    project,
    RenderFormat.QUICKTIME,
    VideoCodec.PRORES_4444_XQ,
)
set_render_settings(
    project,
    {"TargetDir": r"C:\output", "CustomName": "master"},
)
job_id = add_render_job(project)
start_render_job(project, job_id)
wait_for_render_job(project, job_id)
delete_render_job(project, job_id)
```

利用可能な値は`get_render_formats()`、`get_render_codecs()`、`get_render_resolutions()`で照会できます。Resolve 21.0.4公式APIの対応箇所は[README.txt](official_documents/21.0.4_Scripting/README.txt)のProject API一覧を参照してください。

## テスト

単体テストはResolveを起動せずに実行できます。

```powershell
python -m pytest tests/unit
```

Resolve 21.0.4を使用する短い実機テストは次のコマンドで分離して実行します。

```powershell
python -m pytest -m resolve_integration tests/integration/test_project_lifecycle.py
python -m pytest -m resolve_integration tests/integration/test_native_fusion_composition.py
python -m pytest -m resolve_integration tests/integration/test_p1_resolve_workflow.py
```

Resolveを終了・再起動するテストは、他の実機テストが動いていない状態で単独実行します。

```powershell
python -m pytest -m resolve_restart tests/integration/test_restart.py -s
```

Countdown V2の4条件・384枚をrenderし、参照ZIPとdecode後の16-bit RGB全sampleを完全一致比較する場合は次のように実行します。

```powershell
python -m pytest -m countdown_regression tests/integration/test_countdown_regression.py -s
```

派生スクリプトを直接実行する場合は、出力先を必ず指定します。

```powershell
python tests/countdown_regression/create_countdown_v2.py `
  --output-dir "F:\abuse\Countdown\temp_seq"
```

派生版は`2025/02_Countdown_V2/create_countdown_v2.py`を変更せず、テスト専用adapterから新パッケージを利用します。`ty_lib/transfer_functions.py`はimportせず、必要なST 2084 inverse EOTFだけをNumPyで実装しています。

詳細な移行・実装方針は[MIGRATION_PLAN.md](MIGRATION_PLAN.md)、実装とResolve 21.0.4公式APIの対応は[API_REFERENCE.md](API_REFERENCE.md)を参照してください。

## 備考

本リポジトリは個人開発の成果公開を目的としており、
Pull Request は受け付けていません。クローズします。
