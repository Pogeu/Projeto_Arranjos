"""Steering vector implementation following the assignment convention."""

from __future__ import annotations

import numpy as np


def direction_unit_vector(azimuth: np.ndarray, elevation: np.ndarray) -> np.ndarray:
    """Return unit propagation vectors for azimuth phi and elevation theta.

    Angles are in radians. Broadcasting is supported and the last dimension of
    the returned array stores the x, y and z components.
    """

    azimuth, elevation = np.broadcast_arrays(azimuth, elevation)
    return np.stack(
        (
            np.cos(elevation) * np.cos(azimuth),
            np.cos(elevation) * np.sin(azimuth),
            np.sin(elevation),
        ),
        axis=-1,
    )


def steering_vector(
    positions: np.ndarray,
    azimuth: np.ndarray,
    elevation: np.ndarray,
    wavelength: float,
) -> np.ndarray:
    """Compute a(theta, phi) = exp(-j k r_m^T u).

    The output shape is ``broadcast(azimuth, elevation).shape + (M,)``.
    """

    positions = np.asarray(positions, dtype=float)
    if positions.ndim != 2 or positions.shape[1] != 3:
        raise ValueError("positions must have shape (M, 3)")
    wavelength = float(wavelength)
    if wavelength <= 0:
        raise ValueError("wavelength must be positive")

    unit_vectors = direction_unit_vector(np.asarray(azimuth), np.asarray(elevation))
    phase = np.tensordot(unit_vectors, positions.T, axes=([-1], [0]))
    return np.exp(-1j * (2.0 * np.pi / wavelength) * phase)
