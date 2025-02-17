import json
import random

# Liste des appareils
appareils = [
    {"id": 1, "nom": "Réfrigérateur", "consommation_W": 150, "appel_puissance_W": 600},
    {"id": 2, "nom": "Congélateur", "consommation_W": 200, "appel_puissance_W": 800},
    {"id": 3, "nom": "Lave-linge", "consommation_W": 500, "appel_puissance_W": 2500},
    {"id": 4, "nom": "Lave-vaisselle", "consommation_W": 1200, "appel_puissance_W": 2200},
    {"id": 5, "nom": "Four électrique", "consommation_W": 2500, "appel_puissance_W": 3000},
    {"id": 6, "nom": "Micro-ondes", "consommation_W": 1200, "appel_puissance_W": 1500},
    {"id": 7, "nom": "Plaque de cuisson électrique", "consommation_W": 2000, "appel_puissance_W": 2500},
    {"id": 8, "nom": "Téléviseur LCD", "consommation_W": 100, "appel_puissance_W": 150},
    {"id": 9, "nom": "Ordinateur de bureau", "consommation_W": 300, "appel_puissance_W": 500},
    {"id": 10, "nom": "Aspirateur", "consommation_W": 800, "appel_puissance_W": 1600},
    {"id": 11, "nom": "Climatiseur", "consommation_W": 2000, "appel_puissance_W": 3000},
    {"id": 12, "nom": "Ventilateur", "consommation_W": 50, "appel_puissance_W": 100},
    {"id": 13, "nom": "Radiateur électrique", "consommation_W": 1500, "appel_puissance_W": 2000},
    {"id": 14, "nom": "Chauffe-eau électrique", "consommation_W": 3000, "appel_puissance_W": 3500},
    {"id": 15, "nom": "Fer à repasser", "consommation_W": 1200, "appel_puissance_W": 1500},
    {"id": 16, "nom": "Kit vidéo surveillance, 4 caméras", "consommation_W": 50, "appel_puissance_W": 100},
    {"id": 17, "nom": "6 Ampoules LED (18 W)", "consommation_W": 108, "appel_puissance_W": 108},
    {"id": 18, "nom": "Ascenseur", "consommation_W": 3000, "appel_puissance_W": 5000},
    {"id": 19, "nom": "Porte de garage motorisée", "consommation_W": 150, "appel_puissance_W": 500},
    {"id": 20, "nom": "Plaques de cuisson à induction", "consommation_W": 2500, "appel_puissance_W": 3000},
    {"id": 21, "nom": "Ordinateur Mac Pro", "consommation_W": 350, "appel_puissance_W": 500},
    {"id": 22, "nom": "Téléviseur TV QLED 55 en mode HDR", "consommation_W": 200, "appel_puissance_W": 250},
    {"id": 23, "nom": "Four électrique (3000W)", "consommation_W": 3000, "appel_puissance_W": 3500},
    {"id": 24, "nom": "Friteuse", "consommation_W": 1800, "appel_puissance_W": 2000},
    {"id": 25, "nom": "Plancha", "consommation_W": 2000, "appel_puissance_W": 2200},
    {"id": 26, "nom": "Sèche-cheveux (2000W)", "consommation_W": 2000, "appel_puissance_W": 2200},
    {"id": 27, "nom": "Bouilloire", "consommation_W": 2200, "appel_puissance_W": 2500},
    {"id": 28, "nom": "Console de jeu, PlayStation 5", "consommation_W": 200, "appel_puissance_W": 250},
    {"id": 29, "nom": "Cafetière", "consommation_W": 1000, "appel_puissance_W": 1500},
    {"id": 30, "nom": "Four à micro-ondes (1000W)", "consommation_W": 1000, "appel_puissance_W": 1200},
    {"id": 31, "nom": "Grille-pain", "consommation_W": 800, "appel_puissance_W": 1000},
    {"id": 32, "nom": "Gaufrier", "consommation_W": 1000, "appel_puissance_W": 1200},
    {"id": 33, "nom": "Mixeur", "consommation_W": 500, "appel_puissance_W": 700},
    {"id": 34, "nom": "Voiture électrique, 1 Twingo 22kWh", "consommation_W": 22000, "appel_puissance_W": 25000},
    {"id": 35, "nom": "Chauffage d'appoint", "consommation_W": 2000, "appel_puissance_W": 2500},
    {"id": 36, "nom": "Sèche-linge (classe A+++)","consommation_W": 1500, "appel_puissance_W": 2000},
    {"id": 37, "nom": "Pompe à chaleur air-air maison 100m²", "consommation_W": 2500, "appel_puissance_W": 3000},
    {"id": 38, "nom": "Voiture électrique, Capture 10kWh", "consommation_W": 10000, "appel_puissance_W": 12000},
    {"id": 39, "nom": "Kit vidéo surveillance, alarme", "consommation_W": 50, "appel_puissance_W": 100},
    {"id": 40, "nom": "Ordinateur pour école", "consommation_W": 250, "appel_puissance_W": 400},
    {"id": 41, "nom": "Pompe à chaleur air-air bureau 100m²", "consommation_W": 3000, "appel_puissance_W": 3500},
    {"id": 42, "nom": "Pompe à chaleur air-air école 100m²", "consommation_W": 3500, "appel_puissance_W": 4000},
    {"id": 43, "nom": "Écran d'ordinateur", "consommation_W": 50, "appel_puissance_W": 100},
    {"id": 44, "nom": "Radio-réveil", "consommation_W": 10, "appel_puissance_W": 20},
    {"id": 45, "nom": "Sèche-serviette", "consommation_W": 500, "appel_puissance_W": 1000},
    {"id": 46, "nom": "Chargeur de téléphone", "consommation_W": 5, "appel_puissance_W": 10},
    {"id": 47, "nom": "Box internet", "consommation_W": 15, "appel_puissance_W": 30},
    {"id": 48, "nom": "Scie sous table", "consommation_W": 1800, "appel_puissance_W": 2500},
    {"id": 49, "nom": "Scie à onglets", "consommation_W": 1500, "appel_puissance_W": 2200},
    {"id": 50, "nom": "Raboteuse", "consommation_W": 1200, "appel_puissance_W": 1800},
    {"id": 51, "nom": "Aspirateur de chantier", "consommation_W": 1400, "appel_puissance_W": 2000},
    {"id": 52, "nom": "Vaporisateur laveur de sol", "consommation_W": 1000, "appel_puissance_W": 1500},
    {"id": 53, "nom": "Robot aspirateur", "consommation_W": 50, "appel_puissance_W": 100}
]

# Créer un fichier JSON pour chaque minute de la journée (1440 minutes)
activites = []
for minute in range(1440):  # 1440 minutes dans une journée
    # Pour chaque minute, déterminer aléatoirement quels appareils sont en activité
    appareils_en_activite = random.sample([appareil['id'] for appareil in appareils], k=random.randint(0, len(appareils)))
    
    activites.append({
        "minute": minute,
        "appareils_en_activite": appareils_en_activite
    })

# Enregistrer dans un fichier JSON
with open('activites.json', 'w') as json_file:
    json.dump({"activites": activites}, json_file, indent=4)

print("Fichier JSON 'activites.json' créé.")