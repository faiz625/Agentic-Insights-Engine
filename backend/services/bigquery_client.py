from typing import Optional
import pandas as pd
from ..utils.config import Config
from ..utils.logger import logger

try:
    from google.cloud import bigquery
except Exception:
    bigquery = None

class BigQueryClient:
    def __init__(self):
        self.use_bq = Config.USE_BIGQUERY and bigquery is not None
        if self.use_bq:
            self.client = bigquery.Client(project=Config.PROJECT_ID)
            logger.info("BigQuery client initialized.")
        else:
            self.client = None
            logger.warning("BigQuery disabled or not available. Using CSV fallback.")

    def query(self, sql: Optional[str] = None, limit: int = 1000) -> pd.DataFrame:
        if self.use_bq and sql:
            logger.info("Executing BigQuery SQL")
            return self.client.query(sql).to_dataframe()
        # Fallback: read local CSV sample
        logger.info("Returning sample data from CSV.")
        df = pd.read_csv(Config.DATA_PATH)
        if limit:
            df = df.head(limit)
        return df

    def simple_select(self, limit: int = 1000) -> pd.DataFrame:
        if self.use_bq:
            table = f"`{Config.PROJECT_ID}.{Config.DATASET_ID}.{Config.TABLE_ID}`"
            sql = f"SELECT * FROM {table} LIMIT {limit}"
            return self.query(sql)
        return self.query(limit=limit)
