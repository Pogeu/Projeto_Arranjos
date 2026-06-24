"""Array factor and beampattern calculations."""

from __future__ import annotations

import numpy as np

from .steering_vector import steering_vector


def conventional_weights(
    positions: np.ndarray,
    azimuth: float,
    elevation: float,
    wavelength: float,
    normalize: bool = True,
) -> np.ndarray:
    """Return delay-and-sum weights steered to one direction."""

    weights = steering_vector(positions, azimuth, elevation, wavelength).reshape(-1)
    if normalize:
        weights = weights / weights.size
    return weights


def array_factor(
    positions: np.ndarray,
    azimuth: np.ndarray,
    elevation: np.ndarray,
    wavelength: float,
    weights: np.ndarray | None = None,
) -> np.ndarray:
    """Compute AF(theta, phi) = w^H a(theta, phi)."""

    positions = np.asarray(positions, dtype=float)
    if weights is None:
        weights = np.ones(positions.shape[0], dtype=complex)
    weights = np.asarray(weights, dtype=complex).reshape(-1)
    if weights.size != positions.shape[0]:
        raise ValueError("weights must have one entry per sensor")

    a = steering_vector(positions, azimuth, elevation, wavelength)
    return np.einsum("m,...m->...", np.conj(weights), a)


def beampattern(
    positions: np.ndarray,
    azimuth: np.ndarray,
    elevation: np.ndarray,
    wavelength: float,
    weights: np.ndarray | None = None,
    floor_db: float = -80.0,
) -> np.ndarray:
    """Return the normalized beampattern in dB."""

    af = array_factor(positions, azimuth, elevation, wavelength, weights)
    magnitude = np.abs(af)
    max_value = np.max(magnitude)
    if max_value <= 0:
        normalized = magnitude
    else:
        normalized = magnitude / max_value

    with np.errstate(divide="ignore"):
        pattern_db = 20.0 * np.log10(np.maximum(normalized, 10.0 ** (floor_db / 20.0)))
    return pattern_db
