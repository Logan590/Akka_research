import json

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