
python -m venv venv 
venv\Scripts\activate

pip install -r requirements.txt

python web_app.py &

sleep 5

xdg-open http://127.0.0.1:5000