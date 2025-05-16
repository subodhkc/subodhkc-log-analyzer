"""
history.py – Run history logger for SKC Log Reader

Appends session metadata to a local CSV for auditing and tracking.
"""

import csv
from pathlib import Path
from typing import Dict
from datetime import datetime

HISTORY_FILE = Path("run_history.csv")


def log_run(metadata: Dict) -> None:
    """
    Append a row of metadata to the history CSV file.
    """
    headers = [
        "timestamp", "user", "filename", "event", "project_name",
        "app_name", "build_version", "test_type",
        "total_events", "failures_detected", "anomalies", "used_ai_rca"
    ]

    # Add timestamp if not present
    metadata["timestamp"] = metadata.get("timestamp", datetime.utcnow().isoformat())

    # Prepare row based on expected headers
    row = [metadata.get(k, "") for k in headers]

    try:
        write_header = not HISTORY_FILE.exists()
        with open(HISTORY_FILE, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            if write_header:
                writer.writerow(headers)
            writer.writerow(row)
    except Exception as e:
        print(f"⚠️ Failed to write run history: {e}")
