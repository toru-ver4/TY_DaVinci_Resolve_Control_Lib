# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_project_setting_gui_coverage.py -q

from __future__ import annotations

import json
import re
from pathlib import Path

from ty_davinci_resolve import ProjectSetting, TimelineSetting


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


def test_versioned_observations_have_valid_constants_and_evidence() -> None:
    coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    classes = {"ProjectSetting": ProjectSetting, "TimelineSetting": TimelineSetting}
    identities = set()
    for record in coverage["observations"]:
        identity = (record["scope"], record["label"], record["condition"])
        assert identity not in identities
        identities.add(identity)
        assert record["resolve_version"] == coverage["resolve_version"]
        assert record["environment"] and record["condition"] and record["evidence"]
        assert record["status"] in {
            "verified_bidirectional", "verified_gui_to_api", "query_only", "unmapped",
        }
        for relative_path in record["evidence"]:
            path = (ROOT / "docs" / relative_path).resolve()
            assert path.is_relative_to(ROOT / "docs")
            assert path.is_file(), relative_path
        for constant in record["ty_constants"]:
            namespace, member = constant.split(".")
            assert classes[namespace][member].value in record["api_keys"]


def test_unmapped_gui_controls_are_not_assigned_api_constants() -> None:
    coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    unmapped = [r for r in coverage["observations"] if r["status"] == "unmapped"]
    assert any(r["label"] == "Limit output gamut to" for r in unmapped)
    for record in unmapped:
        assert record["api_keys"] == []
        assert record["ty_constants"] == []
