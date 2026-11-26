
import os
from pathlib import Path

from flask import Flask, request, jsonify
from flask_cors import CORS

# VDF Games Support Tool
app = Flask(__name__)
CORS(app)

app.config["MAX_CONTENT_LENGTH"] = 32 * 1024


# 1. Firemní dokumentace

BASE_DIR = Path(__file__).resolve().parent
DOCUMENTATION_PATH = BASE_DIR / "docs" / "podpora.md"

try:
    documentation = DOCUMENTATION_PATH.read_text(
        encoding="utf-8"
    )
except FileNotFoundError:
    documentation = ""


# 2. Test serveru

@app.get("/")
def home():
    return "VDF Support Backend is running"


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "mode": "demo",
        "documentation": bool(documentation)
    })


# 3. Zákaznická podpora

@app.post("/chat")
def chat():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Neplatná data."
        }), 400

    message = data.get("message")

    if not isinstance(message, str) or not message.strip():
        return jsonify({
            "error": "Dotaz je prázdný."
        }), 400

    message = message.strip()

    if len(message) > 2000:
        return jsonify({
            "error": "Dotaz je příliš dlouhý."
        }), 400

    # Testovací odpověď bez externí AI
    reply = (
        "[DEMO] Děkujeme za váš dotaz.\n\n"
        f"Váš problém: {message}\n\n"
        "Požadavek byl úspěšně přijat serverem."
    )

    return jsonify({
        "reply": reply
    })


# 4. Lokální spuštění

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))

    app.run(
        host="127.0.0.1",
        port=port,
        debug=False
    )
