import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Agentic Insights Engine", layout="wide")
st.title("📊 Agentic Insights Engine — Analyst Console")

api_base = st.secrets.get("API_BASE", "http://localhost:8000")

with st.sidebar:
    st.header("Run Parameters")
    sql = st.text_area("Optional SQL (BigQuery)", height=120, placeholder="SELECT * FROM `project.dataset.table` LIMIT 1000")
    limit = st.number_input("Limit", min_value=10, max_value=5000, value=1000, step=10)
    run_btn = st.button("Run Orchestrator", use_container_width=True)

if run_btn:
    with st.spinner("Running multi-agent pipeline..."):
        resp = requests.post(f"{api_base}/run", json={"sql": sql or None, "limit": limit})
        data = resp.json()

    st.subheader("Narrative Summary")
    st.write(data["narrative"])

    st.subheader("Training Metrics")
    st.json(data["training_metrics"])

    st.subheader("Top Features (mean |SHAP|)")
    st.table(pd.DataFrame(data["feature_importance"], columns=["feature", "importance"]))

    st.subheader("Anomalies (preview)")
    st.dataframe(pd.DataFrame(data["anomalies"]))

    st.subheader("Sample (preview)")
    st.dataframe(pd.DataFrame(data["sample"]))

    st.subheader("Charts (payloads sent to React)")
    st.json(data["charts"])
else:
    st.info("Configure parameters in the left sidebar and click **Run Orchestrator**.")
