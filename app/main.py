from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# from predict import predict_severity

from app.predict import predict_severity

app = FastAPI(
    title="Home Maintenance AI API",
    description="AI Service for Predicting Maintenance Problem Severity",
    version="1.0.0"
)


# ==========================================
# Request Model
# ==========================================

class PredictionRequest(BaseModel):
    category: str
    description: str


# ==========================================
# Root Endpoint
# ==========================================

@app.get("/")
def home():
    return {
        "message": "Home Maintenance AI API is running"
    }


# ==========================================
# Health Check
# ==========================================

@app.get("/health")
def health():
    return {
        "status": "OK"
    }


# ==========================================
# Prediction Endpoint
# ==========================================

@app.post("/predict")
def predict(request: PredictionRequest):

    try:

        result = predict_severity(
            category=request.category,
            description=request.description
        )

        return result

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
    )

