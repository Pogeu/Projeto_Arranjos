from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src import beampattern, generate_ula


theta_deg = np.linspace(-90.0, 90.0, 721)
positions = generate_ula(16, 0.5)
pattern = beampattern(positions, 0.0, np.deg2rad(theta_deg), 1.0)

fig, ax = plt.subplots(figsize=(6.0, 3.6), constrained_layout=True)
ax.plot(theta_deg, pattern, label="M=16")
ax.set_xlabel("Elevacao theta (graus)")
ax.set_ylabel("Ganho normalizado (dB)")
ax.set_title("Exemplo: ULA M=16")
ax.grid(True, alpha=0.35)
ax.legend()
fig.savefig(ROOT / "figures" / "example_ula_m16.png", dpi=180)
plt.close(fig)
print(ROOT / "figures" / "example_ula_m16.png")
