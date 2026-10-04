# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: .venv313/Scripts/python.exe tests/integration/probe_official_api_diff.py

"""Inventory official method signatures without treating stub omissions as removals."""

import ast
import json
import re
from pathlib import Path


def main() -> None:
    """Compare the old method table with the new official type definitions.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Notes
    -----
    The old README has a malformed InsertAudioToCurrentTrackAtPlayhead signature.
    Defaults and return types require reading its prose as well as this inventory.
    Deprecated and unsupported sections are reviewed separately in the report.

    Examples
    --------
    >>> main()  # doctest: +SKIP
    """
    old = Path("official_documents/21.0.4_Scripting/README.txt").read_text(encoding="utf-8")
    old = old.split("List and Dict Data Structures")[0]
    new = ast.parse(Path("official_documents/21.1.0_Scripting/DaVinciResolveScript.pyi").read_text(encoding="utf-8"))
    classes = {
        cls.name: {method.name: ast.unparse(method).split(":\n")[0]
                   for method in cls.body if isinstance(method, ast.FunctionDef)}
        for cls in new.body if isinstance(cls, ast.ClassDef)
    }
    methods = {}
    owner = None
    pending = ""
    for line in old.splitlines():
        if line in classes:
            owner, pending = line, ""
        if re.match(r"  \w+\(", line):
            pending = line.strip()
        elif pending and "-->" not in pending:
            pending += " " + line.strip()
        if pending and "-->" in pending and owner:
            name = re.match(r"(\w+)\(", pending)[1]
            methods.setdefault(owner, {}).setdefault(name, []).append(pending.split("#")[0].strip())
            pending = ""
    report = {
        owner: {
            "added": {key: value for key, value in classes[owner].items() if key not in entries},
            "absent_from_stub": {key: value for key, value in entries.items() if key not in classes[owner]},
            "common_signatures": {key: {"21.0.4": value, "21.1": classes[owner][key]}
                                  for key, value in entries.items() if key in classes[owner]},
        }
        for owner, entries in methods.items()
    }
    output = Path("docs/verification/21.1.0.17/api-signatures.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
