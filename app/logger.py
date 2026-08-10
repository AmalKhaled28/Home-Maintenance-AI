import csv
from pathlib import Path
from datetime import datetime

# ==========================================
# Log File Path
# ==========================================
# Absolute path (independent of the working directory the server is
# launched from), stored under a dedicated "logs" folder next to "app".

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "prediction_logs.csv"


def log_prediction(
    request_id,
    category,
    description,
    severity,
    confidence,
    needs_review
):
    """
    Append one prediction record to the CSV log.

    Structured (columnar) logging is used instead of free-text logs so
    this file can later be loaded directly into pandas / a database
    table, and so each row can be matched back to the technician's
    actual severity using request_id.
    """

    file_exists = LOG_FILE.exists()

    with open(LOG_FILE, "a", newline="", encoding="utf-8-sig") as f:

        writer = csv.writer(f)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "request_id",
                "category",
                "description",
                "severity",
                "confidence",
                "needs_review"
            ])

        writer.writerow([
            datetime.now().isoformat(),
            request_id,
            category,
            description,
            severity,
            confidence,
            needs_review
        ])
