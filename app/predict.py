from app.clean import clean_text

from app.models import MODELS

def predict_severity(category: str, description: str):

    # ==========================================
    # Check Category
    # ==========================================

    if category not in MODELS:
        raise ValueError(f"Unsupported category: {category}")

    # ==========================================
    # Check Description
    # ==========================================

    if not description.strip():
        raise ValueError("Description cannot be empty")

    # ==========================================
    # Get Model & Encoder
    # ==========================================

    model = MODELS[category]["model"]
    encoder = MODELS[category]["encoder"]

    # ==========================================
    # Clean Text
    # ==========================================

    clean_description = clean_text(description)

    # ==========================================
    # Prediction
    # ==========================================

    prediction = model.predict([clean_description])[0]

    severity = encoder.inverse_transform([prediction])[0]

    # ==========================================
    # Prediction Probabilities
    # ==========================================

    probabilities = model.predict_proba([clean_description])[0]

    probability_dict = {}

    for label, probability in zip(encoder.classes_, probabilities):

        probability_dict[label] = round(float(probability), 4)

    confidence = max(probabilities)

    # ==========================================
    # Response
    # ==========================================

    return {

        "category": category,

        "description": description,

        "severity": severity,

        "confidence": round(confidence, 4),

        "probabilities": probability_dict

    }