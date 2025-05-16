"""
test_plan.py – Test Plan Validator for SKC Log Reader

- Validates log events against test plan steps
- Saves uploaded test plans to disk for reuse
- Supports listing and loading saved plans
"""

import os
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from modules.analysis import LogEvent

TEST_PLAN_DIR = Path("test_plans")

def save_test_plan(plan_json: Dict, plan_name: str) -> str:
    """
    Saves a test plan to the local test_plans/ directory.
    """
    TEST_PLAN_DIR.mkdir(parents=True, exist_ok=True)
    plan_path = TEST_PLAN_DIR / f"{plan_name}.json"
    with open(plan_path, "w", encoding="utf-8") as f:
        json.dump(plan_json, f, indent=2)
    return str(plan_path)

def list_saved_plans() -> List[str]:
    """
    Lists all saved test plans in the test_plans/ folder.
    """
    if not TEST_PLAN_DIR.exists():
        return []
    return [f.name for f in TEST_PLAN_DIR.glob("*.json")]

def load_test_plan(path: str) -> Optional[Dict]:
    """
    Loads a test plan JSON file from disk.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load test plan: {e}")
        return None

def match_step_to_logs(step: Dict, events: List[LogEvent]) -> Tuple[bool, List[LogEvent]]:
    """
    Checks whether a step's expected keywords appear in the log events.
    Returns (match_found, matching_events).
    """
    keywords = step.get("expected_keywords", [])
    matches = []

    for event in events:
        if all(re.search(k, event.raw, re.IGNORECASE) for k in keywords):
            matches.append(event)

    return (len(matches) > 0, matches)

def validate_test_plan(plan: Dict, events: List[LogEvent]) -> List[Dict]:
    """
    Validates a test plan against parsed log events.
    Returns a list of validation results per step.
    """
    results = []
    for step in plan.get("steps", []):
        matched, logs = match_step_to_logs(step, events)
        result = {
            "step_id": step.get("id"),
            "description": step.get("description"),
            "required": step.get("must_occur", True),
            "status": "PASSED" if matched else "FAILED" if step.get("must_occur", True) else "OPTIONAL",
            "matched_logs": [e.raw for e in logs]
        }
        results.append(result)
    return results

def summarize_results(results: List[Dict]) -> Dict:
    """
    Creates a summary dictionary from validation results.
    """
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASSED")
    failed = sum(1 for r in results if r["status"] == "FAILED")
    optional = sum(1 for r in results if r["status"] == "OPTIONAL")

    return {
        "total_steps": total,
        "passed": passed,
        "failed": failed,
        "optional": optional,
        "status": "PASS" if failed == 0 else "FAIL"
    }
