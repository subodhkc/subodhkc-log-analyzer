"""
ai_rca.py – GPT-based RCA generation module for SKC Log Reader

Prepares prompts and fetches AI-generated root cause analysis.
"""

import os
import openai
from typing import List, Dict, Optional

# Get API key from environment or Streamlit secrets
openai.api_key = os.getenv("OPENAI_API_KEY")
try:
    import streamlit as st
    if not openai.api_key and st.secrets.get("general"):
        openai.api_key = st.secrets["general"].get("OPENAI_API_KEY")
except Exception:
    pass


def prepare_prompt(errors: List[str], metadata: Dict) -> str:
    """
    Builds a GPT-compatible prompt from log errors and metadata.
    """
    app = metadata.get("app_name", "Unknown App")
    build = metadata.get("build_version", "Unknown Build")
    test = metadata.get("test_type", "Unknown Test Type")
    project = metadata.get("project_name", "Untitled Project")

    prompt = f"""You are an expert QA engineer.
Given the following log errors, provide a root cause analysis (RCA).

Project: {project}
App: {app}
Build: {build}
Test Type: {test}

Errors:
"""
    for e in errors[:50]:
        prompt += f"- {e}\n"

    prompt += "\nExplain what might be causing these errors and suggest fixes."
    return prompt


def fetch_gpt_rca(prompt: str, model: str = "gpt-4") -> Optional[str]:
    """
    Sends the prompt to GPT and returns the result.
    """
    if not openai.api_key:
        return "❌ Missing OpenAI API key. Please set it in your environment or secrets."

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert QA and software tester."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=800
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ GPT API call failed: {e}"
