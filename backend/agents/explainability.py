from typing import Dict, Any
import numpy as np
import pandas as pd
from ..models.forecast_model import ForecastModel
from ..utils.config import Config
from ..utils.logger import logger

class ExplainabilityAgent:
    """
    Trains a simple model and returns explainability. Tries SHAP TreeExplainer first,
    then general SHAP, then a sklearn permutation-importance fallback to avoid crashes.
    """
    def __init__(self):
        self.model = ForecastModel()

    def _prep_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        num = df.select_dtypes(include="number").copy()
        if "y" not in num.columns:
            # Synthesize a simple target for demo
            cols = num.columns.tolist()
            if not cols:
                raise ValueError("No numeric columns available for training.")
            a = num[cols[0]]
            b = num[cols[1]] if len(cols) > 1 else a
            num["y"] = 0.5 * a + 0.25 * b
        return num

    def run(self, df: pd.DataFrame) -> Dict[str, Any]:
        num = self._prep_numeric(df)
        metrics = self.model.fit(num)

        X = num.drop(columns=["y"])
        feature_names = list(X.columns)
        out: Dict[str, Any] = {
            "training_metrics": metrics,
            "feature_importance": [],
            "feature_names": feature_names,
            "explain_method": None,
            "notes": [],
        }

        # If the user asked to keep it safe, skip SHAP entirely
        if Config.SAFE_EXPLAIN:
            try:
                from sklearn.inspection import permutation_importance
                importances = permutation_importance(self.model.model, X, num["y"], n_repeats=5, random_state=42)
                ranked = sorted(zip(feature_names, importances.importances_mean.astype(float)), key=lambda x: x[1], reverse=True)
                out["feature_importance"] = ranked[:10]
                out["explain_method"] = "permutation_fallback (SAFE_EXPLAIN=true)"
                return out
            except Exception as e:
                logger.exception(e)
                out["notes"].append("Permutation importance failed.")
                out["explain_method"] = "none"
                return out

        # Try SHAP TreeExplainer (fastest for XGBoost) — can crash on some Windows setups
        try:
            import shap  # import inside try to avoid crashing module import
            explainer = shap.TreeExplainer(self.model.model)
            sample_X = X.head(min(len(X), 200))
            shap_values = explainer.shap_values(sample_X)
            importances = np.abs(shap_values).mean(axis=0).tolist()
            ranked = sorted(zip(feature_names, map(float, importances)), key=lambda x: x[1], reverse=True)
            out["feature_importance"] = ranked[:10]
            out["shap_values_preview"] = [list(map(float, row[:10])) for row in shap_values[:10]]
            out["explain_method"] = "shap_treeexplainer"
            return out
        except Exception as e1:
            logger.warning(f"TreeExplainer failed, trying generic SHAP. Reason: {e1}")

        # Try generic SHAP Explainer
        try:
            import shap
            sample_X = X.head(min(len(X), 200))
            explainer = shap.Explainer(self.model.model, sample_X)
            sv = explainer(sample_X)
            if hasattr(sv, "values") and sv.values is not None:
                importances = np.abs(sv.values).mean(axis=0).tolist()
            else:
                # some SHAP versions return .values None, fall back to base values diffs
                vals = np.array(sv)  # __array__ fallback
                importances = np.abs(vals).mean(axis=0).tolist()
            ranked = sorted(zip(feature_names, map(float, importances)), key=lambda x: x[1], reverse=True)
            out["feature_importance"] = ranked[:10]
            out["shap_values_preview"] = [list(map(float, row[:10])) for row in np.array(sv)[:10]]
            out["explain_method"] = "shap_explainer_generic"
            return out
        except Exception as e2:
            logger.warning(f"Generic SHAP failed, falling back to permutation importance. Reason: {e2}")

        # Final fallback — permutation importance (pure sklearn, very stable)
        try:
            from sklearn.inspection import permutation_importance
            importances = permutation_importance(self.model.model, X, num["y"], n_repeats=5, random_state=42)
            ranked = sorted(zip(feature_names, importances.importances_mean.astype(float)), key=lambda x: x[1], reverse=True)
            out["feature_importance"] = ranked[:10]
            out["explain_method"] = "permutation_fallback"
            return out
        except Exception as e3:
            logger.exception(e3)
            out["notes"].append("All explainability methods failed.")
            out["explain_method"] = "none"
            return out