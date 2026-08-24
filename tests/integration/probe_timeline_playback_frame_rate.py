# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python tests/integration/probe_timeline_playback_frame_rate.py

"""Compare project and timeline playback-frame-rate settings on Resolve."""

from __future__ import annotations

import time

from ty_davinci_resolve import (
    ResolveSession,
    close_project,
    create_project,
    delete_project,
)


PROJECT_NAME = "TY_TIMELINE_FPS_PYTHON_PROBE"


def _show(label: str, value: object) -> None:
    """Print one labeled probe result.

    Parameters
    ----------
    label
        Result label.
    value
        Value reported by Resolve.

    Returns
    -------
    None

    Examples
    --------
    >>> _show("result", True)
    result=True
    """
    print(f"{label}={value!r}", flush=True)


def main() -> None:
    """Compare playback-frame-rate writes on an empty project and timeline.

    Returns
    -------
    None

    Notes
    -----
    The disposable project is closed and deleted even when a probe assertion
    fails.

    Examples
    --------
    >>> main()  # doctest: +SKIP
    """
    session = ResolveSession.connect()
    manager = session.project_manager
    if PROJECT_NAME in manager.GetProjectListInCurrentFolder():
        delete_project(session, PROJECT_NAME)
    project = create_project(session, PROJECT_NAME)

    try:
        _show("project.initial.timelineFrameRate", project.GetSetting("timelineFrameRate"))
        _show(
            "project.initial.timelinePlaybackFrameRate",
            project.GetSetting("timelinePlaybackFrameRate"),
        )

        result = project.SetSetting("timelineFrameRate", "24")
        time.sleep(0.35)
        _show("project.set.timelineFrameRate.24", result)
        _show("project.after.timelineFrameRate", project.GetSetting("timelineFrameRate"))

        result = project.SetSetting("timelinePlaybackFrameRate", "25")
        time.sleep(0.35)
        _show("project.set.timelinePlaybackFrameRate.25", result)
        _show(
            "project.after.timelinePlaybackFrameRate",
            project.GetSetting("timelinePlaybackFrameRate"),
        )

        media_pool = project.GetMediaPool()
        timeline = media_pool.CreateEmptyTimeline("Timeline Playback Probe")
        if timeline is None:
            raise RuntimeError("Failed to create an empty timeline.")
        time.sleep(0.35)

        _show("timeline.initial.useCustomSettings", timeline.GetSetting("useCustomSettings"))
        _show("timeline.initial.timelineFrameRate", timeline.GetSetting("timelineFrameRate"))
        _show(
            "timeline.initial.timelinePlaybackFrameRate",
            timeline.GetSetting("timelinePlaybackFrameRate"),
        )
        snapshot = timeline.GetSetting()
        for key in sorted(key for key in snapshot if "framerate" in key.lower()):
            _show(f"timeline.snapshot.{key}", snapshot[key])

        result = timeline.SetSetting("timelinePlaybackFrameRate", "25")
        time.sleep(0.35)
        _show("timeline.direct.set.timelinePlaybackFrameRate.25", result)
        _show(
            "timeline.direct.after.timelinePlaybackFrameRate",
            timeline.GetSetting("timelinePlaybackFrameRate"),
        )

        result = timeline.SetSetting("useCustomSettings", "1")
        time.sleep(0.35)
        _show("timeline.set.useCustomSettings.1", result)
        _show(
            "timeline.custom.after.useCustomSettings",
            timeline.GetSetting("useCustomSettings"),
        )

        for value in ("23.976", "23.9760", "24", "24.0", "25", "25.0"):
            result = timeline.SetSetting("timelinePlaybackFrameRate", value)
            time.sleep(0.35)
            _show(f"timeline.custom.set.timelinePlaybackFrameRate.{value}", result)
            _show(
                f"timeline.custom.after.timelinePlaybackFrameRate.{value}",
                timeline.GetSetting("timelinePlaybackFrameRate"),
            )
            _show(
                f"timeline.custom.after.timelineFrameRate.{value}",
                timeline.GetSetting("timelineFrameRate"),
            )

        for value in ("23.976", "24", "25"):
            result = timeline.SetSetting("timelineFrameRate", value)
            time.sleep(0.35)
            _show(f"timeline.custom.set.timelineFrameRate.{value}", result)
            _show(
                f"timeline.custom.after.frameRate.timelineFrameRate.{value}",
                timeline.GetSetting("timelineFrameRate"),
            )
            _show(
                f"timeline.custom.after.frameRate.timelinePlaybackFrameRate.{value}",
                timeline.GetSetting("timelinePlaybackFrameRate"),
            )

        _show("project.final.timelineFrameRate", project.GetSetting("timelineFrameRate"))
        _show(
            "project.final.timelinePlaybackFrameRate",
            project.GetSetting("timelinePlaybackFrameRate"),
        )
    finally:
        current = manager.GetCurrentProject()
        if current is not None and current.GetName() == PROJECT_NAME:
            close_project(session, current)
        if PROJECT_NAME in manager.GetProjectListInCurrentFolder():
            delete_project(session, PROJECT_NAME)


if __name__ == "__main__":
    main()
