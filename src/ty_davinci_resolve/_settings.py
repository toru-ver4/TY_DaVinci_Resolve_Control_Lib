"""Canonical 21.1 settings calls with a legacy 21.0.4 path."""

from typing import Any

from .errors import ResolveOperationError


def read_setting(target: Any, scope: str, name: str) -> object:
    """Read a setting using the available official calling convention.

    Parameters
    ----------
    target
        Project or Timeline remote object.
    scope
        Object name used in error messages.
    name
        Setting key.

    Returns
    -------
    object
        Reported setting value.

    Examples
    --------
    >>> read_setting(project, "Project", "timelineFrameRate")  # doctest: +SKIP
    24.0
    """
    getter = getattr(target, "GetSettings", None)
    operation = f"{scope}.GetSettings" if callable(getter) else f"{scope}.GetSetting"
    if callable(getter):
        snapshot = getter()
        if not isinstance(snapshot, dict) or name not in snapshot:
            raise ResolveOperationError(operation, snapshot, f"{operation}: missing setting {name!r}.")
        result = snapshot[name]
    else:
        result = target.GetSetting(name)
    if result is None:
        raise ResolveOperationError(operation, result)
    return result


def write_setting(target: Any, scope: str, name: str, value: str | int) -> None:
    """Write one setting and stop on rejection without retrying another API.

    Parameters
    ----------
    target
        Project or Timeline remote object.
    scope
        Object name used in error messages.
    name
        Setting key.
    value
        Setting value.

    Returns
    -------
    None

    Examples
    --------
    >>> write_setting(project, "Project", "timelineFrameRate", "24")  # doctest: +SKIP
    """
    setter = getattr(target, "SetSettings", None)
    operation = f"{scope}.SetSettings" if callable(setter) else f"{scope}.SetSetting"
    result = setter({name: value}) if callable(setter) else target.SetSetting(name, value)
    if result is not True:
        raise ResolveOperationError(operation, result, f"{operation}: {scope} rejected setting {name!r}.")
