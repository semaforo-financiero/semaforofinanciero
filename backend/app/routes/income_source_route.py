from fastapi import APIRouter, Depends
from supabase import Client
from typing import List
from app.models.schemas.income_source_schema import IncomeSourceCreate
from app.models.schemas.income_source_schema import IncomeSourceResponse
from app.services.income_source_service import IncomeSourceService
from app.db.database import get_supabase_client
from app.core.security import get_current_user_id

router = APIRouter(prefix="/income-sources", tags=["income-sources"])


@router.post("/")
def create_income_source(
    data: IncomeSourceCreate,
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = IncomeSourceService(supabase)
    return service.create_income_source(user_id, data)


@router.get("/", response_model=List[IncomeSourceResponse])
def get_income_sources(
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = IncomeSourceService(supabase)
    return service.get_income_sources(user_id)


@router.delete("/{income_source_id}")
def delete_income_source(
    income_source_id: str,
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = IncomeSourceService(supabase)
    return service.delete_income_source(user_id, income_source_id)
