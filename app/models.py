import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"

# تخزين الموديلات بعد تحميلها لأول مرة
_LOADED_MODELS = {}

MODEL_FILES = {
    "Plumbing": ("plumbing_model.pkl", "plumbing_encoder.pkl"),
    "Electrical": ("electrical_model.pkl", "electrical_encoder.pkl"),
    "Carpentry": ("carpentry_model.pkl", "carpentry_encoder.pkl"),
    "Painting": ("painting_model.pkl", "painting_encoder.pkl"),
}

def get_model_and_encoder(category: str):
    if category not in MODEL_FILES:
        raise ValueError(f"Unsupported category: {category}")
    
    # إذا كان الموديل محملاً في الذاكرة مسبقاً، ارجعه مباشرة
    if category in _LOADED_MODELS:
        return _LOADED_MODELS[category]
    
    # تحميل الموديل المطلوب فقط عند الحاجة إليه
    model_file, encoder_file = MODEL_FILES[category]
    model = joblib.load(MODELS_DIR / model_file)
    encoder = joblib.load(MODELS_DIR / encoder_file)
    
    _LOADED_MODELS[category] = {"model": model, "encoder": encoder}
    return _LOADED_MODELS[category]