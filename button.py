from flask import Flask, render_template, redirect
import requests
from waitress import serve
import os

app = Flask(__name__)

AGV_IP = os.getenv("AGV_IP", '192.168.1.233')  # Replace with your AGV IP address
AGV_PORT = os.getenv("AGV_PORT", 8000)


@app.route('/')
def home():
    return render_template('index.html')  # this expects your HTML file to be named "index.html"

# Dispatch route
@app.route('/dispatch_agv')
def dispatch_agv():
    target_url = f'{AGV_IP}:{AGV_PORT}/receive_mission'  # <-- Replace with your AGV endpoint
    payload = {"location": 1}
    headers = {'Content-Type': 'application/json'}
    try:
        # Send HTTP POST
        response = requests.post(target_url, json=payload, headers=headers)

        if response.status_code == 200:
            print('AGV dispatched successfully.')
        else:
            print(f'Failed to dispatch AGV. Status code: {response.status_code}')

    except requests.exceptions.RequestException as e:
        print(f'Error sending POST request: {e}')

    # Redirect back to home
    return redirect('/')
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8001)