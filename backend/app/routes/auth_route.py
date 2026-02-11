from fastapi import APIRouter, Depends
from supabase import Client

from app.db.database import get_supabase_client
from app.services.auth_service import AuthService
from app.models.schemas.user_schema import UserRegister
from app.repositories.auth_repository import AuthRepository
from app.models.schemas.user_schema import LoginRequest
from app.models.schemas.user_schema import LoginResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register")
def register_user(
    user_data: UserRegister,
    supabase: Client = Depends(get_supabase_client)
):
    service = AuthService(supabase)
    return service.register_user(user_data)

@router.post("/login", response_model=LoginResponse)
def login(
    payload: LoginRequest,
    supabase: Client = Depends(get_supabase_client),
) -> LoginResponse:
    service = AuthService(supabase)
    result = service.login(payload.email, payload.password)
    return LoginResponse(**result)

