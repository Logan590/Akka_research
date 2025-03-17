from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from datetime import datetime, time, timedelta
import json
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app import functions as f
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

##########################################################################################################
#Routes GET
##########################################################################################################
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
     return RedirectResponse("/add_devices", status_code=303)
    

@app.get("/add_devices", response_class=HTMLResponse)
async def add_device(request: Request):
    devices_list = f.load_devices()
    return templates.TemplateResponse("Set_device_list.html", {"request": request, "devices": devices_list})

@app.get("/add_device_list", response_class=HTMLResponse)
async def set_device_list(request: Request):
    devices_list = f.load_devices()
    return templates.TemplateResponse("Add_device.html", {"request": request, "devices": devices_list})

@app.get("/add_duration", response_class=HTMLResponse)
async def set_duration_list(request: Request):
    try:
        with open("json/DevicesOwnByUser.json", "r") as file:
            data = json.load(file)
            devices_own = data.get("devices",[])
            return templates.TemplateResponse("Durations.html", {"request": request, "devices": devices_own})
    except FileNotFoundError:
        print("Vous devez d'abord renseigner une liste d'appareils")

@app.get("/show_matrix", response_class=HTMLResponse)
async def show_matrix(request: Request):
    try:
        with open("json/DevicesOwnByUser.json", "r") as file:
            data = json.load(file)
            devices_own = data.get("devices",[])
    except FileNotFoundError:
        print("Vous devez d'abord renseigner une liste d'appareils")
    try:
        with open("json/matrix.json", "r") as file:
            matrice = json.load(file)
    except FileNotFoundError:
        print("Vous devez d'abord renseigner une matrice de probabilité")
    return templates.TemplateResponse("matrice.html", {"request": request, "probabilites":matrice, "devices": devices_own})

@app.get("/additional_tool", response_class=HTMLResponse)
async def additional_tool(request: Request):
    return templates.TemplateResponse("additional_tool.html", {"request": request})

@app.get("/gen_consumption", response_class=HTMLResponse)
async def gen_consumption(request: Request):
    f.generate_multiple_files()
    with open("templates/consumption.html", "r", encoding="utf-8") as fi:
        html_content = fi.read()
    return HTMLResponse(content=html_content)

@app.get("/api/consommation")
async def get_consumption():
    data = []
    folder = "./output"  # 📂 Dossier contenant les fichiers JSON

    for i in range(1, 21):  # 🔄 Lire consommation_1.json → consommation_20.json
        filename = os.path.join(folder, f"consommation_{i}.json")
        if os.path.exists(filename):
            data.append(f.load_json(filename))

    # 🔍 Récupérer les noms des appareils depuis DevicesOwnByUser.json
    devices_info = f.load_json("json/DevicesOwnByUser.json")  # Charger les appareils
    device_names = [device["nom"] for device in devices_info["devices"]]

    return JSONResponse(content={"datasets": data, "deviceNames": device_names})

##########################################################################################################
#Routes POST
##########################################################################################################
@app.post("/save-devices")
async def save_devices(request: Request, selected_devices: list[str] = Form(...)):  
    # Filtrer les appareils sélectionnés
    devices_list = f.load_devices()
    selected_devices_list = [device for device in devices_list if str(device["id"]) in selected_devices]

    # Sauvegarder dans DevicesOwnByUser.json
    with open("json/DevicesOwnByUser.json", "w", encoding="utf-8") as file:
        json.dump({"devices": selected_devices_list}, file, indent=4, ensure_ascii=False)

    return templates.TemplateResponse("Sleep_time.html", {"request": request, "devices": selected_devices_list})


@app.post("/enregistrer_probabilites/")
async def enregistrer_probabilites(request: Request):
    form_data = await request.form()

    # Récupération des horaires
    bedtime = f.time_to_minutes(form_data["bedtime"])
    getuptime = f.time_to_minutes(form_data["getuptime"])
    home_start = [f.time_to_minutes(t) for t in form_data.getlist("home_start[]") if t.strip()]
    home_end = [f.time_to_minutes(t) for t in form_data.getlist("home_end[]") if t.strip()]
    matrice = []

    try:
        with open("json/DevicesOwnByUser.json", "r") as file:
            data = json.load(file)
            devices_own = data.get("devices",[])
    except FileNotFoundError:
        print("DevicesOwnByUser.json not found.")

    for minute in range(0, 1440, 10):  # De 00:00 à 23:50 par pas de 10 minutes
        minute_data = []

        # Si la personne est chez elle -> probabilité = 1 et qu'elle ne dort pas:
        if any(start <= minute < end for start, end in zip(home_start, home_end)) and bedtime > minute >= getuptime:
            prob_value = 1
        else:
            prob_value = 0  # Par défaut, absent = 0

        # Stocke la probabilité pour chaque appareil
        for appareil in devices_own:
            if prob_value == 1:
                minute_data.append(appareil["proba_defaut"])
            else:
                minute_data.append(appareil["proba_off"])

        # Format de l'heure
        matrice.append({f"{minute // 60:02d}h{minute % 60:02d}": minute_data})

    # Sauvegarde dans un fichier JSON
    with open("json/Matrix.json", "w") as file:
        json.dump(matrice, file, indent=4)


    return RedirectResponse("/add_duration", status_code=303)
    # return templates.TemplateResponse("matrice.html", {"request": request, "probabilites":matrice, "devices": devices_own})



@app.post("/enregistrer_matrice/")
async def enregistrer_probabilites(request: Request):
    # Récupére les données du formulaire
    form_data = await request.form()

    # Initialise la structure de la matrice
    matrice = []

    try:
        with open("json/DevicesOwnByUser.json", "r") as file:
            data = json.load(file)
            devices_own = data.get("devices",[])
    except FileNotFoundError:
        print("DevicesOwnByUser.json not found.")
    
    # Plages horaires toutes les 10 minutes, de 0 à 1430 (1440 minutes en total)
    for minute in range(0, 1440, 10):  # Pour chaque minute de la journée (par tranches de 10 minutes)
        minute_data = []
        for appareil in devices_own:
            # Accéde à l'ID et récupérer la probabilité pour chaque appareil à cette minute
            device_id = appareil["id"]
            plage_horaire = f.minutes_to_time(minute)
            prob_key = f"proba_{plage_horaire}_{device_id}"
            prob_value = form_data.get(prob_key, 0)  # Valeur par défaut à 0 si non fournie
            minute_data.append(float(prob_value))  # Ajoute la probabilité à la liste des minutes
        
        # Ajoute les données de chaque minute à la matrice
        matrice.append({f"{minute // 60:02d}h{minute % 60:02d}": minute_data})

    # Sauvegarde dans un fichier JSON
    with open("json/Matrix.json", "w") as file:
        json.dump(matrice, file, indent=4)

    return RedirectResponse("/gen_consumption/", status_code=303)
    # return templates.TemplateResponse("matrice.html", {"request": request, "probabilites":matrice, "devices":devices_own})


@app.post("/add_duration/")
async def add_duration(request: Request):
    form_data = await request.form()  # Récupération des données du formulaire
    result = []

    # Transforme les données en JSON
    for key, value in form_data.items():
        if key.startswith("duration_min_"):
            appareil_id = key.split("_")[-1]
            duration_min = float(value)
            duration_max = float(form_data.get(f"duration_max_{appareil_id}", 0))

            result.append({
                "appareil_id": appareil_id,
                "duration_min": duration_min,
                "duration_max": duration_max
            })

    # Sauvegarde en fichier JSON (facultatif)
    with open("json/DeviceDurations.json", "w") as f:
        json.dump(result, f, indent=4)

    # return {"message": "Données enregistrées", "data": result}
    return RedirectResponse("/show_matrix", status_code=303)



@app.post("/add_device_list/")
def add_device(
    id: int = Form(...),
    nom: str = Form(...),
    consommation_W: int = Form(...),
    appel_puissance_W: int = Form(...),
    proba_defaut: float = Form(...),
    proba_off: float = Form(...)
):
    data = f.load_devices()
    device = {
        "id": id,
        "nom": nom,
        "consommation_W": consommation_W,
        "appel_puissance_W": appel_puissance_W,
        "proba_defaut": proba_defaut,
        "proba_off": proba_off
    }

    # Vérifier si l'appareil existe déjà
    for i, d in enumerate(data):
        if d["id"] == id:
            data[i] = device
            # Sauvegarder dans DevicesOwnByUser.json
            with open("json/DevicesList.json", "w", encoding="utf-8") as file:
                json.dump({"devices": data}, file, indent=4, ensure_ascii=False)
            return RedirectResponse("/", status_code=303)

    # Ajouter un nouvel appareil
    data.append(device)

    # Sauvegarder dans DevicesOwnByUser.json
    with open("json/DevicesList.json", "w", encoding="utf-8") as file:
        json.dump({"devices": data}, file, indent=4, ensure_ascii=False)
    return RedirectResponse("/", status_code=303)


@app.post("/gen_consumption/")
async def gen_consumption(request: Request):
    f.generate_multiple_files()
    with open("templates/consumption.html", "r", encoding="utf-8") as fi:
        html_content = fi.read()
    return HTMLResponse(content=html_content)