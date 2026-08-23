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

Projectの作成・保存・終了・読込・削除では、Resolve内部の非同期処理を待ってから次のAPIへ進みます。待機時間を調整する場合は`ProjectLifecycleTiming`を各project lifecycle関数の`timing=`へ指定してください。

## Project・render定数

旧`ty_davinci_constants.py`の固定値は、用途別の`StrEnum`／`IntEnum`とimmutableなpresetへ移植しました。旧名のaliasは提供しません。

```python
from ty_davinci_resolve import (
    BT2100_PROJECT_SETTINGS,
    ColorSpace,
    Gamma,
    ProjectSetting,
    set_settings,
)

assert ColorSpace.P3_D65 == "P3-D65"
assert Gamma.ST2084 == "ST2084"
set_settings(project, BT2100_PROJECT_SETTINGS, settle_delay=0.35)
```

Resolve Studio 21.0.4.5 の Project Settings > Color Management で、Color
processing mode が Custom になる条件
（`colorScienceMode=davinciYRGBColorManagedv2`、`rcmPresetMode=Custom`、
`separateColorSpaceAndGamma=1`）を実機確認しました。Custom の各一覧は次の
定数で網羅しています。

- `ColorSpace`: Input／Timeline の43件。`OUTPUT_COLOR_SPACES`: Output の39件
  （`HSL`、`HSV`、`Lab (CIE)`、`Y'UV`を除外）。
- `Gamma`: Input／Timeline／Output に共通する63件。
- `WorkingLuminanceMode`: Timeline working luminance の11件。`Custom`時の
  `timelineWorkingLuminance` は48–10,000 nitで設定可能。

UIとAPIで表記が異なる値はAPI表記を定数値にしています（例：UIの`P3 DCI`／
`SMPTE C`／`YUV`に対して`P3-DCI`／`SMPTE-C`／`Y'UV`）。Input の
`Same as Timeline`はUI一覧用の`InputColorSpaceMode`に収録していますが、
`SetSetting()`では拒否されるため設定可能値としては保証しません。

値の根拠は次のように区別しています。

- Resolve 21.0.4公式Scripting README由来：`SuperScale`、`UniqueFilenameStyle`、`PixelAspectRatio`、`AlphaMode`、`SubtitleFormat`など。
- Windows版Resolve Studio 21.0.4.5実機の`SetSetting()`／`GetSetting()` readback由来：`ColorSpace`、`Gamma`、`ColorSpaceGamma`、`WorkingLuminanceMode`、`AcesOutputTransform`など。各呼出し間に0.35秒置いた使い捨てprojectで確認しています。

ACES ODTは現行実機値に合わせ、旧`nits`を`nit`へ、`Rec.2020 ST2084`を`Rec.2100 ST2084`へ変更しました。`FrameRate`はProject Settings UIの19値（16–120 fps）と公式仕様の`29.97 DF`／`59.94 DF`を合わせた21件です。`PlaybackFrameRate`はUIの19値を収録しますが、`timelinePlaybackFrameRate`キー自体はread-onlyで、`"24"`と旧値`"24.0"`の双方が拒否されたため`BT2100_PROJECT_SETTINGS`から除外しています。

Project Settingsの158-key snapshotを既存36キーと照合し、未収録122キーのうち使い捨てprojectで現在値の再設定とreadback一致を確認した115キーを追加しました。拒否された7キーは除外し、`ProjectSetting`は計151キーです。`ResolutionValue`はProject／Deliver UIのpresetに現れる28寸法、`RenderFormat`は`GetRenderFormats()`が返した23識別子、`VideoCodec`はformat別に返った196識別子と旧3識別子を収録します。codecの利用可否はOS、edition、hardware、formatで変わるため、使用前に`get_render_codecs()`で現在のResolveを照会してください。`VideoQuality`の固定名称はUI／公式仕様とも`Least`、`Low`、`Medium`、`High`、`Best`の5件で、Automaticは`VIDEO_QUALITY_AUTOMATIC = 0`です。

旧video monitor format 40定数は、解像度とfpsから同じ文字列を生成する`make_video_monitor_format()`へ統合しました。

## 参考：Resolve APIの非同期完了と安定化workaround

DaVinci Resolve 21.0.4.5の実機検証中、`ProjectManager` APIが成功を返した直後に次のAPIを呼ぶと、Resolveが異常終了するケースを確認しました。Resolveのログではprojectのload処理終了からcurrent projectの切替までさらに約0.27秒かかっており、その間に`LoadProject()`が返したremote objectの`GetName()`を呼んだ試行で異常終了しました。この結果から、本ライブラリではAPIの成功値を内部処理の完了とは見なしません。なお、これはResolveの公式仕様ではなく、Windows上のResolve Studio 21.0.4.5で得た実機観測に基づくworkaroundです。

Project lifecycle関数は、API成功後に次の処理を行います。

| 操作 | 最初の静穏時間 | 完了確認 |
|---|---:|---|
| `create_project()` | 0.75秒 | 指定projectがcurrentになるまで確認 |
| `save_project()` | 0.75秒 | 確認用APIがないため固定待機 |
| `close_project()` | 0.75秒 | 対象projectがcurrentでなくなるまで確認 |
| `load_project()` | 1.5秒 | 指定projectがcurrentになるまで確認 |
| `delete_project()` | 0.75秒 | project一覧から消えるまで確認 |

状態確認は0.25秒間隔、timeoutは15秒です。特に`load_project()`では、`LoadProject()`が直接返したremote objectへすぐには触れず、静穏時間後に`GetCurrentProject()`から取得した安定状態のobjectを返します。これにより、待機中のResolveへ高頻度のpollingを行うことも避けています。

環境に応じて待機時間を延長する場合は、次のように指定できます。

```python
from ty_davinci_resolve import ProjectLifecycleTiming, load_project

timing = ProjectLifecycleTiming(
    load_delay=2.0,
    timeout=20.0,
    poll_interval=0.5,
)
project = load_project(session, "Automation Test", timing=timing)
```

再現確認とworkaround検証用に、projectの作成→設定→保存→終了→再読込→終了→削除を反復する負荷試験を用意しています。各反復を別Python processで実行し、1反復が45秒を超えた場合も応答停止として検出します。

```powershell
python tests/stress/project_lifecycle_stress.py --iterations 20
```

今回の環境では、workaround適用前は最初のlifecycle試行でResolveが異常終了しました。適用後は20回すべて成功し、合計160.92秒の試験終了後もResolveは応答可能でした。この数値は特定環境での調査結果であり、すべてのPC構成での無停止を保証するものではありません。

メディアは、import先のMedia Poolを明示して追加します。

```python
from pathlib import Path

from ty_davinci_resolve import get_media_pool, import_files

media_pool = get_media_pool(project)
clips = import_files(media_pool, [Path(r"C:\media\clip.mov")])
```

## P1便利関数

固定長のFusion Compositionは、Timelineの解像度・fpsに合う同梱dummy mediaを自動選択して追加します。長さを省略した場合はResolve 21.0.4公式のnative挿入を使用します。

```python
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
)
```

特殊な動画を使う場合だけ`dummy_media=`でpathを明示して上書きできます。

そのほか、page/playhead/timeline設定、Media Storage range import、generator挿入、render一括実行、render preset、DCTL・font検証・Fusion builderをトップレベルAPIから利用できます。render一括実行は、この呼出しが作成したjob IDだけを操作します。

```python
from ty_davinci_resolve import Page, open_page, render_current_settings

open_page(session, Page.EDIT)
status = render_current_settings(
    project,
    delete_completed_job=True,
)
```

P2ではRectangle builder、immutableなfont一覧、明示的なFusion page切替付きTool位置設定、任意directoryからのdummy media選択を提供します。

```python
from pathlib import Path

from ty_davinci_resolve import (
    build_rectangle,
    get_fusion_fonts,
    select_fusion_duration_media,
    set_tool_position,
)

fonts = get_fusion_fonts(session.fusion)
rectangle = build_rectangle(
    comp,
    (1.0, 1.0, 1.0, 1.0),
    width=0.2,
    height=0.1,
)
set_tool_position(
    comp,
    rectangle,
    (2, 3),
    session=session,
    activate_fusion_page=True,
)
dummy_media = select_fusion_duration_media(
    Path(r"C:\media\resolve_duration_media"),
    1280,
    720,
    23.976,
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
python -m pytest -m resolve_integration tests/integration/test_p2_resolve_workflow.py
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
