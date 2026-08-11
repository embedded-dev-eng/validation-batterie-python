"""Detection des depassements de seuil de securite sur un log batterie.

C'est le coeur metier de l'outil : separe de la lecture (io_utils) et du
rendu (report / plotting), il peut etre teste unitairement avec des
donnees synthetiques, sans dependre d'un vrai fichier CSV.
"""

from dataclasses import dataclass, field
from io_utils import LogRecord
from config import Thresholds


@dataclass(frozen=True)
class AnomalyEvent:
    time_s: float
    metric: str          # "temperature" ou "voltage"
    value: float
    threshold: float
    direction: str        # "au-dessus de" ou "en-dessous de"


@dataclass
class AnalysisResult:
    max_temperature_c: float
    min_voltage_v: float
    max_voltage_v: float
    anomalies: list[AnomalyEvent] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return len(self.anomalies) == 0


def analyze(records: list[LogRecord], thresholds: Thresholds) -> AnalysisResult:
    """Parcourt les enregistrements et detecte tout depassement des seuils
    de temperature et de tension definis dans `thresholds`.
    """
    max_temp = max(r.temperature_c for r in records)
    max_volt = max(r.voltage_v for r in records)
    min_volt = min(r.voltage_v for r in records)

    anomalies: list[AnomalyEvent] = []

    for r in records:
        if r.temperature_c > thresholds.temp_max_celsius:
            anomalies.append(AnomalyEvent(
                time_s=r.time_s,
                metric="temperature",
                value=r.temperature_c,
                threshold=thresholds.temp_max_celsius,
                direction="au-dessus de",
            ))
        if r.voltage_v > thresholds.voltage_max_volts:
            anomalies.append(AnomalyEvent(
                time_s=r.time_s,
                metric="tension",
                value=r.voltage_v,
                threshold=thresholds.voltage_max_volts,
                direction="au-dessus de",
            ))
        if r.voltage_v < thresholds.voltage_min_volts:
            anomalies.append(AnomalyEvent(
                time_s=r.time_s,
                metric="tension",
                value=r.voltage_v,
                threshold=thresholds.voltage_min_volts,
                direction="en-dessous de",
            ))

    return AnalysisResult(
        max_temperature_c=max_temp,
        min_voltage_v=min_volt,
        max_voltage_v=max_volt,
        anomalies=anomalies,
    )
