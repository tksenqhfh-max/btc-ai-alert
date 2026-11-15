import os
from flask import Flask, request, jsonify
from openai import OpenAI

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

    print("TradingView alert received", flush=True)

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"status": "received", "ai": "not configured"}), 200

    try:
        client = OpenAI(api_key=api_key)
        result = client.responses.create(
            model="gpt-4.1-mini",
            input=(
                "다음 트레이딩뷰 알림을 한국어로 간단히 분석해줘. "
                "매매 지시가 아니라 참고용으로 설명해줘.\n"
                f"알림: { {k: v for k, v in data.items() if k != 'secret'} }"
            )
        )
        print("AI analysis:", result.output_text, flush=True)
        return jsonify({"status": "received", "analysis": result.output_text}), 200
    except Exception as e:
        print("AI error:", str(e), flush=True)
        return jsonify({"status": "received", "ai": "error"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
