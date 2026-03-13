from fastapi import APIRouter, Depends
from supabase import Client
from typing import List

from app.models.schemas.expense_schema import ExpenseCreate, ExpenseUpdateAmount, ExpenseResponse
from app.services.expense_service import ExpenseService
from app.db.database import get_supabase_client
from app.core.security import get_current_user_id

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.post("/")
def create_expense(
    data: ExpenseCreate,
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = ExpenseService(supabase)
    return service.create_expense(user_id, data)


@router.get("/", response_model=List[ExpenseResponse])
def get_expenses(
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = ExpenseService(supabase)
    return service.get_expenses(user_id)


@router.patch("/{expense_id}")
def update_expense_amount(
    expense_id: str,
    data: ExpenseUpdateAmount,
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = ExpenseService(supabase)
    return service.update_expense_amount(user_id, expense_id, data.amount)