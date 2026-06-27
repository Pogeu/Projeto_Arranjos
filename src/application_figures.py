"""Code-generated illustrations for sensor array applications."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Arc, Circle, Ellipse, FancyArrowPatch, Polygon, Rectangle


def _prepare_panel(ax: plt.Axes, title: str, color: str) -> None:
    ax.set_xlim(0.0, 10.0)
    ax.set_ylim(0.0, 7.0)
    ax.set_aspect("equal")
    ax.set_facecolor(color)
    ax.set_title(title, fontsize=11, fontweight="bold", pad=7)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#c7d0d9")


def _draw_array(ax: plt.Axes, x: float, y: float, rows: int, cols: int, scale: float = 1.0) -> None:
    width = cols * 0.28 * scale
    height = rows * 0.28 * scale
    ax.add_patch(
        Rectangle(
            (x - 0.18 * scale, y - 0.18 * scale),
            width + 0.36 * scale,
            height + 0.36 * scale,
            facecolor="#34495e",
            edgecolor="#1f2f3d",
            linewidth=1.0,
            zorder=3,
        )
    )
    for row in range(rows):
        for col in range(cols):
            ax.add_patch(
                Circle(
                    (x + col * 0.28 * scale, y + row * 0.28 * scale),
                    0.07 * scale,
                    facecolor="#d9eef7",
                    edgecolor="none",
                    zorder=4,
                )
            )


def _draw_radar(ax: plt.Axes) -> None:
    _prepare_panel(ax, "Radar", "#eef5fa")
    ax.plot([0, 10], [0.9, 0.9], color="#6b7b55", linewidth=2)
    _draw_array(ax, 1.0, 1.2, rows=8, cols=3, scale=0.9)
    source = (1.65, 2.25)
    targets = [(7.8, 5.7), (8.7, 3.9)]
    colors = ["#e74c3c", "#f39c12"]
    for target, color in zip(targets, colors, strict=True):
        ax.add_patch(
            FancyArrowPatch(
                source,
                target,
                arrowstyle="-|>",
                mutation_scale=12,
                linewidth=2.2,
                color=color,
                alpha=0.85,
            )
        )
        x, y = target
        ax.add_patch(
            Polygon(
                [(x - 0.45, y), (x + 0.45, y), (x + 0.05, y + 0.12), (x - 0.1, y + 0.35)],
                closed=True,
                facecolor="#40556b",
                edgecolor="none",
            )
        )
    ax.text(0.65, 0.35, "varredura e rastreamento", fontsize=8.5, color="#32475b")


def _draw_sonar(ax: plt.Axes) -> None:
    _prepare_panel(ax, "Sonar", "#dff4fb")
    ax.plot([0, 10], [5.9, 5.9], color="#2f90b7", linewidth=2)
    ax.add_patch(Polygon([(1.8, 6.2), (4.5, 6.2), (4.0, 5.65), (2.2, 5.65)], color="#516b78"))
    ax.add_patch(Rectangle((2.5, 6.2), 1.25, 0.45, color="#e8ecef"))
    source = (3.15, 5.55)
    ax.add_patch(Circle(source, 0.14, color="#f39c12"))
    for radius in (1.5, 2.4, 3.3):
        ax.add_patch(
            Arc(source, 2 * radius, 1.4 * radius, theta1=205, theta2=335, color="#1687b0", linewidth=1.6)
        )
    ax.add_patch(Ellipse((7.25, 2.35), 2.0, 0.65, facecolor="#4d6470", edgecolor="#2e424c"))
    ax.add_patch(Polygon([(8.0, 2.35), (8.75, 2.8), (8.75, 1.9)], color="#4d6470"))
    ax.plot([0, 2, 4, 6, 8, 10], [0.45, 0.7, 0.4, 0.65, 0.35, 0.55], color="#9b7653", linewidth=2)
    ax.text(5.65, 0.75, "eco e direcao de chegada", fontsize=8.5, color="#1b607a")


def _draw_wireless(ax: plt.Axes) -> None:
    _prepare_panel(ax, "Comunicacoes sem fio", "#f4f7f1")
    ax.plot([1.5, 1.5], [0.8, 5.8], color="#46595f", linewidth=3)
    ax.plot([0.9, 2.1], [0.8, 0.8], color="#46595f", linewidth=3)
    _draw_array(ax, 1.05, 4.2, rows=5, cols=3, scale=0.72)
    endpoints = [(7.8, 5.5), (8.2, 3.4), (7.2, 1.5)]
    colors = ["#2e86de", "#9b59b6", "#16a085"]
    for idx, (target, color) in enumerate(zip(endpoints, colors, strict=True), start=1):
        ax.add_patch(
            FancyArrowPatch(
                (2.0, 4.8),
                target,
                arrowstyle="-|>",
                mutation_scale=12,
                connectionstyle=f"arc3,rad={0.12 * (idx - 2)}",
                linewidth=2.1,
                color=color,
            )
        )
        ax.add_patch(Circle((target[0], target[1] + 0.2), 0.2, facecolor="#f2c9a5", edgecolor="none"))
        ax.plot([target[0], target[0]], [target[1] - 0.55, target[1]], color="#46595f", linewidth=2)
    ax.text(4.25, 0.55, "feixes por usuario", fontsize=8.5, color="#3e5b43")


def _draw_acoustic(ax: plt.Axes) -> None:
    _prepare_panel(ax, "Sistemas acusticos", "#fbf4ed")
    ax.add_patch(Circle((1.6, 4.35), 0.35, facecolor="#e0ad87", edgecolor="none"))
    ax.plot([1.6, 1.6], [1.5, 4.0], color="#59636b", linewidth=3)
    ax.plot([1.6, 0.9], [3.1, 2.3], color="#59636b", linewidth=2)
    ax.plot([1.6, 2.3], [3.1, 2.3], color="#59636b", linewidth=2)
    for radius in (0.7, 1.2, 1.7):
        ax.add_patch(Arc((2.05, 4.15), 2 * radius, 1.25 * radius, theta1=-35, theta2=35, color="#d35400"))
    center = np.array([7.3, 3.5])
    for angle in np.linspace(0.0, 2.0 * np.pi, 10, endpoint=False):
        point = center + 1.35 * np.array([np.cos(angle), np.sin(angle)])
        ax.add_patch(Circle(point, 0.18, facecolor="#2471a3", edgecolor="white", linewidth=0.8))
    ax.add_patch(Circle(center, 0.26, facecolor="#1f618d", edgecolor="none"))
    ax.text(5.0, 0.55, "captacao e supressao de ruido", fontsize=8.5, color="#734c2f")


def _draw_massive_mimo(ax: plt.Axes) -> None:
    _prepare_panel(ax, "Massive MIMO", "#f3f0fa")
    _draw_array(ax, 0.8, 1.35, rows=12, cols=6, scale=0.86)
    users = [(7.4, 5.6), (8.65, 3.5), (7.0, 1.35)]
    colors = ["#8e44ad", "#2980b9", "#c0392b"]
    for idx, ((x, y), color) in enumerate(zip(users, colors, strict=True), start=1):
        ax.add_patch(
            FancyArrowPatch(
                (2.35, 3.3),
                (x - 0.35, y),
                arrowstyle="simple",
                mutation_scale=8,
                linewidth=0,
                color=color,
                alpha=0.65,
                connectionstyle=f"arc3,rad={0.09 * (idx - 2)}",
            )
        )
        ax.add_patch(Circle((x, y + 0.25), 0.22, facecolor="#e0ad87", edgecolor="none"))
        ax.plot([x, x], [y - 0.55, y], color="#4e5963", linewidth=2.2)
        label_x = x + 0.28 if x < 8.0 else x - 1.35
        ax.text(label_x, y - 0.15, f"Usuario {idx}", fontsize=7.8)
    ax.text(3.4, 0.3, "multiplexacao espacial multiusuario", fontsize=8.5, color="#57366d")


def save_application_overview(path: Path) -> None:
    """Generate a five-panel overview of array processing applications."""

    fig = plt.figure(figsize=(12.2, 7.9), constrained_layout=True)
    grid = fig.add_gridspec(2, 6)
    _draw_radar(fig.add_subplot(grid[0, 0:2]))
    _draw_sonar(fig.add_subplot(grid[0, 2:4]))
    _draw_wireless(fig.add_subplot(grid[0, 4:6]))
    _draw_acoustic(fig.add_subplot(grid[1, 0:3]))
    _draw_massive_mimo(fig.add_subplot(grid[1, 3:6]))
    fig.savefig(path, dpi=200, facecolor="white")
    plt.close(fig)
