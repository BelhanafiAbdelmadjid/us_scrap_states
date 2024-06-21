python -m venv venv 
call venv\Scripts\activate

pip install -r requirements.txt
echo "Starting the app"
start http://127.0.0.1:5000
python web_app.py &

