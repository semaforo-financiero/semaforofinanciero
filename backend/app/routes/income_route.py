from fastapi import APIRouter, Depends
from supabase import Client
from app.db.database import get_supabase_client
from app.core.security import get_current_user_id
from app.models.schemas.income_schema import CreateIncomeRequest
from app.models.schemas.income_schema import UpdateIncomeRequest
from app.services.income_service import IncomeService

router = APIRouter(prefix="/income", tags=["income"])

@router.post("/")
def create_income(
    data: CreateIncomeRequest,
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = IncomeService(supabase)
    return service.create_income(user_id, data)

@router.get("/")
def get_incomes(
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = IncomeService(supabase)
    return service.get_user_incomes(user_id)

@router.patch("/{income_id}")
def update_income(
    income_id: str,
    data: UpdateIncomeRequest,
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = IncomeService(supabase)
    return service.update_income(user_id, income_id, data)

