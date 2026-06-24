from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.transmission import simulate_directional_link


angles = np.array([-90.0, -60.0, -30.0, 0.0, 10.0, 20.0, 30.0, 60.0, 90.0])
_, _, rows = simulate_directional_link(angles)

for row in rows:
    print(
        f"theta_R={row['theta_rx_deg']:6.1f} deg | "
        f"P_R={row['rx_power']:.6f} | "
        f"G={row['gain_db']:7.2f} dB | "
        f"corr={row['correlation']:.3f}"
    )
