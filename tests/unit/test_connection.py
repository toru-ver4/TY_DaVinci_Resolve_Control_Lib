# Run from: sample_code/ty_lib/TY_DaVinci_Resolve_Control_Lib
# Command: python -m unittest discover -s tests/unit -v

from __future__ import annotations

from pathlib import Path
import sys
import unittest
from unittest.mock import patch

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = PACKAGE_ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from ty_davinci_resolve import (  # noqa: E402
    ResolveConnectionError,
    ResolveSession,
    ResolveVersionError,
)


class FakeResolve:
    """Minimal Resolve object used by connection tests."""

    def __init__(
        self,
        version: tuple[int, ...] = (21, 0, 4, 10),
        fusion: object | None = None,
    ) -> None:
        """Initialize a fake Resolve object.

        Parameters
        ----------
        version
            Version fields returned by the fake.
        fusion
            Fusion object returned by the fake.

        Returns
        -------
        None

        Examples
        --------
        >>> FakeResolve().GetVersion()[:3]
        [21, 0, 4]
        """
        self._version = version
        self._fusion = fusion if fusion is not None else object()
        self.quit_called = False

    def GetProductName(self) -> str:
        """Return a fake product name.

        Returns
        -------
        str
            Fake product name.

        Examples
        --------
        >>> FakeResolve().GetProductName()
        'DaVinci Resolve Studio'
        """
        return "DaVinci Resolve Studio"

    def GetVersion(self) -> list[int]:
        """Return fake version fields.

        Returns
        -------
        list of int
            Fake version fields.

        Examples
        --------
        >>> FakeResolve().GetVersion()[:3]
        [21, 0, 4]
        """
        return list(self._version)

    def GetVersionString(self) -> str:
        """Return a fake version string.

        Returns
        -------
        str
            Fake version string.

        Examples
        --------
        >>> FakeResolve().GetVersionString()
        '21.0.4.10'
        """
        return ".".join(str(value) for value in self._version)

    def Fusion(self) -> object:
        """Return the fake Fusion object.

        Returns
        -------
        object
            Fake Fusion object.

        Examples
        --------
        >>> FakeResolve().Fusion() is not None
        True
        """
        return self._fusion

    def Quit(self) -> None:
        """Record a fake quit request.

        Returns
        -------
        None

        Examples
        --------
        >>> resolve = FakeResolve(); resolve.Quit(); resolve.quit_called
        True
        """
        self.quit_called = True


class FakeScriptModule:
    """Minimal DaVinciResolveScript module used by tests."""

    def __init__(self, resolve: FakeResolve | None) -> None:
        """Initialize a fake script module.

        Parameters
        ----------
        resolve
            Object returned by `scriptapp`.

        Returns
        -------
        None

        Examples
        --------
        >>> FakeScriptModule(None).scriptapp("Resolve") is None
        True
        """
        self._resolve = resolve

    def scriptapp(self, app_name: str) -> FakeResolve | None:
        """Return the configured fake Resolve object.

        Parameters
        ----------
        app_name
            Requested application name.

        Returns
        -------
        FakeResolve or None
            Configured fake object.

        Examples
        --------
        >>> FakeScriptModule(None).scriptapp("Resolve") is None
        True
        """
        if app_name != "Resolve":
            raise ValueError(f"Unexpected app name: {app_name}")
        return self._resolve


class ResolveSessionTests(unittest.TestCase):
    """Tests for `ResolveSession`."""

    def test_connect_returns_validated_session(self) -> None:
        resolve = FakeResolve()
        module = FakeScriptModule(resolve)

        session = ResolveSession.connect(module_loader=lambda: module)

        self.assertIs(session.resolve, resolve)
        self.assertEqual(session.version[:3], (21, 0, 4))
        self.assertEqual(session.product_name, "DaVinci Resolve Studio")

    def test_connect_rejects_unsupported_version(self) -> None:
        module = FakeScriptModule(FakeResolve(version=(21, 0, 3, 10)))

        with self.assertRaises(ResolveVersionError):
            ResolveSession.connect(module_loader=lambda: module)

    def test_connect_fails_when_resolve_is_not_running(self) -> None:
        module = FakeScriptModule(None)

        with self.assertRaises(ResolveConnectionError):
            ResolveSession.connect(module_loader=lambda: module)

    def test_connect_can_skip_version_check_explicitly(self) -> None:
        module = FakeScriptModule(FakeResolve(version=(22, 0, 0, 1)))

        session = ResolveSession.connect(
            expected_version=None,
            module_loader=lambda: module,
        )

        self.assertEqual(session.version[:3], (22, 0, 0))

    def test_connect_accepts_non_empty_version_suffix(self) -> None:
        resolve = FakeResolve()
        resolve.GetVersion = lambda: [21, 0, 4, 10, "B"]  # type: ignore[method-assign]

        session = ResolveSession.connect(
            module_loader=lambda: FakeScriptModule(resolve)
        )

        self.assertEqual(session.version, (21, 0, 4, 10))

    def test_connect_fails_when_fusion_is_unavailable(self) -> None:
        resolve = FakeResolve()
        resolve._fusion = None

        with self.assertRaises(ResolveConnectionError):
            ResolveSession.connect(
                module_loader=lambda: FakeScriptModule(resolve)
            )

    def test_quit_calls_official_api(self) -> None:
        resolve = FakeResolve()
        session = ResolveSession.connect(
            module_loader=lambda: FakeScriptModule(resolve)
        )

        session.quit()

        self.assertTrue(resolve.quit_called)

    def test_restart_waits_for_disconnect_launches_and_reconnects(self) -> None:
        resolve = FakeResolve()
        session = ResolveSession.connect(
            module_loader=lambda: FakeScriptModule(resolve)
        )
        replacement = ResolveSession(
            resolve=object(),
            fusion=object(),
            product_name="DaVinci Resolve Studio",
            version=(21, 0, 4, 10),
            version_string="21.0.4.10",
        )
        executable = PACKAGE_ROOT / "tests" / "unit" / "Resolve.exe"

        with (
            patch.object(Path, "is_file", return_value=True),
            patch.object(
                ResolveSession,
                "connect",
                side_effect=[ResolveConnectionError("stopped"), replacement],
            ) as connect,
            patch("ty_davinci_resolve.connection.subprocess.Popen") as popen,
        ):
            restarted = session.restart(
                executable=executable,
                timeout=1,
                poll_interval=0.001,
            )

        self.assertIs(restarted, replacement)
        self.assertTrue(resolve.quit_called)
        popen.assert_called_once_with([str(executable)])
        self.assertEqual(connect.call_count, 2)


if __name__ == "__main__":
    unittest.main()
