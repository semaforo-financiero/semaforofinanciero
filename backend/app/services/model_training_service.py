from __future__ import annotations

from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from supabase import Client

from app.services.dataset_service import DatasetService


class ModelTrainingService:
    MODEL_OUTPUT_PATH = "app/core/model_store/risk_pipeline.joblib"

    def __init__(self, supabase: Client):
        self.dataset_service = DatasetService(supabase)

    def train_and_save_model(self) -> dict:
        df = self.dataset_service.build_dataframe()

        if df.empty:
            raise ValueError("El dataset está vacío.")

        target_col = "risk_label"

        X = df.drop(columns=[target_col])
        y = df[target_col]

        numeric_features = [
            "income",
            "expense",
            "savings",
            "expense_ratio",
            "debt_expense_amount",
            "debt_ratio",
            "fixed_expense_amount",
            "fixed_expense_ratio",
            "variable_expense_amount",
            "variable_expense_ratio",
            "savings_ratio",
            "months_analyzed",
            "variable_income_sources_ratio",
            "years_working",
        ]

        categorical_features = [
            "employment_status",
        ]

        numeric_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )

        categorical_transformer = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("onehot", OneHotEncoder(handle_unknown="ignore")),
            ]
        )

        preprocessor = ColumnTransformer(
            transformers=[
                ("num", numeric_transformer, numeric_features),
                ("cat", categorical_transformer, categorical_features),
            ]
        )

        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            random_state=42,
            class_weight="balanced",
        )

        pipeline = Pipeline(
            steps=[
                ("preprocessor", preprocessor),
                ("model", model),
            ]
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y,
        )

        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        report = classification_report(y_test, y_pred, output_dict=True)

        Path(self.MODEL_OUTPUT_PATH).parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(pipeline, self.MODEL_OUTPUT_PATH)

        return {
            "message": "Modelo entrenado y guardado correctamente.",
            "model_path": self.MODEL_OUTPUT_PATH,
            "samples": len(df),
            "classes": sorted(df[target_col].astype(str).unique().tolist()),
            "metrics": report,
        }