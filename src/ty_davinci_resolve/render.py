"""Render capability lookup and job-ID-scoped render management."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
import time
from typing import Any

from .errors import ResolveOperationError, ResolveValidationError


@dataclass(frozen=True, slots=True)
class RenderJobStatus:
    """Normalized status returned for one Resolve render job."""

    job_id: str
    state: str
    completion_percentage: float | None
    raw: Mapping[str, Any]


def get_render_formats(project: Any) -> dict[str, str]:
    """Return render format descriptions mapped to identifiers.

    Parameters
    ----------
    project
        Resolve Project remote object.

    Returns
    -------
    dict of str to str
        Available render formats reported by the current host.

    Examples
    --------
    >>> get_render_formats(project)  # doctest: +SKIP
    {'QuickTime': 'mov'}
    """
    result = project.GetRenderFormats()
    if not isinstance(result, dict) or not result:
        raise ResolveOperationError("Project.GetRenderFormats", result)
    return dict(result)


def get_render_codecs(project: Any, render_format: str) -> dict[str, str]:
    """Return codec descriptions mapped to identifiers for a format.

    Parameters
    ----------
    project
        Resolve Project remote object.
    render_format
        Format identifier such as ``mov``.

    Returns
    -------
    dict of str to str
        Available codecs reported by the current host.

    Examples
    --------
    >>> get_render_codecs(project, "mov")  # doctest: +SKIP
    {'Apple ProRes 4444 XQ': 'ProRes4444XQ'}
    """
    if not isinstance(render_format, str) or not render_format:
        raise ResolveValidationError("render_format must be a non-empty string.")
    formats = get_render_formats(project)
    if render_format not in formats.values():
        raise ResolveValidationError(
            f"Unsupported render format {render_format!r}; available identifiers: "
            f"{sorted(set(formats.values()))}."
        )
    result = project.GetRenderCodecs(render_format)
    if not isinstance(result, dict) or not result:
        raise ResolveOperationError("Project.GetRenderCodecs", result)
    return dict(result)


def set_render_format_codec(
    project: Any,
    render_format: str,
    codec: str,
) -> None:
    """Select an available render format and codec.

    Parameters
    ----------
    project
        Resolve Project remote object.
    render_format
        Format identifier such as ``mov``.
    codec
        Codec identifier such as ``ProRes4444XQ``.

    Returns
    -------
    None

    Examples
    --------
    >>> set_render_format_codec(project, "mov", "ProRes4444XQ")  # doctest: +SKIP
    """
    codecs = get_render_codecs(project, render_format)
    if codec not in codecs.values():
        raise ResolveValidationError(
            f"Unsupported codec {codec!r} for {render_format!r}; "
            f"available identifiers: {sorted(set(codecs.values()))}."
        )
    result = project.SetCurrentRenderFormatAndCodec(render_format, codec)
    if result is not True:
        raise ResolveOperationError(
            "Project.SetCurrentRenderFormatAndCodec", result
        )


def get_render_resolutions(
    project: Any,
    render_format: str,
    codec: str,
) -> tuple[dict[str, Any], ...]:
    """Return supported resolutions for one format and codec.

    Parameters
    ----------
    project
        Resolve Project remote object.
    render_format
        Format identifier.
    codec
        Codec identifier.

    Returns
    -------
    tuple of dict
        Resolution dictionaries reported by Resolve.

    Examples
    --------
    >>> get_render_resolutions(project, "mov", "ProRes4444XQ")  # doctest: +SKIP
    """
    codecs = get_render_codecs(project, render_format)
    if codec not in codecs.values():
        raise ResolveValidationError(
            f"Unsupported codec {codec!r} for {render_format!r}."
        )
    result = project.GetRenderResolutions(render_format, codec)
    if result is None:
        raise ResolveOperationError("Project.GetRenderResolutions", result)
    return tuple(dict(item) for item in result)


def set_render_settings(project: Any, settings: Mapping[str, Any]) -> None:
    """Apply render settings in one official API call.

    Parameters
    ----------
    project
        Resolve Project remote object.
    settings
        Non-empty render settings mapping.

    Returns
    -------
    None

    Examples
    --------
    >>> set_render_settings(project, {"TargetDir": "C:/output"})  # doctest: +SKIP
    """
    if not isinstance(settings, Mapping) or not settings:
        raise ResolveValidationError("settings must be a non-empty mapping.")
    result = project.SetRenderSettings(dict(settings))
    if result is not True:
        raise ResolveOperationError("Project.SetRenderSettings", result)


def add_render_job(project: Any) -> str:
    """Add and return one render job ID.

    Parameters
    ----------
    project
        Resolve Project remote object.

    Returns
    -------
    str
        Unique Resolve render job ID.

    Examples
    --------
    >>> add_render_job(project)  # doctest: +SKIP
    'job-id'
    """
    job_id = project.AddRenderJob()
    if not isinstance(job_id, str) or not job_id:
        raise ResolveOperationError("Project.AddRenderJob", job_id)
    return job_id


def start_render_job(project: Any, job_id: str) -> None:
    """Start exactly one render job.

    Parameters
    ----------
    project
        Resolve Project remote object.
    job_id
        Unique render job ID.

    Returns
    -------
    None

    Examples
    --------
    >>> start_render_job(project, "job-id")  # doctest: +SKIP
    """
    if not isinstance(job_id, str) or not job_id:
        raise ResolveValidationError("job_id must be a non-empty string.")
    result = project.StartRendering(job_id)
    if result is not True:
        raise ResolveOperationError("Project.StartRendering", result)


def get_render_job_status(project: Any, job_id: str) -> RenderJobStatus:
    """Return normalized status for one render job.

    Parameters
    ----------
    project
        Resolve Project remote object.
    job_id
        Unique render job ID.

    Returns
    -------
    RenderJobStatus
        Normalized state and completion percentage.

    Examples
    --------
    >>> get_render_job_status(project, "job-id")  # doctest: +SKIP
    """
    if not isinstance(job_id, str) or not job_id:
        raise ResolveValidationError("job_id must be a non-empty string.")
    result = project.GetRenderJobStatus(job_id)
    if not isinstance(result, dict) or not result:
        raise ResolveOperationError("Project.GetRenderJobStatus", result)
    state = result.get("JobStatus")
    if not isinstance(state, str) or not state:
        raise ResolveOperationError(
            "Project.GetRenderJobStatus",
            result,
            f"Render status for {job_id!r} has no JobStatus field.",
        )
    percentage = result.get("CompletionPercentage")
    normalized_percentage = (
        float(percentage) if isinstance(percentage, (int, float)) else None
    )
    return RenderJobStatus(job_id, state, normalized_percentage, dict(result))


def wait_for_render_job(
    project: Any,
    job_id: str,
    *,
    timeout: float = 3600.0,
    poll_interval: float = 0.5,
) -> RenderJobStatus:
    """Wait until one render job completes or fails.

    Parameters
    ----------
    project
        Resolve Project remote object.
    job_id
        Unique render job ID.
    timeout
        Maximum wait time in seconds.
    poll_interval
        Delay between status queries in seconds.

    Returns
    -------
    RenderJobStatus
        Final successful job status.

    Notes
    -----
    The function does not delete any render jobs.

    Examples
    --------
    >>> wait_for_render_job(project, "job-id", timeout=60)  # doctest: +SKIP
    """
    for value, name in ((timeout, "timeout"), (poll_interval, "poll_interval")):
        if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
            raise ResolveValidationError(f"{name} must be a positive number.")
    deadline = time.monotonic() + timeout
    while True:
        status = get_render_job_status(project, job_id)
        state = status.state.casefold()
        if state == "complete":
            return status
        if state in {"failed", "cancelled", "canceled"}:
            raise ResolveOperationError(
                "Project.GetRenderJobStatus",
                status.raw,
                f"Render job {job_id!r} ended with status {status.state!r}.",
            )
        if time.monotonic() >= deadline:
            raise ResolveOperationError(
                "Project.GetRenderJobStatus",
                status.raw,
                f"Timed out waiting for render job {job_id!r} after {timeout} seconds.",
            )
        time.sleep(poll_interval)


def delete_render_job(project: Any, job_id: str) -> None:
    """Delete exactly one render job.

    Parameters
    ----------
    project
        Resolve Project remote object.
    job_id
        Unique render job ID.

    Returns
    -------
    None

    Examples
    --------
    >>> delete_render_job(project, "job-id")  # doctest: +SKIP
    """
    if not isinstance(job_id, str) or not job_id:
        raise ResolveValidationError("job_id must be a non-empty string.")
    result = project.DeleteRenderJob(job_id)
    if result is not True:
        raise ResolveOperationError("Project.DeleteRenderJob", result)


def render_current_settings(
    project: Any,
    *,
    timeout: float = 3600.0,
    poll_interval: float = 0.5,
    delete_completed_job: bool = False,
) -> RenderJobStatus:
    """Create, run, and wait for exactly one render job.

    Parameters
    ----------
    project
        Resolve Project remote object.
    timeout
        Maximum wait time in seconds.
    poll_interval
        Delay between status queries in seconds.
    delete_completed_job
        Delete this function's job after successful completion.

    Returns
    -------
    RenderJobStatus
        Final successful status.

    Notes
    -----
    Failed and timed-out jobs are deliberately retained for diagnosis.

    Examples
    --------
    >>> render_current_settings(project, timeout=60)  # doctest: +SKIP
    """
    if not isinstance(delete_completed_job, bool):
        raise ResolveValidationError("delete_completed_job must be a bool.")
    job_id = add_render_job(project)
    start_render_job(project, job_id)
    status = wait_for_render_job(project, job_id, timeout=timeout, poll_interval=poll_interval)
    if delete_completed_job:
        delete_render_job(project, job_id)
    return status


def delete_render_preset(project: Any, name: str) -> None:
    """Delete a named render preset.

    Parameters
    ----------
    project
        Resolve Project remote object.
    name
        Existing render preset name.

    Returns
    -------
    None

    Examples
    --------
    >>> delete_render_preset(project, "Automation Preset")  # doctest: +SKIP
    """
    if not isinstance(name, str) or not name.strip():
        raise ResolveValidationError("name must be a non-empty string.")
    result = project.DeleteRenderPreset(name)
    if result is not True:
        raise ResolveOperationError("Project.DeleteRenderPreset", result)


def _render_preset_names(project: Any) -> set[str]:
    result = project.GetRenderPresetList()
    if result is None:
        raise ResolveOperationError("Project.GetRenderPresetList", result)
    names: set[str] = set()
    for item in result:
        if isinstance(item, str):
            names.add(item)
        elif isinstance(item, Mapping):
            name = item.get("Name") or item.get("PresetName")
            if isinstance(name, str):
                names.add(name)
    return names


def import_render_preset(resolve: Any, project: Any, preset_path: str | Path) -> None:
    """Import a render preset without deleting an existing preset.

    Parameters
    ----------
    resolve
        Resolve application remote object.
    project
        Current Resolve Project remote object used for collision checking.
    preset_path
        Absolute existing preset file.

    Returns
    -------
    None

    Examples
    --------
    >>> import_render_preset(session.resolve, project, "C:/presets/example.xml")  # doctest: +SKIP
    """
    path = Path(preset_path).expanduser()
    if not path.is_absolute() or not path.is_file():
        raise ResolveValidationError(f"Render preset does not exist: {path}.")
    if path.stem in _render_preset_names(project):
        raise ResolveValidationError(f"Render preset already exists: {path.stem!r}.")
    result = resolve.ImportRenderPreset(str(path))
    if result is not True:
        raise ResolveOperationError("Resolve.ImportRenderPreset", result)
