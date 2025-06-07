from flask import Flask, request, jsonify

app = Flask(__name__)

# Сховище в пам’яті
log_store = {}

@app.route('/log', methods=['POST'])
def log_message():
    data = request.get_json()
    uid = data.get("UUID")
    msg = data.get("msg")
    if uid and msg:
        log_store[uid] = msg
        print(f"Logged: {uid} -> {msg}")
        return jsonify({"status": "saved"}), 200
    return jsonify({"error": "invalid input"}), 400

@app.route('/all', methods=['GET'])
def get_all_messages():
    return "\n".join(log_store.values()), 200

if __name__ == '__main__':
    app.run(port=5001)
