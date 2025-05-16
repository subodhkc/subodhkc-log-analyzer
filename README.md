

SKC Log Reader is a modular, local-first Python app designed to analyze and summarize complex log files with optional GPT-powered Root Cause Analysis (RCA). It’s built for TPMs, QA teams, and test engineers to streamline debugging and validation workflows.

## Features

- Multi-format log ingestion (.txt, .log, .json, .zip)
- Sensitive data redaction (emails, usernames, IPs, product names)
- Log normalization into structured events
- Timeline stitching and anomaly detection
- Test plan validation against structured JSON test plans
- Actionable recommendations (rule-based)
- PDF and Text report generation
- Optional authentication with SHA-256 password
- History tracking of log uploads and RCA attempts
- Streamlit UI (modular, clean, and interactive)

## Module Overview

| Module             | Purpose                                                       |
|--------------------|---------------------------------------------------------------|
| analysis.py        | Parses logs, categorizes errors, detects anomalies            |
| ai_rca.py          | Uses GPT to generate RCA summaries from errors (optional)     |
| auth.py            | Local password-based authentication                           |
| history.py         | Tracks usage and uploads in data/history_log.jsonl            |
| ingestion.py       | Unpacks and reads logs from ZIPs, folders, or files           |
| redaction.py       | Detects and redacts sensitive information                     |
| recommendations.py | Provides issue-based suggestions                              |
| report.py          | Generates structured TXT and PDF reports                      |
| test_plan.py       | Validates logs against test plans (JSON, saved locally)       |

## Folder Structure

subodhkc-log-analyzer/
├── modules/
│   ├── analysis.py
│   ├── ai_rca.py
│   ├── auth.py
│   ├── history.py
│   ├── ingestion.py
│   ├── redaction.py
│   ├── recommendations.py
│   ├── report.py
│   └── test_plan.py
├── config/
│   └── auth_config.json (optional)
├── test_plans/
│   └── *.json (saved test plans)
├── data/
│   ├── report.txt / report.pdf / history_log.jsonl
├── LICENSE
├── .gitignore
├── README.md
└── skc_log_reader.py (Streamlit app)

## Installation

Clone the repo and install dependencies:

    git clone https://github.com/subodhkc/subodhkc-log-analyzer.git
    cd subodhkc-log-analyzer
    pip install -r requirements.txt
    streamlit run skc_log_reader.py

You must create a file config/auth_config.json if using password login.

## Example Test Plan (JSON)

    {
      "app_name": "Audio Control 2022",
      "test_type": "Softpaq",
      "steps": [
        {
          "id": "step1",
          "description": "Install driver",
          "expected_keywords": ["install", "success"],
          "must_occur": true
        },
        {
          "id": "step2",
          "description": "Check service",
          "expected_keywords": ["service", "running"],
          "must_occur": false
        }
      ]
    }

## Optional Authentication

To enable login protection:

1. Generate password hash:
    from modules.auth import hash_password
    print(hash_password("your_password"))

2. Create file: config/auth_config.json
    {
      "username": "admin",
      "password_hash": "your_sha256_hash"
    }

## GPT-Based RCA (Optional)

Set your OpenAI API key in .streamlit/secrets.toml:

    [general]
    OPENAI_API_KEY = "sk-xxxx"

## License

Apache License 2.0  
© 2025 Subodh KC

## Acknowledgements

This tool was built by Subodh KC to simplify log analysis and empower TPMs and test engineers with modern tools for debugging and decision-making.
'''

# Save plain README text file for download
readme_txt = Path("/mnt/data/README_SKC_Log_Reader.txt")
readme_txt.write_text(readme_plain)

readme_txt.name
