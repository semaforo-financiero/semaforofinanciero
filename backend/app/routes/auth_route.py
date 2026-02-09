from fastapi import APIRouter, Depends
from supabase import Client

from app.db.database import get_supabase_client
from app.services.auth_service import AuthService
from app.models.schemas.user_schema import UserRegister

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register_user(
    user_data: UserRegister,
    supabase: Client = Depends(get_supabase_client)
):
    service = AuthService(supabase)
    return service.register_user(user_data)
