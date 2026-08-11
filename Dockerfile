# syntax=docker/dockerfile:1

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Dependencies first, so this layer is only rebuilt when requirements.txt changes.
# The scikit-learn pin must keep matching the version the .pkl models were
# trained with, otherwise joblib.load() will warn or fail at startup.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/
COPY models/ ./models/

# logs/ is written at runtime (prediction_logs.csv + server.log). Create it here
# and hand /app to the unprivileged user, so a named volume mounted on
# /app/logs inherits the right ownership on first start.
RUN mkdir -p /app/logs \
 && useradd --create-home --uid 10001 appuser \
 && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import sys,urllib.request; sys.exit(0 if urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3).status == 200 else 1)"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
