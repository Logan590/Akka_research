# Installation de l'Application

Ce guide explique comment installer et exécuter l'application sous Linux et Windows.

## Prérequis

- **Python 3** (de préférence 3.7 ou plus récent)
- **pip3** (gestionnaire de paquets Python)

## Installation sous Linux

1. **Cloner le dépôt (si nécessaire) :**
   ```bash
   git clone https://github.com/Logan590/Akka_research.git
   cd Akka_research
   ```
2. **Executer le fichier init_app.sh:**
   ```bash
   chmod +x init_app.sh
   ./init_app.sh
   ```
## Installation sous Windows

1. **Ouvrir une invite de commande (cmd) ou PowerShell et cloner le dépôt**
   ```powershell
   git clone https://github.com/Logan590/Akka_research.git
    ```
    
2. **Aller dans le répertoire cloné et double-cliquer sur init_app.bat.**
 

## Accès à l'application
Ouvrez un navigateur et allez sur http://localhost:8000

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

