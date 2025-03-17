import json
import csv
import random
import os

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

# 📌 Sauvegarder un fichier CSV
def save_csv(filename, data):
    if not os.path.exists(filename):
        with open(filename, "a", encoding="utf-8") as f:
            f.write(','.join([str(f"{h:02d}")+"h"+str(f"{m:02d}") for h in range (24) for m in range(60)])+"\n")
    with open(filename, "a", encoding="utf-8", newline='') as f:
        csv_file = csv.writer(f, delimiter=',')
        csv_file.writerow([sum(device_power) for instant_conso in data for minute, device_power in instant_conso.items()])

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

    consommation = []  # Stocke la consommation par minute

    # Associer les appareils par ID
    appareils_dict = {str(d["id"]): d for d in devices}

    # Dictionnaire pour suivre le temps restant de fonctionnement des appareils
    appareil_en_marche = {str(d["id"]): 0 for d in devices}

    # Générer la liste des minutes de la journée (00:00 → 23:59)
    for heure in range(24):
        for minute in range(60):
            time_key = f"{heure:02d}:{minute:02d}"  # Format HH:MM

            # Trouver la plage de 10 min correspondante dans `probability_matrix`
            block_index = (heure * 60 + minute) // 10
            block_key = list(probability_matrix[block_index].keys())[0]
            probabilities = probability_matrix[block_index][block_key]

            consommation_entry = {time_key: [0.0] * len(devices)}

            for i, device_id in enumerate(appareils_dict.keys()):
                # Vérifier si l'appareil est encore en fonctionnement
                if appareil_en_marche[device_id] > 0:
                    consommation_entry[time_key][i] = appareils_dict[device_id]["consommation_W"]
                    appareil_en_marche[device_id] -= 1  # 🔹 Réduire le temps restant de 1 minute
                else:
                    # Vérifier si l'appareil se déclenche selon la probabilité
                    if random.random() < probabilities[i]:  
                        min_duree, max_duree = get_durations(device_id, durations)
                        duree = random.randint(int(min_duree), int(max_duree))
                        appareil_en_marche[device_id] = duree  # 🔹 Fixer durée en minutes
                        consommation_entry[time_key][i] = appareils_dict[device_id]["consommation_W"]

            consommation.append(consommation_entry)

    return consommation

# 📌 Générer 20 fichiers différents
def generate_multiple_files():
    for i in range(1, 21):
        consommation = generate_consumption()
        if not os.path.exists("output"):
            os.makedirs("output")
        save_json(f"output/consommation_{i}.json", consommation)
        print(f"✅ Fichier consommation_{i}.json généré.")
        save_csv(f"output/consommations.csv", consommation)
        print(f"✅ Fichier consommation.csv généré.")
