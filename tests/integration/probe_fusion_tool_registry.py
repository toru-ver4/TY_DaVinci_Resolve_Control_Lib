# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python tests/integration/probe_fusion_tool_registry.py

"""Print Python enums for Blackmagic-provided Fusion tool Registry IDs."""

from __future__ import annotations

import re
from pathlib import Path
import sys
from typing import Any

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = PACKAGE_ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from ty_davinci_resolve.connection import ResolveSession


_BLACKMAGIC_OFX_PREFIXES = (
    "ofx.com.blackmagicdesign.resolvefx.",
    "ofx.com.blackmagicdesign.openfx.",
)
_BUILTIN_WITHOUT_FILENAME = frozenset({"MtlBlinn", "Note", "Underlay"})
_CURATED_FUSION_MODIFIER_IDS = (
    "BezierSpline",
    "BSplinePath",
    "Expression",
    "Offset",
    "Path",
    "PerturbNumber",
    "PerturbPoint",
    "PolyPath",
    "Shake",
    "TrackerModifier",
    "XYPath",
)


def _member_name(registry_id: str, *, prefixes: tuple[str, ...] = ()) -> str:
    """Convert one Fusion Registry ID to a Python enum member name.

    Parameters
    ----------
    registry_id
        Fusion Tool Registry ID.
    prefixes
        Optional prefixes removed before conversion.

    Returns
    -------
    str
        Upper snake-case enum member name.

    Examples
    --------
    >>> _member_name("RectangleMask")
    'RECTANGLE_MASK'
    """
    stem = registry_id
    for prefix in prefixes:
        if stem.startswith(prefix):
            stem = stem[len(prefix) :]
            break
    stem = re.sub(r"(?<=[A-Za-z])([23])D", r"_\1D", stem)
    stem = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", stem)
    stem = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", stem)
    stem = re.sub(r"[^A-Za-z0-9]+", "_", stem).strip("_").upper()
    stem = stem.replace("_3_D", "_3D").replace("_2_D", "_2D")
    stem = {
        "CLEAN_P_LATE": "CLEAN_PLATE",
        "OCIOCDL_TRANSFORM": "OCIO_CDL_TRANSFORM",
    }.get(stem, stem)
    if not stem or stem[0].isdigit():
        stem = f"TOOL_{stem}"
    return stem


def _is_blackmagic_fusion_tool(attrs: dict[str, Any]) -> bool:
    """Return whether Registry attributes describe a bundled non-OFX Tool.

    Parameters
    ----------
    attrs
        Mapping returned by ``Registry.GetAttrs``.

    Returns
    -------
    bool
        ``True`` for a public Blackmagic-provided Fusion Tool.

    Examples
    --------
    >>> _is_blackmagic_fusion_tool({"REGS_ID": "Background", "REGS_FileName": ":/FusionApp/tool"})
    True
    """
    registry_id = str(attrs.get("REGS_ID", ""))
    if registry_id.startswith("ofx.") or registry_id.startswith("KD_"):
        return False
    filename = str(attrs.get("REGS_FileName", ""))
    if registry_id in _BUILTIN_WITHOUT_FILENAME:
        return True
    if filename.startswith(":/FusionApp/"):
        return True
    normalized = filename.replace("/", "\\").lower()
    return (
        "blackmagic design\\davinci resolve\\" in normalized
        and "\\krokodove.plugin" not in normalized
    )


def _enum_lines(
    rows: list[dict[str, Any]],
    *,
    prefixes: tuple[str, ...] = (),
) -> list[str]:
    """Render Registry rows as deterministic enum assignments.

    Parameters
    ----------
    rows
        Fusion Registry attribute mappings.
    prefixes
        Registry ID prefixes omitted from member names.

    Returns
    -------
    list of str
        Sorted indented assignment lines.

    Examples
    --------
    >>> _enum_lines([{"REGS_ID": "Background", "REGS_Name": "Background"}])
    ['    BACKGROUND = "Background"']
    """
    assignments: dict[str, tuple[str, str]] = {}
    for attrs in rows:
        registry_id = str(attrs["REGS_ID"])
        member = _member_name(registry_id, prefixes=prefixes)
        display_name = str(attrs.get("REGS_Name", registry_id))
        if member in assignments and assignments[member][0] != registry_id:
            raise RuntimeError(
                f"Enum member collision: {member} maps to "
                f"{assignments[member][0]!r} and {registry_id!r}."
            )
        assignments[member] = (registry_id, display_name)

    lines: list[str] = []
    for member, (registry_id, display_name) in sorted(assignments.items()):
        line = f"    {member} = {registry_id!r}"
        if display_name != registry_id:
            line += f"  # {display_name}"
        lines.append(line.replace("'", '"'))
    return lines


def main() -> None:
    """Print the current Blackmagic Fusion Tool enums to standard output.

    Returns
    -------
    None

    Examples
    --------
    >>> main()  # doctest: +SKIP
    """
    session = ResolveSession.connect()
    summary = session.fusion.GetRegSummary(session.fusion.CT_Tool, False)
    if not isinstance(summary, dict) or not summary:
        raise RuntimeError("Fusion.GetRegSummary returned no Tool records.")

    rows = []
    for item in summary.values():
        registry = session.fusion.FindReg(item["REGS_ID"])
        if registry is None:
            raise RuntimeError(f"Fusion.FindReg failed for {item['REGS_ID']!r}.")
        rows.append(registry.GetAttrs())

    fusion_rows = [row for row in rows if _is_blackmagic_fusion_tool(row)]
    modifier_rows = []
    for registry_id in _CURATED_FUSION_MODIFIER_IDS:
        registry = session.fusion.FindReg(registry_id)
        if registry is None:
            raise RuntimeError(
                f"Fusion.FindReg failed for Modifier {registry_id!r}."
            )
        modifier_rows.append(registry.GetAttrs())

    # Compatibility: XYPath was initially exposed through FusionTool.
    fusion_rows.append(
        next(
            row for row in modifier_rows if row.get("REGS_ID") == "XYPath"
        )
    )
    resolve_fx_rows = [
        row
        for row in rows
        if str(row.get("REGS_ID", "")).startswith(_BLACKMAGIC_OFX_PREFIXES)
    ]
    version = ".".join(str(value) for value in session.version[:3])

    print('"""Fusion Tool Registry IDs verified with Resolve ' + version + '."""')
    print()
    print("from enum import StrEnum")
    print()
    print()
    print("class FusionTool(StrEnum):")
    print('    """Blackmagic-provided Fusion Tool Registry IDs."""')
    print()
    print(*_enum_lines(fusion_rows), sep="\n")
    print()
    print()
    print("class FusionModifier(StrEnum):")
    print('    """Blackmagic-provided Fusion Modifier Registry IDs."""')
    print()
    print(*_enum_lines(modifier_rows), sep="\n")
    print()
    print()
    print("class FusionResolveFxTool(StrEnum):")
    print('    """Blackmagic Resolve FX Tool Registry IDs exposed in Fusion."""')
    print()
    print(
        *_enum_lines(resolve_fx_rows, prefixes=_BLACKMAGIC_OFX_PREFIXES),
        sep="\n",
    )


if __name__ == "__main__":
    main()
