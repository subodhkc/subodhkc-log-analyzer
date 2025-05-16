# Placeholder for ingestion.pyfrom pathlib import Path

# Define the content for ingestion.py
ingestion_code = '''"""
ingestion.py – Handles log ingestion for SKC Log Reader

Supports single log files, folders, or ZIP uploads.
Handles recursive scanning and returns list of log lines with file metadata.
"""

import os
import zipfile
from typing import List, Tuple, Dict
from pathlib import Path


SUPPORTED_EXTENSIONS = [".log", ".txt", ".json", ".csv"]


def extract_zip(zip_path: str, extract_to: str = "temp_extracted") -> str:
    """
    Extracts a ZIP file to a temp directory and returns the path.
    """
    os.makedirs(extract_to, exist_ok=True)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    return extract_to


def collect_log_files(directory: str) -> List[Path]:
    """
    Recursively collects all supported log files in a directory.
    """
    logs = []
    for path in Path(directory).rglob("*"):
        if path.suffix.lower() in SUPPORTED_EXTENSIONS and path.is_file():
            logs.append(path)
    return logs


def read_logs_from_files(file_paths: List[Path]) -> List[Tuple[str, List[str]]]:
    """
    Reads lines from each file and returns a list of (filename, lines) tuples.
    """
    results = []
    for file in file_paths:
        try:
            with open(file, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
            results.append((str(file), lines))
        except Exception as e:
            results.append((str(file), [f"⚠️ Error reading file: {e}"]))
    return results


def ingest(input_path: str) -> List[Tuple[str, List[str]]]:
    """
    Ingests a ZIP file or directory of logs and returns parsed content.
    """
    path_obj = Path(input_path)

    if path_obj.suffix == ".zip":
        extracted_path = extract_zip(input_path)
        files = collect_log_files(extracted_path)
    elif path_obj.is_dir():
        files = collect_log_files(input_path)
    elif path_obj.is_file() and path_obj.suffix.lower() in SUPPORTED_EXTENSIONS:
        files = [path_obj]
    else:
        return [("Unknown Input", ["❌ Unsupported input format"])]

    return read_logs_from_files(files)
'''

# Write the file to the correct directory
modules_dir = Path("/mnt/data/skc_log_reader/modules")
modules_dir.mkdir(parents=True, exist_ok=True)
ingestion_file = modules_dir / "ingestion.py"

with open(ingestion_file, "w") as f:
    f.write(ingestion_code)

ingestion_file.name
