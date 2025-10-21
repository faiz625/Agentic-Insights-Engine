from typing import Dict, Any, List
import pandas as pd

class VisualizationAgent:
    """
    Prepares chart-friendly payloads (time series, bar charts) from a DataFrame.
    """
    def timeseries(self, df: pd.DataFrame, x_col: str, y_col: str) -> Dict[str, Any]:
        # Ensure types
        if x_col in df.columns:
            try:
                df = df.copy()
                df[x_col] = pd.to_datetime(df[x_col], errors="coerce")
                df = df.dropna(subset=[x_col])
                df = df.sort_values(x_col)
            except Exception:
                pass
        data = [{"x": str(row[x_col]), "y": float(row[y_col])} for _, row in df[[x_col, y_col]].dropna().iterrows()]
        return {"type": "timeseries", "series": data, "x": x_col, "y": y_col}

    def bar(self, df: pd.DataFrame, cat_col: str, val_col: str, top_k: int = 12) -> Dict[str, Any]:
        grouped = df.groupby(cat_col)[val_col].mean().nlargest(top_k).reset_index()
        data = [{"label": str(r[cat_col]), "value": float(r[val_col])} for _, r in grouped.iterrows()]
        return {"type": "bar", "series": data, "x": cat_col, "y": val_col}
