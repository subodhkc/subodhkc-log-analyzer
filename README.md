

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



===============================
🔧 LOG ANALYZER SETUP GUIDE
===============================

This guide will help you set up and run the SKC Log Analyzer on your local Windows machine.

--------------------------------
 STEP 1: INSTALL PREREQUISITES
--------------------------------

 1.1 Install Git in your Pc(if not already installed)
--------------------------------------------
Git is required to clone the project from GitHub.

➡ Download link:
https://git-scm.com/download/win

After installing, open CMD and type:
    git --version
You should see a version number like `git version 2.43.0`

1.2 Install Python 3.8 or newer in your Pc (if not installed)
------------------------------------------------------
➡ Download link:
https://www.python.org/downloads/windows/

IMPORTANT:
✔ During installation, make sure to check: "Add Python to PATH"

After installing, open CMD and type:
    python --version
You should see something like: `Python 3.10.9`

-------------------------------------------------
STEP 2: CLONE THE REPO FROM GITHUB TO YOUR PC
-------------------------------------------------

1. Open Command Prompt (CMD) in your pc
2. Navigate to a folder where you want to store the code:

    cd %USERPROFILE%\Documents

3. Run the following command to clone:

    git clone https://github.com/subodhkc/subodhkc-log-analyzer.git

4. Move into the project directory:

    cd subodhkc-log-analyzer

------------------------------------------------
STEP 3: SET UP A PYTHON VIRTUAL ENVIRONMENT
------------------------------------------------

This keeps your dependencies clean and isolated.

Run these commands in the project folder:

    python -m venv venv
    venv\Scripts\activate

After this, your prompt should change to show `(venv)`

---------------------------------------
STEP 4: INSTALL REQUIRED DEPENDENCIES
---------------------------------------

OPTION A: If there is a file named `requirements.txt`:

    pip install -r requirements.txt

OPTION B: Manually install each package:

    pip install streamlit>=1.28.0
    pip install pandas>=1.5.3
    pip install PyYAML>=6.0.1
    pip install python-dateutil>=2.8.2
    pip install unicodedata2>=15.1.0
    pip install matplotlib>=3.7.0
    pip install seaborn>=0.12.2
    pip install fpdf2>=2.7.7
    pip install openai>=1.2.3
    pip install scikit-learn>=1.2.2
    pip install transformers
    pip install torch

 NOTE: `difflib` is already included with Python — no need to install.

-------------------------------
 STEP 5: RUN THE APPLICATION
-------------------------------

1. Make sure your virtual environment is activated:

    venv\Scripts\activate

2. Run the Streamlit app (example if entry point is `app.py`):

    streamlit run app.py

This will:
- Launch a local development server
- Open the SKC Log Analyzer in your default web browser
- Typically at: `http://localhost:8501/`

If that doesn't happen automatically, open your browser and paste the URL above.

-------------------------------
 WHAT TO EXPECT
-------------------------------

Once the app is running:
- You'll see a web UI with options to upload logs, select test plans, and view clustering/severity/ML outputs.
- Navigate through the steps with buttons or sidebars.
- Generated PDF reports (if enabled) will be downloadable via buttons in the app.

-------------------------------
 TROUBLESHOOTING TIPS
-------------------------------

- If a package fails to install, make sure pip is updated:

    python -m pip install --upgrade pip

- If Streamlit doesn't launch:

    python -m streamlit run app.py

- To stop the app:

    Press `CTRL + C` in the terminal

===============================
SETUP COMPLETE!
===============================
You are now ready to use the SKC Log Analyzer on your machine.


## License

Apache License 2.0  
© 2025 Subodh KC

## Acknowledgements

This tool was built by Subodh KC to simplify log analysis and empower Enterprise with modern Standalone compliance tool for debugging and decision-making.
'''

# Save plain README text file for download
readme_txt = Path("/mnt/data/README_SKC_Log_Reader.txt")
readme_txt.write_text(readme_plain)

readme_txt.name
