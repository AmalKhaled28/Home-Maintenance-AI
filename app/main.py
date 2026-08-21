# app/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.predict import predict_severity


app = FastAPI(
    title="Home Maintenance AI API",
    description="AI Service for Predicting Maintenance Problem Severity",
    version="1.0.0"
)


class PredictionRequest(BaseModel):
    category: str
    description: str


@app.get("/")
@app.get("/api")
def home():
    return {
        "message": "Home Maintenance AI API is running"
    }


@app.get("/health")
@app.get("/api/health")
def health():
    return {
        "status": "OK"
    }


@app.post("/predict")
@app.post("/api/predict")
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

    except Exception as e:
        print(f"Prediction error: {str(e)}")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )