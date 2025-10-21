from typing import Dict, Any
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import xgboost as xgb

class ForecastModel:
    """
    Simple XGBoost regressor for demo. Tuned lighter to reduce Windows binary hiccups.
    """
    def __init__(self):
        self.model = xgb.XGBRegressor(
            n_estimators=120,
            max_depth=4,
            learning_rate=0.1,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=42,
            tree_method="hist",           # safer CPU path
            enable_categorical=False
        )
        self.fitted = False
        self.feature_names: list[str] = []

    def fit(self, df: pd.DataFrame) -> Dict[str, Any]:
        numeric = df.select_dtypes(include="number").copy()
        if "y" not in numeric.columns:
            cols = numeric.columns.tolist()
            a = numeric[cols[0]]
            b = numeric[cols[1]] if len(cols) > 1 else a
            numeric["y"] = 0.5 * a + 0.25 * b

        X = numeric.drop(columns=["y"])
        y = numeric["y"]
        self.feature_names = X.columns.tolist()

        Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(Xtr, ytr)
        self.fitted = True
        pred = self.model.predict(Xte)
        mae = float(mean_absolute_error(yte, pred))
        return {"mae": mae, "n_train": len(Xtr), "n_test": len(Xte)}

    def predict(self, X: pd.DataFrame):
        if not self.fitted:
            raise RuntimeError("Model not fitted")
        return self.model.predict(X[self.feature_names])
