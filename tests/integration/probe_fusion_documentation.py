# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: .venv313/Scripts/python.exe tests/integration/probe_fusion_documentation.py
# Read-only audit of documents and source; does not connect to Resolve.

"""Inventory the 21.2.0 Fusion reference without executing its examples."""

import ast
import hashlib
import json
from pathlib import Path
import re

from ty_davinci_resolve import FusionModifier, FusionTool


def main() -> None:
    """Compare documented IDs and explicit control tables with current stubs.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Notes
    -----
    Missing headings can be aliases or typed modifier families. Missing inputs
    can be conditional or dynamic controls. Neither list is an API deletion
    report, nor a reason to add unverified constants or inputs automatically.

    Examples
    --------
    >>> main()  # doctest: +SKIP
    """
    root = Path(__file__).resolve().parents[2]
    official = root / "official_documents/21.2.0_Fusion"
    installed = Path("C:/ProgramData/Blackmagic Design/DaVinci Resolve/Support/Developer/Fusion")
    sources = {}
    for name in ("FusionTools.md", "FusionToolReference.md"):
        data = (official / name).read_bytes()
        sources[name] = {
            "sha256": hashlib.sha256(data).hexdigest(),
            "matches_installed": data == (installed / name).read_bytes(),
        }
        if not sources[name]["matches_installed"]:
            raise RuntimeError(f"Installed Fusion document differs: {name}")
    reference = (official / "FusionToolReference.md").read_text(encoding="utf-8")
    sections = re.findall(
        r"^## (.+?) \(`([^`]+)`\)\s*\n(.*?)(?=^## |\Z)",
        reference, re.MULTILINE | re.DOTALL,
    )
    if not sections:
        raise RuntimeError("No Fusion reference headings were parsed.")
    constants = set(FusionTool) | set(FusionModifier)
    ids = {tool_id for _, tool_id, _ in sections}
    tool_stub = ast.parse((root / "src/ty_davinci_resolve/fusion_tool_types.pyi").read_text(encoding="utf-8"))
    stub_fields = {
        cls.name: {node.target.id for node in cls.body if isinstance(node, ast.AnnAssign)}
        for cls in tool_stub.body if isinstance(cls, ast.ClassDef)
    }
    facade = ast.parse((root / "src/ty_davinci_resolve/fusion.pyi").read_text(encoding="utf-8"))
    protocol_by_id = {}
    for node in facade.body:
        if not isinstance(node, ast.FunctionDef) or node.name not in {"add_fusion_tool", "add_fusion_modifier"}:
            continue
        arg = node.args.args[1].annotation
        if isinstance(arg, ast.Subscript) and isinstance(arg.slice, ast.Attribute):
            enum = {"FusionTool": FusionTool, "FusionModifier": FusionModifier}.get(arg.slice.value.id)
            if enum is not None:
                protocol_by_id[enum[arg.slice.attr].value] = node.returns.id
    controls = []
    for label, tool_id, body in sections:
        if tool_id not in protocol_by_id:
            continue
        listed = set()
        in_control_table = False
        for line in body.splitlines():
            if not line.startswith("|"):
                in_control_table = False
                continue
            cells = [cell.strip() for cell in line.strip("|").split("|")]
            if len(cells) > 1 and cells[1] == "ID":
                in_control_table = True
            elif in_control_table and len(cells) > 1:
                listed.update(re.findall(r"`([A-Za-z_]\w*(?:\.\w+)*)`", cells[1]))
        fields = stub_fields[protocol_by_id[tool_id]]
        absent = listed - fields
        dotted = {name for name in absent if "." in name}
        numbered = {
            name for name in absent
            if re.search(re.escape(f"`{name}`") + r"\*[a-z]\*", body)
        }
        reserved = absent & {"Delete"}
        controls.append({
            "id": tool_id, "label": label,
            "documented_control_ids": sorted(listed),
            "absent_from_generated_attributes": sorted(absent),
            "attribute_gap_classification": {
                "dotted_ids_use_item_syntax": sorted(dotted),
                "numbered_id_templates": sorted(numbered),
                "reserved_method_names_use_item_syntax": sorted(reserved),
                "unclassified": sorted(absent - dotted - numbered - reserved),
            },
        })
    result = {
        "sources": sources, "reference_tool_sections": len(sections),
        "unique_reference_ids": len(ids), "unique_public_native_modifier_ids": len(constants),
        "public_ids_with_exact_heading": len(constants & ids),
        "public_ids_without_exact_heading": sorted(constants - ids),
        "documented_outside_public_enums": sorted(ids - constants),
        "control_table_comparisons": controls,
        "notes": [
            "Krokodove and additional modifiers are outside the curated public enums.",
            "Perturb*, Publish* and Switch* are families, not AddTool IDs.",
            "Dotted IDs use item syntax and are intentionally omitted from attribute completion.",
            "Overview/reference coverage is not a complete registry or a live behavior guarantee.",
        ],
    }
    output = root / "docs/verification/21.2.0.5/fusion-documentation-audit.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Reviewed {len(sections)} tool sections; {len(constants & ids)}/{len(constants)} public IDs have exact headings.")
    missing = [row for row in controls if row["absent_from_generated_attributes"]]
    print(f"Control tables with attributes requiring review: {len(missing)}")


if __name__ == "__main__":
    main()
