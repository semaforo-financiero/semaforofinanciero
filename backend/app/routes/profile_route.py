from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from supabase import Client

from app.db.database import get_supabase_client
from app.models.schemas.profile_schema import (
    SocioeconomicProfileResponse,
    SocioeconomicProfileUpsertRequest,
)
from app.services.profile_service import ProfileService


# =========================
# CONSTANTS
# =========================

ROUTER_PREFIX = "/profile"
ROUTER_TAGS = ["Profile"]
UNAUTHORIZED_MESSAGE = "No autorizado"


# =========================
# ROUTER
# =========================

router = APIRouter(prefix=ROUTER_PREFIX, tags=ROUTER_TAGS)


# =========================
# SECURITY
# =========================

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    supabase: Client = Depends(get_supabase_client),
) -> str:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UNAUTHORIZED_MESSAGE,
        )

    access_token = credentials.credentials.strip()

    try:
        user_response = supabase.auth.get_user(access_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UNAUTHORIZED_MESSAGE,
        )

    user = getattr(user_response, "user", None)
    user_id = getattr(user, "id", None)

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=UNAUTHORIZED_MESSAGE,
        )

    return user_id


# =========================
# ENDPOINTS
# =========================

@router.put("", response_model=SocioeconomicProfileResponse)
def upsert_profile(
    payload: SocioeconomicProfileUpsertRequest,
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_client),
) -> SocioeconomicProfileResponse:
    service = ProfileService(supabase)
    result = service.upsert_socioeconomic_profile(user_id, payload.model_dump())
    return SocioeconomicProfileResponse(**result)