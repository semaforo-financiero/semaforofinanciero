from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ExpenseSourceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    stability: str = Field(pattern="^(FIXED|VARIABLE)$")
    is_debt: bool = False
    description: Optional[str] = Field(default=None, max_length=255)


class ExpenseSourceResponse(BaseModel):
    id: str
    user_id: str
    name: str
    stability: str
    is_debt: bool
    description: Optional[str]
    is_active: bool
    created_at: datetime