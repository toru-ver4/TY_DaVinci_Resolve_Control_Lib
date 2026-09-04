# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_media_and_timeline.py -q

from pathlib import Path
from types import SimpleNamespace

import pytest

from ty_davinci_resolve import (
    MediaType,
    ResolveOperationError,
    ResolveValidationError,
    append_clip_to_current_timeline,
    get_track_items,
    import_media_files,
    import_image_sequence,
    insert_fusion_composition,
)


class FakeMediaPool:
    def __init__(self, result: list[object] | None = None) -> None:
        self.result = result if result is not None else [object()]
        self.arguments: object = None

    def ImportMedia(self, arguments: object) -> list[object]:
        self.arguments = arguments
        return self.result

    def AppendToTimeline(self, arguments: object) -> list[object]:
        self.arguments = arguments
        return self.result


def test_import_media_files_validates_all_paths_before_api_call(tmp_path: Path) -> None:
    existing = tmp_path / "clip.mov"
    existing.write_bytes(b"test")
    media_pool = FakeMediaPool()

    with pytest.raises(ResolveValidationError):
        import_media_files(media_pool, [existing, tmp_path / "missing.mov"])

    assert media_pool.arguments is None


def test_import_media_files_calls_import_media(tmp_path: Path) -> None:
    existing = tmp_path / "clip.mov"
    existing.write_bytes(b"test")
    media_pool = FakeMediaPool()

    items = import_media_files(media_pool, [existing])

    assert len(items) == 1
    assert media_pool.arguments == [str(existing)]


def test_import_image_sequence_builds_documented_clip_info(tmp_path: Path) -> None:
    media_pool = FakeMediaPool()
    pattern = tmp_path / "frame_%04d.png"

    item = import_image_sequence(media_pool, pattern, 0, 95)

    assert item is not None
    assert media_pool.arguments == [
        {"FilePath": str(pattern), "StartIndex": 0, "EndIndex": 95}
    ]


def test_append_clip_to_current_timeline_builds_documented_clip_info() -> None:
    media_pool = FakeMediaPool()
    clip = object()

    item = append_clip_to_current_timeline(
        media_pool,
        clip,
        record_frame=100,
        start_frame=0,
        end_frame=23,
        media_type=MediaType.VIDEO_ONLY,
        track_index=2,
    )

    assert item is not None
    assert media_pool.arguments == [
        {
            "mediaPoolItem": clip,
            "trackIndex": 2,
            "recordFrame": 100,
            "startFrame": 0,
            "endFrame": 23,
            "mediaType": 1,
        }
    ]


def test_append_clip_to_current_timeline_rejects_incomplete_source_range_before_api() -> None:
    media_pool = FakeMediaPool()
    with pytest.raises(ResolveValidationError):
        append_clip_to_current_timeline(media_pool, object(), start_frame=0)
    assert media_pool.arguments is None


def test_get_track_items_accepts_empty_track() -> None:
    timeline = SimpleNamespace(
        GetTrackCount=lambda track_type: 1,
        GetItemListInTrack=lambda track_type, index: [],
    )
    assert get_track_items(timeline, "video", 1) == ()


def test_get_track_items_rejects_index_before_item_query() -> None:
    timeline = SimpleNamespace(
        GetTrackCount=lambda track_type: 1,
        GetItemListInTrack=lambda *args: pytest.fail("query must not occur"),
    )
    with pytest.raises(ResolveValidationError):
        get_track_items(timeline, "video", 2)


def test_insert_fusion_composition_converts_none_to_exception() -> None:
    timeline = SimpleNamespace(InsertFusionCompositionIntoTimeline=lambda: None)
    with pytest.raises(ResolveOperationError):
        insert_fusion_composition(timeline)
