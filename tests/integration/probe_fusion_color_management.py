# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: .venv313/Scripts/python.exe tests/integration/probe_fusion_color_management.py
# Run alone: renders all four Countdown conditions with the page refresh disabled.

"""Compare the no-refresh output with the approved Resolve 21.1 master."""

import json
import os
from pathlib import Path
import sys
from tempfile import TemporaryDirectory
from uuid import uuid4
from zipfile import ZipFile

from ty_davinci_resolve import ResolveSession, close_project, delete_project, list_projects, load_project

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tests/countdown_regression"))
import create_countdown_v2 as countdown
import countdown_adapter as adapter
from png_compare import REFERENCE_SHA256_RESOLVE_21_1_0, compare_png_samples, validate_reference_archive


def main() -> None:
    """Render without the workaround and retain comparison evidence only.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Notes
    -----
    A pixel mismatch is the observation being investigated. API or render failures
    are errors and stop the probe. Installed fonts, DCTLs and masters are untouched.

    Examples
    --------
    >>> main()  # doctest: +SKIP
    """
    session = ResolveSession.connect()
    if session.version_string not in ("21.1.0.17", "21.1.2.10", "21.2.0.5"):
        raise RuntimeError("This probe uses the approved 21.1 image master.")
    manager = session.project_manager
    original = manager.GetCurrentProject()
    original_name = original.GetName() if original else None
    project_name = "TY_NO_REFRESH_" + uuid4().hex[:12]
    previous_refresh = adapter.api.refresh_fusion_color_management
    previous_directory = Path.cwd()
    archive = ROOT / "tests/countdown_reference_data/ref_data_1280x720_resolve_21_1_0.zip"
    names = validate_reference_archive(archive, expected_sha256=REFERENCE_SHA256_RESOLVE_21_1_0)
    failures = []
    try:
        adapter.api.refresh_fusion_color_management = lambda *args, **kwargs: None
        with TemporaryDirectory(prefix=".pytest-tmp-no-refresh-", dir=ROOT) as directory:
            countdown.main(["--output-dir", directory, "--project-name", project_name,
                            "--width", "1280", "--height", "720", "--framerate", "23.976",
                            "--gamut", "P3-D65", "Rec.2020", "--gamma", "Gamma 2.4", "ST2084"])
            output = Path(directory)
            if sorted(path.name for path in output.glob("*.png")) != list(names):
                raise RuntimeError("Rendered PNG filenames differ from the master.")
            with ZipFile(archive) as reference:
                for name in names:
                    try:
                        compare_png_samples(reference.read(name), output / name, name)
                    except AssertionError as error:
                        failures.append(str(error))
            os.chdir(previous_directory)
    finally:
        adapter.api.refresh_fusion_color_management = previous_refresh
        os.chdir(previous_directory)
        current = manager.GetCurrentProject()
        if current and current.GetName() == project_name:
            close_project(session, current)
        if project_name in list_projects(session):
            delete_project(session, project_name)
        if original_name and original_name in list_projects(session):
            load_project(session, original_name)
    result = {"resolve": session.version_string, "refresh_enabled": False,
              "master_sha256": REFERENCE_SHA256_RESOLVE_21_1_0,
              "compared_frames": len(names), "different_frames": len(failures), "mismatches": failures}
    output = ROOT / "docs/verification" / session.version_string
    output.mkdir(parents=True, exist_ok=True)
    (output / "fusion-without-refresh.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "mismatches"}, indent=2))


if __name__ == "__main__":
    main()
