# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_render.py -q

from collections.abc import Iterator

import pytest

from ty_davinci_resolve import (
    ResolveOperationError,
    ResolveValidationError,
    add_render_job,
    delete_render_job,
    get_render_codecs,
    set_render_format_codec,
    start_render_job,
    wait_for_render_job,
)


class FakeRenderProject:
    def __init__(self) -> None:
        self.selected: tuple[str, str] | None = None
        self.started: list[str] = []
        self.deleted: list[str] = []
        self.statuses: Iterator[dict[str, object]] = iter(
            [
                {"JobStatus": "Rendering", "CompletionPercentage": 50},
                {"JobStatus": "Complete", "CompletionPercentage": 100},
            ]
        )

    def GetRenderFormats(self) -> dict[str, str]:
        return {"QuickTime": "mov", "MP4": "mp4"}

    def GetRenderCodecs(self, render_format: str) -> dict[str, str]:
        assert render_format == "mov"
        return {"Apple ProRes 4444 XQ": "ProRes4444XQ"}

    def SetCurrentRenderFormatAndCodec(self, render_format: str, codec: str) -> bool:
        self.selected = (render_format, codec)
        return True

    def AddRenderJob(self) -> str:
        return "job-1"

    def StartRendering(self, job_id: str) -> bool:
        self.started.append(job_id)
        return True

    def GetRenderJobStatus(self, job_id: str) -> dict[str, object]:
        assert job_id == "job-1"
        return next(self.statuses)

    def DeleteRenderJob(self, job_id: str) -> bool:
        self.deleted.append(job_id)
        return True


def test_codec_is_validated_using_host_capabilities() -> None:
    project = FakeRenderProject()
    assert get_render_codecs(project, "mov") == {
        "Apple ProRes 4444 XQ": "ProRes4444XQ"
    }
    set_render_format_codec(project, "mov", "ProRes4444XQ")
    assert project.selected == ("mov", "ProRes4444XQ")


def test_unknown_codec_is_rejected_before_mutation() -> None:
    project = FakeRenderProject()
    with pytest.raises(ResolveValidationError):
        set_render_format_codec(project, "mov", "unknown")
    assert project.selected is None


def test_job_operations_only_use_returned_job_id() -> None:
    project = FakeRenderProject()
    job_id = add_render_job(project)
    start_render_job(project, job_id)
    status = wait_for_render_job(project, job_id, timeout=1, poll_interval=0.001)
    delete_render_job(project, job_id)

    assert status.state == "Complete"
    assert project.started == ["job-1"]
    assert project.deleted == ["job-1"]


def test_failed_job_raises_and_is_not_deleted() -> None:
    project = FakeRenderProject()
    project.statuses = iter([{"JobStatus": "Failed", "CompletionPercentage": 10}])
    with pytest.raises(ResolveOperationError):
        wait_for_render_job(project, "job-1", timeout=1, poll_interval=0.001)
    assert project.deleted == []
