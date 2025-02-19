@echo off
python -m venv env
call env\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python --version
pip --version
uvicorn --version

:: Lancer Uvicorn en arrière-plan
start /B uvicorn app.main:app --reload

:: Attendre quelques secondes pour laisser le serveur démarrer
timeout /t 3 >nul

:: Ouvrir l'application dans le navigateur par défaut
start http://localhost:8000
