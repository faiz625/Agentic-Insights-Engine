from typing import Dict, Any
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import xgboost as xgb

class ForecastModel:
    """
    A simple supervised regressor for demo purposes.
    Expects a numeric target 'y' with numeric features.
    """
    def __init__(self):
        self.model = xgb.XGBRegressor(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            subsample=0.9,
            colsample_bytree=0.9,
            random_state=42,
        )
        self.fitted = False
        self.feature_names = []

    def fit(self, df: pd.DataFrame) -> Dict[str, Any]:
        numeric = df.select_dtypes(include="number")
        if "y" not in numeric.columns:
            # Create a synthetic target for demo if needed
            numeric = numeric.copy()
            numeric["y"] = numeric.iloc[:, 0] * 0.5 + numeric.iloc[:, 1 % numeric.shape[1]] * 0.25

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
