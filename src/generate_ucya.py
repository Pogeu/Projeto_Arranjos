"""Uniform cylindrical array geometry."""

from __future__ import annotations

import numpy as np

from .generate_ula import _validate_positive_float, _validate_positive_int


def generate_ucya(Mc: int, Nz: int, R: float, dz: float) -> np.ndarray:
    """Return coordinates for a uniform cylindrical array.

    Mc is the number of sensors per ring and Nz is the number of vertical rings.
    """

    Mc = _validate_positive_int("Mc", Mc)
    Nz = _validate_positive_int("Nz", Nz)
    R = _validate_positive_float("R", R)
    dz = _validate_positive_float("dz", dz)

    angles = 2.0 * np.pi * np.arange(Mc, dtype=float) / Mc
    z = (np.arange(Nz, dtype=float) - 0.5 * (Nz - 1)) * dz
    aa, zz = np.meshgrid(angles, z, indexing="xy")

    return np.column_stack(
        (
            R * np.cos(aa).ravel(),
            R * np.sin(aa).ravel(),
            zz.ravel(),
        )
    )
