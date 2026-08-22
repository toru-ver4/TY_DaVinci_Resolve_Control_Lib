# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_project.py -q

from types import SimpleNamespace

import pytest

from ty_davinci_resolve import (
    ResolveOperationError,
    ResolveSession,
    ResolveValidationError,
    create_project,
    get_timeline,
    list_projects,
    set_settings,
)


class FakeProjectManager:
    def __init__(self) -> None:
        self.names = ["Existing"]
        self.created: list[str] = []

    def GetProjectListInCurrentFolder(self) -> list[str]:
        return self.names

    def CreateProject(self, name: str) -> object:
        self.created.append(name)
        return object()


def make_session(manager: FakeProjectManager) -> ResolveSession:
    resolve = SimpleNamespace(GetProjectManager=lambda: manager)
    return ResolveSession(resolve, object(), "Resolve", (21, 0, 4, 5), "21.0.4.5")


def test_list_projects_returns_immutable_names() -> None:
    assert list_projects(make_session(FakeProjectManager())) == ("Existing",)


def test_create_project_checks_duplicate_before_mutation() -> None:
    manager = FakeProjectManager()
    with pytest.raises(ResolveValidationError):
        create_project(make_session(manager), "Existing")
    assert manager.created == []


def test_create_project_calls_official_api() -> None:
    manager = FakeProjectManager()
    created = create_project(make_session(manager), "New")
    assert created is not None
    assert manager.created == ["New"]


def test_set_settings_stops_at_first_failure() -> None:
    calls: list[tuple[str, str]] = []

    class Project:
        def SetSetting(self, name: str, value: str) -> bool:
            calls.append((name, value))
            return name != "bad"

    with pytest.raises(ResolveOperationError):
        set_settings(Project(), {"good": "1", "bad": "2", "later": "3"})
    assert calls == [("good", "1"), ("bad", "2")]


def test_get_timeline_validates_before_lookup() -> None:
    project = SimpleNamespace(
        GetTimelineCount=lambda: 1,
        GetTimelineByIndex=lambda index: pytest.fail("lookup must not occur"),
    )
    with pytest.raises(ResolveValidationError):
        get_timeline(project, 2)
