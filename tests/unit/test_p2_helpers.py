# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_p2_helpers.py -q

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest
import ty_davinci_resolve.fusion as fusion_module

from ty_davinci_resolve import (
    ResolveOperationError,
    ResolveSession,
    ResolveValidationError,
    build_fusion_rectangle,
    get_fusion_fonts,
    get_packaged_fusion_duration_media,
    select_fusion_duration_media,
    set_fusion_tool_flow_position,
)


class FakeTool:
    def __init__(self, tool_type: str, position: tuple[float, float]) -> None:
        self.tool_type = tool_type
        self.position = position
        self.values: dict[str, object] = {}

    def SetInput(self, name: str, value: object) -> None:
        self.values[name] = value

    def GetInput(self, name: str) -> object:
        return self.values[name]


class FakeComp:
    def __init__(self) -> None:
        self.tools: list[FakeTool] = []
        self.CurrentFrame: object | None = None

    def AddTool(self, tool_type: str, x: float, y: float) -> FakeTool:
        tool = FakeTool(tool_type, (x, y))
        self.tools.append(tool)
        return tool


class FakeFlow:
    def __init__(self) -> None:
        self.positions: dict[int, tuple[float, float]] = {}

    def SetPos(self, tool: object, x: float, y: float) -> None:
        self.positions[id(tool)] = (x, y)

    def GetPosTable(self, tool: object) -> dict[int, float]:
        x, y = self.positions[id(tool)]
        return {1: x, 2: y}


def make_session(resolve: object) -> ResolveSession:
    return ResolveSession(
        resolve,
        object(),
        "Resolve",
        (21, 0, 4, 5),
        "21.0.4.5",
    )


def test_build_fusion_rectangle_creates_masked_background() -> None:
    comp = FakeComp()

    background = build_fusion_rectangle(
        comp,
        (0.1, 0.2, 0.3, 0.4),
        center=(0.25, 0.75),
        width=0.2,
        height=0.3,
        position=(2, 4),
    )

    mask, created_background = comp.tools
    assert background is created_background
    assert mask.tool_type == "RectangleMask"
    assert mask.position == (2, 3)
    assert mask.values == {
        "Center": {1: 0.25, 2: 0.75, 3: 0.0},
        "Width": 0.2,
        "Height": 0.3,
    }
    assert background.values["TopLeftAlpha"] == 0.4
    assert background.values["EffectMask"] is mask


def test_get_fusion_fonts_normalizes_and_freezes_mapping() -> None:
    fusion = SimpleNamespace(
        FontManager=SimpleNamespace(
            GetFontList=lambda: {
                "Z Family": ["Bold", "Regular", "Bold"],
                "A Family": {"Light": object(), "Regular": object()},
            }
        )
    )

    fonts = get_fusion_fonts(fusion)

    assert tuple(fonts) == ("A Family", "Z Family")
    assert fonts["A Family"] == ("Light", "Regular")
    assert fonts["Z Family"] == ("Bold", "Regular")
    with pytest.raises(TypeError):
        fonts["New"] = ("Regular",)  # type: ignore[index]


def test_set_fusion_tool_flow_position_requires_explicit_page_activation() -> None:
    comp = FakeComp()
    tool = object()
    flow = FakeFlow()
    opened: list[str] = []

    def open_page(page: str) -> bool:
        opened.append(page)
        comp.CurrentFrame = SimpleNamespace(FlowView=flow)
        return True

    session = make_session(SimpleNamespace(OpenPage=open_page))

    with pytest.raises(ResolveOperationError):
        set_fusion_tool_flow_position(comp, tool, (1, 2))

    set_fusion_tool_flow_position(
        comp,
        tool,
        (1, 2),
        session=session,
        activate_fusion_page=True,
    )

    assert opened == ["fusion"]
    assert flow.positions[id(tool)] == (1, 2)


def test_set_fusion_tool_flow_position_rejects_activation_without_session() -> None:
    comp = FakeComp()
    with pytest.raises(ResolveValidationError):
        set_fusion_tool_flow_position(
            comp,
            object(),
            (1, 2),
            activate_fusion_page=True,
        )


def test_set_fusion_tool_flow_position_waits_for_current_frame(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    tool = object()
    flow = FakeFlow()

    class DelayedComp:
        def __init__(self) -> None:
            self.read_count = 0

        @property
        def CurrentFrame(self) -> object | None:
            self.read_count += 1
            if self.read_count < 4:
                return None
            return SimpleNamespace(FlowView=flow)

    comp = DelayedComp()
    session = make_session(SimpleNamespace(OpenPage=lambda page: True))
    monkeypatch.setattr(fusion_module.time, "sleep", lambda seconds: None)

    set_fusion_tool_flow_position(
        comp,
        tool,
        (3, 4),
        session=session,
        activate_fusion_page=True,
    )

    assert comp.read_count == 4
    assert flow.positions[id(tool)] == (3, 4)


def test_select_fusion_duration_media_uses_normalized_filename(tmp_path: Path) -> None:
    media = tmp_path / "dummy_video_1280x720_23.976P.mp4"
    media.write_bytes(b"dummy")

    selected = select_fusion_duration_media(tmp_path, 1280, 720, "23.9760")

    assert selected == media


def test_select_fusion_duration_media_fails_before_use(tmp_path: Path) -> None:
    with pytest.raises(ResolveValidationError, match="does not exist"):
        select_fusion_duration_media(tmp_path, 1920, 1080, 24)


def test_packaged_fusion_duration_media_exists() -> None:
    selected = get_packaged_fusion_duration_media(1280, 720, "23.9760")

    assert selected.is_file()
    assert selected.name == "dummy_video_1280x720_23.976P.mp4"
