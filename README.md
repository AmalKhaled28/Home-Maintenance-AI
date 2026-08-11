# Home Maintenance AI API

AI-powered REST API for predicting the severity of home maintenance problems using Machine Learning models.

The API receives a maintenance category and a problem description, then predicts the severity level with a confidence score, class probabilities, and a human-review flag.

---

## Features

- Predict maintenance problem severity.
- Supports multiple maintenance categories.
- Arabic text preprocessing.
- Confidence score for every prediction.
- Probability for each severity class.
- Automatic human-review flag for low-confidence predictions.
- Unique request ID for every prediction, for downstream tracking.
- Structured CSV logging of every prediction.
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
│   ├── models.py
│   └── logger.py
│
├── logs/
│   ├── prediction_logs.csv
│   └── server.log
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

The `logs/` folder is created automatically on first run.

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

## Run with Docker

```bash
docker build -t home-maintenance-ai .
docker run -p 8000:8000 -v home-maintenance-logs:/app/logs home-maintenance-ai
```

The image runs as an unprivileged user and exposes port 8000. `logs/` is a
volume so `prediction_logs.csv` survives container restarts and redeploys.

---

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`, which:

1. Builds the image.
2. Smoke tests it — boots the container, checks `/health`, and runs a real
   `/predict` call so a broken model file or a scikit-learn version mismatch
   fails the build instead of reaching the server.
3. Pushes it to GHCR as `ghcr.io/<owner>/<repo>:latest` and `:<commit-sha>`.
4. SSHes into the server, copies `docker-compose.yml` plus the image tag, runs
   `docker compose pull && docker compose up -d`, and waits for the container
   healthcheck to report `healthy` (the deploy fails if it never does).

### Server prerequisites

- Docker Engine with the Compose v2 plugin.
- The deploy user in the `docker` group.
- A public key in the deploy user's `~/.ssh/authorized_keys`.

### Required repository secrets

| Secret | Description |
|--------|-------------|
| `SSH_HOST` | Server hostname or IP |
| `SSH_USER` | SSH user to deploy as |
| `DEPLOY_KEY` | Private key (full contents) for that user |
| `DEPLOY_KNOWN_HOSTS` | Optional. Output of `ssh-keyscan -p <port> <host>`. Without it the workflow trusts the host key on first connection |

### Optional repository variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DEPLOY_PORT` | `22` | SSH port |
| `DEPLOY_PATH` | `home-maintenance-ai` | Directory on the server holding the compose file |
| `HOST_PORT` | `8000` | Host port the API binds to |

By default the container binds to `127.0.0.1:8000` on the server, so it is not
reachable from the internet directly — put a reverse proxy (nginx, Caddy) in
front of it for TLS. To expose it directly instead, change the `ports` entry in
`docker-compose.yml` to `"${HOST_PORT:-8000}:8000"`.

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
  "request_id": "3f1b2c4a-7e2d-4b6a-9c1e-2a8f5d6e9b0c",
  "category": "Plumbing",
  "description": "في تسريب تحت الحوض",
  "severity": "Medium",
  "confidence": 0.9052,
  "needs_review": false,
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
| request_id | string | Unique ID for this prediction. The backend should store this alongside the request and use it to attach the technician's actual severity later. |
| category | string | Selected category (normalized to title case) |
| description | string | Original user description |
| severity | string | Predicted severity |
| confidence | float | Highest prediction probability |
| needs_review | boolean | `true` when confidence is below the review threshold (currently 0.70), meaning the prediction should not be trusted as-is and should be checked by a human before being used for downstream decisions such as pricing |
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
3. Normalize the category (case-insensitive matching).
4. Clean the Arabic text.
5. Select the appropriate model.
6. Predict the severity.
7. Calculate prediction probabilities and confidence.
8. Flag the prediction for human review if confidence is below threshold.
9. Generate a unique request ID.
10. Log the prediction to `logs/prediction_logs.csv`.
11. Return the prediction result.

---

## Prediction Logging

Every successful prediction is appended as a row to `logs/prediction_logs.csv`, containing:

- timestamp
- request_id
- category
- description
- severity
- confidence
- needs_review

This file is the source of truth for later evaluating the model against real technician outcomes: once the backend records the technician's actual severity for a given `request_id`, the two can be joined together to measure real-world accuracy.

Unexpected errors and validation warnings are logged separately to `logs/server.log` for debugging.

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
- The API logs every prediction to a local CSV file (`logs/prediction_logs.csv`) for analysis, but does not persist requests to a database.
- Full request storage, linking predictions to real outcomes, and AI estimation persistence should be handled by the backend service, using `request_id` as the join key.
- `needs_review` should be treated as a signal, not just metadata: predictions with `needs_review: true` should not be used as a final input to downstream decisions (e.g. pricing) without a human check.
