"""Tests unitaires du module io_utils : verifie la gestion d'erreurs,
pas seulement le cas ideal."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import pytest
from io_utils import read_log


def test_read_valid_log(tmp_path):
    csv_content = "Temps(s),Tension(V),Temperature(C)\n0.0,4.1,25.0\n1.0,4.0,26.5\n"
    log_file = tmp_path / "log.csv"
    log_file.write_text(csv_content, encoding="utf-8")

    records = read_log(log_file)
    assert len(records) == 2
    assert records[0].time_s == 0.0
    assert records[1].temperature_c == 26.5


def test_missing_file_raises_clear_error(tmp_path):
    missing_path = tmp_path / "does_not_exist.csv"
    with pytest.raises(FileNotFoundError):
        read_log(missing_path)


def test_missing_column_raises_value_error(tmp_path):
    csv_content = "Temps(s),Tension(V)\n0.0,4.1\n"  # colonne Temperature(C) absente
    log_file = tmp_path / "bad_log.csv"
    log_file.write_text(csv_content, encoding="utf-8")

    with pytest.raises(ValueError, match="Colonne"):
        read_log(log_file)


def test_non_numeric_value_raises_value_error(tmp_path):
    csv_content = "Temps(s),Tension(V),Temperature(C)\n0.0,4.1,PANNE_CAPTEUR\n"
    log_file = tmp_path / "corrupted_log.csv"
    log_file.write_text(csv_content, encoding="utf-8")

    with pytest.raises(ValueError, match="ligne 2"):
        read_log(log_file)


def test_empty_log_raises_value_error(tmp_path):
    csv_content = "Temps(s),Tension(V),Temperature(C)\n"  # entete seule, aucune donnee
    log_file = tmp_path / "empty_log.csv"
    log_file.write_text(csv_content, encoding="utf-8")

    with pytest.raises(ValueError, match="aucune donnee"):
        read_log(log_file)
