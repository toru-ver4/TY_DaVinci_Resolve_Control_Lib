"""Project lifecycle and setting helpers."""

from __future__ import annotations

from collections.abc import Mapping
import math
from typing import Any

from .connection import ResolveSession
from .errors import ResolveOperationError, ResolveValidationError


def _non_empty_text(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ResolveValidationError(f"{name} must be a non-empty string.")
    return value


def list_projects(session: ResolveSession) -> tuple[str, ...]:
    """List project names in the current Project Manager folder.

    Parameters
    ----------
    session
        Connected Resolve session.

    Returns
    -------
    tuple of str
        Project names in the current folder.

    Examples
    --------
    >>> list_projects(session)  # doctest: +SKIP
    ('Project A', 'Project B')
    """
    result = session.project_manager.GetProjectListInCurrentFolder()
    if result is None:
        raise ResolveOperationError(
            "ProjectManager.GetProjectListInCurrentFolder", result
        )
    return tuple(result)


def get_current_project(session: ResolveSession) -> Any:
    """Return the currently open project.

    Parameters
    ----------
    session
        Connected Resolve session.

    Returns
    -------
    Any
        Resolve Project remote object.

    Examples
    --------
    >>> get_current_project(session)  # doctest: +SKIP
    """
    project = session.project_manager.GetCurrentProject()
    if project is None:
        raise ResolveOperationError(
            "ProjectManager.GetCurrentProject",
            project,
            "No DaVinci Resolve project is currently open.",
        )
    return project


def create_project(session: ResolveSession, name: str) -> Any:
    """Create and open a project whose name is not already in use.

    Parameters
    ----------
    session
        Connected Resolve session.
    name
        New project name.

    Returns
    -------
    Any
        Created Resolve Project remote object.

    Examples
    --------
    >>> create_project(session, "Automation Test")  # doctest: +SKIP
    """
    name = _non_empty_text(name, "name")
    if name in list_projects(session):
        raise ResolveValidationError(f"Project already exists: {name!r}.")
    project = session.project_manager.CreateProject(name)
    if project is None:
        raise ResolveOperationError("ProjectManager.CreateProject", project)
    return project


def load_project(session: ResolveSession, name: str) -> Any:
    """Load an existing project by name.

    Parameters
    ----------
    session
        Connected Resolve session.
    name
        Existing project name.

    Returns
    -------
    Any
        Loaded Resolve Project remote object.

    Examples
    --------
    >>> load_project(session, "Automation Test")  # doctest: +SKIP
    """
    name = _non_empty_text(name, "name")
    if name not in list_projects(session):
        raise ResolveValidationError(f"Project does not exist: {name!r}.")
    project = session.project_manager.LoadProject(name)
    if project is None:
        raise ResolveOperationError("ProjectManager.LoadProject", project)
    return project


def save_project(session: ResolveSession) -> None:
    """Save the currently open project.

    Parameters
    ----------
    session
        Connected Resolve session.

    Returns
    -------
    None

    Examples
    --------
    >>> save_project(session)  # doctest: +SKIP
    """
    result = session.project_manager.SaveProject()
    if result is not True:
        raise ResolveOperationError("ProjectManager.SaveProject", result)


def close_project(session: ResolveSession, project: Any | None = None) -> None:
    """Close a project without saving it.

    Parameters
    ----------
    session
        Connected Resolve session.
    project
        Project to close. The current project is used when omitted.

    Returns
    -------
    None

    Examples
    --------
    >>> close_project(session)  # doctest: +SKIP
    """
    target = project if project is not None else get_current_project(session)
    result = session.project_manager.CloseProject(target)
    if result is not True:
        raise ResolveOperationError("ProjectManager.CloseProject", result)


def delete_project(session: ResolveSession, name: str) -> None:
    """Delete an existing project by name.

    Parameters
    ----------
    session
        Connected Resolve session.
    name
        Existing project name.

    Returns
    -------
    None

    Notes
    -----
    Resolve does not delete the currently open project. Close it first.

    Examples
    --------
    >>> delete_project(session, "Automation Test")  # doctest: +SKIP
    """
    name = _non_empty_text(name, "name")
    if name not in list_projects(session):
        raise ResolveValidationError(f"Project does not exist: {name!r}.")
    result = session.project_manager.DeleteProject(name)
    if result is not True:
        raise ResolveOperationError("ProjectManager.DeleteProject", result)


def get_setting(project: Any, name: str) -> str:
    """Read one project setting.

    Parameters
    ----------
    project
        Resolve Project remote object.
    name
        Setting name.

    Returns
    -------
    str
        Setting value reported by Resolve.

    Examples
    --------
    >>> get_setting(project, "timelineFrameRate")  # doctest: +SKIP
    '24'
    """
    name = _non_empty_text(name, "name")
    result = project.GetSetting(name)
    if result is None:
        raise ResolveOperationError("Project.GetSetting", result)
    return str(result)


def set_setting(project: Any, name: str, value: str) -> None:
    """Set one project setting and fail immediately on rejection.

    Parameters
    ----------
    project
        Resolve Project remote object.
    name
        Setting name.
    value
        Setting value.

    Returns
    -------
    None

    Examples
    --------
    >>> set_setting(project, "timelineResolutionWidth", "1280")  # doctest: +SKIP
    """
    name = _non_empty_text(name, "name")
    value = _non_empty_text(value, "value")
    result = project.SetSetting(name, value)
    if result is not True:
        raise ResolveOperationError(
            "Project.SetSetting", result, f"Project rejected setting {name!r}."
        )


def set_settings(project: Any, settings: Mapping[str, str]) -> None:
    """Set project settings in mapping order.

    Parameters
    ----------
    project
        Resolve Project remote object.
    settings
        Ordered mapping of setting names to values.

    Returns
    -------
    None

    Notes
    -----
    Processing stops at the first rejected setting.

    Examples
    --------
    >>> set_settings(project, {"timelineResolutionWidth": "1280"})  # doctest: +SKIP
    """
    if not isinstance(settings, Mapping) or not settings:
        raise ResolveValidationError("settings must be a non-empty mapping.")
    for name, value in settings.items():
        set_setting(project, name, value)


def get_timeline_resolution(project: Any) -> tuple[int, int]:
    """Return the configured timeline resolution.

    Parameters
    ----------
    project
        Resolve Project remote object.

    Returns
    -------
    tuple of int
        Timeline width and height.

    Examples
    --------
    >>> get_timeline_resolution(project)  # doctest: +SKIP
    (1280, 720)
    """
    values = (get_setting(project, "timelineResolutionWidth"), get_setting(project, "timelineResolutionHeight"))
    try:
        resolution = tuple(int(value) for value in values)
    except ValueError as error:
        raise ResolveOperationError("Project.GetSetting", values, "Timeline resolution is not an integer pair.") from error
    if any(value <= 0 for value in resolution):
        raise ResolveOperationError("Project.GetSetting", values, "Timeline resolution must be positive.")
    return resolution


def make_video_monitor_format(width: int | str, height: int | str, frame_rate: float) -> str:
    """Build a Resolve ``videoMonitorFormat`` setting value.

    Parameters
    ----------
    width
        Timeline width.
    height
        Timeline height.
    frame_rate
        Positive finite monitor frame rate.

    Returns
    -------
    str
        Resolve monitor format string.

    Examples
    --------
    >>> make_video_monitor_format(1280, 720, 23.976)
    'HD 720p 23.976'
    """
    try:
        width_value = int(width)
        height_value = int(height)
    except (TypeError, ValueError) as error:
        raise ResolveValidationError("width and height must be integers.") from error
    if isinstance(frame_rate, bool) or not isinstance(frame_rate, (int, float)) or not math.isfinite(frame_rate) or frame_rate <= 0:
        raise ResolveValidationError("frame_rate must be a positive finite number.")
    formats = {
        1280: ("HD", 720),
        1920: ("HD", height_value),
        2048: ("2K", height_value),
        2560: ("HD", 1080),
        3840: ("UHD", height_value),
        4096: ("4K", height_value),
    }
    if width_value not in formats or height_value <= 0:
        raise ResolveValidationError(f"Unsupported monitor resolution: {width_value}x{height_value}.")
    prefix, monitor_height = formats[width_value]
    rate_text = str(int(frame_rate)) if float(frame_rate).is_integer() else str(frame_rate)
    return f"{prefix} {monitor_height}p {rate_text}"


def refresh_lut_list(project: Any) -> None:
    """Refresh the current project's LUT and DCTL list.

    Parameters
    ----------
    project
        Resolve Project remote object.

    Returns
    -------
    None

    Examples
    --------
    >>> refresh_lut_list(project)  # doctest: +SKIP
    """
    if project is None:
        raise ResolveValidationError("project must not be None.")
    result = project.RefreshLUTList()
    if result is not True:
        raise ResolveOperationError("Project.RefreshLUTList", result)


def get_timeline(project: Any, index: int) -> Any:
    """Return a timeline using Resolve's one-based index.

    Parameters
    ----------
    project
        Resolve Project remote object.
    index
        One-based timeline index.

    Returns
    -------
    Any
        Resolve Timeline remote object.

    Examples
    --------
    >>> get_timeline(project, 1)  # doctest: +SKIP
    """
    count = project.GetTimelineCount()
    if not isinstance(count, int) or count < 0:
        raise ResolveOperationError("Project.GetTimelineCount", count)
    if isinstance(index, bool) or not isinstance(index, int) or not 1 <= index <= count:
        raise ResolveValidationError(
            f"index must be between 1 and {count}, got {index!r}."
        )
    timeline = project.GetTimelineByIndex(index)
    if timeline is None:
        raise ResolveOperationError("Project.GetTimelineByIndex", timeline)
    return timeline


def select_timeline(project: Any, index: int) -> Any:
    """Select and return a timeline using its one-based index.

    Parameters
    ----------
    project
        Resolve Project remote object.
    index
        One-based timeline index.

    Returns
    -------
    Any
        Selected Resolve Timeline remote object.

    Examples
    --------
    >>> select_timeline(project, 1)  # doctest: +SKIP
    """
    timeline = get_timeline(project, index)
    result = project.SetCurrentTimeline(timeline)
    if result is not True:
        raise ResolveOperationError("Project.SetCurrentTimeline", result)
    return timeline
