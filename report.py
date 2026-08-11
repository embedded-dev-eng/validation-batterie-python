"""Generation du rapport texte de verdict PASS/FAIL."""

from pathlib import Path
from analysis import AnalysisResult
from config import Thresholds


def generate_text_report(result: AnalysisResult, thresholds: Thresholds, log_name: str) -> str:
    lines = []
    lines.append("=== RAPPORT DE VALIDATION - TEST BATTERIE ===")
    lines.append(f"Fichier analyse : {log_name}")
    lines.append("")
    lines.append(f"Temperature maximale enregistree : {result.max_temperature_c:.1f} C "
                  f"(seuil : {thresholds.temp_max_celsius:.1f} C)")
    lines.append(f"Tension min / max enregistree : {result.min_voltage_v:.2f} V / "
                  f"{result.max_voltage_v:.2f} V "
                  f"(plage attendue : {thresholds.voltage_min_volts:.2f}-"
                  f"{thresholds.voltage_max_volts:.2f} V)")
    lines.append("")

    if result.anomalies:
        lines.append(f"{len(result.anomalies)} anomalie(s) detectee(s) :")
        for a in result.anomalies:
            lines.append(
                f"  [ALERTE] t={a.time_s:.1f}s : {a.metric} {a.direction} "
                f"seuil ({a.value:.2f} vs {a.threshold:.2f})"
            )
        lines.append("")
        lines.append("VERDICT : TEST ECHOUE (non conforme aux exigences de securite)")
    else:
        lines.append("Aucune anomalie detectee.")
        lines.append("")
        lines.append("VERDICT : TEST REUSSI (conforme)")

    return "\n".join(lines)


def save_text_report(report_text: str, output_path: Path) -> None:
    output_path.write_text(report_text, encoding="utf-8")
