# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Commands: .venv313/Scripts/python.exe tests/integration/probe_resolve_21_2_0.py api
#           .venv313/Scripts/python.exe tests/integration/probe_resolve_21_2_0.py live
# Run live alone with Resolve Studio 21.2.0; only its own disposable project is changed.

"""Record the patch upgrade without overwriting the earlier evidence."""

import argparse
import ast
from datetime import datetime, timezone, timedelta
import hashlib
import json
from pathlib import Path
import platform
import sys
import time
from uuid import uuid4

import ty_davinci_resolve as tdr


OUTPUT = Path("docs/verification/21.2.0.5")


def write_json(name: str, value: object) -> None:
    """Write one evidence file.

    Parameters
    ----------
    name
        Output filename within the versioned evidence directory.
    value
        JSON-compatible observation.

    Returns
    -------
    None

    Examples
    --------
    >>> write_json("example.json", {"verified": True})  # doctest: +SKIP
    """
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / name).write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def inventory(path: Path) -> dict:
    """Read official class signatures, dictionary fields and enum definitions.

    Parameters
    ----------
    path
        Official Python stub, parsed without executing it.

    Returns
    -------
    dict
        Class bases, all overloads, annotated fields and assignments.

    Examples
    --------
    >>> inventory(Path("DaVinciResolveScript.pyi"))  # doctest: +SKIP
    """
    result = {}
    for cls in ast.parse(path.read_text(encoding="utf-8-sig")).body:
        if not isinstance(cls, ast.ClassDef):
            continue
        methods, fields = {}, {}
        for node in cls.body:
            if isinstance(node, ast.FunctionDef):
                signature = ast.unparse(node.args) + " -> " + (ast.unparse(node.returns) if node.returns else "")
                methods.setdefault(node.name, []).append(signature)
            elif isinstance(node, ast.AnnAssign):
                fields[ast.unparse(node.target)] = ast.unparse(node.annotation)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    fields[ast.unparse(target)] = ast.unparse(node.value)
        result[cls.name] = {"bases": [ast.unparse(x) for x in cls.bases], "methods": methods, "fields": fields}
    return result


def compare_api() -> None:
    """Record method and dictionary differences between official 21.1.2 and 21.2.0 stubs.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Examples
    --------
    >>> compare_api()  # doctest: +SKIP
    """
    base = Path("official_documents")
    old = inventory(base / "21.1.2_Scripting/DaVinciResolveScript.pyi")
    new = inventory(base / "21.2.0_Scripting/DaVinciResolveScript.pyi")
    differences = {}
    for owner in sorted(old.keys() | new.keys()):
        entry = {}
        for kind in ("methods", "fields"):
            a, b = old.get(owner, {}).get(kind, {}), new.get(owner, {}).get(kind, {})
            entry[kind] = {
                "added": {k: b[k] for k in sorted(b.keys() - a.keys())},
                "absent_from_new_stub": {k: a[k] for k in sorted(a.keys() - b.keys())},
                "changed": {k: {"before": a[k], "after": b[k]} for k in sorted(a.keys() & b.keys()) if a[k] != b[k]},
            }
        if old.get(owner) != new.get(owner):
            entry["bases"] = {"before": old.get(owner, {}).get("bases"), "after": new.get(owner, {}).get("bases")}
            differences[owner] = entry
    write_json("api-diff.json", {"before": "21.1.2", "after": "21.2.0", "classes": differences})
    print("API diff:", len(differences), "changed or added classes", flush=True)


def probe_live() -> None:
    """Observe defaults, the new transcription setting and existing conventions.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Notes
    -----
    Expected rejected API conventions are recorded for comparison. Unexpected
    lifecycle, setting or readback failures stop the probe after cleanup.

    Examples
    --------
    >>> probe_live()  # doctest: +SKIP
    """
    session = tdr.ResolveSession.connect(expected_version=(21, 2, 0))
    if session.version_string != "21.2.0.5":
        raise RuntimeError("This evidence directory is pinned to Resolve 21.2.0.5.")
    manager = session.project_manager
    original = manager.GetCurrentProject()
    original_name = original.GetName() if original is not None else None
    original_names = tdr.list_projects(session)
    name = "TY_UPGRADE_2120_" + uuid4().hex[:12]
    try:
        project = tdr.create_project(session, name)
        defaults = project.GetSettings()
        if not isinstance(defaults, dict) or defaults != project.GetSetting():
            raise RuntimeError("Canonical and legacy full settings disagree.")
        write_json("project-default-settings.json", defaults)
        old = json.loads(Path("docs/verification/21.1.2.10/project-default-settings.json").read_text(encoding="utf-8"))
        write_json("setting-comparison.json", {
            "before": "21.1.2.10", "after": session.version_string,
            "added": {k: defaults[k] for k in sorted(defaults.keys() - old.keys())},
            "removed": {k: old[k] for k in sorted(old.keys() - defaults.keys())},
            "changed_defaults": {k: {"before": old[k], "after": defaults[k]} for k in sorted(old.keys() & defaults.keys()) if old[k] != defaults[k]},
            "note": "Defaults may depend on local preferences, presets and environment.",
        })
        official = Path("official_documents/21.2.0_Scripting")
        installed = Path("C:/ProgramData/Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting")
        sources = {}
        for relative in ("README.md", "CHANGELOG.md", "DaVinciResolveScript.pyi", "Modules/DaVinciResolveScript.py"):
            data = (official / relative).read_bytes()
            if data != (installed / relative).read_bytes():
                raise RuntimeError(f"Official copy differs from installed file: {relative}")
            sources[relative] = hashlib.sha256(data).hexdigest()
        write_json("environment.json", {
            "verified_at": datetime.now(timezone(timedelta(hours=9))).isoformat(),
            "resolve": session.version_string, "product": session.product_name,
            "studio": session.resolve.IsStudio(), "python": sys.version,
            "os": platform.platform(), "official_sources": sources,
            "snapshot_count": len(defaults), "legacy_canonical_equal": True,
        })
        formats = project.GetRenderFormats()
        codecs = {fmt: project.GetRenderCodecs(fmt) for fmt in formats.values()}
        write_json("render-formats-codecs.json", {"formats": formats, "codecs": codecs})
        # The 21.1.0 canonical path-only dictionary failed; compare without retrying in production.
        pool = tdr.get_media_pool(project)
        media = str(Path("src/ty_davinci_resolve/assets/duration_media/dummy_video_1280x720_24P.mp4").resolve())
        canonical = pool.ImportMedia([{"FilePath": media}])
        legacy = pool.ImportMedia([media])
        write_json("import-conventions.json", {"canonical_count": len(canonical) if canonical else 0,
                                               "legacy_count": len(legacy) if legacy else 0})
        if not legacy:
            raise RuntimeError("The production ImportMedia convention failed.")
        playback = []
        for method in ("SetSetting", "SetSettings"):
            for key, value in (("timelineFrameRate", "24"),
                               ("timelinePlaybackFrameRate", "25"),
                               ("timelineFrameRate", "30")):
                before = project.GetSettings()
                accepted = (project.SetSetting(key, value) if method == "SetSetting"
                            else project.SetSettings({key: value}))
                time.sleep(0.35)
                after = project.GetSettings()
                expected_playback = value
                if accepted is not True or float(after[key]) != float(value):
                    raise RuntimeError(f"Playback probe failed: {method} {key}")
                if float(after["timelinePlaybackFrameRate"]) != float(expected_playback):
                    raise RuntimeError("Timeline rate did not update playback rate.")
                tdr.save_project(session)
                tdr.close_project(session, project)
                project = tdr.load_project(session, name)
                reloaded = project.GetSettings()
                for check in ("timelineFrameRate", "timelinePlaybackFrameRate"):
                    if float(reloaded[check]) != float(after[check]):
                        raise RuntimeError(f"Frame rate persistence failed: {check}")
                playback.append(dict(method=method, key=key, value=value,
                                     before=before, after=after, reloaded=reloaded))
        write_json("playback-frame-rate.json", {"resolve": session.version_string,
                                               "observations": playback})
        observations = []
        key = str(tdr.ProjectSetting.TRANSCRIPTION_EXTENDED_LANGUAGE_SUPPORT)
        for value in ("0", "1"):
            before = project.GetSettings()
            accepted = project.SetSettings({key: value})
            time.sleep(0.35)
            readback = project.GetSettings()
            if accepted is not True:
                # The official stub documents rejection of 1 without installed models.
                observations.append({"key": key, "value": value, "accepted": accepted,
                                     "before": before, "readback": readback,
                                     "note": "Enabling requires installed extended language models."})
                write_json("transcription-extended-language.json", {"resolve": session.version_string, "observations": observations})
                if value != "1" or readback != before:
                    raise RuntimeError("Unexpected transcription setting rejection or partial mutation.")
                print("Extended language enable rejected without changing settings; models required", flush=True)
                break
            if str(readback[key]) != value:
                raise RuntimeError(f"New transcription setting readback mismatch: {readback[key]!r}")
            tdr.save_project(session)
            tdr.close_project(session, project)
            project = tdr.load_project(session, name)
            reloaded = project.GetSettings()
            if str(reloaded[key]) != value:
                raise RuntimeError(f"New transcription setting persistence mismatch: {reloaded[key]!r}")
            observations.append({"key": key, "value": value, "accepted": accepted, "before": before, "readback": readback, "reloaded": reloaded})
        write_json("transcription-extended-language.json", {"resolve": session.version_string, "observations": observations})
        print("Live probe:", session.version_string, len(defaults), "settings; transcription results recorded", flush=True)
    finally:
        if name in tdr.list_projects(session):
            current = manager.GetCurrentProject()
            if current is not None and current.GetName() == name:
                tdr.close_project(session, current)
            tdr.delete_project(session, name)
        if original_name and original_name in original_names:
            tdr.load_project(session, original_name)
        write_json("cleanup.json", {"project_deleted": name not in tdr.list_projects(session),
                                    "original_project_was_saved": original_name in original_names,
                                    "original_project_restored": (manager.GetCurrentProject().GetName() == original_name
                                                                  if original_name in original_names else None)})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("api", "live"))
    arguments = parser.parse_args()
    if arguments.action == "api":
        compare_api()
    else:
        probe_live()
