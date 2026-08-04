# Home Maintenance AI API

AI-powered REST API for predicting the severity of home maintenance problems using Machine Learning models.

The API receives a maintenance category and a problem description, then predicts the severity level with a confidence score and class probabilities.

---

## Features

- Predict maintenance problem severity.
- Supports multiple maintenance categories.
- Arabic text preprocessing.
- Confidence score for every prediction.
- Probability for each severity class.
- FastAPI with automatic Swagger documentation.

---

## Supported Categories

- Plumbing
- Electrical
- Painting
- Carpentry

---

## Severity Levels

- Small
- Medium
- Large

---

## Project Structure

```
AI/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── predict.py
│   ├── clean.py
│   └── models.py
│
├── models/
│   ├── plumbing_model.pkl
│   ├── plumbing_encoder.pkl
│   ├── electrical_model.pkl
│   ├── electrical_encoder.pkl
│   ├── painting_model.pkl
│   ├── painting_encoder.pkl
│   ├── carpentry_model.pkl
│   └── carpentry_encoder.pkl
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository.

```bash
git clone <repository_url>
cd AI
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

## Run the API

```bash
python -m uvicorn app.main:app --reload
```

The API will be available at

```
http://127.0.0.1:8000
```

Swagger Documentation

```
http://127.0.0.1:8000/docs
```

Alternative Documentation

```
http://127.0.0.1:8000/redoc
```

---

## API Endpoints

### Home

```
GET /
```

Response

```json
{
  "message": "Home Maintenance AI API is running"
}
```

---

### Health Check

```
GET /health
```

Response

```json
{
  "status": "OK"
}
```

---

### Predict Severity

```
POST /predict
```

Request Body

```json
{
  "category": "Plumbing",
  "description": "في تسريب تحت الحوض"
}
```

Example Response

```json
{
  "category": "Plumbing",
  "description": "في تسريب تحت الحوض",
  "severity": "Medium",
  "confidence": 0.9052,
  "probabilities": {
    "Large": 0.0076,
    "Medium": 0.9052,
    "Small": 0.0872
  }
}
```

---

## Request Parameters

| Field | Type | Description |
|-------|------|-------------|
| category | string | Maintenance category |
| description | string | Problem description in Arabic |

---

## Response Parameters

| Field | Type | Description |
|-------|------|-------------|
| category | string | Selected category |
| description | string | Original user description |
| severity | string | Predicted severity |
| confidence | float | Highest prediction probability |
| probabilities | object | Probability of each severity class |

---

## Error Responses

Unsupported category

```json
{
  "detail": "Unsupported category: Gardening"
}
```

Empty description

```json
{
  "detail": "Description cannot be empty"
}
```

Internal server error

```json
{
  "detail": "Internal Server Error"
}
```

---

## Machine Learning Pipeline

1. Receive category and description.
2. Validate the input.
3. Clean the Arabic text.
4. Select the appropriate model.
5. Predict the severity.
6. Calculate prediction probabilities.
7. Return the prediction result.

---

## Technologies

- Python
- FastAPI
- Scikit-learn
- Joblib
- Pandas
- NumPy
- Uvicorn

---

## Notes

- Each maintenance category has its own trained Machine Learning model.
- Arabic text is normalized before prediction.
- The API does not store requests in a database.
- Request storage and AI estimation persistence should be handled by the backend service.
