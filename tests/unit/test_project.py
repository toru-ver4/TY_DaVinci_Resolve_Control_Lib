# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_project.py -q

from types import SimpleNamespace

import pytest

from ty_davinci_resolve import (
    ProjectLifecycleTiming,
    ResolveOperationError,
    ResolveSession,
    ResolveValidationError,
    create_project,
    get_timeline,
    list_projects,
    load_project,
    set_project_settings,
)


class FakeProjectManager:
    def __init__(self) -> None:
        self.names = ["Existing"]
        self.created: list[str] = []
        self.current = None

    def GetProjectListInCurrentFolder(self) -> list[str]:
        return self.names

    def CreateProject(self, name: str) -> object:
        self.created.append(name)
        self.names.append(name)
        self.current = SimpleNamespace(GetName=lambda: name)
        return self.current

    def GetCurrentProject(self) -> object | None:
        return self.current


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


def test_load_project_waits_before_touching_returned_proxy(monkeypatch) -> None:
    slept = False
    project = SimpleNamespace(GetName=lambda: "Existing")

    class Manager(FakeProjectManager):
        def LoadProject(self, name: str) -> object:
            self.current = project
            return SimpleNamespace(
                GetName=lambda: pytest.fail("returned proxy must not be touched")
            )

        def GetCurrentProject(self) -> object:
            assert slept
            return self.current

    def fake_sleep(seconds: float) -> None:
        nonlocal slept
        assert seconds == 1.5
        slept = True

    monkeypatch.setattr("ty_davinci_resolve.project.time.sleep", fake_sleep)
    loaded = load_project(make_session(Manager()), "Existing")
    assert loaded is project


def test_project_lifecycle_timing_rejects_negative_delay() -> None:
    with pytest.raises(ResolveValidationError):
        ProjectLifecycleTiming(load_delay=-0.1)


def test_set_project_settings_stops_at_first_failure() -> None:
    calls: list[tuple[str, str]] = []

    class Project:
        def SetSetting(self, name: str, value: str) -> bool:
            calls.append((name, value))
            return name != "bad"

    with pytest.raises(ResolveOperationError):
        set_project_settings(Project(), {"good": "1", "bad": "2", "later": "3"})
    assert calls == [("good", "1"), ("bad", "2")]


def test_get_timeline_validates_before_lookup() -> None:
    project = SimpleNamespace(
        GetTimelineCount=lambda: 1,
        GetTimelineByIndex=lambda index: pytest.fail("lookup must not occur"),
    )
    with pytest.raises(ResolveValidationError):
        get_timeline(project, 2)
