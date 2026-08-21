from flask import Flask, request, jsonify
from flask_cors import CORS
from app.predict import predict_severity

app = Flask(__name__)
CORS(app)  # تفعيل CORS لجميع المسارات
app.json.ensure_ascii = False

@app.route("/", methods=["GET"])
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK"})

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(force=True)

    category = data.get("category")
    description = data.get("description")

    if not category or not description:
        return jsonify({"detail": "Missing category or description"}), 400

    try:
        result = predict_severity(category=category, description=description)
        return jsonify(result)
    except ValueError as e:
        return jsonify({"detail": str(e)}), 400
    except Exception as e:
        return jsonify({"detail": f"Internal Server Error: {str(e)}"}), 500