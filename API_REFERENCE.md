# Resolve 21.0.4 API対応表

実装の基準資料は `official_documents/21.0.4_Scripting/README.txt` です。行番号はリポジトリに保存した21.0.4版を基準にしています。

| 新モジュール | 主な公開API | Resolve公式API | 公式文書 |
|---|---|---|---|
| `connection.py` | `ResolveSession.connect()` | `scriptapp("Resolve")`, `GetProductName()`, `GetVersion()`, `GetVersionString()`, `Fusion()` | 67–93行 |
| `connection.py` | `ResolveSession.quit()` | `Resolve.Quit()` | 101行 |
| `connection.py` | `ResolveSession.restart()` | `Resolve.Quit()`後にWindows上でResolveを再起動し、version確認付きで再接続 | 101行 |
| `connection.py` | `get_current_page()`, `open_page()` | `Resolve.GetCurrentPage()`, `OpenPage()` | 89–90行 |
| `project.py` | project一覧・作成・読込・保存・終了・削除 | `ProjectManager.GetProjectListInCurrentFolder()`, `CreateProject()`, `LoadProject()`, `SaveProject()`, `CloseProject()`, `DeleteProject()` | 123–143行 |
| `project.py` | setting、timeline取得・選択 | `Project.Get/SetSetting()`, `GetTimelineCount()`, `GetTimelineByIndex()`, `SetCurrentTimeline()` | 162–203行 |
| `project.py` | resolution取得、LUT更新 | `Project.GetSetting()`, `RefreshLUTList()` | 195、204行 |
| `media.py` | folder取得・選択、file・連番import | `MediaPool.GetRootFolder()`, `GetCurrentFolder()`, `SetCurrentFolder()`, `ImportMedia()` | 231–265行 |
| `media.py` | `import_media_storage_items()` | `MediaStorage.AddItemListToMediaPool()` | 225–227行 |
| `timeline.py` | track検証・取得・名称、clip追加 | `Timeline.GetTrackCount()`, `GetItemListInTrack()`, `GetTrackName()`, `SetTrackName()`, `MediaPool.AppendToTimeline()` | 236–238、372–417行 |
| `timeline.py` | native Fusion Composition挿入 | `Timeline.InsertFusionCompositionIntoTimeline()` | 438行 |
| `timeline.py` | current timeline、playhead、timeline setting、generator | `Project.GetCurrentTimeline()`, `Timeline.Get/SetCurrentTimecode()`, `Get/SetSetting()`, `InsertGeneratorIntoTimeline()` | 165、411–412、434–436行 |
| `render.py` | format・codec・解像度照会 | `GetRenderFormats()`, `GetRenderCodecs()`, `GetRenderResolutions()` | 197–203行 |
| `render.py` | job ID単位の追加・開始・監視・削除 | `AddRenderJob()`, `StartRendering(jobId)`, `GetRenderJobStatus(jobId)`, `DeleteRenderJob(jobId)` | 172–189行 |
| `render.py` | render preset import・削除 | `Resolve.ImportRenderPreset()`, `Project.GetRenderPresetList()`, `DeleteRenderPreset()` | 102、177、186行 |
| `fusion.py` | native/固定長Fusion Composition追加 | `InsertFusionCompositionIntoTimeline()`, `GetFusionCompByIndex()`, `AddFusionComp()`と明示dummy media fallback | 438、473–474、502行 |

`fusion.py` の `Composition.AddTool()`、`Tool.ConnectInput()`、`SetInput()`、`GetInput()`、`FlowView.SetPos()` は、Resolve 21.0.4 Scripting READMEのオブジェクト一覧には掲載されていないResolve内蔵Fusion APIです。これらは実機テストとCountdown回帰テストで検証し、未検証の薄いラッパーは追加しません。

非対応方針は次のとおりです。

- deprecated APIは `README.txt` 1099行以降を参照し、新規ラッパーを作りません。
- index指定の旧render APIなどunsupported APIは `README.txt` 1140行以降を参照し、job ID APIを使用します。
- Resolveの版、OS、edition、hardwareで変化するformat・codec一覧は、固定一覧ではなく実機の照会結果を検証に使用します。
