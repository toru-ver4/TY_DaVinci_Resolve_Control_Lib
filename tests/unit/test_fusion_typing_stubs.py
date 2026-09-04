# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_fusion_typing_stubs.py -q

from __future__ import annotations

import ast
from pathlib import Path

from ty_davinci_resolve import FusionModifier, FusionResolveFxTool, FusionTool

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_SOURCE = PACKAGE_ROOT / "src" / "ty_davinci_resolve"


def test_add_tool_has_an_overload_for_every_tool_constant() -> None:
    stub_text = (PACKAGE_SOURCE / "fusion.pyi").read_text(encoding="utf-8")
    ast.parse(stub_text)

    expected_literals = {
        *(f"Literal[FusionTool.{member.name}]" for member in FusionTool),
        *(
            f"Literal[FusionResolveFxTool.{member.name}]"
            for member in FusionResolveFxTool
        ),
    }
    assert len(expected_literals) == len(FusionTool) + len(FusionResolveFxTool)
    assert all(literal in stub_text for literal in expected_literals)
    expected_modifier_literals = {
        f"Literal[FusionModifier.{member.name}]" for member in FusionModifier
    }
    assert all(literal in stub_text for literal in expected_modifier_literals)
    assert stub_text.count("@overload") == (
        len(expected_literals) + len(expected_modifier_literals)
    )


def test_fusion_stub_covers_every_public_runtime_function() -> None:
    runtime_tree = ast.parse(
        (PACKAGE_SOURCE / "fusion.py").read_text(encoding="utf-8")
    )
    stub_tree = ast.parse(
        (PACKAGE_SOURCE / "fusion.pyi").read_text(encoding="utf-8")
    )
    runtime_functions = {
        node.name
        for node in runtime_tree.body
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
    }
    stub_functions = {
        node.name
        for node in stub_tree.body
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
    }
    assert stub_functions == runtime_functions


def test_every_tool_constant_has_a_generated_protocol() -> None:
    stub_path = PACKAGE_SOURCE / "fusion_tool_types.pyi"
    tree = ast.parse(stub_path.read_text(encoding="utf-8"))
    protocol_classes = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.ClassDef)
        and node.name not in {
            "FusionCompositionProtocol",
            "FusionInputProtocol",
            "FusionToolProtocol",
        }
    }
    assert len(protocol_classes) == (
        len(FusionTool) + len(FusionResolveFxTool) + len(FusionModifier) - 1
    )

    rectangle = protocol_classes["RectangleMaskTool"]
    rectangle_inputs = {
        statement.target.id
        for statement in rectangle.body
        if isinstance(statement, ast.AnnAssign)
        and isinstance(statement.target, ast.Name)
    }
    assert {"Angle", "Center", "Height", "Width"} <= rectangle_inputs

    xy_path = protocol_classes["XYPathTool"]
    xy_path_inputs = {
        statement.target.id
        for statement in xy_path.body
        if isinstance(statement, ast.AnnAssign)
        and isinstance(statement.target, ast.Name)
    }
    assert {"Center", "X", "Y", "Z"} <= xy_path_inputs


def test_package_declares_inline_typing_support() -> None:
    assert (PACKAGE_SOURCE / "py.typed").is_file()
