import pandas as pd
from typing import Dict, Any
from ..services.bigquery_client import BigQueryClient
from ..utils.logger import logger

class DataRetrievalAgent:
    """
    Pulls data from BigQuery (or CSV fallback) and does lightweight EDA/anomaly flags.
    """
    def __init__(self):
        self.bq = BigQueryClient()

    def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # Example: accept optional SQL override
        sql = params.get("sql")
        limit = int(params.get("limit", 1000))
        df = self.bq.query(sql=sql, limit=limit)

        # Lightweight anomaly heuristic: z-score on a numeric column if present
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        anomalies = []
        if numeric_cols:
            target = numeric_cols[0]
            series = df[target]
            z = (series - series.mean()) / (series.std(ddof=0) + 1e-9)
            idx = z.abs() > 3
            anomalies = df[idx].head(50).to_dict(orient="records")
            logger.info(f"Found {len(anomalies)} potential anomalies on {target} (|z|>3).")

        return {
            "data_sample": df.head(25).to_dict(orient="records"),
            "columns": df.columns.tolist(),
            "anomalies": anomalies,
            "numeric_cols": numeric_cols,
        }
