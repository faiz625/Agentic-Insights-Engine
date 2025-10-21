import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))

    USE_BIGQUERY = os.getenv("USE_BIGQUERY", "false").lower() == "true"
    USE_VERTEX_GEMINI = os.getenv("USE_VERTEX_GEMINI", "false").lower() == "true"

    # BigQuery
    PROJECT_ID = os.getenv("PROJECT_ID")
    DATASET_ID = os.getenv("DATASET_ID")
    TABLE_ID = os.getenv("TABLE_ID")

    # LLM
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
    VERTEX_LOCATION = os.getenv("VERTEX_LOCATION", "us-central1")
    VERTEX_PROJECT_ID = os.getenv("VERTEX_PROJECT_ID")

    DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sample_data.csv")
