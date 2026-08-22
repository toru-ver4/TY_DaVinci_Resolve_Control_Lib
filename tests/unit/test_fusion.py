# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_fusion.py -q

from types import SimpleNamespace

import pytest

from ty_davinci_resolve import (
    ResolveOperationError,
    add_tool,
    connect_input,
    get_tool,
    set_tool_input,
    set_tool_inputs,
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
    assert add_tool(comp, "Background", (1, 2)) is tool
    assert get_tool(comp, "Background1") is tool


def test_missing_tool_raises_operation_error() -> None:
    comp = SimpleNamespace(GetToolList=lambda: {})
    with pytest.raises(ResolveOperationError):
        get_tool(comp, "Missing")


def test_connect_input_uses_named_target_input() -> None:
    target = FakeTool("MediaOut1")
    source = FakeTool()
    connect_input(target, "Input", source)
    assert target.connections == [("Input", source)]


def test_set_tool_inputs_verifies_scalars_and_dicts() -> None:
    tool = FakeTool()
    values = {"Gain": 0.5, "Label": "test", "Center": {1: 0.5, 2: 0.5}}
    set_tool_inputs(tool, values)
    assert tool.values == values


def test_set_tool_input_detects_readback_mismatch() -> None:
    tool = FakeTool()
    tool.GetInput = lambda name: 0.25  # type: ignore[method-assign]
    with pytest.raises(ResolveOperationError):
        set_tool_input(tool, "Gain", 0.5)
