# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m unittest discover -s tests/unit -v

from pathlib import Path
import sys
import unittest

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = PACKAGE_ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))


class PackageImportTests(unittest.TestCase):
    """Tests for the package's import contract and stable constants."""

    def test_import_does_not_load_resolve_script_module(self) -> None:
        sys.modules.pop("DaVinciResolveScript", None)

        import ty_davinci_resolve

        self.assertNotIn("DaVinciResolveScript", sys.modules)
        self.assertEqual(ty_davinci_resolve.__version__, "0.1.0")

    def test_common_render_codec_is_easy_to_specify(self) -> None:
        from ty_davinci_resolve import RenderFormat, VideoCodec

        self.assertEqual(RenderFormat.QUICKTIME, "mov")
        self.assertEqual(VideoCodec.PRORES_4444_XQ, "ProRes4444XQ")

    def test_page_and_track_values_match_official_api(self) -> None:
        from ty_davinci_resolve import FusionTool, Page, TrackType

        self.assertEqual(Page.FUSION, "fusion")
        self.assertEqual(TrackType.SUBTITLE, "subtitle")
        self.assertEqual(FusionTool.RECTANGLE_MASK, "RectangleMask")


if __name__ == "__main__":
    unittest.main()
