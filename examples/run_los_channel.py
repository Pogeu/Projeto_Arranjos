from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src import free_space_los_channel, generate_ula


wavelength = 0.3
tx = generate_ula(4, wavelength / 2.0, axis="y")
rx = generate_ula(4, wavelength / 2.0, axis="y") + np.array([10.0, 0.0, 0.0])
channel = free_space_los_channel(tx, rx, wavelength)

print("Magnitude do canal LOS:")
print(np.abs(channel))
print("Fase do canal LOS (graus):")
print(np.rad2deg(np.angle(channel)))
