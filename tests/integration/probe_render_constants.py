# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python tests/integration/probe_render_constants.py

"""Report runtime render formats and codecs absent from public enums."""

from __future__ import annotations

import re

from ty_davinci_resolve import RenderFormat, ResolveSession, VideoCodec


def _member_name(value: str) -> str:
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", value).upper()
    return re.sub(r"[^A-Z0-9]+", "_", value).strip("_")


def main() -> None:
    """Print identifiers returned by the connected Resolve host."""
    project = ResolveSession.connect().project_manager.GetCurrentProject()
    formats = project.GetRenderFormats()
    codecs = {
        value
        for format_id in formats.values()
        for value in project.GetRenderCodecs(format_id).values()
    }
    known_formats = {item.value for item in RenderFormat}
    known_codecs = {item.value for item in VideoCodec}
    print(
        f"formats={len(formats)} missing={len(set(formats.values()) - known_formats)}"
    )
    for value in formats.values():
        if value not in known_formats:
            print(f'    {_member_name(value)} = "{value}"')
    print(f"codecs={len(codecs)} missing={len(codecs - known_codecs)}")
    for value in sorted(codecs - known_codecs):
        print(f'    {_member_name(value)} = "{value}"')


if __name__ == "__main__":
    main()
