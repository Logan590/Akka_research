python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
python3 --version
pip3 --version
uvicorn --version
uvicorn app.main:app --reload