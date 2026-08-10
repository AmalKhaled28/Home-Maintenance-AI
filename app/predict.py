import uuid

from app.clean import clean_text
from app.models import MODELS

CONFIDENCE_THRESHOLD = 0.70


def predict_severity(category: str, description: str):

    # ==========================================
    # Validate Input
    # ==========================================

    if not description.strip():
        raise ValueError("Description cannot be empty")

    category = category.strip().title()

    if category not in MODELS:
        raise ValueError(f"Unsupported category: {category}")

    # ==========================================
    # Load Model & Encoder
    # ==========================================

    model = MODELS[category]["model"]
    encoder = MODELS[category]["encoder"]

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
    # Unique identifier returned to the caller so the backend can later
    # attach the technician's actual severity to this exact prediction
    # (e.g. UPDATE ... WHERE request_id = ...), instead of matching on
    # the raw description text.

    request_id = str(uuid.uuid4())

    # ==========================================
    # Response
    # ==========================================

    return {
        "request_id": request_id,
        "category": category,
        "description": description,
        "severity": severity,  # Returns 'LARGE', 'MEDIUM', or 'SMALL'
        "confidence": confidence,
        "needs_review": needs_review,
        "probabilities": (
            probability_dict  # Keys are formatted as 'LARGE', 'MEDIUM', 'SMALL'
        ),
    }