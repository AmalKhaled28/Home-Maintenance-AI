<<<<<<< HEAD
import joblib
from pathlib import Path

# ==========================================
# Models Directory
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODELS_DIR = BASE_DIR / "models"

# ==========================================
# Load Plumbing Model
# ==========================================

plumbing_model = joblib.load(
    MODELS_DIR / "plumbing_model.pkl"
)

plumbing_encoder = joblib.load(
    MODELS_DIR / "plumbing_encoder.pkl"
)

# ==========================================
# Load Electrical Model
# ==========================================

electrical_model = joblib.load(
    MODELS_DIR / "electrical_model.pkl"
)

electrical_encoder = joblib.load(
    MODELS_DIR / "electrical_encoder.pkl"
)

# ==========================================
# Load Carpentry Model
# ==========================================

carpentry_model = joblib.load(
    MODELS_DIR / "carpentry_model.pkl"
)

carpentry_encoder = joblib.load(
    MODELS_DIR / "carpentry_encoder.pkl"
)

# ==========================================
# Load Painting Model
# ==========================================

painting_model = joblib.load(
    MODELS_DIR / "painting_model.pkl"
)

painting_encoder = joblib.load(
    MODELS_DIR / "painting_encoder.pkl"
)

# ==========================================
# Dictionary of Models
# ==========================================

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

# ==========================================
# Loaded Models Message
# ==========================================

=======
import joblib
from pathlib import Path

# ==========================================
# Models Directory
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODELS_DIR = BASE_DIR / "models"

# ==========================================
# Load Plumbing Model
# ==========================================

plumbing_model = joblib.load(
    MODELS_DIR / "plumbing_model.pkl"
)

plumbing_encoder = joblib.load(
    MODELS_DIR / "plumbing_encoder.pkl"
)

# ==========================================
# Load Electrical Model
# ==========================================

electrical_model = joblib.load(
    MODELS_DIR / "electrical_model.pkl"
)

electrical_encoder = joblib.load(
    MODELS_DIR / "electrical_encoder.pkl"
)

# ==========================================
# Load Carpentry Model
# ==========================================

carpentry_model = joblib.load(
    MODELS_DIR / "carpentry_model.pkl"
)

carpentry_encoder = joblib.load(
    MODELS_DIR / "carpentry_encoder.pkl"
)

# ==========================================
# Load Painting Model
# ==========================================

painting_model = joblib.load(
    MODELS_DIR / "painting_model.pkl"
)

painting_encoder = joblib.load(
    MODELS_DIR / "painting_encoder.pkl"
)

# ==========================================
# Dictionary of Models
# ==========================================

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

# ==========================================
# Loaded Models Message
# ==========================================

>>>>>>> be8ae7d0ee85541c3c57c7cc50497ef5c409b537
print("All AI models loaded successfully.")