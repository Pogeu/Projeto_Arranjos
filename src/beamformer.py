"""Conventional delay-and-sum beamformer."""

from __future__ import annotations

import numpy as np

from .beampattern import conventional_weights


def beamformer(
    x: np.ndarray,
    positions: np.ndarray,
    steering_direction: tuple[float, float],
    wavelength: float,
) -> np.ndarray:
    """Apply a delay-and-sum beamformer to sensor signals.

    ``x`` must be shaped as ``(M, N)`` or ``(M,)``. Angles in
    ``steering_direction`` are ``(azimuth, elevation)`` in radians.
    """

    x = np.asarray(x, dtype=complex)
    positions = np.asarray(positions, dtype=float)
    if x.shape[0] != positions.shape[0]:
        raise ValueError("x must have one row per sensor")

    azimuth, elevation = steering_direction
    weights = conventional_weights(positions, azimuth, elevation, wavelength)
    return np.conj(weights) @ x
