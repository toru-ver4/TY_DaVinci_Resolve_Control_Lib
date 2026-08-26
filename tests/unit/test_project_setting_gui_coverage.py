# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_project_setting_gui_coverage.py -q

from __future__ import annotations

import json
import re
from pathlib import Path

from ty_davinci_resolve import ProjectSetting


ROOT = Path(__file__).resolve().parents[2]
COVERAGE_PATH = ROOT / "docs" / "project-setting-gui-coverage.json"
DOCUMENT_PATH = ROOT / "docs" / "project-settings.md"


def test_all_project_settings_have_an_explicit_gui_review_status() -> None:
    coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    documented = set(coverage["documented_gui"])
    pending = set(coverage["pending_gui_review"])
    actual = {setting.name for setting in ProjectSetting}

    assert documented.isdisjoint(pending)
    assert documented | pending == actual


def test_documented_gui_settings_are_present_in_the_document() -> None:
    coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    document = DOCUMENT_PATH.read_text(encoding="utf-8")

    for name in coverage["documented_gui"]:
        pattern = rf"`[^`]*\b{re.escape(name)}\b[^`]*`"
        assert re.search(pattern, document)
