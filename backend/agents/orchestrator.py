from typing import Dict, Any
import pandas as pd
from .data_retrieval import DataRetrievalAgent
from .explainability import ExplainabilityAgent
from .visualization import VisualizationAgent
from .llm_client import LLMClient
from ..utils.logger import logger

class Orchestrator:
    def __init__(self):
        self.retriever = DataRetrievalAgent()
        self.explainer = ExplainabilityAgent()
        self.viz = VisualizationAgent()
        self.llm = LLMClient()

    def run_pipeline(self, params: Dict[str, Any]) -> Dict[str, Any]:
        data_bundle = self.retriever.run(params)
        df = pd.DataFrame(data_bundle["data_sample"])

        # Explainability (robust)
        try:
            exp = self.explainer.run(df)
        except Exception as e:
            logger.exception(e)
            exp = {
                "training_metrics": {},
                "feature_importance": [],
                "feature_names": [],
                "explain_method": "error",
                "notes": ["Explainability step crashed; continuing without it."]
            }

        # Viz payloads
        chart_payloads = []
        numeric_cols = data_bundle.get("numeric_cols", [])
        if len(numeric_cols) >= 2:
            chart_payloads.append(self.viz.bar(df, cat_col=df.columns[0], val_col=numeric_cols[0]))
        if len(numeric_cols) >= 1 and "date" in [c.lower() for c in df.columns]:
            date_col = [c for c in df.columns if c.lower() == "date"][0]
            chart_payloads.append(self.viz.timeseries(df, x_col=date_col, y_col=numeric_cols[0]))

        system = "You are an analytics copilot. Summarize findings for executives clearly and concisely."
        user_msg = (
            f"Columns: {data_bundle['columns']}\n"
            f"Anomalies found: {len(data_bundle['anomalies'])}\n"
            f"Top features (if available): {exp.get('feature_importance', [])[:5]}\n"
            f"Explain method: {exp.get('explain_method')}"
        )
        narrative = self.llm.generate(system, [{"role": "user", "content": user_msg}])

        return {
            "narrative": narrative,
            "anomalies": data_bundle["anomalies"],
            "feature_importance": exp.get("feature_importance", []),
            "training_metrics": exp.get("training_metrics", {}),
            "charts": chart_payloads,
            "columns": data_bundle["columns"],
            "sample": data_bundle["data_sample"],
            "explain_method": exp.get("explain_method"),
            "notes": exp.get("notes", []),
        }
