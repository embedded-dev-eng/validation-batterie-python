# Validation de logs de test batterie

Script Python d'analyse de logs de test embarqué (tension/température d'une batterie),
avec détection automatique de dépassement de seuil de sécurité et génération de graphiques.

## Fonctionnalités

- Lecture de logs CSV (temps, tension, température)
- Détection des dépassements du seuil de sécurité critique
- Génération d'un rapport texte (verdict PASS/FAIL)
- Visualisation graphique avec mise en évidence des anomalies

## Installation

```bash
python -m venv venv
venv\Scripts\Activate.ps1   # Windows
pip install -r requirements.txt
```

## Utilisation

```bash
python rapport_complet.py
```

Génère un fichier `rapport_complet.png` avec les courbes de tension et température,
et affiche un verdict de conformité dans le terminal.

## Exemple de sortie

```
🚨 ALERTE à 5.0s : Température critique de 62.0°C ! (Seuil : 55°C)
❌ VERDICT : TEST ÉCHOUÉ (Le système n'est pas conforme aux exigences)
```