"""Uniform planar array geometry."""

from __future__ import annotations

import numpy as np

from .generate_ula import _validate_positive_float, _validate_positive_int


def generate_upa(Mx: int, My: int, dx: float, dy: float) -> np.ndarray:
    """Return coordinates for an Mx by My planar array in the xz-plane."""

    Mx = _validate_positive_int("Mx", Mx)
    My = _validate_positive_int("My", My)
    dx = _validate_positive_float("dx", dx)
    dy = _validate_positive_float("dy", dy)

    x = (np.arange(Mx, dtype=float) - 0.5 * (Mx - 1)) * dx
    y = (np.arange(My, dtype=float) - 0.5 * (My - 1)) * dy
    xx, yy = np.meshgrid(x, y, indexing="xy")

    return np.column_stack(
        (
            xx.ravel(),
            np.zeros(Mx * My, dtype=float),
            yy.ravel(),
        )
    )
