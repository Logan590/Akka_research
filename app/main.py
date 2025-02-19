from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, time, timedelta
import json
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

class Device(BaseModel):
    id: int
    nom: str
    consommation_W: int
    appel_puissance_W: int

def time_to_minutes(time_str):
    """ Convertit une heure sous forme HH:MM en minutes depuis minuit. """
    if not time_str or ":" not in time_str:  # Vérifie si la valeur est vide ou incorrecte
        raise ValueError(f"Format d'heure invalide : {time_str}")

    try:
        h, m = map(int, time_str.split(":"))
        return h * 60 + m
    except ValueError:
        raise ValueError(f"Format d'heure invalide : {time_str}")

try:
    with open("DevicesList.json", "r") as file:
        data = json.load(file)
        devices_list = data.get("devices",[])
        all_devices = devices_list
except FileNotFoundError:
    print("DevicesList.json not found.")

try:
    with open("DevicesOwnByUser.json", "r") as file:
        data = json.load(file)
        devices = data.get("devices",[])
except FileNotFoundError:
    print("DevicesOwnByUser.json not found.")


templates = Jinja2Templates(directory="templates")

def minutes_to_time(minutes):
    hour = minutes // 60            # Heure de début
    minute = minutes % 60           # Minute de début

    # Formater l'heure et les minutes en chaîne de caractères (HH:MM-HH:MM)
    time = f"{hour:02}h{minute:02}"
    
    # Retourner la plage horaire sous forme de chaîne
    return time


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    with open("ProbabilityDuration.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        activites = data["activites"]
        return templates.TemplateResponse("Set_device_list.html", {"request": request, "devices": devices_list})
    
@app.get("/add_devices", response_class=HTMLResponse)
async def index(request: Request):
    with open("ProbabilityDuration.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        activites = data["activites"]
        return templates.TemplateResponse("Set_device_list.html", {"request": request, "devices": devices_list})
        


@app.post("/save-devices")
async def save_devices(request: Request, selected_devices: list[str] = Form(...)):  
    """
    Endpoint pour sauvegarder les appareils sélectionnés dans DevicesOwnByUser.json.
    """
    # 🔹 Filtrer les appareils sélectionnés
    selected_devices_list = [device for device in all_devices if str(device["id"]) in selected_devices]

    # 🔹 Sauvegarder dans DevicesOwnByUser.json
    with open("DevicesOwnByUser.json", "w", encoding="utf-8") as file:
        json.dump({"devices": selected_devices_list}, file, indent=4, ensure_ascii=False)

    return templates.TemplateResponse("Sleep_time.html", {"request": request, "devices": selected_devices_list})



@app.post("/enregistrer_probabilites/")
async def enregistrer_probabilites(request: Request):
    form_data = await request.form()

    # Récupération des horaires
    bedtime = time_to_minutes(form_data["bedtime"])
    getuptime = time_to_minutes(form_data["getuptime"])
    home_start = [time_to_minutes(t) for t in form_data.getlist("home_start[]") if t.strip()]
    home_end = [time_to_minutes(t) for t in form_data.getlist("home_end[]") if t.strip()]
    matrice = []

    for minute in range(0, 1440, 10):  # De 00:00 à 23:50 par pas de 10 minutes
        minute_data = []

        # Si la personne est chez elle -> probabilité = 1 et qu'elle ne dort pas:
        if any(start <= minute < end for start, end in zip(home_start, home_end)) and bedtime > minute >= getuptime:
            prob_value = 1
        else:
            prob_value = 0  # Par défaut, absent = 0

        # Stocker la probabilité pour chaque appareil
        for appareil in devices:
            if prob_value == 1:
                minute_data.append(appareil["proba_defaut"])
            else:
                minute_data.append(appareil["proba_off"])

        # Format de l'heure
        matrice.append({f"{minute // 60:02d}h{minute % 60:02d}": minute_data})

    # Sauvegarder dans un fichier JSON
    with open("probabilites.json", "w") as file:
        json.dump(matrice, file, indent=4)

    try:
        with open("DevicesOwnByUser.json", "r") as file:
            data = json.load(file)
            devices_own = data.get("devices",[])
    except FileNotFoundError:
        print("DevicesOwnByUser.json not found.")
    
    return templates.TemplateResponse("matrice.html", {"request": request, "probabilites":matrice, "devices": devices_own})



@app.post("/enregistrer_matrice/")
async def enregistrer_probabilites(request: Request):
    # Récupérer les données du formulaire
    form_data = await request.form()

    # Initialiser la structure de la matrice
    matrice = []

    try:
        with open("DevicesOwnByUser.json", "r") as file:
            data = json.load(file)
            devices_own = data.get("devices",[])
    except FileNotFoundError:
        print("DevicesOwnByUser.json not found.")
    
    # Plages horaires toutes les 10 minutes, de 0 à 1430 (1440 minutes en total)
    for minute in range(0, 1440, 10):  # Pour chaque minute de la journée (par tranches de 10 minutes)
        minute_data = []
        for appareil in devices_own:
            # Accéder à l'ID et récupérer la probabilité pour chaque appareil à cette minute
            device_id = appareil["id"]
            plage_horaire = minutes_to_time(minute)
            prob_key = f"proba_{plage_horaire}_{device_id}"
            prob_value = form_data.get(prob_key, 0)  # Valeur par défaut à 0 si non fournie
            minute_data.append(float(prob_value))  # Ajouter la probabilité à la liste des minutes
        
        # Ajouter les données de chaque minute à la matrice
        matrice.append({f"{minute // 60:02d}h{minute % 60:02d}": minute_data})

    # Sauvegarder dans un fichier JSON
    with open("probabilites.json", "w") as file:
        json.dump(matrice, file, indent=4)

    return templates.TemplateResponse("matrice.html", {"request": request, "probabilites":matrice, "devices":devices})


@app.post("/add_duration/")
async def ajouter(
    request: Request,
    device_id: int = Form(...),
    inUseDuration: time = Form(...),
    probability: float = Form(...),
):
    try:
        inUseDuration = inUseDuration.strftime("%H:%M")
    except ValueError:
        return {"error": "Invalid hours format"}


    device = next((a for a in devices if a["id"] == device_id), None)
    if device is None:
        return {"error": "Device not found"}

    new_entry = {
        "device": device,
        "inUseDuration": inUseDuration,
        "probability": probability
    }
    
    try:
        with open("ProbabilityDuration.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"activites": []}

    data["activites"].append(new_entry)

    with open("ProbabilityDuration.json", "w") as file:
        json.dump(data, file, indent=4)

    return templates.TemplateResponse("index.html", {"request": request, "devices": device, "activites": data["activites"]})