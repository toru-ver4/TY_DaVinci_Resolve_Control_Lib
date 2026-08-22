# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest -m resolve_restart tests/integration/test_restart.py -q -s

import pytest

from ty_davinci_resolve import ResolveSession


@pytest.mark.resolve_integration
@pytest.mark.resolve_restart
def test_restart_reconnects_to_supported_resolve() -> None:
    session = ResolveSession.connect()

    restarted = session.restart(timeout=90, poll_interval=1)

    assert restarted.version[:3] == (21, 0, 4)
    assert restarted.product_name == "DaVinci Resolve Studio"
