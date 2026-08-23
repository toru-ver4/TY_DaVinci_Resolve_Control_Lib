# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest -m countdown_regression tests/integration/test_countdown_regression.py -q -s

from __future__ import annotations

from pathlib import Path
import sys
from uuid import uuid4

import pytest

from ty_davinci_resolve import (
    ResolveSession,
    close_project,
    delete_project,
    list_projects,
    load_project,
)

COUNTDOWN_DIR = Path(__file__).resolve().parents[1] / "countdown_regression"
sys.path.insert(0, str(COUNTDOWN_DIR))

import create_countdown_v2 as countdown  # noqa: E402
from png_compare import compare_output_directory  # noqa: E402


@pytest.mark.resolve_integration
@pytest.mark.countdown_regression
def test_countdown_matches_16_bit_reference(tmp_path: Path) -> None:
    session = ResolveSession.connect()
    manager = session.project_manager
    original = manager.GetCurrentProject()
    original_name = original.GetName() if original is not None else None
    original_projects = tuple(manager.GetProjectListInCurrentFolder())
    original_is_saved = original_name in original_projects
    project_name = f"TY_CD_{uuid4().hex[:16]}"
    reference_zip = (
        Path(__file__).resolve().parents[1]
        / "countdown_reference_data"
        / "ref_data_1280x720.zip"
    )

    try:
        countdown.main(
            [
                "--output-dir",
                str(tmp_path),
                "--project-name",
                project_name,
                "--width",
                "1280",
                "--height",
                "720",
                "--framerate",
                "23.976",
                "--gamut",
                "P3-D65",
                "Rec.2020",
                "--gamma",
                "Gamma 2.4",
                "ST2084",
            ]
        )
        compare_output_directory(reference_zip, tmp_path)
    finally:
        current = manager.GetCurrentProject()
        if current is not None and current.GetName() == project_name:
            close_project(session, current)
        if project_name in list_projects(session):
            delete_project(session, project_name)
        if original_is_saved and original_name in list_projects(session):
            load_project(session, original_name)
