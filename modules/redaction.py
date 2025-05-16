from pathlib import Path

# Updated redaction.py with full HP product name support
updated_redaction_code = '''"""
redaction.py – Sensitive data redaction utility for SKC Log Reader

This module identifies and replaces sensitive info in logs like:
- Emails, IPs, hostnames, usernames
- Product names including known HP applications
- Custom user-defined keywords
"""

import re
from typing import List, Dict

# List of known HP product names (add more as needed)
HP_PRODUCT_NAMES = [
    "3D Drive Guard", "Active Pen", "Audio Control 2021", "Audio Control 2022", "Blulb Digital Portfolio",
    "Class Room Manager", "Collaboration Keyboard", "Common Access Service layer", "DSO", "E-sign",
    "eAI- Sage", "Easy Clean", "Eco Meter", "Fuild Math", "Hotkeys CWT", "Hotkeys IJWP",
    "HP thin update 2", "HPQT\\(SA\\)", "Interactive Light", "Omen SDK", "OMEN Light Studio",
    "Pen SDK", "QuickDrop", "Smart Sense", "Software Control Panel", "Softpaq Downloader",
    "Status App", "System Info App", "TabletButtonService", "Tile", "Touchpoint Customizer",
    "Touchpoint Analytics", "Update Assistant", "Voice Notes", "Wacom Pen", "Windows AutoLaunch",
    "Xpress Keypad", "HP Display Control", "HP Device Access Manager", "HP Hotkeys", "HP Support Assistant"
]

# Build a regex pattern to match any product name
PRODUCT_PATTERN = r"\\b(" + "|".join(re.escape(name) for name in HP_PRODUCT_NAMES) + r")\\b"

REDACTION_PATTERNS = {
    "email": r"[\\w\\.-]+@[\\w\\.-]+",
    "ip": r"\\b(?:[0-9]{1,3}\\.){3}[0-9]{1,3}\\b",
    "hostname": r"\\bDESKTOP-[A-Za-z0-9]+\\b",
    "username": r"\\\\[A-Za-z0-9_-]+",
    "token": r"(?i)bearer\\s+[a-z0-9\\._\\-]+",
    "product": PRODUCT_PATTERN
}


def redact_line(line: str, custom: List[str] = []) -> str:
    """
    Redacts sensitive content in a single log line.
    Optionally adds custom keywords to redact.
    """
    redacted = line
    for key, pattern in REDACTION_PATTERNS.items():
        redacted = re.sub(pattern, f"[REDACTED_{key.upper()}]", redacted, flags=re.IGNORECASE)
    for word in custom:
        redacted = re.sub(re.escape(word), "[REDACTED_CUSTOM]", redacted, flags=re.IGNORECASE)
    return redacted


def redact_logs(lines: List[str], custom_words: List[str] = []) -> List[str]:
    """
    Redacts a list of log lines using built-in and custom rules
    """
    return [redact_line(line, custom=custom_words) for line in lines]


def preview_redactions(lines: List[str], custom_words: List[str] = []) -> Dict[str, List[str]]:
    """
    Shows before-and-after samples for visual UI comparison
    """
    original = lines[:10]
    redacted = redact_logs(original, custom_words)
    return {
        "original": original,
        "redacted": redacted
    }
'''

# Write the updated file
modules_dir = Path("/mnt/data/skc_log_reader/modules")
redaction_file = modules_dir / "redaction.py"

with open(redaction_file, "w") as f:
    f.write(updated_redaction_code)

redaction_file.name
