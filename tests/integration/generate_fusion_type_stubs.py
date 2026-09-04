# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python tests/integration/generate_fusion_type_stubs.py --output-directory src/ty_davinci_resolve

"""Generate Fusion Tool typing stubs from a running Resolve instance."""

from __future__ import annotations

import argparse
import ast
from collections.abc import Iterable
import json
import keyword
from pathlib import Path
import sys
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = PACKAGE_ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from ty_davinci_resolve import (
    FusionModifier,
    FusionResolveFxTool,
    FusionTool,
    ResolveSession,
)


_RESERVED_TOOL_ATTRIBUTES = frozenset(
    {
        "ID",
        "Name",
        "ConnectInput",
        "Delete",
        "GetAttrs",
        "GetInputList",
        "GetOutputList",
        "SetInput",
    }
)
_PASCAL_ACRONYMS = frozenset(
    {
        "2D",
        "3D",
        "ACES",
        "CDL",
        "DCTL",
        "DVE",
        "FBX",
        "HSL",
        "LUT",
        "OCIO",
        "OFX",
        "RTXHDR",
        "SSAO",
        "TV",
        "USD",
        "UV",
        "XY",
    }
)


def _class_name(member_name: str, *, resolve_fx: bool) -> str:
    """Return a deterministic Tool Protocol class name.

    Parameters
    ----------
    member_name
        Enum member name in upper snake case.
    resolve_fx
        Prefix the class to distinguish Resolve FX from native Tools.

    Returns
    -------
    str
        Pascal-case Protocol class name.

    Examples
    --------
    >>> _class_name("RECTANGLE_MASK", resolve_fx=False)
    'RectangleMaskTool'
    """
    parts = [
        part if part in _PASCAL_ACRONYMS else part.title()
        for part in member_name.split("_")
    ]
    prefix = "ResolveFx" if resolve_fx else ""
    return f"{prefix}{''.join(parts)}Tool"


def _input_ids(tool: Any) -> tuple[str, ...]:
    """Return statically representable input IDs for one Fusion Tool.

    Parameters
    ----------
    tool
        Fusion Tool remote object.

    Returns
    -------
    tuple of str
        Sorted unique Python attribute names.

    Examples
    --------
    >>> _input_ids(tool)  # doctest: +SKIP
    ('Center', 'Height', 'Width')
    """
    inputs = tool.GetInputList()
    if not isinstance(inputs, dict):
        return ()
    names: set[str] = set()
    for input_object in inputs.values():
        attrs = input_object.GetAttrs()
        input_id = attrs.get("INPS_ID") if isinstance(attrs, dict) else None
        if (
            isinstance(input_id, str)
            and input_id.isidentifier()
            and not keyword.iskeyword(input_id)
            and input_id not in _RESERVED_TOOL_ATTRIBUTES
        ):
            names.add(input_id)
    return tuple(sorted(names, key=str.casefold))


def _inspect_tools(
    comp: Any,
    members: Iterable[FusionModifier | FusionTool | FusionResolveFxTool],
) -> tuple[dict[str, tuple[str, ...]], dict[str, str]]:
    """Inspect Tool inputs once, recording failures without retrying.

    Parameters
    ----------
    comp
        Hidden temporary Fusion Composition.
    members
        Fusion Tool enum members to inspect.

    Returns
    -------
    tuple of dict
        Input IDs by enum member and failure messages by enum member.

    Examples
    --------
    >>> _inspect_tools(comp, [FusionTool.RECTANGLE_MASK])  # doctest: +SKIP
    """
    inputs_by_member: dict[str, tuple[str, ...]] = {}
    failures: dict[str, str] = {}
    for member in members:
        tool = None
        try:
            tool = comp.AddTool(member.value, 0, 0)
            if tool is None:
                failures[member.name] = "Composition.AddTool returned None"
                inputs_by_member[member.name] = ()
                continue
            inputs_by_member[member.name] = _input_ids(tool)
        except Exception as error:
            failures[member.name] = f"{type(error).__name__}: {error}"
            inputs_by_member[member.name] = ()
        finally:
            if tool is not None:
                try:
                    tool.Delete()
                except Exception:
                    pass
    return inputs_by_member, failures


def _render_tool_types(
    native_inputs: dict[str, tuple[str, ...]],
    modifier_inputs: dict[str, tuple[str, ...]],
    resolve_fx_inputs: dict[str, tuple[str, ...]],
) -> str:
    """Render Tool Protocol declarations.

    Parameters
    ----------
    native_inputs
        Native Fusion inputs keyed by enum member name.
    modifier_inputs
        Fusion Modifier inputs keyed by enum member name.
    resolve_fx_inputs
        Resolve FX inputs keyed by enum member name.

    Returns
    -------
    str
        Complete ``fusion_tool_types.pyi`` source.

    Examples
    --------
    >>> 'RectangleMaskTool' in _render_tool_types(
    ...     {'RECTANGLE_MASK': ('Width',)}, {}, {}
    ... )
    True
    """
    lines = [
        '"""Generated Fusion remote-object Protocols for editor completion."""',
        "",
        "from typing import Any, Protocol",
        "",
        "",
        "class FusionInputProtocol(Protocol):",
        "    def __getitem__(self, frame: int | float) -> Any: ...",
        "    def __setitem__(self, frame: int | float, value: Any) -> None: ...",
        "",
        "",
        "class FusionToolProtocol(Protocol):",
        "    ID: str",
        "    Name: str",
        "    def ConnectInput(self, name: str, source: Any) -> bool: ...",
        "    def Delete(self) -> bool: ...",
        "    def GetAttrs(self) -> dict[str, Any]: ...",
        "    def GetInputList(self) -> dict[int, FusionInputProtocol]: ...",
        "    def SetInput(self, name: str, value: Any) -> bool: ...",
        "",
        "",
        "class FusionCompositionProtocol(Protocol):",
        "    def AddTool(self, tool_type: str, x: float, y: float) -> FusionToolProtocol | None: ...",
        "    def BezierSpline(self, settings: Any = ...) -> FusionInputProtocol: ...",
        "    def GetToolList(self, selected: bool = ..., reg_id: str | None = ...) -> dict[Any, FusionToolProtocol]: ...",
    ]

    declarations = {
        _class_name(name, resolve_fx=False): inputs
        for name, inputs in native_inputs.items()
    }
    declarations.update(
        {
            _class_name(name, resolve_fx=False): inputs
            for name, inputs in modifier_inputs.items()
        }
    )
    declarations.update(
        {
            _class_name(name, resolve_fx=True): inputs
            for name, inputs in resolve_fx_inputs.items()
        }
    )
    for class_name, input_ids in sorted(declarations.items()):
        lines.extend(["", "", f"class {class_name}(FusionToolProtocol, Protocol):"])
        if input_ids:
            lines.extend(f"    {input_id}: Any" for input_id in input_ids)
        else:
            lines.append("    pass")
    return "\n".join(lines) + "\n"


def _render_function_stub(node: ast.FunctionDef) -> str:
    """Render a public implementation function as a stub declaration.

    Parameters
    ----------
    node
        Parsed public function definition.

    Returns
    -------
    str
        Function signature followed by an ellipsis body.

    Examples
    --------
    >>> node = ast.parse('def f(value: int) -> str: return str(value)').body[0]
    >>> _render_function_stub(node)
    'def f(value: int) -> str:\\n    ...'
    """
    node = ast.FunctionDef(
        name=node.name,
        args=node.args,
        body=[ast.Expr(value=ast.Constant(value=Ellipsis))],
        decorator_list=[],
        returns=node.returns,
        type_comment=None,
        type_params=getattr(node, "type_params", []),
    )
    return ast.unparse(ast.fix_missing_locations(node))


def _render_fusion_stub() -> str:
    """Render ``fusion.pyi`` with one overload per known Tool enum member.

    Returns
    -------
    str
        Complete ``fusion.pyi`` source.

    Examples
    --------
    >>> 'FusionTool.RECTANGLE_MASK' in _render_fusion_stub()
    True
    """
    lines = [
        '"""Typing facade for Resolve-hosted Fusion helpers."""',
        "",
        "from collections.abc import Mapping, Sequence",
        "from pathlib import Path",
        "from typing import Any, Literal, overload",
        "",
        "from .connection import ResolveSession",
        "from .fusion_tool_constants import FusionModifier, FusionResolveFxTool, FusionTool",
        "from .fusion_tool_types import *",
        "",
        "PACKAGED_DURATION_MEDIA_DIRECTORY: Path",
        "",
    ]
    for member in FusionTool:
        class_name = _class_name(member.name, resolve_fx=False)
        lines.extend(
            [
                "@overload",
                "def add_fusion_tool(",
                "    comp: Any,",
                f"    tool_type: Literal[FusionTool.{member.name}],",
                "    position: Sequence[float] = ...,",
                f") -> {class_name}: ...",
                "",
            ]
        )
    for member in FusionResolveFxTool:
        class_name = _class_name(member.name, resolve_fx=True)
        lines.extend(
            [
                "@overload",
                "def add_fusion_tool(",
                "    comp: Any,",
                f"    tool_type: Literal[FusionResolveFxTool.{member.name}],",
                "    position: Sequence[float] = ...,",
                f") -> {class_name}: ...",
                "",
            ]
        )
    lines.extend(
        [
            "def add_fusion_tool(",
            "    comp: Any,",
            "    tool_type: str,",
            "    position: Sequence[float] = ...,",
            ") -> FusionToolProtocol: ...",
            "",
        ]
    )

    for member in FusionModifier:
        class_name = _class_name(member.name, resolve_fx=False)
        lines.extend(
            [
                "@overload",
                "def add_fusion_modifier(",
                "    comp: Any,",
                f"    modifier_type: Literal[FusionModifier.{member.name}],",
                f") -> {class_name}: ...",
                "",
            ]
        )
    lines.extend(
        [
            "def add_fusion_modifier(",
            "    comp: Any,",
            "    modifier_type: str,",
            ") -> FusionToolProtocol: ...",
            "",
        ]
    )

    tree = ast.parse((SOURCE_ROOT / "ty_davinci_resolve" / "fusion.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.FunctionDef) or node.name.startswith("_"):
            continue
        if node.name in {"add_fusion_modifier", "add_fusion_tool"}:
            continue
        if node.name == "add_fusion_composition_to_clip":
            node.returns = ast.Name(id="FusionCompositionProtocol")
        elif node.name == "get_fusion_tool":
            node.returns = ast.Name(id="FusionToolProtocol")
        elif node.name == "add_fusion_composition_to_timeline":
            node.returns = ast.parse(
                "tuple[Any, FusionCompositionProtocol]", mode="eval"
            ).body
        lines.extend([_render_function_stub(node), "", ""])
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    """Inspect Resolve once and write deterministic typing stubs.

    Returns
    -------
    None

    Examples
    --------
    >>> main()  # doctest: +SKIP
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-directory", type=Path, required=True)
    args = parser.parse_args()
    output_directory = args.output_directory.resolve()
    expected_directory = (SOURCE_ROOT / "ty_davinci_resolve").resolve()
    if output_directory != expected_directory:
        raise RuntimeError(f"Unexpected output directory: {output_directory}")

    session = ResolveSession.connect()
    comp = session.fusion.NewComp(True, True, True)
    if comp is None:
        raise RuntimeError("Fusion.NewComp failed to create a hidden Composition.")
    try:
        native_inputs, native_failures = _inspect_tools(comp, FusionTool)
        modifier_inputs, modifier_failures = _inspect_tools(
            comp, FusionModifier
        )
        resolve_fx_inputs, resolve_fx_failures = _inspect_tools(
            comp, FusionResolveFxTool
        )
    finally:
        comp.Close()

    (output_directory / "fusion_tool_types.pyi").write_text(
        _render_tool_types(native_inputs, modifier_inputs, resolve_fx_inputs),
        encoding="utf-8",
    )
    (output_directory / "fusion.pyi").write_text(
        _render_fusion_stub(), encoding="utf-8"
    )
    summary = {
        "fusion_tools": len(native_inputs),
        "fusion_tools_with_inputs": sum(bool(value) for value in native_inputs.values()),
        "fusion_tool_failures": native_failures,
        "fusion_modifiers": len(modifier_inputs),
        "fusion_modifiers_with_inputs": sum(
            bool(value) for value in modifier_inputs.values()
        ),
        "fusion_modifier_failures": modifier_failures,
        "resolve_fx_tools": len(resolve_fx_inputs),
        "resolve_fx_tools_with_inputs": sum(
            bool(value) for value in resolve_fx_inputs.values()
        ),
        "resolve_fx_failures": resolve_fx_failures,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
