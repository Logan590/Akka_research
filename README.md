# Installation de l'Application

Ce guide explique comment installer et exécuter l'application sous Linux et Windows.

## Prérequis

- **Python 3** (de préférence 3.7 ou plus récent)
- **pip** (gestionnaire de paquets Python)
- **uvicorn** (serveur ASGI pour FastAPI)

## Installation sous Linux

1. **Cloner le dépôt (si nécessaire) :**
   ```bash
   git clone https://github.com/Logan590/Akka_research.git
   cd Akka_research
   ```

2. **Créer et activer un environnement virtuel :**
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Mettre à jour `pip` et installer les dépendances :**
   ```bash
   python3 -m pip install --upgrade pip
   pip3 install -r requirements.txt
   ```

4. **Vérifier les versions installées :**
   ```bash
   python3 --version
   pip3 --version
   uvicorn --version
   ```

5. **Lancer l'application :**
   ```bash
   uvicorn app.main:app --reload
   ```

## Installation sous Windows

1. **Ouvrir une invite de commande (cmd) ou PowerShell et cloner le dépôt**
   ```powershell
   git clone https://github.com/Logan590/Akka_research.git
   cd Akka_research
    ```
    
2. **Créer et activer un environnement virtuel :**
   ```powershell
   python -m venv env
   env\Scripts\activate
   ```

3. **Mettre à jour `pip` et installer les dépendances :**
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Vérifier les versions installées :**
   ```powershell
   python --version
   pip --version
   uvicorn --version
   ```

5. **Lancer l'application :**
   ```powershell
   uvicorn app.main:app --reload
   ```

## Problèmes Courants et Solutions

### 1. `python3` ou `pip3` non reconnu
- Sous Windows, utilisez `python` et `pip` au lieu de `python3` et `pip3`.
- Vérifiez que Python est bien ajouté au `PATH`.

### 2. `venv` non disponible
- Installez `venv` avec :
  ```bash
  sudo apt install python3-venv  # (Linux)
  ```

### 3. Erreur `ModuleNotFoundError: No module named 'uvicorn'`
- Assurez-vous que l'environnement virtuel est bien activé.
- Réinstallez les dépendances :
  ```bash
  pip install -r requirements.txt
  ```

### 4. Port déjà utilisé lors du lancement d'`uvicorn`
- Spécifiez un autre port avec `--port 8080` (ou un autre numéro libre) :
  ```bash
  uvicorn app.main:app --reload --port 8080
  ```

### 5. Erreur `PermissionError: [Errno 13] Permission denied`
- Sous Linux, essayez d’exécuter la commande avec `sudo`.
- Sous Windows, ouvrez l'invite de commande en tant qu'administrateur.

---

Votre application est maintenant installée et fonctionnelle ! 🚀

