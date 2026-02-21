from fastapi import APIRouter, Depends
from supabase import Client
from app.models.schemas.family_schema import FamilyCreate
from app.models.schemas.family_schema import FamilyInviteCreate
from app.models.schemas.family_schema import AcceptInvitation
from app.services.family_service import FamilyService
from app.db.database import get_supabase_client
from app.core.security import get_current_user_id

router = APIRouter(prefix="/families", tags=["families"])

@router.post("/")
def create_family(
    family_data: FamilyCreate,
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = FamilyService(supabase)
    return service.create_family(user_id, family_data)

@router.post("/invite")
def invite_member(
    invite_data: FamilyInviteCreate,
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_client)
):
    service = FamilyService(supabase)
    return service.invite_member(user_id, invite_data)

@router.post("/accept")
def accept_invitation(
    data: AcceptInvitation,
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_client)
):
    service = FamilyService(supabase)
    return service.accept_invitation(user_id, data.token)
