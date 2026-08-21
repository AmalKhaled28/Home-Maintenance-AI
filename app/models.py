# app/models.py
import joblib
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MODELS_DIR = BASE_DIR / "models"


plumbing_model = joblib.load(
    MODELS_DIR / "plumbing_model.pkl"
)

plumbing_encoder = joblib.load(
    MODELS_DIR / "plumbing_encoder.pkl"
)


electrical_model = joblib.load(
    MODELS_DIR / "electrical_model.pkl"
)

electrical_encoder = joblib.load(
    MODELS_DIR / "electrical_encoder.pkl"
)


carpentry_model = joblib.load(
    MODELS_DIR / "carpentry_model.pkl"
)

carpentry_encoder = joblib.load(
    MODELS_DIR / "carpentry_encoder.pkl"
)


painting_model = joblib.load(
    MODELS_DIR / "painting_model.pkl"
)

painting_encoder = joblib.load(
    MODELS_DIR / "painting_encoder.pkl"
)


MODELS = {

    "Plumbing": {
        "model": plumbing_model,
        "encoder": plumbing_encoder
    },

    "Electrical": {
        "model": electrical_model,
        "encoder": electrical_encoder
    },

    "Carpentry": {
        "model": carpentry_model,
        "encoder": carpentry_encoder
    },

    "Painting": {
        "model": painting_model,
        "encoder": painting_encoder
    }

}


print("All AI models loaded successfully.")