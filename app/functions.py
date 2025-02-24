import json
import random

def time_to_minutes(time_str):
    #Convertit une heure sous forme HH:MM en minutes depuis minuit.
    if not time_str or ":" not in time_str:  # Vérifie si la valeur est vide ou incorrecte
        raise ValueError(f"Format d'heure invalide : {time_str}")
    try:
        h, m = map(int, time_str.split(":"))
        return h * 60 + m
    except ValueError:
        raise ValueError(f"Format d'heure invalide : {time_str}")

def minutes_to_time(minutes):
    # Formate l'heure et les minutes en chaîne de caractères (HH:MM-HH:MM)
    hour = minutes // 60            # Heure de début
    minute = minutes % 60           # Minute de début
    time = f"{hour:02}h{minute:02}"
    return time

def load_devices():
    try:
        with open("json/DevicesList.json", "r") as file:
            data = json.load(file)
            devices_list = data.get("devices",[])
            return devices_list
    except FileNotFoundError:
        raise ValueError("DevicesList not found")


# 📌 Charger un fichier JSON
def load_json(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

# 📌 Sauvegarder un fichier JSON
def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

# 📌 Trouver les durées de fonctionnement pour un appareil donné
def get_durations(appareil_id, durations):
    for appareil in durations:
        if str(appareil["appareil_id"]) == str(appareil_id):
            return appareil["duration_min"], appareil["duration_max"]
    return 1, 1  # Valeur par défaut si non trouvé

# 📌 Générer la consommation basée sur la matrice de probabilité
def generate_consumption():
    # Charger les fichiers JSON
    probability_matrix = load_json("json/Matrix.json")
    devices = load_json("json/DevicesOwnByUser.json")["devices"]
    durations = load_json("json/DeviceDurations.json")

    consommation = []  # Liste pour stocker la consommation par tranche horaire

    # Associer les appareils par ID
    appareils_dict = {str(d["id"]): d for d in devices}

    # Dictionnaire pour suivre le temps restant de fonctionnement des appareils
    appareil_en_marche = {str(d["id"]): 0 for d in devices}

    for time_block in probability_matrix:
        time_key = list(time_block.keys())[0]  # Exemple : "00h00"
        probabilities = time_block[time_key]

        # Initialiser la consommation pour cette tranche horaire
        consommation_entry = {time_key: [0.0] * len(devices)}

        for i, device_id in enumerate(appareils_dict.keys()):
            # Vérifier si l'appareil est encore en fonctionnement
            if appareil_en_marche[device_id] > 0:
                consommation_entry[time_key][i] = appareils_dict[device_id]["consommation_W"]
                appareil_en_marche[device_id] -= 10  # Réduire le temps restant (en minutes)
            else:
                # Vérifier si l'appareil se déclenche selon la probabilité
                if random.random() < probabilities[i]:
                    min_duree, max_duree = get_durations(device_id, durations)
                    duree = random.randint(min_duree, max_duree)  # Générer une durée aléatoire
                    appareil_en_marche[device_id] = duree  # L'appareil reste allumé
                    consommation_entry[time_key][i] = appareils_dict[device_id]["consommation_W"]

        consommation.append(consommation_entry)

    save_json("json/Consumption.json", consommation)

    print("✅ Fichier consommation.json généré avec succès !")

