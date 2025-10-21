# Agentic Insights Engine (Enterprise Analytics Copilot)

A multi-agent analytics system where autonomous agents — **DataRetrieval**, **Explainability**, and **Visualization** — collaborate to generate insights, detect anomalies, and surface business recommendations from enterprise data.

---

## Overview

This project demonstrates how specialized AI agents can work together to perform end-to-end analytics: querying data, generating explanations, and visualizing insights autonomously.  
It includes a FastAPI backend, a Streamlit dashboard for analysts, and a React (Vite) frontend for executives.

---

## Tech Stack

| Layer | Technology |
|:------|:------------|
| **Backend API** | FastAPI |
| **Agents & LLM** | LangChain + Gemini (Vertex AI) via pluggable client (fallback: local LLM stub) |
| **Data Layer** | BigQuery (CSV/SQLite fallback for local development) |
| **Explainability** | SHAP (demonstrated with XGBoost) |
| **Dashboards** | Streamlit (Analyst Console) |
| **Frontend** | React (Vite-powered Executive Dashboard) |

## Project Layout
```
agentic-insights-engine/
├── backend/ # Core FastAPI backend & agents
│ ├── app.py # FastAPI entrypoint (API routes)
│ ├── agents/ # Autonomous multi-agent system
│ │ ├── init.py
│ │ ├── orchestrator.py # Coordinates Data, Explainability & Viz agents
│ │ ├── data_retrieval.py # Pulls data from BigQuery / CSV fallback
│ │ ├── explainability.py # SHAP-based model interpretation
│ │ ├── visualization.py # Prepares chart-friendly payloads
│ │ └── llm_client.py # Gemini / Vertex AI integration (or stub)
│ ├── services/ # External integrations
│ │ ├── bigquery_client.py # Query abstraction for BigQuery
│ │ └── model_store.py # Lightweight in-memory model registry
│ ├── models/
│ │ └── forecast_model.py # Example XGBoost model for demo forecasting
│ ├── utils/
│ │ ├── config.py # Configuration and environment management
│ │ └── logger.py # Centralized logging setup
│ └── data/
│ └── sample_data.csv # Local dev dataset fallback
│
├── streamlit_dashboard/ # Analyst-facing Streamlit app
│ └── app.py # UI to trigger orchestrator & display insights
│
├── frontend/ # React/Vite executive dashboard
│ ├── index.html
│ ├── package.json
│ ├── vite.config.js
│ └── src/
│ ├── main.jsx
│ ├── App.jsx
│ ├── api.js
│ └── components/
│ ├── InsightCard.jsx
│ └── Chart.jsx
│
├── requirements.txt # Python dependencies
└── .env.example # Environment variable template
```

## Quickstart (Development)

### 1. Setup Environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
(Optional) configure environment variables such as:
GOOGLE_APPLICATION_CREDENTIALS, PROJECT_ID, DATASET_ID, TABLE_ID, GEMINI_MODEL, etc.
```
2. Run Backend
```bash
uvicorn backend.app:app --reload --port 8000
```
3. Run Streamlit Dashboard
```bash
streamlit run streamlit_dashboard/app.py
```
4. Run Frontend (React/Vite)
```bash
cd frontend
npm install
npm run dev
```

##Local URLs
Service	| URL
API Docs (FastAPI) | http://localhost:8000/docs
Streamlit Dashboard | http://localhost:8501
React Dashboard | http://localhost:5173

Notes
- BigQuery Fallback: If credentials are missing, the system uses backend/data/sample_data.csv.
- LLM Integration: Uses Gemini (Vertex AI) if configured; otherwise falls back to a local template LLM stub.
- Explainability: SHAP demo uses an in-memory XGBoost model trained on the sample dataset.

#.env.example
```
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
```