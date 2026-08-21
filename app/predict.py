import uuid
from app.clean import clean_text
from app.models import get_model_and_encoder

CONFIDENCE_THRESHOLD = 0.60

CATEGORY_MAP = {
    "سباكة": "Plumbing",
    "كهرباء": "Electrical",
    "نجارة": "Carpentry",
    "نقاشة": "Painting",
    "دهانات": "Painting"
}


def predict_severity(category: str, description: str):
    english_category = CATEGORY_MAP.get(category)
    if not english_category:
        raise ValueError(f"Unsupported category: {category}")

    model_data = get_model_and_encoder(english_category)
    model = model_data["model"]
    encoder = model_data["encoder"]

    clean_description = clean_text(description)
    if not clean_description:
        raise ValueError("Description contains no valid Arabic text")

    prediction = model.predict([clean_description])[0]
    severity = str(encoder.inverse_transform([prediction])[0]).upper()

    probabilities = model.predict_proba([clean_description])[0]
    probability_dict = {
        str(label).upper(): round(float(prob), 4)
        for label, prob in zip(encoder.classes_, probabilities)
    }

    confidence = round(float(max(probabilities)), 4)
    needs_review = confidence < CONFIDENCE_THRESHOLD
    request_id = str(uuid.uuid4())

    return {
        "request_id": request_id,
        "category": category,
        "description": description,
        "severity": severity,
        "confidence": confidence,
        "needs_review": needs_review,
        "probabilities": probability_dict,
    }