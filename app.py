# app.py — CarthagoLex Flask Backend
import os
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder=".", static_url_path="")

# ── Servir le frontend ──────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# ── Endpoint : Consultation juridique ──────────────────────────
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Parametre 'message' manquant"}), 400

    user_message = data["message"]
    conversation_history = data.get("history", [])
    mode = data.get("mode", "analyse_risque")

    try:
        from chains.rag_chain import run_chain
        response = run_chain(user_message, conversation_history, mode=mode)
        return jsonify({"response": response, "status": "success"})
    except ImportError as e:
        return jsonify({
            "response": f"[CarthagoLex] Pipeline RAG non connecte : {e}",
            "status": "fallback"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── Endpoint : Generation de documents ─────────────────────────
@app.route("/api/generate-document", methods=["POST"])
def generate_document():
    data = request.get_json()
    doc_type = data.get("type", "contrat")
    params = data.get("params", {})

    try:
        from chains.doc_chain import generate_doc
        document = generate_doc(doc_type, params)
        return jsonify({"document": document, "type": doc_type, "status": "success"})
    except ImportError:
        return jsonify({
            "document": f"[Modele {doc_type}] Generation en cours de developpement.",
            "status": "fallback"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── Endpoint : Analyse de dossier ──────────────────────────────
@app.route("/api/analyze", methods=["POST"])
def analyze_case():
    data = request.get_json()
    case_description = data.get("description", "")
    mode = data.get("mode", "analyse_risque")

    try:
        from chains.rag_chain import run_chain
        result = run_chain(case_description, [], mode=mode)
        return jsonify({"analysis": result, "status": "success"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ── Endpoint : Modes disponibles ───────────────────────────────
@app.route("/api/modes", methods=["GET"])
def get_modes():
    return jsonify({
        "modes": [
            {"id": "analyse_risque", "label": "Analyse de risque"},
            {"id": "controle_qualite", "label": "Controle qualite"},
            {"id": "interpretation_texte", "label": "Interpretation de texte"},
            {"id": "redaction_recours", "label": "Redaction de recours"},
        ]
    })

# ── Endpoint : Sante du serveur ─────────────────────────────────
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "ok",
        "app": "CarthagoLex",
        "version": "2.0.0",
        "model": os.getenv("LLM_MODEL", "non configure")
    })

# ── Lancement ───────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    print(f"CarthagoLex demarre sur http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
