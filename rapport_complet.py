import csv
import matplotlib.pyplot as plt

# Seuil de sécurité critique défini par le cahier des charges
SEUIL_TEMP_MAX = 55
fichier_log = "batterie_logs.csv"

print("=== DÉBUT DE L'ANALYSE DE VALIDATION ===\n")

# Listes pour stocker toutes les valeurs (pour le graphique)
temps_liste = []
tension_liste = []
temperature_liste = []

anomalies_detectees = 0
temperature_maximale = 0

# Lecture du CSV ligne par ligne
with open(fichier_log, mode='r', encoding='utf-8') as fichier:
    lecteur_csv = csv.DictReader(fichier)
    for ligne in lecteur_csv:
        temps = float(ligne["Temps(s)"])
        tension = float(ligne["Tension(V)"])
        temperature = float(ligne["Temperature(C)"])

        # On stocke chaque valeur dans les listes
        temps_liste.append(temps)
        tension_liste.append(tension)
        temperature_liste.append(temperature)

        if temperature > temperature_maximale:
            temperature_maximale = temperature

        if temperature > SEUIL_TEMP_MAX:
            print(f"🚨 ALERTE à {temps}s : Température critique de {temperature}°C ! (Seuil : {SEUIL_TEMP_MAX}°C)")
            anomalies_detectees += 1

# Rapport texte final
print("\n=== RAPPORT FINAL ===")
print(f"Température maximale enregistrée : {temperature_maximale}°C")

if anomalies_detectees > 0:
    print("❌ VERDICT : TEST ÉCHOUÉ (Le système n'est pas conforme aux exigences)")
else:
    print("✅ VERDICT : TEST RÉUSSI (Système conforme)")

# --- Génération du graphique ---

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

# Tension
ax1.plot(temps_liste, tension_liste, marker='o', color='tab:blue')
ax1.set_ylabel("Tension (V)")
ax1.set_title("Tension en fonction du temps")
ax1.grid(True)

# Température, avec la courbe normale en rouge clair
ax2.plot(temps_liste, temperature_liste, color='tab:red', label="Température", zorder=1)

# On sépare les points en 2 groupes : normaux vs anomalies
temps_normaux = [t for t, temp in zip(temps_liste, temperature_liste) if temp <= SEUIL_TEMP_MAX]
temp_normaux = [temp for temp in temperature_liste if temp <= SEUIL_TEMP_MAX]

temps_anomalies = [t for t, temp in zip(temps_liste, temperature_liste) if temp > SEUIL_TEMP_MAX]
temp_anomalies = [temp for temp in temperature_liste if temp > SEUIL_TEMP_MAX]

ax2.scatter(temps_normaux, temp_normaux, color='tab:red', zorder=2)
ax2.scatter(temps_anomalies, temp_anomalies, color='darkred', s=100, marker='X',
            label="Anomalie détectée", zorder=3)

ax2.axhline(y=SEUIL_TEMP_MAX, color='black', linestyle='--', label=f"Seuil critique ({SEUIL_TEMP_MAX}°C)")
ax2.set_xlabel("Temps (s)")
ax2.set_ylabel("Température (°C)")
ax2.set_title("Température en fonction du temps")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig("rapport_complet.png", dpi=150)
print("\nGraphique sauvegardé sous rapport_complet.png")