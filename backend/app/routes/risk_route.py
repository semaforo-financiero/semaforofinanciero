from fastapi import APIRouter, Depends
from supabase import Client
from app.core.security import get_current_user_id
from app.db.database import get_supabase_client
from app.models.schemas.risk_schema import FamilyRiskResponse, RiskResponse
from app.services.risk_service import RiskService

ROUTER_PREFIX = "/risk"
ROUTER_TAGS = ["Risk"]


router = APIRouter(prefix=ROUTER_PREFIX, tags=ROUTER_TAGS)


@router.get("/user", response_model=RiskResponse)
def get_user_risk(
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = RiskService(supabase)
    return service.get_user_risk(user_id)


@router.get("/family", response_model=FamilyRiskResponse)
def get_family_risk(
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_client)
):
    service = RiskService(supabase)
    return service.get_family_risk(user_id)
