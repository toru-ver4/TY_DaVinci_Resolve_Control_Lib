# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m pytest tests/unit/test_countdown_math_and_png.py -q

from array import array
import io
from pathlib import Path
import sys

import numpy as np
import png
import pytest

COUNTDOWN_DIR = Path(__file__).resolve().parents[1] / "countdown_regression"
sys.path.insert(0, str(COUNTDOWN_DIR))

from create_countdown_v2 import st2084_oetf_from_luminance  # noqa: E402
from png_compare import decode_png, validate_reference_archive  # noqa: E402


def test_st2084_representative_luminance_values() -> None:
    luminance = np.array([0, 0.1, 1, 10, 100, 1000, 10000], dtype=np.float64)
    expected = np.array(
        [
            7.309559025783966e-07,
            0.06233686566269587,
            0.14994573210018022,
            0.29969909242098597,
            0.508078421517399,
            0.751827096247041,
            1.0,
        ]
    )
    np.testing.assert_allclose(
        st2084_oetf_from_luminance(luminance), expected, rtol=0, atol=1e-14
    )


@pytest.mark.parametrize("value", [-0.001, 10000.001, np.inf, np.nan])
def test_st2084_rejects_out_of_domain_values(value: float) -> None:
    with pytest.raises(ValueError):
        st2084_oetf_from_luminance(value)


def test_png_decoder_preserves_16_bit_rgb_samples() -> None:
    output = io.BytesIO()
    writer = png.Writer(width=1, height=1, greyscale=False, alpha=False, bitdepth=16)
    writer.write(output, [array("H", [1, 32768, 65535])])
    output.seek(0)

    image, info = decode_png(output)

    assert image.dtype == np.uint16
    assert image.shape == (1, 1, 3)
    assert image[0, 0].tolist() == [1, 32768, 65535]
    assert info["bitdepth"] == 16


def test_reference_archive_integrity_and_safe_names() -> None:
    archive = (
        Path(__file__).resolve().parents[1]
        / "countdown_reference_data"
        / "ref_data_1280x720.zip"
    )
    names = validate_reference_archive(archive)
    assert len(names) == 384
    assert names[0] == "1280x720_23.976P_Gamma 2.4_P3-D65_00086400.png"
    assert names[-1] == "1280x720_23.976P_ST2084_Rec.2020_00086495.png"
