"""
AI RCA Module for SKC Log Reader
Performs redacted log analysis using OpenAI's GPT API
Only invoked after pre-analysis is completed and confirmed
"""

import os
import openai
from typing import List, Optional

# Safe import of API key
try:
    openai.api_key = os.getenv("OPENAI_API_KEY") or \
                     (st.secrets["general"]["OPENAI_API_KEY"] if "general" in st.secrets else None)
except Exception:
    openai.api_key = None


def prepare_prompt(errors: List[str], metadata: dict) -> str:
    """
    Prepares a clean prompt for GPT-4 based on error list and metadata
    """
    app = metadata.get("app_name", "Unknown App")
    build = metadata.get("build_version", "Unknown Build")
    test = metadata.get("test_type", "Unknown Test Type")
    plan_coverage = metadata.get("plan_coverage", "N/A")

    error_excerpt = "\n".join(errors[:50]) if errors else "No errors extracted."

    prompt = f"""You are an RCA (Root Cause Analysis) assistant for software logs.

The user ran a test for **{app}** using **{test}** on build **{build}**.

The test plan coverage was approximately {plan_coverage}%.

Below is a list of redacted error messages extracted from the logs:

{error_excerpt}

Please provide a short, structured root cause summary, and recommend next steps for the TPM or developer.

Explain concisely but with technical insight. Highlight failure phases if detectable.
"""
    return prompt


def call_gpt_for_rca(prompt: str) -> Optional[str]:
    """
    Sends the redacted prompt to GPT-4 API and returns the RCA response.
    """
    if not openai.api_key:
        return "❌ No OpenAI API key detected. Please configure your API key in .streamlit/secrets.toml or set as an environment variable."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant specialized in software log analysis and RCA."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.4
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"❌ GPT API error: {e}"
# Placeholder for ai_rca.py
