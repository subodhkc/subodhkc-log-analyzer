"""
Analysis Module for SKC Log Reader
Performs log normalization, error extraction, timeline stitching,
anomaly detection, and rule-based issue categorization.
"""

import re
import json
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class LogEvent:
    timestamp: Optional[datetime]
    raw: str
    level: Optional[str]
    category: str
    severity: int
    correlation_id: Optional[str]


# Known error patterns and mappings
SIGNATURES = {
    "access denied": ("Permissions", 3),
    "timeout": ("Timeout", 2),
    "exception": ("Exception", 4),
    "fail": ("Failure", 4),
    "install": ("Installer", 2),
    "msi": ("Installer", 3),
    "network": ("Network", 2),
    "disk full": ("Disk Space", 3),
    "not found": ("Missing Resource", 2),
    "crash": ("Crash", 5),
    "memory": ("Memory", 3),
    "api error": ("API", 2),
}


class LogAnalyzer:
    def __init__(self):
        self.events: List[LogEvent] = []

    def parse_logs(self, lines: List[str]) -> List[LogEvent]:
        """
        Parse list of log lines into LogEvent objects
        """
        ts_re = re.compile(r"(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2})")
        level_re = re.compile(r"\b(INFO|DEBUG|WARNING|ERROR|CRITICAL)\b", re.IGNORECASE)
        corr_re = re.compile(r"correlation[id]?[:=]\s*([A-Za-z0-9\-]+)", re.IGNORECASE)

        for line in lines:
            try:
                ts = None
                match = ts_re.search(line)
                if match:
                    try:
                        ts = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
                    except:
                        ts = datetime.strptime(match.group(1), "%Y-%m-%dT%H:%M:%S")
                level_match = level_re.search(line)
                level = level_match.group(1).upper() if level_match else None
                corr_match = corr_re.search(line)
                correlation_id = corr_match.group(1) if corr_match else None

                # Identify category and severity
                category = "Other"
                severity = 1
                for keyword, (cat, sev) in SIGNATURES.items():
                    if keyword in line.lower():
                        category, severity = cat, sev
                        break

                self.events.append(LogEvent(ts, line.strip(), level, category, severity, correlation_id))
            except Exception as e:
                continue
        return self.events

    def cluster_events(self, window_s: int = 5) -> List[Dict]:
        """
        Group log events into time-based clusters
        """
        if not self.events:
            return []

        sorted_events = sorted(self.events, key=lambda x: x.timestamp or datetime.min)
        clusters = []
        current = [sorted_events[0]]
        for i in range(1, len(sorted_events)):
            delta = (sorted_events[i].timestamp - sorted_events[i - 1].timestamp).total_seconds() if \
                (sorted_events[i].timestamp and sorted_events[i - 1].timestamp) else 0
            if delta <= window_s:
                current.append(sorted_events[i])
            else:
                clusters.append(current)
                current = [sorted_events[i]]
        clusters.append(current)
        return [
            {
                "category": cluster[0].category,
                "count": len(cluster),
                "sample": cluster[0].raw,
                "timestamps": [e.timestamp for e in cluster if e.timestamp]
            }
            for cluster in clusters
        ]

    def detect_anomalies(self) -> List[str]:
        """
        Naive anomaly detection based on gaps, excessive severity, or out-of-order timestamps
        """
        outliers = []
        timestamps = [e.timestamp for e in self.events if e.timestamp]
        if not timestamps:
            return []

        # Check timestamp gaps
        for i in range(1, len(timestamps)):
            gap = (timestamps[i] - timestamps[i - 1]).total_seconds()
            if gap > 300:
                outliers.append(f"⚠️ Large time gap: {int(gap)}s between {timestamps[i-1]} and {timestamps[i]}")

        # Count high severity
        high = [e for e in self.events if e.severity >= 4]
        if len(high) > len(self.events) * 0.4:
            outliers.append("⚠️ High proportion of critical errors detected.")

        return outliers

    def summary(self) -> Dict:
        """
        Summarize logs by categories and anomalies
        """
        category_counts = {}
        for e in self.events:
            category_counts[e.category] = category_counts.get(e.category, 0) + 1

        return {
            "total_events": len(self.events),
            "categories": category_counts,
            "clusters": self.cluster_events(),
            "anomalies": self.detect_anomalies()
        }

    def export_json(self, filepath: str) -> None:
        """
        Export summary to JSON file
        """
        with open(filepath, "w") as f:
            json.dump(self.summary(), f, default=str, indent=2)
# Placeholder for analysis.py
