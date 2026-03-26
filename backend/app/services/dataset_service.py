from __future__ import annotations

from pathlib import Path

import pandas as pd
from supabase import Client

from app.repositories.financial_snapshot_repository import FinancialSnapshotRepository


class DatasetService:
    def __init__(self, supabase: Client):
        self.snapshot_repository = FinancialSnapshotRepository(supabase)

    def build_dataframe(self) -> pd.DataFrame:
        res = self.snapshot_repository.get_all_snapshots()
        rows = res.data or []

        if not rows:
            raise ValueError("No hay snapshots suficientes para construir el dataset.")

        df = pd.DataFrame(rows)

        if "expert_risk" not in df.columns:
            raise ValueError("No existe la columna 'expert_risk' en los snapshots.")

        df["risk_label"] = df["expert_risk"]

        keep_columns = [
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
            "employment_status",
            "years_working",
            "risk_label",
            "income_variability",
            "deficit_ratio",
            "expense_trend",

        ]

        return df[keep_columns].copy()

    def export_to_csv(self, output_path: str = "app/core/model_store/risk_dataset.csv") -> str:
        df = self.build_dataframe()
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        return output_path