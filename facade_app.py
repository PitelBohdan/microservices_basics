from flask import Flask, request, jsonify
import uuid
import requests

app = Flask(__name__)

# адреси інших мікросервісів
LOGGING_SERVICE_URL = "http://localhost:5001"
MESSAGES_SERVICE_URL = "http://localhost:5002"

@app.route('/post-msg', methods=['POST'])
def post_message():
    data = request.get_json()
    msg = data.get("msg")
    if not msg:
        return jsonify({"error": "Missing 'msg'"}), 400

    uid = str(uuid.uuid4())
    payload = {"UUID": uid, "msg": msg}

    try:
        response = requests.post(f"{LOGGING_SERVICE_URL}/log", json=payload)
        return jsonify({"UUID": uid, "status": "sent to logging-service"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get-all', methods=['GET'])
def get_all():
    try:
        log_response = requests.get(f"{LOGGING_SERVICE_URL}/all")
        msg_response = requests.get(f"{MESSAGES_SERVICE_URL}/message")

        combined = log_response.text + "\n---\n" + msg_response.text
        return combined, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
