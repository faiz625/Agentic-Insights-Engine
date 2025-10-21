import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Agentic Insights Engine", layout="wide")
st.title("📊 Agentic Insights Engine — Analyst Console")

# Point to your FastAPI
api_base = st.secrets.get("API_BASE", "http://127.0.0.1:8000")

# ---------- helpers ----------
@st.cache_data(ttl=15)
def api_health(base: str) -> tuple[bool, str]:
    try:
        r = requests.get(f"{base}/health", timeout=10)
        if r.status_code == 200 and r.headers.get("content-type", "").startswith("application/json"):
            return True, "ok"
        return False, f"HTTP {r.status_code}: {r.text[:200]}"
    except Exception as e:
        return False, str(e)

def call_orchestrator(base: str, sql: str | None, limit: int):
    try:
        resp = requests.post(
            f"{base}/run",
            json={"sql": sql or None, "limit": int(limit)},
            timeout=60,
        )
    except Exception as e:
        st.error(f"❌ Could not reach API at {base}\n\n{e}")
        return None

    ct = resp.headers.get("content-type", "")
    if resp.status_code != 200:
        st.error(f"❌ API returned {resp.status_code}\n\nBody:\n{resp.text[:1200]}")
        return None
    if "application/json" not in ct:
        st.error(f"❌ API did not return JSON (Content-Type: {ct})\n\nBody:\n{resp.text[:1200]}")
        return None

    try:
        return resp.json()
    except Exception as e:
        st.error(f"❌ Failed to parse JSON\n\n{e}\n\nRaw body:\n{resp.text[:1200]}")
        return None
# -----------------------------

# Connection badge
ok, msg = api_health(api_base)
st.caption(f"API: {api_base} — {'✅ healthy' if ok else '❌ unreachable'}{'' if ok else ' — ' + msg}")

with st.sidebar:
    st.header("Run Parameters")
    sql = st.text_area(
        "Optional SQL (BigQuery)",
        height=120,
        placeholder="SELECT * FROM `project.dataset.table` LIMIT 1000"
    )
    limit = st.number_input("Limit", min_value=10, max_value=5000, value=1000, step=10)
    run_btn = st.button("Run Orchestrator", use_container_width=True, disabled=not ok)

if run_btn:
    with st.spinner("Running multi-agent pipeline..."):
        data = call_orchestrator(api_base, sql, limit)

    if not data:
        st.stop()

    st.subheader("Narrative Summary")
    st.write(data.get("narrative", ""))

    st.subheader("Training Metrics")
    st.json(data.get("training_metrics", {}))

    st.subheader("Top Features (mean |SHAP|)")
    feat = data.get("feature_importance", [])
    st.table(pd.DataFrame(feat, columns=["feature", "importance"]))

    st.subheader("Anomalies (preview)")
    st.dataframe(pd.DataFrame(data.get("anomalies", [])))

    st.subheader("Sample (preview)")
    st.dataframe(pd.DataFrame(data.get("sample", [])))

    st.subheader("Charts (payloads sent to React)")
    st.json(data.get("charts", []))
else:
    st.info("Configure parameters in the left sidebar and click **Run Orchestrator**.")
