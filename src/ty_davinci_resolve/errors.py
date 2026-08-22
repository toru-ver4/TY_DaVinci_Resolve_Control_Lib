"""Exceptions raised by TY DaVinci Resolve Control."""

from __future__ import annotations

from typing import Any


class ResolveError(RuntimeError):
    """Base exception for this package."""


class ResolveConnectionError(ResolveError):
    """Raised when the package cannot connect to DaVinci Resolve."""


class ResolveVersionError(ResolveConnectionError):
    """Raised when the connected Resolve version is unsupported."""

    def __init__(
        self,
        actual: tuple[int, ...],
        expected: tuple[int, int, int],
    ) -> None:
        """Initialize a Resolve version error.

        Parameters
        ----------
        actual
            Version fields reported by Resolve.
        expected
            Required major, minor, and patch version.

        Returns
        -------
        None

        Examples
        --------
        >>> ResolveVersionError((21, 0, 3), (21, 0, 4))
        ResolveVersionError('Unsupported DaVinci Resolve version: expected 21.0.4, got 21.0.3.')
        """
        self.actual = actual
        self.expected = expected
        actual_text = ".".join(str(value) for value in actual[:3])
        expected_text = ".".join(str(value) for value in expected)
        super().__init__(
            "Unsupported DaVinci Resolve version: "
            f"expected {expected_text}, got {actual_text}."
        )


class ResolveOperationError(ResolveError):
    """Raised when a Resolve API operation reports failure."""

    def __init__(
        self,
        operation: str,
        return_value: Any,
        message: str | None = None,
    ) -> None:
        """Initialize a Resolve operation error.

        Parameters
        ----------
        operation
            Resolve API operation name.
        return_value
            Failure value returned by Resolve.
        message
            Optional detailed error message.

        Returns
        -------
        None

        Examples
        --------
        >>> ResolveOperationError("Project.SaveProject", False)
        ResolveOperationError('Project.SaveProject failed (returned False).')
        """
        self.operation = operation
        self.return_value = return_value
        detail = message or f"{operation} failed (returned {return_value!r})."
        super().__init__(detail)


class ResolveValidationError(ResolveError, ValueError):
    """Raised before calling Resolve when an argument is invalid."""

