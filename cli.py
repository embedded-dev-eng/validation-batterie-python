"""Point d'entree en ligne de commande.

Orchestre les modules (config -> io -> analyse -> rapport -> graphique)
sans contenir lui-meme de logique metier : chaque etape est deleguee a
un module testable independamment.
"""

import argparse
import logging
import sys
from pathlib import Path

from config import load_thresholds
from io_utils import read_log
from analysis import analyze
from report import generate_text_report, save_text_report
from plotting import generate_plot

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Valide un log de test batterie contre des seuils de securite."
    )
    parser.add_argument(
        "--log", type=Path, default=Path("example_log_overheat.csv"),
        help="Chemin du fichier CSV de log a analyser.",
    )
    parser.add_argument(
        "--config", type=Path, default=Path("thresholds.yaml"),
        help="Chemin du fichier YAML de seuils.",
    )
    parser.add_argument(
        "--output-dir", type=Path, default=Path("output"),
        help="Dossier ou ecrire le rapport et le graphique.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    try:
        thresholds = load_thresholds(args.config)
        records = read_log(args.log)
    except (FileNotFoundError, ValueError, KeyError) as e:
        logger.error(str(e))
        return 1

    result = analyze(records, thresholds)

    report_text = generate_text_report(result, thresholds, log_name=args.log.name)
    print("\n" + report_text + "\n")

    report_path = args.output_dir / "rapport.txt"
    save_text_report(report_text, report_path)
    logger.info(f"Rapport texte sauvegarde : {report_path}")

    plot_path = args.output_dir / "rapport_complet.png"
    generate_plot(records, result, thresholds, plot_path)
    logger.info(f"Graphique sauvegarde : {plot_path}")

    return 0 if result.passed else 1


if __name__ == "__main__":
    sys.exit(main())
