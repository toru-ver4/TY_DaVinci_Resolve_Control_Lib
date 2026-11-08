# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_fusion.py -q

from types import SimpleNamespace

import pytest

from ty_davinci_resolve import (
    ResolveOperationError,
    ResolveValidationError,
    add_fusion_modifier,
    add_fusion_tool,
    connect_input,
    connect_default_output,
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


def test_default_connection_uses_main_connectors_with_nonstandard_names() -> None:
    mask_output = object()
    connected = []
    source = SimpleNamespace(FindMainOutput=lambda index: mask_output if index == 1 else None)
    target = SimpleNamespace(FindMainInput=lambda index: SimpleNamespace(
        ConnectTo=lambda output: connected.append(output) or True,
    ) if index == 1 else None)
    connect_default_output(source, target)
    assert connected == [mask_output]


def test_missing_main_output_does_not_disconnect_existing_input() -> None:
    connected = []
    source = SimpleNamespace(FindMainOutput=lambda index: None)
    target = SimpleNamespace(FindMainInput=lambda index: SimpleNamespace(
        ConnectTo=lambda output: connected.append(output) or True,
    ))
    with pytest.raises(ResolveValidationError):
        connect_default_output(source, target)
    assert connected == []


@pytest.mark.parametrize("value", [[0.2, 0.3], (0.2, 0.3), {1: 0.2, 2: 0.3}])
def test_point_input_accepts_normalized_three_component_readback(value) -> None:
    tool = FakeTool()
    tool.GetInput = lambda name: {1: 0.2 + 1e-8, 2: 0.3, 3: 0.0}
    set_fusion_tool_input(tool, "Center", value)


def test_point_input_still_rejects_changed_coordinates() -> None:
    tool = FakeTool()
    tool.GetInput = lambda name: {1: 0.2, 2: 0.3, 3: 1.0}
    with pytest.raises(ResolveOperationError):
        set_fusion_tool_input(tool, "Center", [0.2, 0.3])


@pytest.mark.parametrize("remote", [False, True])
def test_empty_readback_is_not_accepted_even_for_remote_values(remote) -> None:
    tool = FakeTool()
    tool.GetInput = lambda name: None
    tool.GetInputList = lambda: {}
    value = type("PyRemoteObject", (), {})() if remote else 0.5
    with pytest.raises(ResolveValidationError if remote else ResolveOperationError):
        set_fusion_tool_input(tool, "MissingInput", value)


def test_remote_mask_is_verified_by_connection_before_image_evaluation() -> None:
    tool = FakeTool()
    connector = SimpleNamespace(
        GetAttrs=lambda: {"INPS_ID": "EffectMask"},
        GetConnectedOutput=lambda: object(),
    )
    tool.GetInputList = lambda: {1: connector}
    tool.GetInput = lambda name: None
    value = type("PyRemoteObject", (), {})()
    set_fusion_tool_input(tool, "EffectMask", value)
    connector.GetConnectedOutput = lambda: None
    with pytest.raises(ResolveOperationError):
        set_fusion_tool_input(tool, "EffectMask", value)
