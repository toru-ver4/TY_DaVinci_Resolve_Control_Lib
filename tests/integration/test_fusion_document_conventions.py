# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: .venv313/Scripts/python.exe -m pytest tests/integration/test_fusion_document_conventions.py -q

"""Exercise documented Point values and nonstandard main connector names."""

import json
from pathlib import Path

import pytest

from ty_davinci_resolve import (
    ResolveValidationError,
    ResolveSession,
    add_fusion_tool,
    connect_default_output,
    set_fusion_tool_input,
)


@pytest.mark.resolve_integration
def test_fusion_document_conventions_on_live_resolve() -> None:
    """Check the corrected wrappers in a disposable hidden composition.

    Parameters
    ----------
    None

    Returns
    -------
    None

    Examples
    --------
    >>> test_fusion_document_conventions_on_live_resolve()  # doctest: +SKIP
    """
    session = ResolveSession.connect()
    comp = session.fusion.NewComp(True, True, True)
    assert comp is not None
    observations = []
    try:
        mask = add_fusion_tool(comp, "RectangleMask")
        blur = add_fusion_tool(comp, "Blur", (1, 0))
        assert mask.Output is None
        connect_default_output(mask, blur)
        connected = blur.FindMainInput(1).GetConnectedOutput()
        assert connected.GetAttrs()["OUTS_ID"] == "Mask"
        assert connected.GetTool().Name == mask.Name
        for point in ([0.2, 0.3], {1: 0.4, 2: 0.6}, [0.1, 0.2, 0.0]):
            set_fusion_tool_input(mask, "Center", point)
            observations.append({"written": point, "readback": mask.GetInput("Center")})
        set_fusion_tool_input(blur, "EffectMask", mask)
        assert blur.EffectMask.GetConnectedOutput().GetTool().Name == mask.Name
        with pytest.raises(ResolveValidationError):
            set_fusion_tool_input(blur, "TY_MissingInput", mask)
        assert blur.FindMainInput(1).GetConnectedOutput().GetTool().Name == mask.Name
    finally:
        assert comp.Close() is True
    output = Path("docs/verification") / session.version_string / "fusion-document-conventions.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps({
        "resolve": session.version_string,
        "main_output_id": "Mask",
        "point_values": observations,
        "valid_remote_connection_verified": True,
        "missing_remote_input_rejected": True,
        "hidden_comp_closed": True,
    }, indent=2) + "\n", encoding="utf-8")
