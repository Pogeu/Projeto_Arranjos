"""Build the report application panel from externally sourced photographs."""

from __future__ import annotations

from pathlib import Path

import matplotlib.image as mpimg
import matplotlib.pyplot as plt


PANELS = (
    ("applications/radar_phased_array.jpg", "Radar faseado"),
    ("applications/sonar_principle.png", "Sonar"),
    ("applications/wireless_base_station.jpg", "Comunicações sem fio"),
    ("applications/acoustic_microphone_array.jpg", "Sistemas acústicos"),
    ("applications/massive_mimo_5g_antennas.jpg", "Massive MIMO"),
)


def save_application_overview(figures_dir: Path) -> None:
    """Create one reproducible multi-panel figure from the source images."""

    figures_dir = Path(figures_dir)
    missing = [relative for relative, _ in PANELS if not (figures_dir / relative).is_file()]
    if missing:
        names = ", ".join(missing)
        raise FileNotFoundError(
            f"missing application source images: {names}; "
            "run examples/download_application_images.py"
        )

    fig = plt.figure(figsize=(10.2, 5.2), constrained_layout=True)
    grid = fig.add_gridspec(2, 6)
    slots = ((0, slice(0, 2)), (0, slice(2, 4)), (0, slice(4, 6)), (1, slice(1, 3)), (1, slice(3, 5)))

    for (relative, title), (row, columns) in zip(PANELS, slots, strict=True):
        ax = fig.add_subplot(grid[row, columns])
        ax.imshow(mpimg.imread(figures_dir / relative))
        ax.set_title(title, fontsize=10, fontweight="bold")
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color("0.75")
            spine.set_linewidth(0.7)

    fig.savefig(figures_dir / "applications_overview.png", dpi=180, facecolor="white")
    plt.close(fig)
