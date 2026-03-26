from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class FinancialSnapshotCreate(BaseModel):
    user_id: Optional[str] = None
    family_id: Optional[str] = None
    analysis_scope: str

    income: float
    expense: float
    savings: float
    expense_ratio: float
    debt_expense_amount: float
    debt_ratio: float
    fixed_expense_amount: float
    fixed_expense_ratio: float
    variable_expense_amount: float
    variable_expense_ratio: float
    savings_ratio: float
    months_analyzed: int
    variable_income_sources_ratio: float
    employment_status: str
    years_working: Optional[int] = None
    income_variability: float
    deficit_ratio: float
    expense_trend: float

    expert_risk: str
    expert_score: int