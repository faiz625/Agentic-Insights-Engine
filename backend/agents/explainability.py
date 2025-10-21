from typing import Dict, Any
import pandas as pd
import shap
from ..models.forecast_model import ForecastModel

class ExplainabilityAgent:
    """
    Trains a simple model (or reuses one) and returns SHAP values and feature importances.
    """
    def __init__(self):
        self.model = ForecastModel()

    def run(self, df: pd.DataFrame) -> Dict[str, Any]:
        metrics = self.model.fit(df)
        # Use TreeExplainer for XGBoost
        explainer = shap.TreeExplainer(self.model.model)
        # Limit size for performance
        sample = df.select_dtypes(include="number").head(200)
        if "y" not in sample.columns:
            sample = sample.copy()
            sample["y"] = sample.iloc[:, 0] * 0.5 + sample.iloc[:, 1 % sample.shape[1]] * 0.25
        shap_values = explainer.shap_values(sample.drop(columns=["y"]))

        # mean |SHAP| importances
        importances = dict(zip(
            self.model.feature_names,
            [float(abs(shap_values[:, i]).mean()) for i in range(len(self.model.feature_names))]
        ))
        ranked = sorted(importances.items(), key=lambda x: x[1], reverse=True)

        return {
            "training_metrics": metrics,
            "feature_importance": ranked[:10],
            "shap_values_preview": [list(map(float, row[:10])) for row in shap_values[:10]],
            "feature_names": self.model.feature_names,
        }
