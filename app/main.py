from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging

from app.predict import predict_severity
from app.logger import log_prediction, LOG_DIR

# ==========================================
# Logging Setup
# ==========================================
# Two separate logs, on purpose:
# - prediction_logs.csv (via log_prediction): structured, one row per
#   successful prediction, meant for later analysis / DB import.
# - server.log (via logging): free-text errors and warnings, meant for
#   debugging the service itself.

logging.basicConfig(
    filename=LOG_DIR / "server.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

app = FastAPI(
    title="Home Maintenance AI API",
    description="AI Service for Predicting Maintenance Problem Severity",
    version="1.0.0"
)


class PredictionRequest(BaseModel):
    category: str
    description: str


@app.get("/")
def home():
    return {
        "message": "Home Maintenance AI API is running"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }


@app.post("/predict")
def predict(request: PredictionRequest):

    try:

        result = predict_severity(
            category=request.category,
            description=request.description
        )

        # Structured CSV log — one row per successful prediction.
        log_prediction(
            request_id=result["request_id"],
            category=result["category"],
            description=result["description"],
            severity=result["severity"],
            confidence=result["confidence"],
            needs_review=result["needs_review"]
        )

        return result

    except ValueError as e:

        logging.warning(str(e))

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception:

        logging.exception("Unexpected Error")

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )
