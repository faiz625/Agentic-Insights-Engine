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
aagentic-insights-engine/
├── backend/                              # Core FastAPI backend & agents
│   ├── app.py                            # FastAPI entrypoint (API routes)
│   ├── agents/                           # Autonomous multi-agent system
│   │   ├── __init__.py
│   │   ├── orchestrator.py               # Coordinates Data, Explainability & Viz agents
│   │   ├── data_retrieval.py             # Pulls data from BigQuery / CSV fallback
│   │   ├── explainability.py             # SHAP-based model interpretation
│   │   ├── visualization.py              # Prepares chart-friendly payloads
│   │   └── llm_client.py                 # Gemini / Vertex AI integration (or stub)
│   ├── services/                         # External integrations
│   │   ├── bigquery_client.py            # Query abstraction for BigQuery
│   │   └── model_store.py                # Lightweight in-memory model registry
│   ├── models/
│   │   └── forecast_model.py             # Example XGBoost model for demo forecasting
│   ├── utils/                            # Shared configs and logging
│   │   ├── config.py
│   │   └── logger.py
│   └── data/
│       └── sample_data.csv               # Local dev dataset fallback
│
├── streamlit_dashboard/                  # Analyst-facing Streamlit app
│   └── app.py                            # UI to trigger orchestrator + display insights
│
├── frontend/                             # React/Vite executive dashboard
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── main.jsx
│       ├── App.jsx
│       ├── api.js
│       └── components/
│           ├── InsightCard.jsx
│           └── Chart.jsx
│
├── requirements.txt                      # Python dependencies
└── .env.example                          # Environment variable template



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