"""Directional transmission experiment."""

from __future__ import annotations

import numpy as np

from .beampattern import array_factor, conventional_weights
from .generate_ula import generate_ula

C0 = 299_792_458.0


def message_signal(fs: float = 20_000.0, duration: float = 0.02) -> tuple[np.ndarray, np.ndarray]:
    """Return the assignment message signal m(t)."""

    t = np.arange(0.0, duration, 1.0 / fs)
    m = np.sin(2.0 * np.pi * 500.0 * t) + 0.5 * np.sin(2.0 * np.pi * 1500.0 * t)
    return t, m


def normalized_correlation(x: np.ndarray, y: np.ndarray) -> float:
    """Return the magnitude of the normalized correlation coefficient."""

    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    denom = np.linalg.norm(x) * np.linalg.norm(y)
    if denom <= 1e-15:
        return 0.0
    return float(abs(np.vdot(x, y)) / denom)


def directional_link_response(
    theta_rx_deg: float,
    theta_tx_deg: float = 20.0,
    fc: float = 1.0e9,
    elements: int = 8,
) -> dict[str, float]:
    """Return normalized voltage and power gains for the ULA-to-ULA link."""

    wavelength = C0 / fc
    positions = generate_ula(elements, wavelength / 2.0)
    theta_tx = np.deg2rad(theta_tx_deg)
    theta_rx = np.deg2rad(theta_rx_deg)

    tx_weights = conventional_weights(positions, 0.0, theta_tx, wavelength)
    rx_weights = conventional_weights(positions, 0.0, theta_rx, wavelength)

    tx_voltage = array_factor(positions, 0.0, theta_tx, wavelength, tx_weights)
    rx_voltage = array_factor(positions, 0.0, theta_tx, wavelength, rx_weights)
    voltage_gain = float(abs(tx_voltage * rx_voltage))
    power_gain = voltage_gain**2
    gain_db = 10.0 * np.log10(max(power_gain, 1e-16))

    return {
        "theta_rx_deg": float(theta_rx_deg),
        "voltage_gain": voltage_gain,
        "power_gain": power_gain,
        "gain_db": float(gain_db),
    }


def simulate_directional_link(
    theta_rx_deg_values: list[float] | np.ndarray,
    theta_tx_deg: float = 20.0,
    fc: float = 1.0e9,
    elements: int = 8,
    fs: float = 20_000.0,
    duration: float = 0.02,
) -> tuple[np.ndarray, np.ndarray, list[dict[str, float]]]:
    """Simulate received waveform power for receiver pointing angles."""

    t, m = message_signal(fs=fs, duration=duration)
    p_tx = float(np.mean(m**2))
    rows: list[dict[str, float]] = []
    for theta_rx in theta_rx_deg_values:
        response = directional_link_response(theta_rx, theta_tx_deg, fc, elements)
        rx = response["voltage_gain"] * m
        response["rx_power"] = float(np.mean(rx**2))
        response["tx_power"] = p_tx
        response["correlation"] = normalized_correlation(m, rx)
        rows.append(response)
    return t, m, rows
