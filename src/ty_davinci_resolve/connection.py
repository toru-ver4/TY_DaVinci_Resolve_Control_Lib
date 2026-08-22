"""Lazy loading and connection management for DaVinci Resolve."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import importlib
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import time
from types import ModuleType
from typing import Any

from .constants import Page, SUPPORTED_RESOLVE_VERSION
from .errors import (
    ResolveConnectionError,
    ResolveOperationError,
    ResolveValidationError,
    ResolveVersionError,
)

ResolveScriptLoader = Callable[[], Any]


def get_current_page(session: ResolveSession) -> Page:
    """Return the page currently displayed by Resolve.

    Parameters
    ----------
    session
        Connected Resolve session.

    Returns
    -------
    Page
        Validated current page.

    Examples
    --------
    >>> get_current_page(session)  # doctest: +SKIP
    <Page.EDIT: 'edit'>
    """
    result = session.resolve.GetCurrentPage()
    try:
        return Page(result)
    except (TypeError, ValueError) as error:
        raise ResolveOperationError("Resolve.GetCurrentPage", result) from error


def open_page(session: ResolveSession, page: Page | str) -> None:
    """Switch Resolve to a validated page.

    Parameters
    ----------
    session
        Connected Resolve session.
    page
        Page enum or documented page identifier.

    Returns
    -------
    None

    Examples
    --------
    >>> open_page(session, Page.FUSION)  # doctest: +SKIP
    """
    try:
        page_value = Page(page).value
    except (TypeError, ValueError) as error:
        raise ResolveValidationError(f"Invalid Resolve page: {page!r}.") from error
    result = session.resolve.OpenPage(page_value)
    if result is not True:
        raise ResolveOperationError("Resolve.OpenPage", result)


def _default_resolve_script_path() -> Path:
    """Return the platform's default DaVinciResolveScript.py path.

    Returns
    -------
    pathlib.Path
        Expected path to the official Resolve scripting module.

    Examples
    --------
    >>> _default_resolve_script_path().name
    'DaVinciResolveScript.py'
    """
    if sys.platform == "win32":
        program_data = Path(os.environ.get("PROGRAMDATA", r"C:\ProgramData"))
        base_path = (
            program_data
            / "Blackmagic Design"
            / "DaVinci Resolve"
            / "Support"
            / "Developer"
            / "Scripting"
        )
    elif sys.platform == "darwin":
        base_path = Path(
            "/Library/Application Support/Blackmagic Design/"
            "DaVinci Resolve/Developer/Scripting"
        )
    elif sys.platform.startswith("linux"):
        base_path = Path("/opt/resolve/Developer/Scripting")
    else:
        raise ResolveConnectionError(f"Unsupported platform: {sys.platform}.")

    return base_path / "Modules" / "DaVinciResolveScript.py"


def _load_module_from_path(module_path: Path) -> ModuleType:
    """Load the official Resolve scripting module from a file.

    Parameters
    ----------
    module_path
        Path to `DaVinciResolveScript.py`.

    Returns
    -------
    types.ModuleType
        Loaded Resolve scripting module.

    Examples
    --------
    >>> _load_module_from_path(Path("missing.py"))
    Traceback (most recent call last):
    ...
    ty_davinci_resolve.errors.ResolveConnectionError: DaVinci Resolve scripting module was not found: missing.py
    """
    if not module_path.is_file():
        raise ResolveConnectionError(
            f"DaVinci Resolve scripting module was not found: {module_path}"
        )

    module_name = "_ty_davinci_resolve_script"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ResolveConnectionError(
            f"Failed to create a module loader for: {module_path}"
        )

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as error:
        sys.modules.pop(module_name, None)
        raise ResolveConnectionError(
            "Failed to load the DaVinci Resolve scripting module: "
            f"{module_path} ({type(error).__name__}: {error}). "
            "Verify the Resolve edition and the External scripting preference."
        ) from error

    loaded_module = sys.modules.get(module_name, module)
    return loaded_module


def load_resolve_script_module() -> Any:
    """Load the official DaVinci Resolve scripting module lazily.

    Returns
    -------
    Any
        Module-like object that provides `scriptapp`.

    Notes
    -----
    Importing `ty_davinci_resolve` does not call this function. Loading occurs
    only when `ResolveSession.connect()` is called.

    Examples
    --------
    >>> module = load_resolve_script_module()  # doctest: +SKIP
    >>> callable(module.scriptapp)  # doctest: +SKIP
    True
    """
    try:
        return importlib.import_module("DaVinciResolveScript")
    except ImportError:
        return _load_module_from_path(_default_resolve_script_path())


def _normalize_version(version_fields: Any) -> tuple[int, ...]:
    """Convert Resolve version fields to an integer tuple.

    Parameters
    ----------
    version_fields
        Value returned by `Resolve.GetVersion()`.

    Returns
    -------
    tuple of int
        Normalized version fields.

    Examples
    --------
    >>> _normalize_version([21, 0, 4, 10, ""])
    (21, 0, 4, 10)
    """
    if not isinstance(version_fields, (list, tuple)) or len(version_fields) < 3:
        raise ResolveConnectionError(
            f"Resolve.GetVersion returned an invalid value: {version_fields!r}."
        )

    normalized: list[int] = []
    for value in version_fields[:4]:
        try:
            normalized.append(int(value))
        except (TypeError, ValueError) as error:
            raise ResolveConnectionError(
                f"Resolve.GetVersion returned an invalid field: {value!r}."
            ) from error
    return tuple(normalized)


@dataclass(slots=True)
class ResolveSession:
    """Connected DaVinci Resolve and Fusion objects."""

    resolve: Any
    fusion: Any
    product_name: str
    version: tuple[int, ...]
    version_string: str

    @property
    def project_manager(self) -> Any:
        """Return the connected Resolve project manager.

        Returns
        -------
        Any
            Resolve ProjectManager remote object.

        Examples
        --------
        >>> session.project_manager  # doctest: +SKIP
        """
        manager = self.resolve.GetProjectManager()
        if manager is None:
            raise ResolveOperationError("Resolve.GetProjectManager", manager)
        return manager

    @property
    def media_storage(self) -> Any:
        """Return the connected Resolve media storage object.

        Returns
        -------
        Any
            Resolve MediaStorage remote object.

        Examples
        --------
        >>> session.media_storage  # doctest: +SKIP
        """
        storage = self.resolve.GetMediaStorage()
        if storage is None:
            raise ResolveOperationError("Resolve.GetMediaStorage", storage)
        return storage

    @classmethod
    def connect(
        cls,
        *,
        expected_version: tuple[int, int, int] | None = SUPPORTED_RESOLVE_VERSION,
        module_loader: ResolveScriptLoader | None = None,
    ) -> ResolveSession:
        """Connect to a running DaVinci Resolve instance.

        Parameters
        ----------
        expected_version
            Required major, minor, and patch version. Pass `None` to skip the
            version check.
        module_loader
            Optional loader used for tests or non-standard installations.

        Returns
        -------
        ResolveSession
            Connected Resolve session.

        Examples
        --------
        >>> session = ResolveSession.connect()  # doctest: +SKIP
        >>> session.version[:3]  # doctest: +SKIP
        (21, 0, 4)
        """
        loader = module_loader or load_resolve_script_module
        try:
            script_module = loader()
            scriptapp = getattr(script_module, "scriptapp")
            resolve = scriptapp("Resolve")
        except ResolveConnectionError:
            raise
        except Exception as error:
            raise ResolveConnectionError(
                "Failed to initialize the DaVinci Resolve scripting API."
            ) from error

        if resolve is None:
            raise ResolveConnectionError(
                "DaVinci Resolve is not running or scripting is unavailable."
            )

        try:
            product_name = resolve.GetProductName()
            version = _normalize_version(resolve.GetVersion())
            version_string = resolve.GetVersionString()
            fusion = resolve.Fusion()
        except ResolveConnectionError:
            raise
        except Exception as error:
            raise ResolveConnectionError(
                "Failed to query the connected DaVinci Resolve instance."
            ) from error

        if not isinstance(product_name, str) or not product_name:
            raise ResolveConnectionError(
                f"Resolve.GetProductName returned an invalid value: {product_name!r}."
            )
        if not isinstance(version_string, str) or not version_string:
            raise ResolveConnectionError(
                "Resolve.GetVersionString returned an invalid value: "
                f"{version_string!r}."
            )
        if expected_version is not None and version[:3] != expected_version:
            raise ResolveVersionError(version, expected_version)
        if fusion is None:
            raise ResolveConnectionError("Resolve.Fusion returned None.")

        return cls(
            resolve=resolve,
            fusion=fusion,
            product_name=product_name,
            version=version,
            version_string=version_string,
        )

    def quit(self) -> None:
        """Quit DaVinci Resolve through the official scripting API.

        Returns
        -------
        None

        Examples
        --------
        >>> session.quit()  # doctest: +SKIP
        """
        try:
            self.resolve.Quit()
        except Exception as error:
            raise ResolveConnectionError(
                "Resolve.Quit failed."
            ) from error

    def restart(
        self,
        *,
        executable: str | Path | None = None,
        timeout: float = 90.0,
        poll_interval: float = 1.0,
    ) -> ResolveSession:
        """Quit, launch, and reconnect to DaVinci Resolve on Windows.

        Parameters
        ----------
        executable
            Optional Resolve executable path. The standard Windows install
            path is used when omitted.
        timeout
            Maximum seconds for each shutdown and reconnect phase.
        poll_interval
            Delay between connection attempts in seconds.

        Returns
        -------
        ResolveSession
            Newly connected Resolve session.

        Notes
        -----
        This method is Windows-only. It launches Resolve without a shell and
        validates the same major, minor, and patch version as this session.

        Examples
        --------
        >>> session = session.restart()  # doctest: +SKIP
        """
        if sys.platform != "win32":
            raise ResolveValidationError(
                "ResolveSession.restart is supported only on Windows."
            )
        for value, name in ((timeout, "timeout"), (poll_interval, "poll_interval")):
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
                or value <= 0
            ):
                raise ResolveValidationError(f"{name} must be a positive number.")
        executable_path = Path(
            executable
            if executable is not None
            else Path(
                os.environ.get(
                    "PROGRAMFILES", r"C:\Program Files"
                )
            )
            / "Blackmagic Design"
            / "DaVinci Resolve"
            / "Resolve.exe"
        )
        if not executable_path.is_file():
            raise ResolveValidationError(
                f"Resolve executable was not found: {executable_path}."
            )

        self.quit()
        expected_version = tuple(self.version[:3])
        shutdown_deadline = time.monotonic() + timeout
        while time.monotonic() < shutdown_deadline:
            try:
                type(self).connect(expected_version=expected_version)
            except ResolveConnectionError:
                break
            time.sleep(poll_interval)
        else:
            raise ResolveConnectionError(
                f"DaVinci Resolve did not stop within {timeout} seconds."
            )

        try:
            subprocess.Popen([str(executable_path)])
        except OSError as error:
            raise ResolveConnectionError(
                f"Failed to launch DaVinci Resolve: {executable_path}."
            ) from error

        reconnect_deadline = time.monotonic() + timeout
        last_error: ResolveConnectionError | None = None
        while time.monotonic() < reconnect_deadline:
            try:
                return type(self).connect(expected_version=expected_version)
            except ResolveConnectionError as error:
                last_error = error
                time.sleep(poll_interval)
        raise ResolveConnectionError(
            f"DaVinci Resolve did not reconnect within {timeout} seconds."
        ) from last_error
