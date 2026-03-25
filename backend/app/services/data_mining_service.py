from __future__ import annotations

from pathlib import Path
from typing import Optional

import joblib
import pandas as pd


class DataMiningService:
    def __init__(self) -> None:
        self.pipeline_path = Path("app/core/model_store/risk_pipeline.joblib")
        self.pipeline = joblib.load(self.pipeline_path) if self.pipeline_path.exists() else None

    def is_available(self) -> bool:
        return self.pipeline is not None

    def _build_feature_dataframe(self, profile: dict) -> pd.DataFrame:
        row = {
            "income": profile["income"],
            "expense": profile["expense"],
            "savings": profile["savings"],
            "expense_ratio": profile["expense_ratio"],
            "debt_expense_amount": profile["debt_expense_amount"],
            "debt_ratio": profile["debt_ratio"],
            "fixed_expense_amount": profile["fixed_expense_amount"],
            "fixed_expense_ratio": profile["fixed_expense_ratio"],
            "variable_expense_amount": profile["variable_expense_amount"],
            "variable_expense_ratio": profile["variable_expense_ratio"],
            "savings_ratio": profile["savings_ratio"],
            "months_analyzed": profile["months_analyzed"],
            "variable_income_sources_ratio": profile["variable_income_sources_ratio"],
            "employment_status": profile["employment_status"],
            "years_working": profile["years_working"],
        }
        return pd.DataFrame([row])

    def predict_risk(self, profile: dict) -> Optional[dict]:
        if not self.is_available():
            return None

        X = self._build_feature_dataframe(profile)
        prediction = self.pipeline.predict(X)[0]

        confidence = 0.70
        model = self.pipeline.named_steps.get("model")
        preprocessor = self.pipeline.named_steps.get("preprocessor")

        if model is not None and preprocessor is not None and hasattr(model, "predict_proba"):
            X_transformed = preprocessor.transform(X)
            proba = model.predict_proba(X_transformed)[0]
            confidence = float(max(proba))

        return {
            "model_name": type(model).__name__ if model is not None else "UnknownModel",
            "predicted_risk": str(prediction).upper(),
            "confidence": round(confidence, 4),
        }