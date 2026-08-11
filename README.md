# Battery Log Validator

Outil de **validation automatisée de logs de test batterie** (tension / température),
avec détection de dépassement de seuils de sécurité et génération d'un rapport
PASS/FAIL traçable — le type de vérification effectuée en amont d'une homologation
ou d'un essai de qualification cellule Li-ion.

## Pourquoi ce projet

Un test batterie génère un log brut (temps, tension, température). Avant de le
considérer conforme, il faut vérifier automatiquement qu'aucune valeur n'a dépassé
les seuils de sécurité définis — et produire une preuve écrite du résultat. C'est
exactement ce que fait cet outil.

## Fonctionnalités

- Lecture de logs CSV (temps, tension, température) avec gestion d'erreurs
  explicite (fichier absent, colonne manquante, valeur non numérique)
- Seuils de sécurité **externalisés** dans `thresholds.yaml`, tracés à leur
  source normative (voir plus bas)
- Détection des dépassements de température **et** de tension (sur-tension
  et sous-tension)
- Génération d'un rapport texte horodaté avec verdict PASS/FAIL
- Génération d'un graphique tension/température avec mise en évidence visuelle
  des anomalies
- Deux jeux de données synthétiques générables (`generate_sample_logs.py`) : un
  scénario nominal et un scénario d'emballement thermique
- Suite de tests unitaires (`pytest`) couvrant la logique de détection et les
  cas d'erreur

## Références normatives des seuils

- **Température** : dérivé des recommandations **UN 38.3** (transport des
  batteries au lithium) et de fiches techniques constructeur typiques pour
  cellules Li-ion NMC/NCA
- **Tension** : plage de fonctionnement nominale d'une cellule Li-ion standard
- **Méthodologie** : structure de validation (seuil → détection → verdict tracé)
  inspirée de l'approche de sécurité fonctionnelle **ISO 26262**

## Installation

```bash
python -m pip install -r requirements.txt
```

## Utilisation

```bash
# 1. Générer les logs d'exemple (à faire une seule fois)
python generate_sample_logs.py

# 2. Lancer la validation sur le scénario d'emballement thermique
python cli.py --log example_log_overheat.csv

# 3. Ou sur le scénario nominal
python cli.py --log example_log_nominal.csv
```

Options disponibles : `--log` (fichier à analyser), `--config` (fichier de
seuils, `thresholds.yaml` par défaut), `--output-dir` (dossier de sortie,
`output/` par défaut).

Le programme retourne un code de sortie `0` si le test est conforme, `1` sinon.

## Lancer les tests

```bash
pytest -v
```

## Exemple de sortie (scénario d'emballement thermique)

```
=== RAPPORT DE VALIDATION - TEST BATTERIE ===
Fichier analyse : example_log_overheat.csv

Temperature maximale enregistree : 128.0 C (seuil : 55.0 C)
Tension min / max enregistree : 3.81 V / 4.10 V (plage attendue : 3.00-4.20 V)

7 anomalie(s) detectee(s) :
  [ALERTE] t=7.0s : temperature au-dessus de seuil (58.80 vs 55.00)
  [ALERTE] t=7.5s : temperature au-dessus de seuil (67.30 vs 55.00)
  ...

VERDICT : TEST ECHOUE (non conforme aux exigences de securite)
```

## Structure du projet

```
battery-log-validator/
├── config.py                # chargement des seuils
├── io_utils.py               # lecture des logs CSV
├── analysis.py                # détection des anomalies
├── report.py                   # génération du rapport texte
├── plotting.py                  # génération du graphique
├── cli.py                        # point d'entrée en ligne de commande
├── thresholds.yaml                # seuils de sécurité, externalisés
├── generate_sample_logs.py         # génère les logs synthétiques
├── test_analysis.py                 # tests unitaires - analyse
├── test_io_utils.py                  # tests unitaires - lecture CSV
└── requirements.txt
```

## Stack technique

- Python (`csv`, `dataclasses`, `argparse`, `logging`)
- `matplotlib` pour la visualisation
- `PyYAML` pour la configuration externalisée
- `pytest` pour les tests unitaires

## Auteur

Maroua Taouil — Ingénieure systèmes embarqués.
