from pathlib import Path
import hashlib
import json

# Define the content for auth.py
auth_code = '''"""
auth.py – Optional authentication module for SKC Log Reader

This module provides basic local authentication using SHA-256 hashed passwords.
Intended for optional protection in Streamlit-based UI.
"""

import hashlib
import json
import os
from typing import Optional

DEFAULT_CRED_PATH = "config/auth_config.json"


def is_auth_enabled(path: str = DEFAULT_CRED_PATH) -> bool:
    """
    Checks whether authentication is enabled by verifying if the credential file exists.
    """
    return os.path.isfile(path)


def load_credentials(path: str = DEFAULT_CRED_PATH) -> Optional[dict]:
    """
    Loads hashed credentials from the local JSON config file.
    Expected format:
    {
        "username": "admin",
        "password_hash": "..."
    }
    """
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None


def verify_password(input_pwd: str, stored_hash: str) -> bool:
    """
    Hashes the input password and compares with stored hash
    """
    input_hash = hashlib.sha256(input_pwd.encode()).hexdigest()
    return input_hash == stored_hash


def hash_password(plain_pwd: str) -> str:
    """
    Utility to hash a plain text password (for setup or testing)
    """
    return hashlib.sha256(plain_pwd.encode()).hexdigest()
'''

# Write the file to the correct directory
modules_dir = Path("/mnt/data/skc_log_reader/modules")
modules_dir.mkdir(parents=True, exist_ok=True)
auth_file = modules_dir / "auth.py"

with open(auth_file, "w") as f:
    f.write(auth_code)

auth_file.name
# Placeholder for auth.py
