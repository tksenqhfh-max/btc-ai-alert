
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "BTC AI Alert Server Running"

@app.route("/webhook", methods=["POST"])
def webhook():
    secret = os.environ.get("WEBHOOK_SECRET")
    if not secret:
        return jsonify({"error": "Not configured"}), 503

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON"}), 400

    if data.get("secret") != secret:
        return jsonify({"error": "Unauthorized"}), 401

    print("TradingView alert received")
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
