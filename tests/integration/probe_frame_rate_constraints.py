# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: .venv313/Scripts/python.exe tests/integration/probe_frame_rate_constraints.py
# Run alone; records canonical settings rejection/readback before and after media.

"""Observe frame-rate constraints and special GUI color-space labels on Resolve 21.1."""

import json
import time
from pathlib import Path
from uuid import uuid4

from ty_davinci_resolve import (
    ResolveSession, close_project, create_empty_timeline, create_project,
    delete_project, get_media_pool, import_media_files, list_projects, load_project,
    set_project_settings, set_timeline_settings,
)


def main() -> None:
    """Record constraints without assuming the historical results still apply.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Notes
    -----
    Rejection is an observation, not a reason to retry a deprecated API.
    Unexpected import or append failures stop the probe. Projects are deleted.

    Examples
    --------
    >>> main()  # doctest: +SKIP
    """
    session = ResolveSession.connect()
    if session.version_string not in ("21.1.0.17", "21.1.2.10"):
        raise RuntimeError("This constraint probe requires a verified Resolve 21.1 build.")
    manager = session.project_manager
    original = manager.GetCurrentProject()
    original_name = original.GetName() if original else None
    original_names = list_projects(session)
    observations = []
    try:
        for experiment in ("frame_rate", "special_color_label"):
            name = "TY_CONSTRAINT_" + uuid4().hex[:12]
            try:
                project = create_project(session, name)
                if experiment == "frame_rate":
                    set_project_settings(project, {"timelineFrameRate": "24"})
                    pool = get_media_pool(project)
                    timeline = create_empty_timeline(pool, "Empty custom timeline")
                    set_timeline_settings(timeline, {"timelineFrameRate": "25"})
                    candidates = [(timeline, "Empty custom timeline", "timelineFrameRate", value)
                                  for value in ("23.976", "29.97", "59.94", "24", "25", "30", "50", "60")]
                    candidates.append((project, "Project with empty timeline", "timelineFrameRate", "30"))
                else:
                    set_project_settings(project, {"colorScienceMode": "davinciYRGBColorManagedv2",
                                                  "rcmPresetMode": "Custom",
                                                  "separateColorSpaceAndGamma": "1"})
                    candidates = [(project, "RCM Custom Separate", key, "Same as Timeline")
                                  for key in ("colorSpaceInput", "colorSpaceOutput")]
                for target, condition, key, value in candidates:
                    before = target.GetSettings()
                    accepted = target.SetSettings({key: value})
                    time.sleep(0.35)
                    observations.append(dict(condition=condition, key=key, value=value,
                                             accepted=accepted, before=before, after=target.GetSettings()))
                if experiment == "frame_rate":
                    media = Path("src/ty_davinci_resolve/assets/duration_media/dummy_video_1280x720_24P.mp4").resolve()
                    clip = import_media_files(pool, [media])[0]
                    if project.SetCurrentTimeline(timeline) is not True:
                        raise RuntimeError("Could not select the probe timeline.")
                    if not pool.AppendToTimeline([{"mediaPoolItem": clip, "startFrame": 0, "endFrame": 10}]):
                        raise RuntimeError("Could not append the probe media.")
                    for target, condition in ((project, "Project with imported media"),
                                              (timeline, "Timeline with a clip")):
                        before = target.GetSettings()
                        accepted = target.SetSettings({"timelineFrameRate": "25"})
                        time.sleep(0.35)
                        observations.append(dict(condition=condition, key="timelineFrameRate", value="25",
                                                 accepted=accepted, before=before, after=target.GetSettings()))
            finally:
                if name in list_projects(session):
                    current = manager.GetCurrentProject()
                    if current and current.GetName() == name:
                        close_project(session, current)
                    delete_project(session, name)
    finally:
        if original_name and original_name in original_names:
            load_project(session, original_name)
    result = dict(resolve=session.version_string, observations=observations)
    output = Path("docs/verification") / session.version_string
    output.mkdir(parents=True, exist_ok=True)
    (output / "frame-rate-constraints.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    for row in observations:
        print(row["condition"], row["key"], row["value"], row["accepted"], row["after"][row["key"]])


if __name__ == "__main__":
    main()
