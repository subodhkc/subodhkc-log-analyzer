"""
auth.py – Simple credential loader for SKC Log Reader

Handles optional login flow using a local JSON config file.
"""

import os
import json
from typing import Optional
from pathlib import Path
import hashlib

CONFIG_PATH = Path("config/auth_config.json")


def is_auth_enabled() -> bool:
    """
    Check if authentication should be enforced.
    """
    return CONFIG_PATH.exists()


def load_credentials() -> Optional[dict]:
    """
    Loads credentials from the config file.
    """
    if not CONFIG_PATH.exists():
        return None
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load credentials: {e}")
        return None


def verify_password(input_password: str, stored_hash: str) -> bool:
    """
    Compare SHA-256 hash of input password with stored hash.
    """
    hashed_input = hashlib.sha256(input_password.encode()).hexdigest()
    return hashed_input == stored_hash
