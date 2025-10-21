from typing import Dict, Any
import pandas as pd
from .data_retrieval import DataRetrievalAgent
from .explainability import ExplainabilityAgent
from .visualization import VisualizationAgent
from .llm_client import LLMClient

class Orchestrator:
    """
    Coordinates agent calls and composes an LLM narrative.
    """
    def __init__(self):
        self.retriever = DataRetrievalAgent()
        self.explainer = ExplainabilityAgent()
        self.viz = VisualizationAgent()
        self.llm = LLMClient()

    def run_pipeline(self, params: Dict[str, Any]) -> Dict[str, Any]:
        # Step 1: Data retrieval and anomaly check
        data_bundle = self.retriever.run(params)
        df = pd.DataFrame(data_bundle["data_sample"])

        # Step 2: Explainability over the same sample (or a larger pull in real life)
        exp = self.explainer.run(df)

        # Step 3: Visualization payloads
        chart_payloads = []
        numeric_cols = data_bundle.get("numeric_cols", [])
        if len(numeric_cols) >= 2:
            chart_payloads.append(self.viz.bar(df, cat_col=df.columns[0], val_col=numeric_cols[0]))
        if len(numeric_cols) >= 1 and "date" in [c.lower() for c in df.columns]:
            # try to find 'date' column
            date_col = [c for c in df.columns if c.lower() == "date"][0]
            chart_payloads.append(self.viz.timeseries(df, x_col=date_col, y_col=numeric_cols[0]))

        # Step 4: Narrative via LLM
        system = "You are an analytics copilot. Summarize findings for executives clearly and concisely."
        user_msg = (
            f"Columns: {data_bundle['columns']}\n"
            f"Anomalies found: {len(data_bundle['anomalies'])}\n"
            f"Top features by SHAP: {exp['feature_importance'][:5]}"
        )
        narrative = self.llm.generate(system, [{"role": "user", "content": user_msg}])

        return {
            "narrative": narrative,
            "anomalies": data_bundle["anomalies"],
            "feature_importance": exp["feature_importance"],
            "training_metrics": exp["training_metrics"],
            "charts": chart_payloads,
            "columns": data_bundle["columns"],
            "sample": data_bundle["data_sample"],
        }
