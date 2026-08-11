"""Lecture des fichiers de log CSV de test batterie.

Isoler la lecture de fichier dans son propre module permet de la tester
independamment de l'analyse, et de retourner des erreurs claires plutot
qu'un plantage brut si le fichier est absent ou mal forme.
"""

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class LogRecord:
    time_s: float
    voltage_v: float
    temperature_c: float


REQUIRED_COLUMNS = ("Temps(s)", "Tension(V)", "Temperature(C)")


def read_log(csv_path: Path) -> list[LogRecord]:
    """Lit un fichier CSV de log et retourne une liste de LogRecord.

    Leve FileNotFoundError si le fichier n'existe pas, et ValueError si
    une colonne attendue est absente ou une valeur n'est pas convertible
    en nombre (avec le numero de ligne concerne, pour faciliter le debug).
    """
    if not csv_path.exists():
        raise FileNotFoundError(f"Fichier de log introuvable : {csv_path}")

    records: list[LogRecord] = []

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        missing = [c for c in REQUIRED_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(
                f"Colonne(s) manquante(s) dans {csv_path} : {missing}. "
                f"Colonnes attendues : {REQUIRED_COLUMNS}"
            )

        for line_number, row in enumerate(reader, start=2):  # 2 = apres l'entete
            try:
                records.append(
                    LogRecord(
                        time_s=float(row["Temps(s)"]),
                        voltage_v=float(row["Tension(V)"]),
                        temperature_c=float(row["Temperature(C)"]),
                    )
                )
            except (ValueError, TypeError) as e:
                raise ValueError(
                    f"Valeur non numerique a la ligne {line_number} de {csv_path} : {row}"
                ) from e

    if not records:
        raise ValueError(f"Le fichier {csv_path} ne contient aucune donnee exploitable.")

    return records
