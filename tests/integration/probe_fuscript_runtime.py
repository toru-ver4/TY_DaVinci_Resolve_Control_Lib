# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: "C:\Program Files\Blackmagic Design\DaVinci Resolve\fuscript.exe" -l py3 tests/integration/probe_fuscript_runtime.py

"""Report whether Resolve's bundled script interpreter can reach Resolve."""

from __future__ import annotations


def main() -> None:
    """Print the scripting globals and Resolve connection state.

    Returns
    -------
    None

    Examples
    --------
    >>> main()  # doctest: +SKIP
    """
    print("TY_FUSCRIPT_PROBE_START", flush=True)
    runtime = globals().get("bmd")
    print(f"bmd_available={runtime is not None}", flush=True)
    if runtime is None:
        import DaVinciResolveScript as runtime

    resolve = runtime.scriptapp("Resolve")
    print(f"resolve_available={resolve is not None}", flush=True)
    if resolve is not None:
        print(f"product={resolve.GetProductName()!r}", flush=True)
        print(f"version={resolve.GetVersionString()!r}", flush=True)


if __name__ == "__main__":
    main()
