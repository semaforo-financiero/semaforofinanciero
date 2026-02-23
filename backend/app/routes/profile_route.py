from fastapi import APIRouter, Depends
from supabase import Client

from app.core.security import get_current_user_id
from app.db.database import get_supabase_client
from app.models.schemas.profile_schema import (
    SocioeconomicProfileResponse,
    SocioeconomicProfileUpsertRequest,
)
from app.services.profile_service import ProfileService


ROUTER_PREFIX = "/profile"
ROUTER_TAGS = ["Profile"]


router = APIRouter(prefix=ROUTER_PREFIX, tags=ROUTER_TAGS)


@router.put("", response_model=SocioeconomicProfileResponse)
def upsert_profile(
    payload: SocioeconomicProfileUpsertRequest,
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_client),
) -> SocioeconomicProfileResponse:
    service = ProfileService(supabase)
    result = service.upsert_socioeconomic_profile(user_id, payload.model_dump())
    return SocioeconomicProfileResponse(**result)