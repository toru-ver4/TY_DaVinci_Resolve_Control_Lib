# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python tests/integration/probe_project_setting_values.py

"""Probe candidate Resolve setting values in a disposable project."""

from __future__ import annotations

import time
from uuid import uuid4

from ty_davinci_resolve import (
    ResolveSession,
    close_project,
    create_project,
    delete_project,
    list_projects,
)


COLOR_SPACES = (
    "ACES (AP0)",
    "ACES (AP1)",
    "Adobe RGB",
    "Apple Log 2",
    "ARRI Wide Gamut 3",
    "ARRI Wide Gamut 4",
    "AstroDesign",
    "Blackmagic Design 4.6K Film Gen 1",
    "Blackmagic Design 4.6K Film Gen 3",
    "Blackmagic Design 4K Film Gen 1",
    "Blackmagic Design 4K Film Gen 3",
    "Blackmagic Design Film Gen 1",
    "Blackmagic Design Pocket 4K Film Gen 4",
    "Blackmagic Design Video Gamut Gen 4",
    "Blackmagic Design Video Gen 5",
    "Blackmagic Design Wide Gamut Gen 4 / 5",
    "Canon Cinema Gamut",
    "DaVinci WG",
    "DCI XYZ",
    "DJI D-Gamut",
    "DRAGONcolor",
    "DRAGONcolor2",
    "Fujifilm F-Gamut C",
    "HSL",
    "HSV",
    "Lab (CIE)",
    "P3-D60",
    "P3-D65",
    "P3 DCI",
    "Panasonic V-Gamut",
    "Rec.709",
    "Rec.2020",
    "REDcolor2",
    "REDcolor3",
    "REDcolor4",
    "REDWideGamutRGB",
    "SMPTE C",
    "Sony S-Gamut",
    "Sony S-Gamut3",
    "Sony S-Gamut3.Cine",
    "sRGB",
    "XYZ (CIE)",
    "YUV",
    # Known API spellings that differ from the Resolve UI label.
    "P3-DCI",
    "SMPTE-C",
    "Y'UV",
)

GAMMAS = (
    "ACEScc",
    "ACEScct",
    "Adobe RGB",
    "Apple Log",
    "ARIB STD-B67 HLG",
    "ARRI LogC3",
    "ARRI LogC4",
    "AstroDesign A Log",
    "Blackmagic Design 4.6K Film",
    "Blackmagic Design 4K Film",
    "Blackmagic Design Broadcast Film Gen 4",
    "Blackmagic Design Extended Video Gen 4",
    "Blackmagic Design Extended Video Gen 5",
    "Blackmagic Design Film",
    "Blackmagic Design Film Gen 5",
    "Blackmagic Design Pocket 4K Film Gen 4",
    "Blackmagic Design Pocket 6K Film Gen 4",
    "Blackmagic Design Video",
    "Blackmagic Design Video Gen 3",
    "Blackmagic Design Video Gen 4",
    "Blackmagic Design Video Gen 5",
    "Canon Log",
    "Canon Log 2",
    "Canon Log 3",
    "Cineon Film Log",
    "DaVinci Intermediate",
    "DCI",
    "DJI D Log",
    "Fujifilm F-Log",
    "Fujifilm F-Log2",
    "Gamma 2.2",
    "Gamma 2.4",
    "Gamma 2.5",
    "Gamma 2.6",
    "Insta360 I-Log",
    "Leica L Log",
    "Linear",
    "Nikon N Log",
    "Panasonic V-Log",
    "Rec.709",
    "Rec.709-A",
    "Rec.2100 HLG",
    "Rec.2100 HLG (Scene)",
    "Rec.2100 ST2084",
    "Rec.2100 ST2084 (Scene)",
    "RED Log3G10",
    "REDgamma3",
    "REDgamma4",
    "REDlogFilm",
    "Samsung Log",
    "S-Log",
    "S Log2",
    "S-Log3",
    "sRGB",
    "ST2084",
    "ST2084 300 nit",
    "ST2084 500 nit",
    "ST2084 800 nit",
    "ST2084 1000 nit",
    "ST2084 2000 nit",
    "ST2084 3000 nit",
    "ST2084 4000 nit",
    "Stops (18% Gray)",
    # Candidate API spellings for UI labels rejected verbatim by SetSetting.
    "AstroDesign A-Log",
    "DJI D-Log",
    "Leica L-Log",
    "Nikon N-Log",
    "S-Log2",
)

DRT_VALUES = (
    "None",
    "Simple",
    "Luminance Mapping",
    "DaVinci",
    "Saturation Preserving",
)

OUTPUT_GAMUT_MAPPINGS = (
    "None",
    "Output color space",
    "P3-D60",
    "P3-D65",
    "P3-DCI",
    "Rec.709",
    "Rec.2020",
)

RESIZE_TRANSFORMATIONS = (
    "Timeline",
    "Log",
    "Linear",
    "Linear - Tone Mapped",
    "Gamma",
    "Gamma - Tone Mapped",
)

ACES_ODTS = (
    "No Output Transform",
    "P3-D65 ST2084 (108 nit)",
    "P3-D65 ST2084 (1000 nit)",
    "P3-D65 ST2084 (4000 nit)",
    "Rec.2100 ST2084 (1000 nit)",
)

COMBINED_COLOR_SPACES = (
    "Rec.709-A",
    "Rec.709 (Scene)",
    "Rec.709 Gamma 2.2",
    "Rec.709 Gamma 2.4",
    "Linear",
    "DaVinci WG/Intermediate",
)

WORKING_LUMINANCE_MODES = (
    "SDR 100",
    "HDR 400",
    "HDR 500",
    "HDR 1000",
    "HDR 2000",
    "HDR 4000",
    "SDR ER 100/200",
    "HDR ER 1000/2000",
    "HDR ER 1000/4000",
    "HDR ER 1000/10000",
    "HDR ER 4000/10000",
    "Custom",
)


def _probe(project: object, key: str, candidates: tuple[str, ...]) -> None:
    """Print candidates accepted and read back by Resolve.

    Parameters
    ----------
    project
        Disposable Resolve Project remote object.
    key
        Project setting key.
    candidates
        Candidate values to probe.

    Returns
    -------
    None

    Examples
    --------
    >>> _probe(project, "colorSpaceTimeline", ("Rec.709",))  # doctest: +SKIP
    """
    print(f"[{key}]", flush=True)
    for candidate in candidates:
        accepted = project.SetSetting(key, candidate)
        time.sleep(0.35)
        actual = project.GetSetting(key)
        print(
            f"{candidate!r}: accepted={accepted!r}, actual={actual!r}, "
            f"match={actual == candidate}",
            flush=True,
        )


def _probe_rejected(project: object, key: str, candidates: tuple[str, ...]) -> None:
    """Print only values rejected by one Resolve setting key."""
    rejected = []
    for candidate in candidates:
        if project.SetSetting(key, candidate) is not True:
            rejected.append(candidate)
    print(f"[{key}] rejected={rejected!r}", flush=True)


def main() -> None:
    """Probe candidates and delete the disposable project.

    Returns
    -------
    None

    Examples
    --------
    >>> main()  # doctest: +SKIP
    """
    session = ResolveSession.connect()
    name = f"TY_SETTING_PROBE_{uuid4().hex}"
    project = None
    try:
        project = create_project(session, name)
        for key, value in (
            ("colorScienceMode", "davinciYRGBColorManagedv2"),
            ("rcmPresetMode", "Custom"),
            ("separateColorSpaceAndGamma", "1"),
        ):
            result = project.SetSetting(key, value)
            time.sleep(0.5)
            print(key, result, project.GetSetting(key), flush=True)
        for key in (
            "colorSpaceInput",
            "colorSpaceTimeline",
            "colorSpaceOutput",
        ):
            _probe_rejected(project, key, COLOR_SPACES)
        for key in (
            "colorSpaceInputGamma",
            "colorSpaceTimelineGamma",
            "colorSpaceOutputGamma",
        ):
            _probe_rejected(project, key, GAMMAS)
        project.SetSetting("separateColorSpaceAndGamma", "0")
        time.sleep(0.5)
        _probe(project, "colorSpaceTimeline", COMBINED_COLOR_SPACES)
        project.SetSetting("separateColorSpaceAndGamma", "1")
        time.sleep(0.5)
        _probe(
            project,
            "timelineWorkingLuminanceMode",
            WORKING_LUMINANCE_MODES,
        )
        _probe(project, "inputDRT", DRT_VALUES)
        _probe(project, "outputDRT", DRT_VALUES)
        _probe(
            project,
            "colorSpaceOutputGamutMapping",
            OUTPUT_GAMUT_MAPPINGS,
        )
        _probe(project, "imageResizingGamma", RESIZE_TRANSFORMATIONS)
        project.SetSetting("colorScienceMode", "acescct")
        time.sleep(0.75)
        _probe(project, "colorAcesODT", ACES_ODTS)
    finally:
        current = session.project_manager.GetCurrentProject()
        if current is not None and current.GetName() == name:
            close_project(session, current)
        if name in list_projects(session):
            delete_project(session, name)


if __name__ == "__main__":
    main()
