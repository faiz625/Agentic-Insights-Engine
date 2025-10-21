# Agentic Insights Engine (Enterprise Analytics Copilot)

Multi-agent analytics engine where autonomous agents (DataRetrieval, Explainability, Visualization) collaborate to generate insights, detect anomalies, and surface recommendations from enterprise data.

## Stack
- **Backend API:** FastAPI
- **Agents & LLM:** LangChain + Gemini (Vertex AI) via pluggable client (falls back to local LLM stub)
- **Data:** BigQuery (with local CSV/SQLite fallback for dev)
- **Explainability:** SHAP (example with XGBoost)
- **Dashboards:** Streamlit (analyst console)
- **Frontend:** React (Vite) exec dashboard

## Project Layout
agentic-insights-engine/
backend/
    app.py
    agents/
        init.py
        orchestrator.py
        data_retrieval.py
        explainability.py
        visualization.py
        llm_client.py
    services/
        bigquery_client.py
        model_store.py
    models/
        forecast_model.py
    utils/
        config.py
        logger.py
    data/
        sample_data.csv
streamlit_dashboard/
    app.py
frontend/
    index.html
    package.json
    vite.config.js
    src/
        main.jsx
        App.jsx
        api.js
        components/
            InsightCard.jsx
            Chart.jsx
requirements.txt
.env.example


## Quickstart (Dev)
1) Create venv and install deps:
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# (optional) set GOOGLE_APPLICATION_CREDENTIALS, PROJECT_ID, DATASET_ID, TABLE_ID, GEMINI_MODEL etc.


uvicorn backend.app:app --reload --port 8000


streamlit run streamlit_dashboard/app.py


cd frontend
npm install
npm run dev


Open:

API: http://localhost:8000/docs

Streamlit: http://localhost:8501

React: http://localhost:5173

Notes

If BigQuery creds are missing, the engine uses backend/data/sample_data.csv.

LLM client uses Gemini if configured; otherwise uses a local template stub.

SHAP demo uses an in-memory XGBoost model fitted on the sample dataset to illustrate explainability.

---

# 2) `.env.example`
```bash
# ==== BigQuery ====
PROJECT_ID=your-gcp-project
DATASET_ID=your_dataset
TABLE_ID=your_table
# GOOGLE_APPLICATION_CREDENTIALS=/absolute/path/to/sa.json  # optional if using default creds

# ==== LLM (Gemini) ====
GEMINI_MODEL=gemini-1.5-pro
VERTEX_LOCATION=us-central1
VERTEX_PROJECT_ID=your-gcp-project

# ==== Backend ====
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO

# ==== Feature Flags ====
USE_BIGQUERY=false
USE_VERTEX_GEMINI=false