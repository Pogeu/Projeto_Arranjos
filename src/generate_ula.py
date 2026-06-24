"""Uniform linear array geometry."""

from __future__ import annotations

import numpy as np

_AXES = {"x": 0, "y": 1, "z": 2}


def _validate_positive_int(name: str, value: int) -> int:
    value = int(value)
    if value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def _validate_positive_float(name: str, value: float) -> float:
    value = float(value)
    if value <= 0:
        raise ValueError(f"{name} must be positive")
    return value


def generate_ula(M: int, d: float, axis: str = "z", center: bool = True) -> np.ndarray:
    """Return M three-dimensional coordinates for a ULA.

    The default axis is z so the elevation angle in the assignment behaves as
    the broadside scan angle for the one-dimensional examples.
    """

    M = _validate_positive_int("M", M)
    d = _validate_positive_float("d", d)
    if axis not in _AXES:
        raise ValueError(f"axis must be one of {sorted(_AXES)}")

    offsets = np.arange(M, dtype=float) * d
    if center:
        offsets -= 0.5 * (M - 1) * d

    positions = np.zeros((M, 3), dtype=float)
    positions[:, _AXES[axis]] = offsets
    return positions
