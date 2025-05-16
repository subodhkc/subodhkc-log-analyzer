"""
recommendations.py – Rule-Based Recommendation Generator

Uses known patterns and log analysis summary to provide helpful insights.
"""

from typing import List, Dict


def generate_recommendations(summary: Dict) -> List[str]:
    """
    Generate human-readable recommendations from analysis summary
    """
    recs = []

    # Check categories
    if "Timeout" in summary.get("categories", {}):
        recs.append("Check network stability or timeout thresholds.")
    if "Permissions" in summary.get("categories", {}):
        recs.append("Ensure the process has correct permissions.")
    if "Installer" in summary.get("categories", {}):
        recs.append("Review installer logs for MSI exit codes.")
    if "Crash" in summary.get("categories", {}):
        recs.append("Review stack traces or memory dumps for crash analysis.")
    if "API" in summary.get("categories", {}):
        recs.append("Validate external service availability or API keys.")

    # Check anomalies
    for anomaly in summary.get("anomalies", []):
        if "time gap" in anomaly.lower():
            recs.append("Investigate gaps in log timeline — possible crash or idle period.")
        if "critical errors" in anomaly.lower():
            recs.append("Review critical errors and correlate with test steps.")

    # Default fallback
    if not recs:
        recs
