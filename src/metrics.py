"""Small numerical summaries for beampatterns."""

from __future__ import annotations

import numpy as np


def _interp_crossing(x0: float, y0: float, x1: float, y1: float, level: float) -> float:
    if y1 == y0:
        return x0
    return x0 + (level - y0) * (x1 - x0) / (y1 - y0)


def main_lobe_metrics(
    angle_deg: np.ndarray,
    pattern_db: np.ndarray,
    target_deg: float | None = None,
    level_db: float = -3.0,
) -> dict[str, float]:
    """Estimate main-lobe direction, -3 dB beamwidth and max sidelobe level."""

    angle_deg = np.asarray(angle_deg, dtype=float)
    pattern_db = np.asarray(pattern_db, dtype=float)
    pattern_db = pattern_db - np.max(pattern_db)

    if target_deg is None:
        main_idx = int(np.argmax(pattern_db))
    else:
        main_idx = int(np.argmin(np.abs(angle_deg - target_deg)))

    left = angle_deg[0]
    for idx in range(main_idx, 0, -1):
        if pattern_db[idx - 1] <= level_db <= pattern_db[idx]:
            left = _interp_crossing(
                angle_deg[idx - 1], pattern_db[idx - 1], angle_deg[idx], pattern_db[idx], level_db
            )
            break

    right = angle_deg[-1]
    for idx in range(main_idx, len(angle_deg) - 1):
        if pattern_db[idx] >= level_db >= pattern_db[idx + 1]:
            right = _interp_crossing(
                angle_deg[idx], pattern_db[idx], angle_deg[idx + 1], pattern_db[idx + 1], level_db
            )
            break

    guard_left = min(left, right)
    guard_right = max(left, right)

    left_null = guard_left
    for idx in range(main_idx - 1, 0, -1):
        if pattern_db[idx] <= pattern_db[idx - 1] and pattern_db[idx] <= pattern_db[idx + 1]:
            left_null = angle_deg[idx]
            break

    right_null = guard_right
    for idx in range(main_idx + 1, len(angle_deg) - 1):
        if pattern_db[idx] <= pattern_db[idx - 1] and pattern_db[idx] <= pattern_db[idx + 1]:
            right_null = angle_deg[idx]
            break

    guard_left = min(left_null, right_null)
    guard_right = max(left_null, right_null)
    outside = (angle_deg < guard_left) | (angle_deg > guard_right)
    sidelobe_db = float(np.max(pattern_db[outside])) if np.any(outside) else float("nan")

    return {
        "main_angle_deg": float(angle_deg[main_idx]),
        "beamwidth_deg": float(abs(right - left)),
        "sidelobe_db": sidelobe_db,
    }
