# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_fusion.py -q

from types import SimpleNamespace

import pytest

from ty_davinci_resolve import (
    ResolveOperationError,
    add_fusion_modifier,
    add_fusion_tool,
    connect_input,
    get_fusion_tool,
    set_fusion_tool_input,
    set_fusion_tool_inputs,
)


class FakeTool:
    def __init__(self, name: str = "Background1") -> None:
        self.Name = name
        self.values: dict[str, object] = {}
        self.connections: list[tuple[str, object]] = []

    def SetInput(self, name: str, value: object) -> None:
        self.values[name] = value

    def GetInput(self, name: str) -> object:
        return self.values[name]

    def ConnectInput(self, name: str, source: object) -> bool:
        self.connections.append((name, source))
        return True


def test_add_and_find_tool() -> None:
    tool = FakeTool()
    comp = SimpleNamespace(
        AddTool=lambda tool_type, x, y: tool,
        GetToolList=lambda: {1: tool},
    )
    assert add_fusion_tool(comp, "Background", (1, 2)) is tool
    assert get_fusion_tool(comp, "Background1") is tool


def test_add_fusion_modifier_uses_hidden_flow_position() -> None:
    modifier = FakeTool("XYPath1")
    calls: list[tuple[str, float, float]] = []

    def add_tool_call(tool_type: str, x: float, y: float) -> FakeTool:
        calls.append((tool_type, x, y))
        return modifier

    comp = SimpleNamespace(AddTool=add_tool_call)
    assert add_fusion_modifier(comp, "XYPath") is modifier
    assert calls == [("XYPath", 0.0, 0.0)]


def test_missing_tool_raises_operation_error() -> None:
    comp = SimpleNamespace(GetToolList=lambda: {})
    with pytest.raises(ResolveOperationError):
        get_fusion_tool(comp, "Missing")


def test_connect_input_uses_named_target_input() -> None:
    target = FakeTool("MediaOut1")
    source = FakeTool()
    connect_input(target, "Input", source)
    assert target.connections == [("Input", source)]


def test_set_fusion_tool_inputs_verifies_scalars_and_dicts() -> None:
    tool = FakeTool()
    values = {"Gain": 0.5, "Label": "test", "Center": {1: 0.5, 2: 0.5}}
    set_fusion_tool_inputs(tool, values)
    assert tool.values == values


def test_set_fusion_tool_input_detects_readback_mismatch() -> None:
    tool = FakeTool()
    tool.GetInput = lambda name: 0.25  # type: ignore[method-assign]
    with pytest.raises(ResolveOperationError):
        set_fusion_tool_input(tool, "Gain", 0.5)
