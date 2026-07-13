import csv

SEUIL_TEMP_MAX = 55
fichier_log = "batterie_logs.csv"

print("=== DÉBUT DE L'ANALYSE DE VALIDATION ===\n")
print("Temps | Profil Thermique")
print("------|---------------------------------------------")

with open(fichier_log, mode='r', encoding='utf-8') as fichier:
    lecteur_csv = csv.DictReader(fichier)
    
    anomalies_detectees = 0
    temperature_maximale = 0
    somme_tensions = 0.0
    nombre_de_mesures = 0
    
    for ligne in lecteur_csv:
        temps = float(ligne["Temps(s)"])
        tension = float(ligne["Tension(V)"])
        temperature = float(ligne["Temperature(C)"])
        
        somme_tensions += tension
        nombre_de_mesures += 1
        
        if temperature > temperature_maximale:
            temperature_maximale = temperature
            
        # 🆕 VISUALISATION : On crée une barre de caractères proportionnelle à la température
        # On divise par 2 pour que la barre ne soit pas trop longue à l'écran
        taille_barre = int(temperature / 2) 
        
        if temperature > SEUIL_TEMP_MAX:
            # Si surchauffe, on dessine avec des '!'
            barre_graphique = "!" * taille_barre
            print(f"{temps:5.1f}s | {barre_graphique} ({temperature}°C) 🚨 ALERTE")
            anomalies_detectees += 1
        else:
            # Sinon, fonctionnement normal avec des '*'
            barre_graphique = "*" * taille_barre
            print(f"{temps:5.1f}s | {barre_graphique} ({temperature}°C)")

tension_moyenne = somme_tensions / nombre_de_mesures

print("\n=== RAPPORT FINAL ===")
print(f"Température maximale enregistrée : {temperature_maximale}°C")
print(f"Tension moyenne de la batterie : {tension_moyenne:.2f} V") 

if anomalies_detectees > 0:
    print("❌ VERDICT : TEST ÉCHOUÉ (Non conforme)")
else:
    print("✅ VERDICT : TEST RÉUSSI (Conforme)")