from pathlib import Path

# Define the content for history.py
history_code = '''"""
history.py – User action and log upload history tracking for SKC Log Reader

This module logs analysis history, file uploads, and AI-RCA usage
to a local JSONL file. Useful for auditing or resuming sessions.
"""

import os
import json
from datetime import datetime
from typing import Optional, Dict

HISTORY_LOG_PATH = "data/history_log.jsonl"


def log_event(event_type: str, metadata: Optional[Dict] = None):
    """
    Records an event (e.g., log uploaded, RCA run, summary exported)
    to the local history log.
    """
    record = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "meta": metadata or {}
    }
    os.makedirs(os.path.dirname(HISTORY_LOG_PATH), exist_ok=True)
    with open(HISTORY_LOG_PATH, "a") as f:
        f.write(json.dumps(record) + "\\n")


def read_history(limit: Optional[int] = 100) -> list:
    """
    Reads recent history from the history log.
    Returns the last `limit` entries (default: 100).
    """
    if not os.path.exists(HISTORY_LOG_PATH):
        return []
    with open(HISTORY_LOG_PATH, "r") as f:
        lines = f.readlines()[-limit:]
    return [json.loads(line.strip()) for line in lines]
'''

# Write the file to the correct directory
modules_dir = Path("/mnt/data/skc_log_reader/modules")
modules_dir.mkdir(parents=True, exist_ok=True)
history_file = modules_dir / "history.py"

with open(history_file, "w") as f:
    f.write(history_code)

history_file.name
# Placeholder for history.py
