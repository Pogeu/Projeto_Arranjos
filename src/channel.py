"""Narrowband line-of-sight propagation channel models."""

from __future__ import annotations

import numpy as np


def free_space_los_channel(
    tx_positions: np.ndarray,
    rx_positions: np.ndarray,
    wavelength: float,
) -> np.ndarray:
    """Return the free-space LOS channel matrix between two sensor arrays.

    Positions and wavelength use the same distance unit. The returned matrix
    has shape ``(N_rx, N_tx)`` and applies the Friis voltage factor together
    with the propagation phase for every transmitter-receiver pair.
    """

    tx_positions = np.asarray(tx_positions, dtype=float)
    rx_positions = np.asarray(rx_positions, dtype=float)
    if tx_positions.ndim != 2 or tx_positions.shape[1] != 3:
        raise ValueError("tx_positions must have shape (N_tx, 3)")
    if rx_positions.ndim != 2 or rx_positions.shape[1] != 3:
        raise ValueError("rx_positions must have shape (N_rx, 3)")

    wavelength = float(wavelength)
    if wavelength <= 0:
        raise ValueError("wavelength must be positive")

    displacement = rx_positions[:, None, :] - tx_positions[None, :, :]
    distance = np.linalg.norm(displacement, axis=-1)
    if np.any(distance <= 0):
        raise ValueError("transmit and receive elements cannot occupy the same position")

    voltage_gain = wavelength / (4.0 * np.pi * distance)
    phase = np.exp(-1j * 2.0 * np.pi * distance / wavelength)
    return voltage_gain * phase
