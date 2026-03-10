from fastapi import APIRouter, Depends
from supabase import Client
from typing import List

from app.models.schemas.expense_source_schema import ExpenseSourceCreate
from app.models.schemas.expense_source_schema import ExpenseSourceResponse
from app.services.expense_source_service import ExpenseSourceService
from app.db.database import get_supabase_client
from app.core.security import get_current_user_id

router = APIRouter(prefix="/expense-sources", tags=["expense-sources"])


@router.post("/")
def create_expense_source(
    data: ExpenseSourceCreate,
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = ExpenseSourceService(supabase)
    return service.create_expense_source(user_id, data)


@router.get("/", response_model=List[ExpenseSourceResponse])
def get_expense_sources(
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = ExpenseSourceService(supabase)
    return service.get_expense_sources(user_id)


@router.delete("/{expense_source_id}")
def delete_expense_source(
    expense_source_id: str,
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = ExpenseSourceService(supabase)
    return service.delete_expense_source(user_id, expense_source_id)