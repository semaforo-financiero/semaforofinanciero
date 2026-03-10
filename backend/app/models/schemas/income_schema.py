from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional


class CreateIncomeRequest(BaseModel):
    income_source_id: UUID
    amount: float = Field(..., ge=0)
    year: int = Field(..., ge=2000)
    month: int = Field(..., ge=1, le=12)

class UpdateIncomeRequest(BaseModel):
    amount: Optional[float] = Field(None, ge=0)