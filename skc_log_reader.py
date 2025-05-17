"""
skc_log_reader.py – Final merged version for SKC Log Analyzer

Includes:
✔️ Login system
✔️ Log upload + ingestion + preview
✔️ Redaction with custom words
✔️ Auto analysis + summary
✔️ Test plan upload + selection + validation
✔️ Rule-based + AI RCA
✔️ Report generation + download
"""

import streamlit as st
from modules import (
    ingestion, redaction, analysis, test_plan,
    recommendations, report, ai_rca, auth, history
)
import json
import os

st.set_page_config(page_title="SKC Log Analyzer", layout="wide")

# --- AUTH ---
AUTH_ENABLED = auth.is_auth_enabled()
if AUTH_ENABLED:
    st.sidebar.title("🔐 Session Login")
    if not st.session_state.get("auth_ok"):
        with st.sidebar.form("login"):
            st.write("Login to access the tool:")
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
        st.sidebar.success("Logged in as: " + creds["username"])
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.experimental_rerun()

# --- STATE INIT ---
for key in [
    "log_lines", "redacted_lines", "events", "summary", "test_plan_results",
    "recommendations", "plan_refresh", "ai_rca_prompt", "ingested_files",
    "project_name", "app_name", "build_version", "test_type"
]:
    if key not in st.session_state:
        st.session_state[key] = None

# --- TABS ---
tab1, tab2, tab3, tab4, tab5 = st.tabs(["Upload Logs", "Test Plan", "Analysis", "Recommendations", "Report"])

# --- TAB 1: UPLOAD ---
with tab1:
    st.header("📁 Upload and Redact Logs")
    uploaded_file = st.file_uploader("Upload .log/.txt/.zip file", type=["zip", "txt", "log", "json"])
    custom_words = st.text_input("Custom redaction keywords (comma-separated)").split(",")

    col1, col2 = st.columns(2)
    with col1:
        if uploaded_file and st.button("Ingest and Redact"):
            temp_path = "temp.zip" if uploaded_file.name.endswith(".zip") else "temp.log"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.read())

            with st.spinner("🔄 Ingesting and redacting logs..."):
                files = ingestion.ingest(temp_path)
                lines = [line for _, content in files for line in content]
                redacted = redaction.redact_logs(lines, custom_words)
                st.session_state["log_lines"] = lines
                st.session_state["redacted_lines"] = redacted
                st.session_state["ingested_files"] = files
                history.log_event("log_uploaded", {"filename": uploaded_file.name})

            st.success("✅ Logs redacted and loaded. Proceed to Analysis.")

    with col2:
        if st.button("Clear Logs"):
            for key in ["log_lines", "redacted_lines", "events", "summary", "test_plan_results", "recommendations", "ai_rca_prompt", "ingested_files"]:
                st.session_state[key] = None
            st.success("Session reset. You may re-upload logs.")

    if st.session_state["ingested_files"]:
        st.subheader("📂 Ingested Files Preview")
        for fname, content in st.session_state["ingested_files"][:3]:
            with st.expander(f"{fname}"):
                st.code("".join(content[:50]), language="text")

    if st.session_state["redacted_lines"]:
        st.subheader("🔍 Redaction Preview")
        preview = redaction.preview_redactions(st.session_state["log_lines"], custom_words)
        for o, r in zip(preview["original"], preview["redacted"]):
            st.markdown(f"• **Original:** `{o.strip()}`")
            st.markdown(f"• **Redacted:** `{r.strip()}`")
        st.info(f"Total redacted lines: {sum(1 for o, r in zip(st.session_state['log_lines'], st.session_state['redacted_lines']) if o != r)}")

# --- TAB 2: TEST PLAN ---
with tab2:
    st.header("🧪 Test Plan Validation")
    if st.session_state["plan_refresh"]:
        st.experimental_rerun()

    plan_list = test_plan.list_saved_plans()
    selected = st.selectbox("Select existing plan", ["--"] + plan_list) if plan_list else "--"
    uploaded_plan = st.file_uploader("Upload new test plan (JSON)", type=["json"], key="plan")

    if uploaded_plan:
        try:
            plan_json = json.load(uploaded_plan)
            if "steps" not in plan_json:
                st.error("Invalid test plan format. 'steps' key missing.")
            else:
                name = st.text_input("Save this plan as", value="custom_plan")
                if st.button("Save Plan"):
                    test_plan.save_test_plan(plan_json, name)
                    st.session_state["plan_refresh"] = True
                    st.rerun()
        except Exception as e:
            st.error(f"Error reading plan: {e}")

    if selected != "--" and st.session_state["redacted_lines"]:
        plan_obj = test_plan.load_test_plan(f"test_plans/{selected}")
        parsed = analysis.LogAnalyzer().parse_logs(st.session_state["redacted_lines"])
        results = test_plan.validate_test_plan(plan_obj, parsed)
        st.session_state["test_plan_results"] = results
        st.subheader("✅ Test Plan Results")
        st.json(results)

# --- TAB 3: ANALYSIS ---
with tab3:
    st.header("📊 Log Analysis Summary")
    if st.session_state["redacted_lines"]:
        analyzer = analysis.LogAnalyzer()
        events = analyzer.parse_logs(st.session_state["redacted_lines"])
        summary = analyzer.summary()
        st.session_state["events"] = events
        st.session_state["summary"] = summary

        st.metric("Total Events", summary.get("total_events", 0))
        st.subheader("Categories")
        st.json(summary.get("categories", {}))
        st.subheader("Anomalies")
        for a in summary.get("anomalies", []):
            st.markdown(f"- {a}")
        st.subheader("Clusters")
        st.json(summary.get("clusters", []))
    else:
        st.warning("Please upload and ingest logs first.")

# --- TAB 4: RECOMMENDATIONS ---
with tab4:
    st.header("🛠 Recommendations and RCA")
    if st.session_state["summary"]:
        raw = st.session_state["log_lines"]
        recs = recommendations.generate_recommendations(st.session_state["summary"], raw)
        st.session_state["recommendations"] = recs

        st.subheader("Rule-Based Recommendations")
        for r in recs:
            st.markdown(f"- {r}")

        st.divider()
        st.subheader("GPT-Powered RCA (Optional)")
        if st.text_input("OpenAI API Key", type="password"):
            st.caption("Only needed if using GPT")
        if st.button("Generate RCA"):
            errors = [e.raw for e in st.session_state["events"] if e.severity >= 4]
            metadata = {
                "app_name": st.text_input("App Name", "DemoApp"),
                "build_version": st.text_input("Build Version", "1.0"),
                "test_type": st.text_input("Test Type", "SoftPaq"),
                "project_name": st.text_input("Project Name", "SKC Demo")
            }
            prompt = ai_rca.prepare_prompt(errors, metadata)
            result = ai_rca.fetch_gpt_rca(prompt)
            st.text_area("GPT RCA Output", result, height=250)

# --- TAB 5: REPORT ---
with tab5:
    st.header("📄 Generate Report")
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
            st.download_button("⬇️ Download Text Report", f.read(), file_name="report.txt")
    if os.path.exists("data/report.pdf"):
        with open("data/report.pdf", "rb") as f:
            st.download_button("⬇️ Download PDF Report", f, file_name="report.pdf")
