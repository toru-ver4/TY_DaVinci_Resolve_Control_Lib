# TY_DaVinci_Resolve_Control_Lib

DaVinci Resolve 21.0.4をPythonから制御するためのライブラリです。

現在は再設計中のpre-alpha版です。Windows、Python 3.12 64-bitのみを動作保証対象とします。

## 名前の読み方

名前の直前に、Resolveの画面名は**［Resolve GUI］**、Resolve公式Scripting APIは**［Resolve API］**、本ライブラリ`ty_davinci_resolve`のPython APIは**［TY API］**と表記します。例えば［Resolve GUI］「Timeline frame rate」、［Resolve API］`Project.SetSetting()`、［TY API］`ProjectSetting`です。ダブルクォートは実際の文字列にだけ使用します。

公開関数名は操作対象を明示します。プロジェクト設定には
`get_project_setting()`／`set_project_setting()`／`set_project_settings()`、
Media Poolのフォルダー操作には`get_current_media_pool_folder()`など、
Fusionノードの操作には`add_fusion_tool()`などを使用します。旧名の互換エイリアスは提供しません。

`get_project_timeline_resolution()`はプロジェクト設定の解像度を返します。
個別タイムラインの設定は`get_timeline_setting()`で読み取ります。
`set_timeline_playhead_timecode()`は再生ヘッドを移動し、
`set_fusion_tool_flow_position()`はノードエディター上の配置を変更します。

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

プロジェクトの作成と設定は、明示的なsessionを渡して行います。Resolveが設定を受け付けなかった場合は、その時点で例外になり、設定が一部だけ抜けた状態で処理を続けません。

```python
from ty_davinci_resolve import (
    FrameRate,
    ProjectSetting,
    ResolutionValue,
    ResolveSession,
    create_project,
    set_project_settings,
)

session = ResolveSession.connect()
project = create_project(session, "Automation Test")
set_project_settings(
    project,
    {
        ProjectSetting.TIMELINE_RESOLUTION_WIDTH: ResolutionValue.PX_1280,
        ProjectSetting.TIMELINE_RESOLUTION_HEIGHT: ResolutionValue.PX_720,
        ProjectSetting.TIMELINE_FRAME_RATE: FrameRate.FPS_23_976,
    },
)
```

解像度やフレームレートは、素材を読み込んだりtimelineを作ったりする前に設定してください。作品の時間軸が作られた後は、Resolveが変更を拒否する場合があります。Projectの作成・保存・終了・読込・削除に必要な待機はライブラリが行うため、通常は待機時間を意識する必要はありません。

## 制作条件を定数で指定する

Project SettingsやDeliver設定では、Resolve固有の綴りを文字列で直接書く代わりに、本ライブラリが提供する用途別の定数クラスを使用できます。入力補完が効き、`P3 DCI`と`P3-DCI`のようなGUI/API間の表記差もコード側で覚える必要がありません。

```python
from ty_davinci_resolve import (
    BT2100_PROJECT_SETTINGS,
    ColorSpace,
    Gamma,
    ProjectSetting,
    set_project_settings,
)

assert ColorSpace.P3_D65 == "P3-D65"
assert Gamma.ST2084 == "ST2084"
set_project_settings(project, BT2100_PROJECT_SETTINGS, settle_delay=0.35)
```

`BT2100_PROJECT_SETTINGS`のようなpresetは、設定する順番も含めたひとまとまりの制作条件です。依存するColor Management項目を連続して変更するときは、例のように`settle_delay=0.35`を指定し、Resolveが各変更を反映する時間を確保します。

ResolveのProject SettingsにあるTimeline frame rateは、project作成直後に本ライブラリの`ProjectSetting.TIMELINE_FRAME_RATE`で設定します。Project SettingsのPlayback frame rateはPythonから変更できず、本ライブラリの`ProjectSetting.TIMELINE_PLAYBACK_FRAME_RATE`は現在値の確認用です。

一方、特定の空timelineだけ別のフレームレートにすることは可能です。本ライブラリの`set_timeline_settings()`へ`TimelineSetting.TIMELINE_FRAME_RATE`を渡すと、ResolveのTimeline Settingsにあるcustom settingsを有効にして、そのtimelineの「Timeline frame rate」を変更します。名前が似ていますが、本ライブラリの`TimelineSetting.TIMELINE_PLAYBACK_FRAME_RATE`を書き込む操作ではありません。

Color Management、Image Scaling、Video Monitoringを含むGUI項目と本ライブラリの定数との対応、設定可能な値、変更できない項目は[Resolve GUIと本ライブラリ定数の対応](project-settings.md)を参照してください。

Deliverのformatとcodecは、OS、Resolveのedition、hardwareによって利用できる組み合わせが変わります。`VideoCodec`に名前が存在するだけで使用可能とは判断せず、render前に`get_render_codecs()`で現在のResolveへ問い合わせてください。

## Resolveの処理完了を待つ理由

projectを開いた直後など、画面上では切替中なのにAPIだけが先に成功を返すことがあります。その瞬間に次の操作を送るとResolveが異常終了したため、本ライブラリは作成・保存・終了・読込・削除の後に、Resolveの切替完了を待ちます。通常の利用では自動的に処理されます。

通常よりprojectの切替に時間がかかるPCでだけ、次の既定待機時間を調整してください。

| 操作 | 最初の静穏時間 | 完了確認 |
|---|---:|---|
| `create_project()` | 0.75秒 | 指定projectがcurrentになるまで確認 |
| `save_project()` | 0.75秒 | 確認用APIがないため固定待機 |
| `close_project()` | 0.75秒 | 対象projectがcurrentでなくなるまで確認 |
| `load_project()` | 1.5秒 | 指定projectがcurrentになるまで確認 |
| `delete_project()` | 0.75秒 | project一覧から消えるまで確認 |

状態確認は0.25秒間隔、待機上限は15秒です。projectの読込時は最低1.5秒待ち、Resolveが実際にそのprojectへ切り替わったことを確認してから次の処理へ進みます。

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

ライブラリ開発者向けに、projectの作成→設定→保存→終了→再読込→終了→削除を繰り返す負荷試験も用意しています。

```powershell
python tests/stress/project_lifecycle_stress.py --iterations 20
```

Windows版Resolve Studio 21.0.4.5では20回すべて成功しました。この結果は特定環境での実測であり、すべてのPC構成での無停止を保証するものではありません。

メディアは、import先のMedia Poolを明示して追加します。

```python
from pathlib import Path

from ty_davinci_resolve import get_media_pool, import_media_files

media_pool = get_media_pool(project)
clips = import_media_files(media_pool, [Path(r"C:\media\clip.mov")])
```

## Fusion Compositionを自動で配置する

指定した長さのFusion Compositionをtimelineへ追加できます。ライブラリはtimelineの解像度とfpsに合う内部メディアを選ぶため、尺合わせ用の素材を利用者が用意する必要はありません。長さを省略すると、Resolve標準のFusion Compositionを挿入します。

```python
from ty_davinci_resolve import (
    add_fusion_composition_to_timeline,
    get_current_timeline,
    get_media_pool,
)

timeline = get_current_timeline(project)
item, comp = add_fusion_composition_to_timeline(
    timeline,
    duration_frames=24,
    record_frame=86400,
    media_pool=get_media_pool(project),
)
```

独自の尺合わせ用動画を使う場合だけ、`dummy_media=`でファイルを指定します。

ページ移動、再生ヘッド移動、素材の読み込み、generator挿入、render、DCTLやfontの確認もトップレベルAPIから利用できます。render関数は自分で追加したjobだけを操作するため、Deliver pageに既にある別のjobを誤って開始しません。

```python
from ty_davinci_resolve import Page, open_page, render_current_settings

open_page(session, Page.EDIT)
status = render_current_settings(
    project,
    delete_completed_job=True,
)
```

Fusionでは、Rectangleの作成、利用可能fontの確認、Flow上でのTool配置も行えます。次の例は白いRectangleを作成し、Flow上の座標`(2, 3)`へ配置します。

`Composition.AddTool()`へ渡すRegistry IDは、`FusionTool`から指定できます。Resolve FX（OFX）は`FusionResolveFxTool`へ分けています。

```python
from ty_davinci_resolve import FusionTool, add_fusion_tool

background = add_fusion_tool(comp, FusionTool.BACKGROUND, (0, 0))
mask = add_fusion_tool(comp, FusionTool.RECTANGLE_MASK, (0, -1))
```

`FusionTool`または`FusionResolveFxTool`のenum memberを`add_fusion_tool()`へ直接渡すと、同梱の型stubによりTool固有の入力名が補完されます。例えば`FusionTool.RECTANGLE_MASK`の戻り値では`Width`、`Height`、`Center`などが候補に表示されます。Fusion remote objectの入力値型は実行時に変化し得るため、入力名はTool別に定義し、値自体は`Any`としています。

PointやNumber入力へ接続するModifierは、`FusionModifier`と`add_fusion_modifier()`を使用します。`FusionTool.XY_PATH`は互換性用で、新規コードでは`FusionModifier.XY_PATH`を指定します。

```python
from ty_davinci_resolve import FusionModifier, add_fusion_modifier

xy_path = add_fusion_modifier(comp, FusionModifier.XY_PATH)
mask.Center = xy_path
```

### Toolの入力名を実機から調べる

各Toolで利用できる入力は、Tool remote objectの`GetInputList()`で取得できます。各Inputの`GetAttrs()`に含まれる`INPS_ID`が、`Width`や`Center`のようにPython APIへ渡す入力IDです。`INPS_Name`はGUI上の表示名、`INPS_DataType`は`Number`や`Point`などの概略データ型です。

次の関数は、実機から入力ID、表示名、データ型を取得して、入力ID順に返します。

```python
from typing import Any


def get_fusion_tool_input_info(
    tool: Any,
) -> tuple[tuple[str, str, str], ...]:
    """Return input information reported by a Fusion Tool.

    Parameters
    ----------
    tool
        Fusion Tool remote object.

    Returns
    -------
    tuple of tuple of str
        Input ID, display name, and data type for every reported input.

    Examples
    --------
    >>> get_fusion_tool_input_info(rectangle_mask)  # doctest: +SKIP
    """
    input_list = tool.GetInputList()
    if not isinstance(input_list, dict):
        raise RuntimeError("Tool.GetInputList returned an invalid value.")

    rows: list[tuple[str, str, str]] = []
    for input_object in input_list.values():
        attrs = input_object.GetAttrs()
        if not isinstance(attrs, dict):
            raise RuntimeError("Input.GetAttrs returned an invalid value.")
        input_id = attrs.get("INPS_ID")
        if not isinstance(input_id, str) or not input_id:
            continue
        display_name = attrs.get("INPS_Name")
        data_type = attrs.get("INPS_DataType")
        rows.append(
            (
                input_id,
                display_name if isinstance(display_name, str) else "",
                data_type if isinstance(data_type, str) else "",
            )
        )
    return tuple(sorted(rows, key=lambda row: row[0].casefold()))
```

RectangleMaskを調べる例です。`comp`は前述の`add_fusion_composition_to_timeline()`などで取得したCompositionを使用します。

```python
from ty_davinci_resolve import FusionTool, add_fusion_tool

rectangle_mask = add_fusion_tool(
    comp,
    FusionTool.RECTANGLE_MASK,
    (0, -1),
)
for input_id, display_name, data_type in get_fusion_tool_input_info(
    rectangle_mask
):
    print(f"{input_id:24} {data_type:10} {display_name}")
```

出力には共通設定も含まれますが、Rectangle固有の主要部分は次のように確認できます。

```text
Angle                    Number     Angle
Center                   Point      Center
Height                   Number     Height
Width                    Number     Width
```

表示される入力はResolveのversion、edition、Tool設定によって変わる可能性があります。入力IDが有効なPython識別子なら`rectangle_mask.Width`のようにアクセスできます。識別子として扱えない入力や補完に未収録の入力も、`set_fusion_tool_input(rectangle_mask, input_id, value)`なら入力ID文字列で指定できます。調査だけのために追加したToolは、確認後に`rectangle_mask.Delete()`で削除してください。

```python
from pathlib import Path

from ty_davinci_resolve import (
    build_fusion_rectangle,
    get_fusion_fonts,
    select_fusion_duration_media,
    set_fusion_tool_flow_position,
)

fonts = get_fusion_fonts(session.fusion)
rectangle = build_fusion_rectangle(
    comp,
    (1.0, 1.0, 1.0, 1.0),
    width=0.2,
    height=0.1,
)
set_fusion_tool_flow_position(
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

利用可能な値は`get_render_formats()`、`get_render_codecs()`、`get_render_resolutions()`で照会できます。Resolve 21.0.4公式APIの対応箇所は[README.txt](../official_documents/21.0.4_Scripting/README.txt)のProject API一覧を参照してください。

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

詳細な移行・実装方針は[移行・再設計計画](migration-plan.md)、本ライブラリの実装とResolve 21.0.4公式APIの対応は[API対応表](api-reference.md)、Project Settingsと本ライブラリの定数との対応は[GUI対応表](project-settings.md)を参照してください。

## 備考

本リポジトリは個人開発の成果公開を目的としており、
Pull Request は受け付けていません。クローズします。
