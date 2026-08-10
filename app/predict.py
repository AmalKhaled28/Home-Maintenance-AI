import uuid

from app.clean import clean_text
from app.models import MODELS

CONFIDENCE_THRESHOLD = 0.70

# Mapping dictionary from Arabic category names to English keys used in MODELS
CATEGORY_MAP = {
    "سباكة": "Plumbing",
    "كهرباء": "Electrical",
    "نجارة": "Carpentry",
    "دهانات": "Painting",
}


def predict_severity(category: str, description: str):

    # ==========================================
    # Validate & Map Category Input
    # ==========================================

    if not description.strip():
        raise ValueError("Description cannot be empty")

    category = category.strip()

    # Map Arabic category to English key, or keep it if it's already in English
    english_category = CATEGORY_MAP.get(category, category).title()

    if english_category not in MODELS:
        raise ValueError(f"Unsupported category: {category}")

    # ==========================================
    # Load Model & Encoder
    # ==========================================

    model = MODELS[english_category]["model"]
    encoder = MODELS[english_category]["encoder"]

    # ==========================================
    # Clean Text
    # ==========================================

    clean_description = clean_text(description)

    # ==========================================
    # Prediction & Formatting
    # ==========================================

    prediction = model.predict([clean_description])[0]

    # Convert predicted class to uppercase to match Backend Enum (e.g., 'LARGE')
    severity = str(encoder.inverse_transform([prediction])[0]).upper()

    probabilities = model.predict_proba([clean_description])[0]

    probability_dict = {}

    # Map target classes to their probabilities with uppercase keys
    for label, probability in zip(encoder.classes_, probabilities):
        probability_dict[str(label).upper()] = round(float(probability), 4)

    confidence = round(float(max(probabilities)), 4)

    # ==========================================
    # Human Review Flag
    # ==========================================

    needs_review = confidence < CONFIDENCE_THRESHOLD

    # ==========================================
    # Request ID
    # ==========================================

    request_id = str(uuid.uuid4())

    # ==========================================
    # Response
    # ==========================================

    return {
        "request_id": request_id,
        "category": category,  # Returns the original category received from Backend
        "description": description,
        "severity": severity,  # Returns 'LARGE', 'MEDIUM', or 'SMALL'
        "confidence": confidence,
        "needs_review": needs_review,
        "probabilities": probability_dict,
<<<<<<< HEAD
    }
=======
    }
>>>>>>> be8ae7d0ee85541c3c57c7cc50497ef5c409b537
