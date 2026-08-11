"""Generation du graphique tension/temperature avec mise en evidence
des anomalies detectees."""

from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # rendu sans interface graphique (utile en CI / serveur)
import matplotlib.pyplot as plt

from io_utils import LogRecord
from analysis import AnalysisResult
from config import Thresholds


def generate_plot(
    records: list[LogRecord],
    result: AnalysisResult,
    thresholds: Thresholds,
    output_path: Path,
) -> None:
    temps = [r.time_s for r in records]
    tensions = [r.voltage_v for r in records]
    temperatures = [r.temperature_c for r in records]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

    ax1.plot(temps, tensions, marker="o", color="tab:blue")
    ax1.axhline(thresholds.voltage_max_volts, color="black", linestyle="--",
                linewidth=0.8, label=f"Max ({thresholds.voltage_max_volts} V)")
    ax1.axhline(thresholds.voltage_min_volts, color="gray", linestyle="--",
                linewidth=0.8, label=f"Min ({thresholds.voltage_min_volts} V)")
    ax1.set_ylabel("Tension (V)")
    ax1.set_title("Tension en fonction du temps")
    ax1.legend(fontsize=8)
    ax1.grid(True)

    ax2.plot(temps, temperatures, color="tab:red", zorder=1)

    temp_anomaly_times = [a.time_s for a in result.anomalies if a.metric == "temperature"]
    temp_anomaly_values = [a.value for a in result.anomalies if a.metric == "temperature"]

    ax2.scatter(temps, temperatures, color="tab:red", s=15, zorder=2)
    if temp_anomaly_times:
        ax2.scatter(temp_anomaly_times, temp_anomaly_values, color="darkred",
                    s=100, marker="X", label="Anomalie detectee", zorder=3)

    ax2.axhline(thresholds.temp_max_celsius, color="black", linestyle="--",
                label=f"Seuil critique ({thresholds.temp_max_celsius} C)")
    ax2.set_xlabel("Temps (s)")
    ax2.set_ylabel("Temperature (C)")
    ax2.set_title("Temperature en fonction du temps")
    ax2.legend(fontsize=8)
    ax2.grid(True)

    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close(fig)
