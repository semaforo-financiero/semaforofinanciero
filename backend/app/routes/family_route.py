from fastapi import APIRouter, Depends
from supabase import Client
from app.models.schemas.family_schema import FamilyCreate
from app.models.schemas.family_schema import FamilyUpdate
from app.models.schemas.family_schema import FamilyInviteCreate
from app.models.schemas.family_schema import AcceptInvitation
from app.models.schemas.family_schema import RejectInvitation
from app.models.schemas.family_schema import FamilyWithMembersResponse
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

@router.delete("/")
def delete_family(
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = FamilyService(supabase)
    return service.delete_family(user_id)

@router.put("/")
def update_family(
    family_data: FamilyUpdate,
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = FamilyService(supabase)
    return service.update_family(user_id, family_data)

@router.get("/", response_model=FamilyWithMembersResponse)
def get_family(
    supabase: Client = Depends(get_supabase_client),
    user_id: str = Depends(get_current_user_id)
):
    service = FamilyService(supabase)
    return service.get_family(user_id)

@router.post("/invite")
def invite_member(
    invite_data: FamilyInviteCreate,
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_client)
):
    service = FamilyService(supabase)
    return service.invite_member(user_id, invite_data)

@router.delete("/members/{target_user_id}")
def remove_member(
    target_user_id: str,
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_client)
):
    service = FamilyService(supabase)
    return service.remove_member(user_id, target_user_id)


@router.post("/accept")
def accept_invitation(
    data: AcceptInvitation,
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_client)
):
    service = FamilyService(supabase)
    return service.accept_invitation(user_id, data.family_id)

@router.patch("/reject")
def reject_invitation(
    data: RejectInvitation,
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_client)
):
    service = FamilyService(supabase)
    return service.reject_invitation(user_id, data.family_id)

@router.get("/invitations")
def get_user_invitations(
    user_id: str = Depends(get_current_user_id),
    supabase: Client = Depends(get_supabase_client)
):
    service = FamilyService(supabase)
    return service.list_user_invitations(user_id)
