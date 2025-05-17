# Create an enhanced version of recommendations.py that uses error_codes.py for context-aware suggestions
from pathlib import Path

recommendation_code = '''"""
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
        "Installer": "Check if the app is already installed or blocked by policy. Run the installer manually to observe UI errors.",
        "SoftPaq": "Ensure the correct SoftPaq version is used. Try downloading again or running from a clean environment.",
        "DISM": "Run: DISM /Online /Cleanup-Image /RestoreHealth. Add /Source if using WSUS or offline media.",
        "CBS": "Check C:\\Windows\\Logs\\CBS\\CBS.log for full error trace. Reapply the update if needed.",
        "WindowsUpdate": "Try resetting Windows Update components or using the Update Troubleshooter.",
        "Permissions": "Ensure user has admin rights. Try running the failing command with elevated privileges.",
        "Crash": "Look for crash dumps or Event Viewer logs. Analyze EventID 1000 for application name and module.",
        "ServiceFailure": "Open 'services.msc' and verify the affected service is set to auto-restart or fix dependency errors."
    }

    for cat in summary.get("categories", {}):
        if cat in category_map:
            recs.append(f"💡 {cat}: {category_map[cat]}")

    # Error code-specific recommendations
    for line in raw_logs:
        for code, info in ERROR_CODES.items():
            if code.lower() in line.lower():
                recs.append(f"🔍 Error {code}: {info['meaning']} → Fix: {info['fix']}")

    if not recs:
        recs.append("✅ No known critical issues found. Review anomalies and test plan results for further guidance.")

    return list(set(recs))  # De-duplicate
'''

# Save updated file
rec_path = Path("/mnt/data/skc_log_reader/modules/recommendations.py")
rec_path.parent.mkdir(parents=True, exist_ok=True)
rec_path.write_text(recommendation_code)

rec_path.name
