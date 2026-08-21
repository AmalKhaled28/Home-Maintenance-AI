# app/predict.py

import uuid

from app.clean import clean_text
from app.models import MODELS


CONFIDENCE_THRESHOLD = 0.70


CATEGORY_MAP = {
    "سباكة": "Plumbing",
    "كهرباء": "Electrical",
    "نجارة": "Carpentry",
    "دهانات": "Painting",
}


def predict_severity(category: str, description: str):

    # ==========================================
    # Validate Input
    # ==========================================

    if not description or not description.strip():
        raise ValueError("Description cannot be empty")

    if not category or not category.strip():
        raise ValueError("Category cannot be empty")

    category = category.strip()

    # ==========================================
    # Map Category
    # ==========================================

    english_category = CATEGORY_MAP.get(
        category,
        category.strip().lower().capitalize()
    )

    if english_category not in MODELS:
        raise ValueError(f"Unsupported category: {category}")

    # ==========================================
    # Get Model & Encoder
    # ==========================================

    model = MODELS[english_category]["model"]
    encoder = MODELS[english_category]["encoder"]

    # ==========================================
    # Clean Description
    # ==========================================

    clean_description = clean_text(description)

    if not clean_description:
        raise ValueError("Description contains no valid Arabic text")

    # ==========================================
    # Prediction
    # ==========================================

    prediction = model.predict(
        [clean_description]
    )[0]

    severity = str(
        encoder.inverse_transform([prediction])[0]
    ).upper()

    # ==========================================
    # Probabilities
    # ==========================================

    probabilities = model.predict_proba(
        [clean_description]
    )[0]

    probability_dict = {}

    for label, probability in zip(
        encoder.classes_,
        probabilities
    ):
        probability_dict[
            str(label).upper()
        ] = round(float(probability), 4)

    confidence = round(
        float(max(probabilities)),
        4
    )

    # ==========================================
    # Human Review
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
        "category": category,
        "description": description,
        "severity": severity,
        "confidence": confidence,
        "needs_review": needs_review,
        "probabilities": probability_dict,
    }