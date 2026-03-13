from pydantic import BaseModel, Field
from datetime import datetime


class ExpenseCreate(BaseModel):
    expense_source_id: str
    amount: float = Field(gt=0)
    year: int = Field(gt=2000)
    month: int = Field(ge=1, le=12)


class ExpenseUpdateAmount(BaseModel):
    amount: float = Field(gt=0)


class ExpenseResponse(BaseModel):
    id: str
    expense_source_id: str
    amount: float
    year: int
    month: int
    created_at: datetime