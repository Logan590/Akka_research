from fastapi import FastAPI, Form, Request
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
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

# Liste d'appareils fictifs (à adapter à ton besoin)
appareils = [
    {"id": 1, "nom": "Réfrigérateur", "consommation_W": 150, "appel_puissance_W": 600},
    {"id": 2, "nom": "Congélateur", "consommation_W": 200, "appel_puissance_W": 800},
    # Ajouter plus d'appareils ici
]

# Dossier de templates pour rendre les HTML
templates = Jinja2Templates(directory="templates")

# Route principale pour afficher le formulaire
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "appareils": appareils})


# Simuler une liste d'appareils pour l'exemple
appareils = [{"id": 1, "nom": "Appareil 1"}, {"id": 2, "nom": "Appareil 2"}]

@app.post("/ajouter/")
async def ajouter(
    # appareil_id: int = Form(...),
    # date_debut: str = Form(...),
    # date_fin: str = Form(...)
):
    print("toto")
    # Convertir les dates en objets datetime
    # try:
    #     date_debut = datetime.strptime(date_debut, "%Y-%m-%dT%H:%M")
    #     date_fin = datetime.strptime(date_fin, "%Y-%m-%dT%H:%M")
    # except ValueError:
    #     return {"error": "Format de date invalide"}

    # # Chercher l'appareil par ID
    # appareil = next((a for a in appareils if a["id"] == appareil_id), None)
    # if appareil is None:
    #     return {"error": "Appareil non trouvé"}

    # # Ajouter les périodes de fonctionnement dans le fichier JSON ou dans la liste
    # new_entry = { 
    #     "appareil": appareil,
    #     "date_debut": date_debut.isoformat(),  # Convertir datetime en chaîne ISO 8601
    #     "date_fin": date_fin.isoformat()       # Convertir datetime en chaîne ISO 8601
    # }
    # print(new_entry)
    # Sauvegarde dans un fichier JSON
    # try:
    #     with open("activites.json", "r") as file:
    #         try:
    #             data = json.load(file)
    #         except json.JSONDecodeError:
    #             return {"error": "Le fichier JSON est corrompu ou invalide"}
    # except FileNotFoundError:
    #     data = {"activites": []}

    # data["activites"].append(new_entry)

    # # Sauvegarder dans le fichier
    # with open("activites.json", "w") as file:
    #     json.dump(data, file, indent=4)

    return {"message": "Entrée ajoutée avec succès"}


# Route pour télécharger le fichier JSON
@app.get("/telecharger/")
async def telecharger():
    with open("activites.json", "r") as file:
        data = json.load(file)
    return JSONResponse(content=data)
