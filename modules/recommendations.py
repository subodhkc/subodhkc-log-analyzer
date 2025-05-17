# Final recommendation.py without emojis and using plain text for compatibility with cp1252 encoding
from pathlib import Path

recommendation_plain = '''"""
recommendations.py – Rule-based recommendation engine for SKC Log Reader

Uses error categories and known error codes to suggest human-readable fixes.
"""

from typing import List, Dict
from modules.error_codes import ERROR_CODES


def generate_recommendations(summary: Dict, raw_logs: List[str]) -> List[str]:
    """
    Returns actionable recommendations based on log summary and content.
    """
    recs = []

    # Category-based recommendations
    category_map = {
        "Installer": "Hint: Check if the app is already installed or blocked by policy. Run the installer manually to observe UI errors.",
        "SoftPaq": "Hint: Ensure the correct SoftPaq version is used. Try downloading again or running from a clean environment.",
        "DISM": "Hint: Run DISM /Online /Cleanup-Image /RestoreHealth. Add /Source if using WSUS or offline media.",
        "CBS": "Hint: Check C:\\Windows\\Logs\\CBS\\CBS.log for full error trace. Reapply the update if needed.",
        "WindowsUpdate": "Hint: Try resetting Windows Update components or using the Update Troubleshooter.",
        "Permissions": "Hint: Ensure user has admin rights. Try running the failing command with elevated privileges.",
        "Crash": "Hint: Look for crash dumps or Event Viewer logs. Analyze EventID 1000 for application name and module.",
        "ServiceFailure": "Hint: Open 'services.msc' and verify the affected service is set to auto-restart or fix dependency errors."
    }

    for cat in summary.get("categories", {}):
        if cat in category_map:
            recs.append(f"{category_map[cat]}")

    # Error code-specific recommendations
    for line in raw_logs:
        for code, info in ERROR_CODES.items():
            if code.lower() in line.lower():
                recs.append(f"Error {code}: {info['meaning']} → Fix: {info['fix']}")

    if not recs:
        recs.append("No known critical issues found. Review anomalies and test plan results for further guidance.")

    return list(set(recs))  # De-duplicate
'''

# Save updated file with safe encoding
rec_file = Path("/mnt/data/skc_log_reader/modules/recommendations.py")
rec_file.write_text(recommendation_plain, encoding="utf-8")

rec_file.name
