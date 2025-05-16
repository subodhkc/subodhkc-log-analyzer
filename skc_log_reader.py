"""
skc_log_reader.py – Final full version for SKC Log Reader

Includes features from Step 1 through Step 7:
- Login, upload, preview, validation, analysis, recommendation, RCA, and reporting
"""

import streamlit as st
from modules import (
    ingestion, redaction, analysis, test_plan,
    recommendations, report, ai_rca, auth, history
)
import json
from io import StringIO
import os

st.set_page_config(page_title="SKC Log Reader", layout="wide")

# Auth Setup
AUTH_ENABLED = auth.is_auth_enabled()
if AUTH_ENABLED:
    st.sidebar.title("🔐 Session")
    if not st.session_state.get("auth_ok"):
        with st.sidebar.form("login"):
            st.write("Login to access the app:")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            creds = auth.load_credentials()
            if submitted:
                if creds and username == creds["username"] and auth.verify_password(password, creds["password_hash"]):
                    st.session_state["auth_ok"] = True
                    st.sidebar.success("✅ Login successful")
                else:
                    st.sidebar.error("❌ Invalid credentials")
        st.stop()
    else:
        st.sidebar.success("✅ Logged in as " + creds["username"])
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.experimental_rerun()

# Title
st.title("📊 SKC Log Reader – Subodh Log Analyzer")

# State setup
for key in [
    "log_lines", "redacted_lines", "events", "summary", "test_plan_results",
    "recommendations", "plan_refresh", "ai_rca_prompt", "ingested_files",
    "project_name", "app_name", "build_version", "test_type"
]:
    if key not in st.session_state:
        st.session_state[key] = None

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Upload Logs", "Test Plan", "Analysis", "Recommendations", "Report"])

# Upload Logs
with tab1:
    st.header("📁 Upload and Redact Logs")
    uploaded_file = st.file_uploader("Upload a log file or ZIP", type=["log", "txt", "json", "zip"])
    custom_words = st.text_input("Custom redaction keywords (comma-separated)").split(",")

    col1, col2 = st.columns(2)
    with col1:
        if uploaded_file and st.button("Ingest and Redact"):
            temp_path = "temp.zip" if uploaded_file.name.endswith(".zip") else "temp.log"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())
            files = ingestion.ingest(temp_path)
            lines = [line for _, content in files for line in content]
            st.session_state["log_lines"] = lines
            st.session_state["ingested_files"] = files
            st.session_state["redacted_lines"] = redaction.redact_logs(lines, custom_words)
            history.log_event("log_uploaded", {"filename": uploaded_file.name})
            st.success("Logs redacted and loaded.")
    with col2:
        if st.button("Clear Logs"):
            for key in ["log_lines", "redacted_lines", "events", "summary", "test_plan_results", "recommendations", "ai_rca_prompt", "ingested_files"]:
                st.session_state[key] = None
            st.success("Session reset. You may re-upload logs.")

    if st.session_state["ingested_files"]:
        st.subheader("📂 Ingested File Overview")
        for fname, content in st.session_state["ingested_files"]:
            with st.expander(f"View content: {fname}"):
                st.code("".join(content[:200]), language="text")

    if st.session_state["redacted_lines"]:
        st.subheader("🔍 Redacted Logs Preview (Top 10)")
        preview = redaction.preview_redactions(st.session_state["log_lines"], custom_words)
        for i in range(len(preview["original"])):
            st.markdown(f"**Original:** `{preview['original'][i].strip()}`")
            st.markdown(f"**Redacted:** `{preview['redacted'][i].strip()}`")
            st.markdown("---")
        total_redactions = sum(1 for o, r in zip(st.session_state["log_lines"], st.session_state["redacted_lines"]) if o != r)
        st.info(f"Total redacted lines: {total_redactions}")

# Test Plan
with tab2:
    st.header("📋 Test Plan Validation")
    if st.session_state["plan_refresh"]:
        st.experimental_rerun()
    plan_list = test_plan.list_saved_plans()
    selected = st.selectbox("Choose existing plan", plan_list) if plan_list else None
    uploaded_plan = st.file_uploader("Upload new test plan (JSON)", type=["json"], key="plan")

    if uploaded_plan:
        try:
            plan_json = json.load(uploaded_plan)
            required_keys = {"steps"}
            if not required_keys.issubset(plan_json.keys()):
                st.error("Invalid test plan format. 'steps' key missing.")
            else:
                name = st.text_input("Save this plan as:", value="new_plan")
                if st.button("Save Plan"):
                    test_plan.save_test_plan(plan_json, name)
                    st.session_state["plan_refresh"] = True
                    st.rerun()
        except Exception as e:
            st.error(f"Error loading plan: {e}")

    plan_obj = test_plan.load_test_plan(f"test_plans/{selected}") if selected else None
    if plan_obj and st.session_state["log_lines"]:
        parsed = analysis.LogAnalyzer().parse_logs(st.session_state["redacted_lines"])
        results = test_plan.validate_test_plan(plan_obj, parsed)
        st.session_state["test_plan_results"] = results
        st.json(results)

# Analysis
with tab3:
    st.header("📈 Analyze Logs")
    if st.session_state["redacted_lines"]:
        analyzer = analysis.LogAnalyzer()
        events = analyzer.parse_logs(st.session_state["redacted_lines"])
        summary = analyzer.summary()
        st.session_state["events"] = events
        st.session_state["summary"] = summary

        st.subheader("Summary Overview")
        st.metric("Total Events", summary.get("total_events", 0))
        st.write("### Categories")
        st.json(summary.get("categories"))
        st.write("### Anomalies")
        st.write(summary.get("anomalies"))
        st.write("### Clusters")
        st.json(summary.get("clusters"))

# Recommendations + AI RCA
with tab4:
    st.header("💡 Recommendations and RCA")
    if st.session_state["summary"]:
        recs = recommendations.get_recommendations_from_summary(st.session_state["summary"])
        st.session_state["recommendations"] = recs
        st.subheader("🛠 Rule-Based Recommendations")
        for r in recs:
            st.markdown(f"- {r}")

        st.divider()
        st.subheader("🤖 GPT-Powered RCA (Optional)")
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            st.warning("OpenAI API key not set. Skipping AI RCA.")
        else:
            estimated_tokens = len(st.session_state["events"]) * 10
            st.caption(f"Estimated tokens: {estimated_tokens} | May incur cost.")
            if st.button("Run AI RCA Now"):
                metadata = {
                    "app_name": st.session_state.get("app_name", "N/A"),
                    "build_version": st.session_state.get("build_version", "N/A"),
                    "test_type": st.session_state.get("test_type", "N/A")
                }
                errors = [e.raw for e in st.session_state["events"] if e.severity >= 4]
                try:
                    rca = ai_rca.prepare_prompt(errors, metadata)
                    st.session_state["ai_rca_prompt"] = rca
                    st.success("AI RCA prompt generated.")
                except Exception as e:
                    st.error(f"Failed to generate RCA: {e}")

            if st.session_state["ai_rca_prompt"]:
                st.text_area("Generated RCA Prompt", st.session_state["ai_rca_prompt"], height=250)

# Report tab
with tab5:
    st.header("📝 Generate Report")

    st.text_input("Project Name", key="project_name")
    st.text_input("App Name", key="app_name")
    st.text_input("Build Version", key="build_version")
    st.text_input("Test Type", key="test_type")

    if st.button("Generate Report") and st.session_state["summary"] and st.session_state["recommendations"]:
        report.generate_text_report(
            st.session_state["summary"],
            st.session_state["recommendations"],
            test_results=st.session_state.get("test_plan_results"),
            metadata={
                "project_name": st.session_state["project_name"],
                "app_name": st.session_state["app_name"],
                "build_version": st.session_state["build_version"],
                "test_type": st.session_state["test_type"]
            }
        )
        report.generate_pdf_report(
            st.session_state["summary"],
            st.session_state["recommendations"],
            test_results=st.session_state.get("test_plan_results"),
            metadata={
                "project_name": st.session_state["project_name"],
                "app_name": st.session_state["app_name"],
                "build_version": st.session_state["build_version"],
                "test_type": st.session_state["test_type"]
            }
        )

    if os.path.exists("data/report.txt"):
        with open("data/report.txt", "r") as f:
            st.download_button("Download Text Report", f.read(), file_name="report.txt")
    if os.path.exists("data/report.pdf"):
        with open("data/report.pdf", "rb") as f:
            st.download_button("Download PDF Report", f, file_name="report.pdf")
# Placeholder for skc_log_reader.py
