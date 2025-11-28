from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

OPENROUTER_API_KEY = "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"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [{"role": "user", "content": user_message}]
    }

    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )
        ai_message = r.json()["choices"][0]["message"]["content"]
        return jsonify({"reply": ai_message})
    except:
        return jsonify({"reply": "⚠️ Erreur IA temporaire, réessaie."})

app.run(host="0.0.0.0", port=5000)
