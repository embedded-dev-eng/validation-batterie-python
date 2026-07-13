import csv
import matplotlib.pyplot as plt

SEUIL_TEMP_MAX = 55
fichier_log = "batterie_logs.csv"

temps_liste = []
tension_liste = []
temperature_liste = []

with open(fichier_log, mode='r', encoding='utf-8') as fichier:
    lecteur_csv = csv.DictReader(fichier)
    for ligne in lecteur_csv:
        temps_liste.append(float(ligne["Temps(s)"]))
        tension_liste.append(float(ligne["Tension(V)"]))
        temperature_liste.append(float(ligne["Temperature(C)"]))

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)

ax1.plot(temps_liste, tension_liste, marker='o', color='tab:blue')
ax1.set_ylabel("Tension (V)")
ax1.set_title("Tension en fonction du temps")
ax1.grid(True)

ax2.plot(temps_liste, temperature_liste, marker='o', color='tab:red', label="Température")
ax2.axhline(y=SEUIL_TEMP_MAX, color='black', linestyle='--', label=f"Seuil critique ({SEUIL_TEMP_MAX}°C)")
ax2.set_xlabel("Temps (s)")
ax2.set_ylabel("Température (°C)")
ax2.set_title("Température en fonction du temps")
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.savefig("courbes_test.png", dpi=150)
print("Graphique sauvegardé sous courbes_test.png")