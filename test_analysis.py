"""Tests unitaires du module d'analyse, avec des donnees synthetiques
connues (pas besoin d'un vrai fichier CSV pour tester la logique)."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from io_utils import LogRecord
from config import Thresholds
from analysis import analyze


def make_thresholds() -> Thresholds:
    return Thresholds(
        temp_max_celsius=55.0,
        temp_reference="test",
        voltage_min_volts=3.0,
        voltage_max_volts=4.2,
        voltage_reference="test",
    )


def test_no_anomaly_when_within_bounds():
    records = [
        LogRecord(time_s=0.0, voltage_v=4.0, temperature_c=30.0),
        LogRecord(time_s=1.0, voltage_v=3.9, temperature_c=35.0),
    ]
    result = analyze(records, make_thresholds())
    assert result.passed
    assert result.anomalies == []


def test_detects_temperature_overshoot():
    records = [
        LogRecord(time_s=0.0, voltage_v=4.0, temperature_c=30.0),
        LogRecord(time_s=5.0, voltage_v=3.9, temperature_c=62.0),
    ]
    result = analyze(records, make_thresholds())
    assert not result.passed
    assert len(result.anomalies) == 1
    assert result.anomalies[0].metric == "temperature"
    assert result.anomalies[0].time_s == 5.0


def test_exact_threshold_is_not_an_anomaly():
    """Cas limite : une valeur exactement egale au seuil ne doit pas
    declencher d'alerte (l'anomalie est un depassement STRICT du seuil)."""
    records = [LogRecord(time_s=1.0, voltage_v=4.0, temperature_c=55.0)]
    result = analyze(records, make_thresholds())
    assert result.passed


def test_detects_voltage_undervoltage():
    records = [LogRecord(time_s=2.0, voltage_v=2.5, temperature_c=30.0)]
    result = analyze(records, make_thresholds())
    assert not result.passed
    assert result.anomalies[0].metric == "tension"
    assert result.anomalies[0].direction == "en-dessous de"


def test_detects_multiple_anomalies_same_record():
    """Un enregistrement peut violer plusieurs seuils en meme temps."""
    records = [LogRecord(time_s=3.0, voltage_v=4.5, temperature_c=60.0)]
    result = analyze(records, make_thresholds())
    assert len(result.anomalies) == 2
