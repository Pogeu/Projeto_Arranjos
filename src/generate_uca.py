"""Uniform circular array geometry."""

from __future__ import annotations

import numpy as np

from .generate_ula import _validate_positive_float, _validate_positive_int


def generate_uca(M: int, R: float) -> np.ndarray:
    """Return M coordinates uniformly distributed on a circle in the xy-plane."""

    M = _validate_positive_int("M", M)
    R = _validate_positive_float("R", R)
    angles = 2.0 * np.pi * np.arange(M, dtype=float) / M

    return np.column_stack(
        (
            R * np.cos(angles),
            R * np.sin(angles),
            np.zeros(M, dtype=float),
        )
    )
