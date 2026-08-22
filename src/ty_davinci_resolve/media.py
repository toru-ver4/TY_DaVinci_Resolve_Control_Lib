"""Media Pool import and folder helpers."""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .errors import ResolveOperationError, ResolveValidationError


@dataclass(frozen=True, slots=True)
class MediaStorageItem:
    """One file or frame range accepted by Resolve Media Storage.

    Parameters
    ----------
    path
        Absolute existing media path.
    start_frame
        Optional inclusive source start frame.
    end_frame
        Optional inclusive source end frame.

    Returns
    -------
    None

    Examples
    --------
    >>> MediaStorageItem("C:/media/clip.mov", 0, 23)
    MediaStorageItem(path='C:/media/clip.mov', start_frame=0, end_frame=23)
    """

    path: str | Path
    start_frame: int | None = None
    end_frame: int | None = None


def get_media_pool(project: Any) -> Any:
    """Return a project's Media Pool.

    Parameters
    ----------
    project
        Resolve Project remote object.

    Returns
    -------
    Any
        Resolve MediaPool remote object.

    Examples
    --------
    >>> get_media_pool(project)  # doctest: +SKIP
    """
    media_pool = project.GetMediaPool()
    if media_pool is None:
        raise ResolveOperationError("Project.GetMediaPool", media_pool)
    return media_pool


def get_root_folder(media_pool: Any) -> Any:
    """Return the root Media Pool folder.

    Parameters
    ----------
    media_pool
        Resolve MediaPool remote object.

    Returns
    -------
    Any
        Root Folder remote object.

    Examples
    --------
    >>> get_root_folder(media_pool)  # doctest: +SKIP
    """
    folder = media_pool.GetRootFolder()
    if folder is None:
        raise ResolveOperationError("MediaPool.GetRootFolder", folder)
    return folder


def get_current_folder(media_pool: Any) -> Any:
    """Return the currently selected Media Pool folder.

    Parameters
    ----------
    media_pool
        Resolve MediaPool remote object.

    Returns
    -------
    Any
        Current Folder remote object.

    Examples
    --------
    >>> get_current_folder(media_pool)  # doctest: +SKIP
    """
    folder = media_pool.GetCurrentFolder()
    if folder is None:
        raise ResolveOperationError("MediaPool.GetCurrentFolder", folder)
    return folder


def set_current_folder(media_pool: Any, folder: Any) -> None:
    """Select a Media Pool folder.

    Parameters
    ----------
    media_pool
        Resolve MediaPool remote object.
    folder
        Resolve Folder remote object.

    Returns
    -------
    None

    Examples
    --------
    >>> set_current_folder(media_pool, folder)  # doctest: +SKIP
    """
    if folder is None:
        raise ResolveValidationError("folder must not be None.")
    result = media_pool.SetCurrentFolder(folder)
    if result is not True:
        raise ResolveOperationError("MediaPool.SetCurrentFolder", result)


def import_files(media_pool: Any, paths: Iterable[str | Path]) -> tuple[Any, ...]:
    """Import existing files into the current Media Pool folder.

    Parameters
    ----------
    media_pool
        Resolve MediaPool remote object.
    paths
        Existing absolute file paths.

    Returns
    -------
    tuple of Any
        Created MediaPoolItem remote objects.

    Examples
    --------
    >>> import_files(media_pool, [Path("C:/media/clip.mov")])  # doctest: +SKIP
    """
    try:
        normalized = tuple(Path(path).expanduser() for path in paths)
    except TypeError as error:
        raise ResolveValidationError("paths must be an iterable of paths.") from error
    if not normalized:
        raise ResolveValidationError("paths must not be empty.")
    for path in normalized:
        if not path.is_absolute():
            raise ResolveValidationError(f"Media path must be absolute: {path}.")
        if not path.is_file():
            raise ResolveValidationError(f"Media file does not exist: {path}.")
    result = media_pool.ImportMedia([str(path) for path in normalized])
    if not result:
        raise ResolveOperationError("MediaPool.ImportMedia", result)
    return tuple(result)


def import_sequence(
    media_pool: Any,
    pattern: str | Path,
    start_index: int,
    end_index: int,
) -> Any:
    """Import an image sequence into the current Media Pool folder.

    Parameters
    ----------
    media_pool
        Resolve MediaPool remote object.
    pattern
        Absolute sequence pattern such as ``C:/seq/frame_%04d.png``.
    start_index
        First inclusive sequence index.
    end_index
        Last inclusive sequence index.

    Returns
    -------
    Any
        Created MediaPoolItem remote object.

    Examples
    --------
    >>> import_sequence(media_pool, "C:/seq/frame_%04d.png", 0, 95)  # doctest: +SKIP
    """
    pattern_path = Path(pattern).expanduser()
    if not pattern_path.is_absolute():
        raise ResolveValidationError(f"Sequence pattern must be absolute: {pattern}.")
    if "%" not in str(pattern_path):
        raise ResolveValidationError("pattern must contain a printf-style frame field.")
    for value, name in ((start_index, "start_index"), (end_index, "end_index")):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ResolveValidationError(f"{name} must be an integer.")
    if start_index > end_index:
        raise ResolveValidationError("start_index must not exceed end_index.")
    clip_info = {
        "FilePath": str(pattern_path),
        "StartIndex": start_index,
        "EndIndex": end_index,
    }
    result = media_pool.ImportMedia([clip_info])
    if not result or result[0] is None:
        raise ResolveOperationError("MediaPool.ImportMedia", result)
    return result[0]


def import_media_storage_items(
    media_storage: Any,
    items: Iterable[MediaStorageItem | str | Path],
) -> tuple[Any, ...]:
    """Import files or source ranges through Resolve Media Storage.

    Parameters
    ----------
    media_storage
        Resolve MediaStorage remote object.
    items
        Existing paths or ``MediaStorageItem`` range specifications.

    Returns
    -------
    tuple of Any
        Created MediaPoolItem remote objects.

    Examples
    --------
    >>> import_media_storage_items(storage, [MediaStorageItem("C:/clip.mov", 0, 23)])  # doctest: +SKIP
    """
    try:
        normalized = tuple(items)
    except TypeError as error:
        raise ResolveValidationError("items must be an iterable.") from error
    if not normalized:
        raise ResolveValidationError("items must not be empty.")
    arguments: list[str | dict[str, Any]] = []
    for item in normalized:
        specification = item if isinstance(item, MediaStorageItem) else MediaStorageItem(item)
        path = Path(specification.path).expanduser()
        if not path.is_absolute() or not path.is_file():
            raise ResolveValidationError(f"Media file does not exist: {path}.")
        if (specification.start_frame is None) != (specification.end_frame is None):
            raise ResolveValidationError("start_frame and end_frame must be provided together.")
        if specification.start_frame is None:
            arguments.append(str(path))
            continue
        for value, name in ((specification.start_frame, "start_frame"), (specification.end_frame, "end_frame")):
            if isinstance(value, bool) or not isinstance(value, int):
                raise ResolveValidationError(f"{name} must be an integer.")
        if specification.start_frame > specification.end_frame:
            raise ResolveValidationError("start_frame must not exceed end_frame.")
        arguments.append({"media": str(path), "startFrame": specification.start_frame, "endFrame": specification.end_frame})
    result = media_storage.AddItemListToMediaPool(arguments)
    if not result or any(item is None for item in result):
        raise ResolveOperationError("MediaStorage.AddItemListToMediaPool", result)
    return tuple(result)
