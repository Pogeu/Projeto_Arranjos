from __future__ import annotations

import argparse
import csv
import json
import subprocess
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from src import (
    beampattern,
    conventional_weights,
    generate_uca,
    generate_ucya,
    generate_ula,
    generate_upa,
)
from src.application_figures import save_application_overview
from src.metrics import main_lobe_metrics
from src.transmission import message_signal, simulate_directional_link

WAVELENGTH = 1.0


def ensure_dirs(root: Path) -> None:
    for name in ("figures", "data", "article"):
        (root / name).mkdir(parents=True, exist_ok=True)


def save_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, float]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def set_equal_3d_axes(ax: plt.Axes, positions: np.ndarray) -> None:
    mins = positions.min(axis=0)
    maxs = positions.max(axis=0)
    center = 0.5 * (mins + maxs)
    radius = 0.5 * max(maxs - mins)
    radius = max(radius, 0.5)
    ax.set_xlim(center[0] - radius, center[0] + radius)
    ax.set_ylim(center[1] - radius, center[1] + radius)
    ax.set_zlim(center[2] - radius, center[2] + radius)


def save_position_plot(positions: np.ndarray, title: str, path: Path) -> None:
    fig = plt.figure(figsize=(5.0, 4.2), constrained_layout=True)
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(positions[:, 0], positions[:, 1], positions[:, 2], s=34, c="#0b5cad")
    ax.set_title(title)
    ax.set_xlabel("x / lambda")
    ax.set_ylabel("y / lambda")
    ax.set_zlabel("z / lambda")
    set_equal_3d_axes(ax, positions)
    ax.view_init(elev=22, azim=-42)
    fig.savefig(path, dpi=180)
    plt.close(fig)


def save_geometry_figures(root: Path) -> dict[str, dict[str, float]]:
    geometries = {
        "ULA 16": generate_ula(16, WAVELENGTH / 2.0),
        "UCA 16": generate_uca(16, WAVELENGTH),
        "UPA 4x4": generate_upa(4, 4, WAVELENGTH / 2.0, WAVELENGTH / 2.0),
        "Cilindrico 16x6": generate_ucya(16, 6, WAVELENGTH, WAVELENGTH / 2.0),
    }
    filenames = {
        "ULA 16": "geometry_ula.png",
        "UCA 16": "geometry_uca.png",
        "UPA 4x4": "geometry_upa.png",
        "Cilindrico 16x6": "geometry_ucya.png",
    }

    summary: dict[str, dict[str, float]] = {}
    for title, positions in geometries.items():
        save_position_plot(positions, title, root / "figures" / filenames[title])
        summary[title] = {
            "sensors": int(positions.shape[0]),
            "x_span": float(np.ptp(positions[:, 0])),
            "y_span": float(np.ptp(positions[:, 1])),
            "z_span": float(np.ptp(positions[:, 2])),
        }
    return summary


def plot_ula(root: Path) -> list[dict[str, float | str]]:
    theta_deg = np.linspace(-90.0, 90.0, 1801)
    theta = np.deg2rad(theta_deg)
    fig, ax = plt.subplots(figsize=(6.4, 3.8), constrained_layout=True)
    rows: list[dict[str, float | str]] = []

    for sensors in (9, 16):
        positions = generate_ula(sensors, WAVELENGTH / 2.0)
        pattern = beampattern(positions, 0.0, theta, WAVELENGTH)
        ax.plot(theta_deg, pattern, label=f"M={sensors}")
        metrics = main_lobe_metrics(theta_deg, pattern, target_deg=0.0)
        rows.append({"array": "ULA", "config": f"M={sensors}", **metrics})

    ax.axhline(-3.0, color="0.35", ls="--", lw=0.9, label="-3 dB")
    ax.set_title("ULA: corte de elevacao")
    ax.set_xlabel("Elevacao theta (graus)")
    ax.set_ylabel("Ganho normalizado (dB)")
    ax.set_ylim(-60.0, 2.0)
    ax.grid(True, alpha=0.35)
    ax.legend()
    fig.savefig(root / "figures" / "beampattern_ula.png", dpi=180)
    plt.close(fig)
    return rows


def plot_uca(root: Path) -> list[dict[str, float | str]]:
    phi_deg = np.linspace(0.0, 360.0, 1801)
    phi = np.deg2rad(phi_deg)
    phi0 = np.deg2rad(90.0)
    fig, ax = plt.subplots(figsize=(6.4, 3.8), constrained_layout=True)
    rows: list[dict[str, float | str]] = []

    for sensors in (9, 16):
        positions = generate_uca(sensors, WAVELENGTH)
        weights = conventional_weights(positions, phi0, 0.0, WAVELENGTH)
        pattern = beampattern(positions, phi, 0.0, WAVELENGTH, weights)
        ax.plot(phi_deg, pattern, label=f"M={sensors}")
        metrics = main_lobe_metrics(phi_deg, pattern, target_deg=90.0)
        rows.append({"array": "UCA", "config": f"M={sensors}", **metrics})

    ax.axhline(-3.0, color="0.35", ls="--", lw=0.9, label="-3 dB")
    ax.set_title("UCA: corte de azimute apontado para 90 graus")
    ax.set_xlabel("Azimute phi (graus)")
    ax.set_ylabel("Ganho normalizado (dB)")
    ax.set_ylim(-60.0, 2.0)
    ax.set_xlim(0.0, 360.0)
    ax.grid(True, alpha=0.35)
    ax.legend()
    fig.savefig(root / "figures" / "beampattern_uca.png", dpi=180)
    plt.close(fig)
    return rows


def compute_grid_pattern(
    positions: np.ndarray,
    az_deg: np.ndarray,
    el_deg: np.ndarray,
    target_az_deg: float,
    target_el_deg: float,
) -> np.ndarray:
    az_grid, el_grid = np.meshgrid(np.deg2rad(az_deg), np.deg2rad(el_deg), indexing="xy")
    weights = conventional_weights(
        positions,
        np.deg2rad(target_az_deg),
        np.deg2rad(target_el_deg),
        WAVELENGTH,
    )
    return beampattern(positions, az_grid, el_grid, WAVELENGTH, weights)


def plot_upa(root: Path) -> list[dict[str, float | str]]:
    az_deg = np.linspace(-180.0, 180.0, 361)
    el_deg = np.linspace(-90.0, 90.0, 181)
    rows: list[dict[str, float | str]] = []

    fig, axes = plt.subplots(1, 2, figsize=(8.3, 3.6), constrained_layout=True)
    for ax, side in zip(axes, (3, 4), strict=True):
        positions = generate_upa(side, side, WAVELENGTH / 2.0, WAVELENGTH / 2.0)
        pattern = compute_grid_pattern(positions, az_deg, el_deg, 90.0, 0.0)
        image = ax.imshow(
            pattern,
            origin="lower",
            aspect="auto",
            extent=[az_deg[0], az_deg[-1], el_deg[0], el_deg[-1]],
            vmin=-40.0,
            vmax=0.0,
            cmap="viridis",
        )
        ax.set_title(f"UPA {side}x{side}")
        ax.set_xlabel("Azimute phi (graus)")
        ax.set_ylabel("Elevacao theta (graus)")

        el_cut = pattern[:, np.argmin(np.abs(az_deg - 90.0))]
        metrics = main_lobe_metrics(el_deg, el_cut, target_deg=0.0)
        rows.append({"array": "UPA", "config": f"{side}x{side}", **metrics})

    fig.colorbar(image, ax=axes, label="Ganho (dB)")
    fig.savefig(root / "figures" / "beampattern_upa_heatmap.png", dpi=180)
    plt.close(fig)

    positions = generate_upa(4, 4, WAVELENGTH / 2.0, WAVELENGTH / 2.0)
    az_surface = np.linspace(-120.0, 120.0, 121)
    el_surface = np.linspace(-20.0, 90.0, 81)
    pattern = compute_grid_pattern(positions, az_surface, el_surface, 90.0, 0.0)
    az_grid, el_grid = np.meshgrid(az_surface, el_surface, indexing="xy")

    fig = plt.figure(figsize=(6.8, 4.4), constrained_layout=True)
    ax = fig.add_subplot(111, projection="3d")
    surface = ax.plot_surface(az_grid, el_grid, pattern, cmap="viridis", linewidth=0, antialiased=True)
    ax.set_title("UPA 4x4: superficie do ganho")
    ax.set_xlabel("Azimute phi (graus)")
    ax.set_ylabel("Elevacao theta (graus)")
    ax.set_zlabel("Ganho (dB)")
    ax.set_zlim(-40.0, 0.0)
    fig.colorbar(surface, ax=ax, shrink=0.7, label="Ganho (dB)")
    fig.savefig(root / "figures" / "beampattern_upa_surface.png", dpi=180)
    plt.close(fig)

    return rows


def plot_ucya(root: Path) -> list[dict[str, float | str]]:
    az_deg = np.linspace(0.0, 360.0, 361)
    el_deg = np.linspace(-90.0, 90.0, 181)
    rows: list[dict[str, float | str]] = []

    fig, axes = plt.subplots(2, 2, figsize=(8.4, 6.4), constrained_layout=True)
    configs = [(9, 4), (9, 6), (16, 4), (16, 6)]
    for ax, (mc, nz) in zip(axes.ravel(), configs, strict=True):
        positions = generate_ucya(mc, nz, WAVELENGTH, WAVELENGTH / 2.0)
        pattern = compute_grid_pattern(positions, az_deg, el_deg, 90.0, 0.0)
        image = ax.imshow(
            pattern,
            origin="lower",
            aspect="auto",
            extent=[az_deg[0], az_deg[-1], el_deg[0], el_deg[-1]],
            vmin=-40.0,
            vmax=0.0,
            cmap="viridis",
        )
        ax.set_title(f"Mc={mc}, Nz={nz}")
        ax.set_xlabel("Azimute phi (graus)")
        ax.set_ylabel("Elevacao theta (graus)")

        az_cut = pattern[np.argmin(np.abs(el_deg - 0.0)), :]
        metrics = main_lobe_metrics(az_deg, az_cut, target_deg=90.0)
        rows.append({"array": "Cilindrico", "config": f"Mc={mc}, Nz={nz}", **metrics})

    fig.colorbar(image, ax=axes, label="Ganho (dB)")
    fig.savefig(root / "figures" / "beampattern_ucya_heatmap.png", dpi=180)
    plt.close(fig)
    return rows


def save_beampattern_figures(root: Path) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    rows.extend(plot_ula(root))
    rows.extend(plot_uca(root))
    rows.extend(plot_upa(root))
    rows.extend(plot_ucya(root))
    return rows


def save_transmission_results(root: Path) -> dict[str, object]:
    discrete_angles = np.array([-90.0, -60.0, -30.0, 0.0, 10.0, 20.0, 30.0, 60.0, 90.0])
    t, message, discrete_rows = simulate_directional_link(discrete_angles)
    sweep_angles = np.linspace(-90.0, 90.0, 721)
    _, _, sweep_rows = simulate_directional_link(sweep_angles)

    write_csv(root / "data" / "transmission_discrete.csv", discrete_rows)
    write_csv(root / "data" / "transmission_sweep.csv", sweep_rows)

    fig, ax1 = plt.subplots(figsize=(6.6, 3.8), constrained_layout=True)
    sweep_power = np.array([row["rx_power"] for row in sweep_rows])
    sweep_gain = np.array([row["gain_db"] for row in sweep_rows])
    ax1.plot(sweep_angles, sweep_power, color="#0b5cad", label="Potencia recebida")
    ax1.set_xlabel("Apontamento do receptor theta_R (graus)")
    ax1.set_ylabel("Potencia recebida normalizada", color="#0b5cad")
    ax1.tick_params(axis="y", labelcolor="#0b5cad")
    ax1.grid(True, alpha=0.35)

    ax2 = ax1.twinx()
    ax2.plot(sweep_angles, sweep_gain, color="#b24a00", ls="--", label="Ganho do enlace")
    ax2.set_ylabel("Ganho do enlace (dB)", color="#b24a00")
    ax2.tick_params(axis="y", labelcolor="#b24a00")
    ax2.set_ylim(-60.0, 2.0)
    fig.savefig(root / "figures" / "transmission_sweep.png", dpi=180)
    plt.close(fig)

    responses = {row["theta_rx_deg"]: row for row in discrete_rows}
    aligned_gain = responses[20.0]["voltage_gain"]
    off_gain = responses[0.0]["voltage_gain"]
    fig, ax = plt.subplots(figsize=(6.6, 3.8), constrained_layout=True)
    mask = t <= 0.006
    ax.plot(1e3 * t[mask], message[mask], label="m(t)")
    ax.plot(1e3 * t[mask], aligned_gain * message[mask], "--", label="Recebido alinhado")
    ax.plot(1e3 * t[mask], off_gain * message[mask], ":", label="Recebido theta_R=0")
    ax.set_title("Formas de onda recebidas")
    ax.set_xlabel("Tempo (ms)")
    ax.set_ylabel("Amplitude")
    ax.grid(True, alpha=0.35)
    ax.legend()
    fig.savefig(root / "figures" / "transmission_waveforms.png", dpi=180)
    plt.close(fig)

    return {
        "discrete": discrete_rows,
        "sweep_max_power": float(np.max(sweep_power)),
        "sweep_min_gain_db": float(np.min(sweep_gain)),
    }


def save_two_source_results(root: Path) -> None:
    theta_grid_deg = np.linspace(-90.0, 90.0, 1201)
    source_angles_deg = np.array([-15.0, 25.0])
    source_power = np.array([1.0, 0.8])
    noise_power = 0.02

    fig, ax = plt.subplots(figsize=(6.6, 3.8), constrained_layout=True)
    rows: list[dict[str, float]] = []

    for sensors in (8, 16):
        positions = generate_ula(sensors, WAVELENGTH / 2.0)
        steering = np.column_stack(
            [
                conventional_weights(positions, 0.0, np.deg2rad(angle), WAVELENGTH, normalize=False)
                for angle in source_angles_deg
            ]
        )
        covariance = steering @ np.diag(source_power) @ steering.conj().T
        covariance += noise_power * np.eye(sensors)

        spectrum = []
        for theta_deg in theta_grid_deg:
            weights = conventional_weights(positions, 0.0, np.deg2rad(theta_deg), WAVELENGTH)
            value = np.real(np.conj(weights) @ covariance @ weights)
            spectrum.append(value)
        spectrum = np.asarray(spectrum)
        spectrum_db = 10.0 * np.log10(np.maximum(spectrum / np.max(spectrum), 1e-8))
        ax.plot(theta_grid_deg, spectrum_db, label=f"M={sensors}")

        for angle in source_angles_deg:
            rows.append(
                {
                    "sensors": float(sensors),
                    "source_angle_deg": float(angle),
                    "spectrum_db_at_source": float(
                        spectrum_db[np.argmin(np.abs(theta_grid_deg - angle))]
                    ),
                }
            )

    for angle in source_angles_deg:
        ax.axvline(angle, color="0.25", ls=":", lw=0.9)
    ax.set_title("Separacao angular de duas fontes")
    ax.set_xlabel("Elevacao theta (graus)")
    ax.set_ylabel("Espectro espacial normalizado (dB)")
    ax.set_ylim(-45.0, 2.0)
    ax.grid(True, alpha=0.35)
    ax.legend()
    fig.savefig(root / "figures" / "two_sources_spatial_spectrum.png", dpi=180)
    plt.close(fig)
    write_csv(root / "data" / "two_sources_summary.csv", rows)


def format_float(value: float, digits: int = 2, zero_tol: float | None = None) -> str:
    if zero_tol is not None and abs(value) < zero_tol:
        value = 0.0
    return f"{value:.{digits}f}"


def write_generated_latex(root: Path, metrics_rows: list[dict[str, float | str]], link: dict[str, object]) -> None:
    selected_metrics = [
        row
        for row in metrics_rows
        if row["array"] in {"ULA", "UCA", "UPA"} or row["config"] in {"Mc=16, Nz=6"}
    ]
    lines: list[str] = [
        "% Generated by main.py. Do not edit by hand.",
        "\\begin{table}[H]",
        "\\caption{Resumo numerico dos lobulos principais.}",
        "\\label{tab:metricas}",
        "\\centering",
        "\\begin{tabular}{lccc}",
        "\\hline",
        "Arranjo & Config. & HPBW (graus) & SLL (dB)\\\\",
        "\\hline",
    ]
    for row in selected_metrics:
        lines.append(
            f"{row['array']} & {row['config']} & "
            f"{format_float(float(row['beamwidth_deg']))} & "
            f"{format_float(float(row['sidelobe_db']))}\\\\"
        )
    lines.extend(["\\hline", "\\end{tabular}", "\\end{table}", ""])

    discrete = link["discrete"]
    assert isinstance(discrete, list)
    lines.extend(
        [
            "\\begin{table}[H]",
            "\\caption{Transmissao direcional para apontamentos discretos do receptor.}",
            "\\label{tab:transmissao}",
            "\\centering",
            "\\begin{tabular}{rrrr}",
            "\\hline",
            "$\\theta_R$ & $P_R$ & Ganho (dB) & Corr.\\\\",
            "\\hline",
        ]
    )
    for row in discrete:
        theta = format_float(float(row["theta_rx_deg"]), 0, zero_tol=0.5)
        power = format_float(float(row["rx_power"]), 4)
        gain = format_float(float(row["gain_db"]), 2)
        corr = format_float(float(row["correlation"]), 3)
        lines.append(f"{theta} & {power} & {gain} & {corr}\\\\")
    lines.extend(["\\hline", "\\end{tabular}", "\\end{table}", ""])

    aligned = next(row for row in discrete if abs(float(row["theta_rx_deg"]) - 20.0) < 1e-9)
    lines.extend(
        [
            f"\\newcommand{{\\AlignedPower}}{{{format_float(float(aligned['rx_power']), 4)}}}",
            f"\\newcommand{{\\AlignedGain}}{{{format_float(float(aligned['gain_db']), 2)}}}",
            f"\\newcommand{{\\AlignedCorr}}{{{format_float(float(aligned['correlation']), 3)}}}",
        ]
    )
    (root / "article" / "generated_results.tex").write_text("\n".join(lines), encoding="utf-8")


def compile_paper(root: Path) -> None:
    try:
        result = subprocess.run(
            ["latexmk", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"],
            cwd=root / "article",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        if result.returncode == 0:
            return
    except FileNotFoundError:
        pass

    for _ in range(2):
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "paper.tex"],
            cwd=root / "article",
            check=True,
        )


def run(root: Path, compile_article: bool = False) -> None:
    ensure_dirs(root)
    geometry_summary = save_geometry_figures(root)
    save_application_overview(root / "figures" / "applications_overview.png")
    metrics_rows = save_beampattern_figures(root)
    link = save_transmission_results(root)
    save_two_source_results(root)
    save_json(root / "data" / "geometry_summary.json", geometry_summary)
    save_json(root / "data" / "beampattern_metrics.json", metrics_rows)
    write_generated_latex(root, metrics_rows, link)
    if compile_article:
        compile_paper(root)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Reproduce the sensor array assignment results.")
    parser.add_argument("--compile-paper", action="store_true", help="Compile article/paper.tex with latexmk.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(Path(__file__).resolve().parent, compile_article=args.compile_paper)
