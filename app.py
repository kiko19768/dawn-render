from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# تحميل التوكنات من ملف
def load_tokens():
    try:
        with open("tokens.txt", "r") as f:
            lines = f.readlines()
            accounts = []
            for i, line in enumerate(lines):
                token = line.strip()
                if token:
                    accounts.append({
                        "name": f"Account {i+1}",
                        "token": token
                    })
            return accounts
    except FileNotFoundError:
        return []

DAWN_ACCOUNTS = load_tokens()

def get_account_data(account):
    headers = {
        "Authorization": account["token"],
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get("https://dawn.network/api/v1/session", headers=headers)
        if response.status_code == 200:
            data = response.json()
            return {
                "name": account["name"],
                "wallet": data.get("walletBalance", 0),
                "points": data.get("points", 0),
                "status": "Connected",
                "quality": "100%",
                "hours": "غير متاح حالياً"
            }
        else:
            return {
                "name": account["name"],
                "wallet": 0,
                "points": 0,
                "status": "Disconnected",
                "quality": "0%",
                "hours": "0"
            }
    except Exception:
        return {
            "name": account["name"],
            "wallet": 0,
            "points": 0,
            "status": "Error",
            "quality": "0%",
            "hours": "0"
        }

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/data')
def get_all_data():
    result = [get_account_data(acc) for acc in DAWN_ACCOUNTS]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/add_token', methods=['POST'])
def add_token():
    new_token = request.json.get("token")
    if new_token:
        with open("tokens.txt", "a") as f:
            f.write(new_token.strip() + "\n")
    return jsonify({"status": "success"})
