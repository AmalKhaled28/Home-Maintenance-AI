# Home Maintenance AI API

AI-powered REST API built with **Flask** and hosted on **PythonAnywhere** for predicting the severity of home maintenance issues in Egypt using Machine Learning models.

The API receives a maintenance category Arabic and a problem description, then predicts the severity level with a confidence score, class probabilities, and a human-review flag.

---

## Live API URL

```
https://amalkhaled.pythonanywhere.com
```

---

## Features

- **Flask API Architecture**: Lightweight and optimized for WSGI web hosting environments.
- **Lazy Loading ML Models**: Memory-efficient model loading on runtime to prevent server memory bloat.
- **Arabic Text Preprocessing**: Cleans and normalizes Arabic text input before vectorization.
- **Category Normalization**: Supports Arabic category names directly from the database (`سباكة`, `دهانات`, `نقاشة`, `كهرباء`, `نجارة`).
- **Severity Prediction**: Categorizes issues into `SMALL`, `MEDIUM`, or `LARGE`.
- **CORS Enabled**: Configured via `flask-cors` for cross-origin integration with Web and Mobile Frontends.
- **Confidence Scoring & Flagging**: Calculates probabilities and automatically sets `needs_review: true` for low-confidence predictions (< 0.70).
- **Request Tracking**: Generates a unique UUID `request_id` for every transaction.

---

## Supported Categories

| Category (Arabic Input) | 
| ------------------------ |
| سباكة                      |
| كهرباء                     |
| نجارة                      |
| دهانات                     |

---

## Severity Levels

- `SMALL`
- `MEDIUM`
- `LARGE`

---

## Project Structure

```
Home-Maintenance-AI/
│
├── api/
│   └── index.py            # Flask Web Application & Routes
│
├── app/
│   ├── __init__.py
│   ├── predict.py          # Category mapping & Model Inference Logic
│   ├── clean.py            # Arabic Text Preprocessing
│   ├── models.py           # Lazy loading for Scikit-learn models & encoders
│   └── logger.py           # Server logging setup
│
├── models/                 # Saved Scikit-Learn Model & Encoder Files
│   ├── plumbing_model.pkl
│   ├── plumbing_encoder.pkl
│   ├── electrical_model.pkl
│   ├── electrical_encoder.pkl
│   ├── painting_model.pkl
│   ├── painting_encoder.pkl
│   ├── carpentry_model.pkl
│   └── carpentry_encoder.pkl
│
├── requirements.txt        # Python dependencies
└── README.md
```

---

## API Endpoints

### 1. Health Check

Checks if the server and Flask application are running.

```http
GET /health
```

**Response (`200 OK`):**

```json
{
  "status": "OK"
}
```

### 2. Predict Severity

Predicts the severity of a maintenance issue based on Arabic description.

```http
POST /predict
```

**Headers:**

```http
Content-Type: application/json
```

**Request Body Example:**

```json
{
  "category": "سباكة",
  "description": "تسريب مياه شديد تحت الحوض"
}
```

**Response Example (`200 OK`):**

```json
{
  "category": "سباكة",
  "description": "تسريب مياه شديد تحت الحوض",
  "severity": "MEDIUM",
  "confidence": 0.8954,
  "needs_review": false,
  "probabilities": {
    "LARGE": 0.0211,
    "MEDIUM": 0.8954,
    "SMALL": 0.0835
  },
  "request_id": "8c3584e1-2220-4112-a111-998877665544"
}
```

---

## Error Responses

### Missing Fields (`400 Bad Request`)

```json
{
  "detail": "Missing category or description"
}
```

### Unsupported Category (`400 Bad Request`)

```json
{
  "detail": "Unsupported category: حدادة"
}
```

### Method Not Allowed (`405 Method Not Allowed`)

Occurs when opening `https://amalkhaled.pythonanywhere.com/predict` directly in a web browser using a `GET` request instead of a `POST` request.

---

## Local Development & Testing

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/AmalKhaled28/Home-Maintenance-AI.git
   cd Home-Maintenance-AI
   ```

2. **Set up Virtual Environment:**

   ```bash
   python -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run Server Locally:**

   ```bash
   python api/index.py
   ```

   The server will run on `http://127.0.0.1:5000`.

---

## Technologies Used

- **Python 3.10+**
- **Flask** (RESTful API Framework)
- **Flask-CORS** (Cross-Origin Resource Sharing)
- **Scikit-learn** (Machine Learning Model Inference)
- **Joblib** (Model Serialization)
- **Pandas & NumPy** (Data Manipulation)
- **PythonAnywhere** (WSGI Production Hosting)
