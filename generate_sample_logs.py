"""Genere deux jeux de logs CSV synthetiques mais physiquement plausibles,
pour demontrer l'outil sans dependre d'un vrai banc de test :

- example_log_nominal.csv   : charge normale, temperature stabilisee sous le seuil
- example_log_overheat.csv  : meme profil, mais avec un emballement thermique
                               simule a partir de t=4s (cas de detection d'anomalie)

Modele physique simplifie : tension qui decroit legerement en decharge
(courbe Li-ion approximee), temperature qui monte avec l'auto-echauffement.
"""

import csv
import math
from pathlib import Path

OUTPUT_DIR = Path(".")
DURATION_S = 10
STEP_S = 0.5


def voltage_profile(t: float) -> float:
    """Decharge Li-ion approximee : legere baisse quasi-lineaire avec un peu de bruit."""
    base = 4.1 - 0.03 * t
    ripple = 0.01 * math.sin(t * 2)
    return round(base + ripple, 3)


def temperature_profile_nominal(t: float) -> float:
    """Montee en temperature qui se stabilise sous le seuil de securite (55 C)."""
    return round(25 + 15 * (1 - math.exp(-t / 5)), 1)


def temperature_profile_overheat(t: float) -> float:
    """Meme depart que le cas nominal, mais emballement thermique a partir de t=4s."""
    base = 25 + 15 * (1 - math.exp(-t / 5))
    if t >= 4.0:
        base += (t - 4.0) ** 2 * 2.5  # emballement quadratique
    return round(base, 1)


def write_log(path: Path, temp_fn) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Temps(s)", "Tension(V)", "Temperature(C)"])
        t = 0.0
        while t <= DURATION_S:
            writer.writerow([round(t, 1), voltage_profile(t), temp_fn(t)])
            t += STEP_S


if __name__ == "__main__":
    write_log(OUTPUT_DIR / "example_log_nominal.csv", temperature_profile_nominal)
    write_log(OUTPUT_DIR / "example_log_overheat.csv", temperature_profile_overheat)
    print(f"OK: {OUTPUT_DIR / 'example_log_nominal.csv'}")
    print(f"OK: {OUTPUT_DIR / 'example_log_overheat.csv'}")
