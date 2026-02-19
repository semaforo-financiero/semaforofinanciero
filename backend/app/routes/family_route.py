from fastapi import APIRouter, Depends
from supabase import Client
from app.models.schemas.family_schema import FamilyCreate
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
