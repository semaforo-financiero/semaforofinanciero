from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class RiskRuleResponse(BaseModel):
    code: str
    severity: str
    score: int
    message: str
    recommendation: str


class RiskIndicatorsResponse(BaseModel):
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


class DataMiningResponse(BaseModel):
    model_name: str
    predicted_risk: str
    confidence: float = Field(ge=0, le=1)
    anomaly_score: Optional[float] = None
    cluster: Optional[int] = None


class RiskResponse(BaseModel):
    risk: str
    score: int = Field(ge=0)
    rules: list[RiskRuleResponse]
    recommendations: list[str]
    indicators: RiskIndicatorsResponse
    data_mining: Optional[DataMiningResponse] = None


class FamilyRiskResponse(RiskResponse):
    family_id: str
    family_name: str
    member_count: int = Field(ge=0)




