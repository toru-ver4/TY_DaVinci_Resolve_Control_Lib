"""Safe 16-bit PNG reference archive validation and pixel comparison."""

from __future__ import annotations

import hashlib
import io
from pathlib import Path, PurePosixPath
import zipfile

import numpy as np
import png


REFERENCE_SHA256 = "490a48b91fe8acd693c31253daf263000d9f1aeb76dc6216f60049590296773d"
EXPECTED_FILE_COUNT = 384
EXPECTED_SIZE = (1280, 720)
EXPECTED_INFO = {
    "greyscale": False,
    "alpha": False,
    "planes": 3,
    "bitdepth": 16,
    "interlace": 0,
}


def validate_reference_archive(path: str | Path) -> tuple[str, ...]:
    """Validate the pinned Countdown reference ZIP and return PNG names.

    Parameters
    ----------
    path
        Reference ZIP path.

    Returns
    -------
    tuple of str
        Sorted safe PNG entry names.

    Examples
    --------
    >>> len(validate_reference_archive("ref_data_1280x720.zip"))  # doctest: +SKIP
    384
    """
    archive = Path(path)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != REFERENCE_SHA256:
        raise AssertionError(
            f"Reference ZIP SHA-256 mismatch: expected {REFERENCE_SHA256}, got {digest}."
        )
    with zipfile.ZipFile(archive) as zip_file:
        names = zip_file.namelist()
    if len(names) != EXPECTED_FILE_COUNT:
        raise AssertionError(
            f"Reference entry count mismatch: expected {EXPECTED_FILE_COUNT}, got {len(names)}."
        )
    if len(set(names)) != len(names):
        raise AssertionError("Reference ZIP contains duplicate entry names.")
    for name in names:
        entry = PurePosixPath(name)
        if entry.is_absolute() or ".." in entry.parts or len(entry.parts) != 1:
            raise AssertionError(f"Unsafe reference ZIP entry: {name!r}.")
        if entry.suffix.casefold() != ".png":
            raise AssertionError(f"Non-PNG reference entry: {name!r}.")
    return tuple(sorted(names))


def decode_png(source) -> tuple[np.ndarray, dict[str, object]]:
    """Decode a PNG without reducing its source bit depth.

    Parameters
    ----------
    source
        Filename or binary file-like object accepted by PyPNG.

    Returns
    -------
    tuple
        Unsigned integer image array and PyPNG metadata.

    Examples
    --------
    >>> image, info = decode_png("frame.png")  # doctest: +SKIP
    >>> image.dtype
    dtype('uint16')
    """
    reader = png.Reader(file=source) if hasattr(source, "read") else png.Reader(filename=str(source))
    width, height, rows, info = reader.read()
    dtype = np.uint16 if info["bitdepth"] > 8 else np.uint8
    image = np.vstack([np.asarray(row, dtype=dtype) for row in rows])
    image = image.reshape(height, width, info["planes"])
    return image, dict(info)


def _validate_png_info(name: str, width: int, height: int, info: dict[str, object]) -> None:
    if (width, height) != EXPECTED_SIZE:
        raise AssertionError(
            f"{name}: expected size {EXPECTED_SIZE}, got {(width, height)}."
        )
    for key, expected in EXPECTED_INFO.items():
        if info.get(key) != expected:
            raise AssertionError(
                f"{name}: expected PNG {key}={expected!r}, got {info.get(key)!r}."
            )


def compare_png_samples(reference_data: bytes, actual_path: str | Path, name: str) -> None:
    """Compare one reference and actual PNG at full 16-bit RGB precision.

    Parameters
    ----------
    reference_data
        Reference PNG bytes.
    actual_path
        Actual PNG file path.
    name
        Diagnostic filename.

    Returns
    -------
    None

    Examples
    --------
    >>> compare_png_samples(reference_bytes, "actual.png", "actual.png")  # doctest: +SKIP
    """
    reference_reader = png.Reader(file=io.BytesIO(reference_data))
    actual_reader = png.Reader(filename=str(actual_path))
    ref_width, ref_height, ref_rows, ref_info = reference_reader.read()
    act_width, act_height, act_rows, act_info = actual_reader.read()
    _validate_png_info(name, ref_width, ref_height, ref_info)
    _validate_png_info(name, act_width, act_height, act_info)

    channels = ("R", "G", "B")
    first_difference: tuple[int, int, str, int, int] | None = None
    difference_count = 0
    for y, (reference_row, actual_row) in enumerate(zip(ref_rows, act_rows)):
        expected = np.asarray(reference_row, dtype=np.uint16)
        actual = np.asarray(actual_row, dtype=np.uint16)
        if expected.shape != actual.shape:
            raise AssertionError(
                f"{name}: row {y} shape mismatch: {expected.shape} != {actual.shape}."
            )
        different = expected != actual
        row_count = int(np.count_nonzero(different))
        difference_count += row_count
        if row_count and first_difference is None:
            sample_index = int(np.flatnonzero(different)[0])
            x, channel_index = divmod(sample_index, 3)
            first_difference = (
                x,
                y,
                channels[channel_index],
                int(expected[sample_index]),
                int(actual[sample_index]),
            )
    if first_difference is not None:
        x, y, channel, expected_value, actual_value = first_difference
        raise AssertionError(
            f"{name}: first mismatch at (x={x}, y={y}, channel={channel}); "
            f"expected {expected_value}, got {actual_value}; "
            f"differing samples={difference_count}."
        )


def compare_output_directory(reference_zip: str | Path, output_dir: str | Path) -> None:
    """Compare all generated PNGs with the pinned reference archive.

    Parameters
    ----------
    reference_zip
        Pinned reference ZIP path.
    output_dir
        Directory containing rendered PNG files.

    Returns
    -------
    None

    Examples
    --------
    >>> compare_output_directory("reference.zip", "output")  # doctest: +SKIP
    """
    names = validate_reference_archive(reference_zip)
    output = Path(output_dir)
    actual_names = tuple(sorted(path.name for path in output.glob("*.png")))
    if actual_names != names:
        missing = sorted(set(names) - set(actual_names))
        extra = sorted(set(actual_names) - set(names))
        raise AssertionError(
            f"PNG filename set mismatch: missing={missing[:10]}, extra={extra[:10]}."
        )
    with zipfile.ZipFile(reference_zip) as zip_file:
        for name in names:
            compare_png_samples(zip_file.read(name), output / name, name)
