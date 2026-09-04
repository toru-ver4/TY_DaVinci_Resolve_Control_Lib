"""Project lifecycle and setting helpers."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import math
import time
from typing import Any

from .connection import ResolveSession
from .errors import ResolveOperationError, ResolveValidationError


@dataclass(frozen=True, slots=True)
class ProjectLifecycleTiming:
    """Timing policy for asynchronous Resolve project operations.

    Parameters
    ----------
    create_delay
        Quiet period after creating a project.
    save_delay
        Quiet period after saving a project.
    close_delay
        Quiet period after closing a project.
    load_delay
        Quiet period after loading a project, before touching its proxy.
    delete_delay
        Quiet period after deleting a project.
    timeout
        Maximum time to wait for an observable state transition.
    poll_interval
        Delay between state checks.

    Returns
    -------
    ProjectLifecycleTiming
        Immutable timing policy.

    Notes
    -----
    Resolve can return from a project API before its internal state transition is
    complete. In particular, immediately calling a method on the object returned
    by ``LoadProject`` can make Resolve 21.0.4 unstable.

    Examples
    --------
    >>> ProjectLifecycleTiming(load_delay=2.0)
    ProjectLifecycleTiming(create_delay=0.75, save_delay=0.75, close_delay=0.75, load_delay=2.0, delete_delay=0.75, timeout=15.0, poll_interval=0.25)
    """

    create_delay: float = 0.75
    save_delay: float = 0.75
    close_delay: float = 0.75
    load_delay: float = 1.5
    delete_delay: float = 0.75
    timeout: float = 15.0
    poll_interval: float = 0.25

    def __post_init__(self) -> None:
        """Validate timing values.

        Returns
        -------
        None

        Examples
        --------
        >>> ProjectLifecycleTiming(timeout=1.0).timeout
        1.0
        """
        delays = (
            self.create_delay,
            self.save_delay,
            self.close_delay,
            self.load_delay,
            self.delete_delay,
        )
        if any(not math.isfinite(value) or value < 0 for value in delays):
            raise ResolveValidationError("Lifecycle delays must be finite and non-negative.")
        if not math.isfinite(self.timeout) or self.timeout <= 0:
            raise ResolveValidationError("timeout must be a positive finite number.")
        if not math.isfinite(self.poll_interval) or self.poll_interval <= 0:
            raise ResolveValidationError("poll_interval must be a positive finite number.")


DEFAULT_PROJECT_LIFECYCLE_TIMING = ProjectLifecycleTiming()


def _wait_for_current_project(
    session: ResolveSession,
    name: str,
    initial_delay: float,
    timing: ProjectLifecycleTiming,
    operation: str,
) -> Any:
    """Wait for a named project to become the stable current project.

    Parameters
    ----------
    session
        Connected Resolve session.
    name
        Expected project name.
    initial_delay
        Quiet period before the first remote-object access.
    timing
        Polling and timeout policy.
    operation
        API operation name used in an error.

    Returns
    -------
    Any
        Stable Resolve Project remote object.

    Examples
    --------
    >>> _wait_for_current_project(session, "Test", 1.5, timing, "LoadProject")  # doctest: +SKIP
    """
    time.sleep(initial_delay)
    deadline = time.monotonic() + timing.timeout
    while True:
        project = session.project_manager.GetCurrentProject()
        if project is not None and project.GetName() == name:
            return project
        if time.monotonic() >= deadline:
            raise ResolveOperationError(
                operation,
                project,
                f"Timed out waiting for project {name!r} to become current.",
            )
        time.sleep(timing.poll_interval)


def _wait_until_project_is_not_current(
    session: ResolveSession,
    name: str,
    timing: ProjectLifecycleTiming,
) -> None:
    """Wait until a named project is no longer current.

    Parameters
    ----------
    session
        Connected Resolve session.
    name
        Closed project name.
    timing
        Polling and timeout policy.

    Returns
    -------
    None

    Examples
    --------
    >>> _wait_until_project_is_not_current(session, "Test", timing)  # doctest: +SKIP
    """
    time.sleep(timing.close_delay)
    deadline = time.monotonic() + timing.timeout
    while True:
        project = session.project_manager.GetCurrentProject()
        if project is None or project.GetName() != name:
            return
        if time.monotonic() >= deadline:
            raise ResolveOperationError(
                "ProjectManager.CloseProject",
                project,
                f"Timed out waiting for project {name!r} to close.",
            )
        time.sleep(timing.poll_interval)


def _wait_until_project_is_deleted(
    session: ResolveSession,
    name: str,
    timing: ProjectLifecycleTiming,
) -> None:
    """Wait until a named project disappears from the current folder.

    Parameters
    ----------
    session
        Connected Resolve session.
    name
        Deleted project name.
    timing
        Polling and timeout policy.

    Returns
    -------
    None

    Examples
    --------
    >>> _wait_until_project_is_deleted(session, "Test", timing)  # doctest: +SKIP
    """
    time.sleep(timing.delete_delay)
    deadline = time.monotonic() + timing.timeout
    while name in session.project_manager.GetProjectListInCurrentFolder():
        if time.monotonic() >= deadline:
            raise ResolveOperationError(
                "ProjectManager.DeleteProject",
                name,
                f"Timed out waiting for project {name!r} to be deleted.",
            )
        time.sleep(timing.poll_interval)


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


def create_project(
    session: ResolveSession,
    name: str,
    *,
    timing: ProjectLifecycleTiming = DEFAULT_PROJECT_LIFECYCLE_TIMING,
) -> Any:
    """Create and open a project whose name is not already in use.

    Parameters
    ----------
    session
        Connected Resolve session.
    name
        New project name.
    timing
        Delays and timeout used while Resolve completes the operation.

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
    return _wait_for_current_project(
        session, name, timing.create_delay, timing, "ProjectManager.CreateProject"
    )


def load_project(
    session: ResolveSession,
    name: str,
    *,
    timing: ProjectLifecycleTiming = DEFAULT_PROJECT_LIFECYCLE_TIMING,
) -> Any:
    """Load an existing project by name.

    Parameters
    ----------
    session
        Connected Resolve session.
    name
        Existing project name.
    timing
        Delays and timeout used while Resolve completes the operation.

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
    return _wait_for_current_project(
        session, name, timing.load_delay, timing, "ProjectManager.LoadProject"
    )


def save_project(
    session: ResolveSession,
    *,
    timing: ProjectLifecycleTiming = DEFAULT_PROJECT_LIFECYCLE_TIMING,
) -> None:
    """Save the currently open project.

    Parameters
    ----------
    session
        Connected Resolve session.
    timing
        Delays used while Resolve completes the operation.

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
    time.sleep(timing.save_delay)


def close_project(
    session: ResolveSession,
    project: Any | None = None,
    *,
    timing: ProjectLifecycleTiming = DEFAULT_PROJECT_LIFECYCLE_TIMING,
) -> None:
    """Close a project without saving it.

    Parameters
    ----------
    session
        Connected Resolve session.
    project
        Project to close. The current project is used when omitted.
    timing
        Delays and timeout used while Resolve completes the operation.

    Returns
    -------
    None

    Examples
    --------
    >>> close_project(session)  # doctest: +SKIP
    """
    target = project if project is not None else get_current_project(session)
    target_name = target.GetName()
    if not isinstance(target_name, str) or not target_name:
        raise ResolveOperationError("Project.GetName", target_name)
    result = session.project_manager.CloseProject(target)
    if result is not True:
        raise ResolveOperationError("ProjectManager.CloseProject", result)
    _wait_until_project_is_not_current(session, target_name, timing)


def delete_project(
    session: ResolveSession,
    name: str,
    *,
    timing: ProjectLifecycleTiming = DEFAULT_PROJECT_LIFECYCLE_TIMING,
) -> None:
    """Delete an existing project by name.

    Parameters
    ----------
    session
        Connected Resolve session.
    name
        Existing project name.
    timing
        Delays and timeout used while Resolve completes the operation.

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
    _wait_until_project_is_deleted(session, name, timing)


def get_project_setting(project: Any, name: str) -> str:
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
    >>> get_project_setting(project, "timelineFrameRate")  # doctest: +SKIP
    '24'
    """
    name = _non_empty_text(name, "name")
    result = project.GetSetting(name)
    if result is None:
        raise ResolveOperationError("Project.GetSetting", result)
    return str(result)


def set_project_setting(project: Any, name: str, value: str | int) -> None:
    """Set one project setting and fail immediately on rejection.

    Parameters
    ----------
    project
        Resolve Project remote object.
    name
        Setting name.
    value
        Setting value. Most project settings use strings. ``superScale`` uses
        an integer from 0 through 4 in the Resolve scripting API.

    Returns
    -------
    None

    Examples
    --------
    >>> set_project_setting(project, "timelineResolutionWidth", "1280")  # doctest: +SKIP
    """
    name = _non_empty_text(name, "name")
    if isinstance(value, str):
        value = _non_empty_text(value, "value")
    elif isinstance(value, bool) or not isinstance(value, int):
        raise ResolveValidationError("value must be a non-empty string or integer.")
    result = project.SetSetting(name, value)
    if result is not True:
        raise ResolveOperationError(
            "Project.SetSetting", result, f"Project rejected setting {name!r}."
        )


def set_project_settings(
    project: Any,
    settings: Mapping[str, str | int],
    *,
    settle_delay: float = 0.0,
) -> None:
    """Set project settings in mapping order.

    Parameters
    ----------
    project
        Resolve Project remote object.
    settings
        Ordered mapping of setting names to values.
    settle_delay
        Quiet period after each accepted setting. Use a positive delay when
        applying dependent settings to Resolve.

    Returns
    -------
    None

    Notes
    -----
    Processing stops at the first rejected setting.

    Examples
    --------
    >>> set_project_settings(project, {"timelineResolutionWidth": "1280"})  # doctest: +SKIP
    """
    if not isinstance(settings, Mapping) or not settings:
        raise ResolveValidationError("settings must be a non-empty mapping.")
    if (
        isinstance(settle_delay, bool)
        or not isinstance(settle_delay, (int, float))
        or not math.isfinite(settle_delay)
        or settle_delay < 0
    ):
        raise ResolveValidationError("settle_delay must be finite and non-negative.")
    for name, value in settings.items():
        set_project_setting(project, name, value)
        if settle_delay:
            time.sleep(settle_delay)


def get_project_timeline_resolution(project: Any) -> tuple[int, int]:
    """Return the timeline resolution configured in project settings.

    Parameters
    ----------
    project
        Resolve Project remote object.

    Returns
    -------
    tuple of int
        Project-level timeline width and height, without timeline overrides.

    Examples
    --------
    >>> get_project_timeline_resolution(project)  # doctest: +SKIP
    (1280, 720)
    """
    values = (get_project_setting(project, "timelineResolutionWidth"), get_project_setting(project, "timelineResolutionHeight"))
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
