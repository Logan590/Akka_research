from fastapi import FastAPI, Form, Request
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, time, timedelta
import json
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

class Device(BaseModel):
    id: int
    nom: str
    consommation_W: int
    appel_puissance_W: int


try:
    with open("DevicesList.json", "r") as file:
        data = json.load(file)
        devices = data.get("devices",[])
except FileNotFoundError:
    print("DevicesList.json not found.")

templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        with open("ProbabilityDuration.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            activites = data["activites"]
            return templates.TemplateResponse("index.html", {"request": request, "devices": devices, "activites": activites})
    except FileNotFoundError:
        return templates.TemplateResponse("index.html", {"request": request, "devices": devices})
    

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



@app.post("/ajouter_rec/")
async def ajouter(
    request: Request,
    device_id: int = Form(...),
    heure_debut: time = Form(...),
    duree: int = Form(...),
    recur: int = Form(...),
    intervalle: int = Form(...)
):
    # Chercher l'device par ID
    device = next((a for a in devices if a["id"] == device_id), None)
    if device is None:
        return {"error": "device not found"}

    activites = []

    # Convertir heure_debut en datetime
    heure_actuelle = datetime.combine(datetime.today(), heure_debut)

    for _ in range(recur):
        heure_fin = heure_actuelle + timedelta(minutes=duree)
        activites.append({
            "device": device,
            "heure_debut": heure_actuelle.strftime("%H:%M"),
            "heure_fin": heure_fin.strftime("%H:%M")
        })
        heure_actuelle = heure_fin + timedelta(minutes=intervalle)  # Ajout de l'intervalle

    # Charger l'existant
    try:
        with open("activites.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"activites": []}

    # Ajouter les nouvelles activités
    data["activites"].extend(activites)

    # Sauvegarde
    with open("activites.json", "w") as file:
        json.dump(data, file, indent=4)

    # return {"message": "Activité ajoutée avec succès", "activites": activites}
    with open("activites.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        activites = data["activites"]

    return templates.TemplateResponse("index.html", {"request": request, "devices": devices, "activites": activites})


# Route pour télécharger le fichier JSON
@app.get("/telecharger/")
async def telecharger():
    with open("activites.json", "r") as file:
        data = json.load(file)
    return JSONResponse(content=data)


@app.post("/enregistrer_probabilites/")
async def enregistrer_probabilites(request: Request):
    # Récupérer les données du formulaire
    form_data = await request.form()

    # Initialiser la structure de la matrice
    matrice = []

    # Plages horaires toutes les 10 minutes, de 0 à 1430 (1440 minutes en total)
    for minute in range(0, 1440, 10):  # Pour chaque minute de la journée (par tranches de 10 minutes)
        minute_data = []
        for appareil in devices:
            # Accéder à l'ID et récupérer la probabilité pour chaque appareil à cette minute
            device_id = appareil["id"]
            print(device_id)
            prob_key = f"proba_{minute}_{device_id}"
            prob_value = form_data.get(prob_key, 0)  # Valeur par défaut à 0 si non fournie
            minute_data.append(float(prob_value))  # Ajouter la probabilité à la liste des minutes
        
        # Ajouter les données de chaque minute à la matrice
        matrice.append({f"{minute // 60:02d}h{minute % 60:02d}": minute_data})

    # Sauvegarder dans un fichier JSON
    with open("probabilites.json", "w") as file:
        json.dump(matrice, file, indent=4)

    return JSONResponse(content={"message": "Probabilités enregistrées avec succès"})
