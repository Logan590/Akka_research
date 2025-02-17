from fastapi import FastAPI, Form, Request
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, time, timedelta
import json
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Modèle de données pour un appareil
class Appareil(BaseModel):
    id: int
    nom: str
    consommation_W: int
    appel_puissance_W: int


try:
    with open("ListeDesAppareilsDom.json", "r") as file:
        data = json.load(file)
        appareils = data.get("appareils",[])
except FileNotFoundError:
    appareils = [
        {"id": 1, "nom": "Réfrigérateur", "consommation_W": 150, "appel_puissance_W": 600},
        {"id": 2, "nom": "Congélateur", "consommation_W": 200, "appel_puissance_W": 800},
        # Ajouter plus d'appareils ici
    ]

# Dossier de templates pour rendre les HTML
templates = Jinja2Templates(directory="templates")

# Charger le fichier JSON


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    try:
        with open("activites.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            activites = data["activites"]
            return templates.TemplateResponse("index.html", {"request": request, "appareils": appareils, "activites": activites})
    except FileNotFoundError:
        return templates.TemplateResponse("index.html", {"request": request, "appareils": appareils})
    

    



# Route pour ajouter des entrées de fonctionnement des appareils
@app.post("/ajouter/")
async def ajouter(
    request: Request,
    appareil_id: int = Form(...),
    heure_debut: time = Form(...),
    heure_fin: time = Form(...),
):
    
    # Convertir les heures en objets datetime
    try:
        heure_debut = heure_debut.strftime("%H:%M")
        heure_fin = heure_fin.strftime("%H:%M")
    except ValueError:
        return {"error": "Format d'heure invalide"}

    print(type(heure_debut))
    print(heure_debut)
    # Chercher l'appareil par ID
    appareil = next((a for a in appareils if a["id"] == appareil_id), None)
    if appareil is None:
        return {"error": "Appareil non trouvé"}

    # Ajouter les périodes de fonctionnement dans le fichier JSON ou dans la liste
    new_entry = {
        "appareil": appareil,
        "heure_debut": heure_debut,
        "heure_fin": heure_fin
    }
    
    # Sauvegarde dans un fichier JSON
    try:
        with open("activites.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"activites": []}

    data["activites"].append(new_entry)

    # Sauvegarder dans le fichier
    with open("activites.json", "w") as file:
        json.dump(data, file, indent=4)

    with open("activites.json", "r", encoding="utf-8") as file:
        data = json.load(file)
        activites = data["activites"]

    return templates.TemplateResponse("index.html", {"request": request, "appareils": appareils, "activites": activites})



@app.post("/ajouter_rec/")
async def ajouter(
    request: Request,
    appareil_id: int = Form(...),
    heure_debut: time = Form(...),
    duree: int = Form(...),
    recur: int = Form(...),
    intervalle: int = Form(...)
):
    # Chercher l'appareil par ID
    appareil = next((a for a in appareils if a["id"] == appareil_id), None)
    if appareil is None:
        return {"error": "Appareil non trouvé"}

    activites = []

    # Convertir heure_debut en datetime
    heure_actuelle = datetime.combine(datetime.today(), heure_debut)

    for _ in range(recur):
        heure_fin = heure_actuelle + timedelta(minutes=duree)
        activites.append({
            "appareil": appareil,
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

    return templates.TemplateResponse("index.html", {"request": request, "appareils": appareils, "activites": activites})


# Route pour télécharger le fichier JSON
@app.get("/telecharger/")
async def telecharger():
    with open("activites.json", "r") as file:
        data = json.load(file)
    return JSONResponse(content=data)
