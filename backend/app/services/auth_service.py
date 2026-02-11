from supabase import Client
from supabase_auth.errors import AuthApiError
from fastapi import HTTPException, status
from app.repositories.auth_repository import AuthRepository
from app.repositories.profile_repository import ProfileRepository
from app.models.schemas.user_schema import UserRegister
import logging

logger = logging.getLogger(__name__)

INVALID_CREDENTIALS_MESSAGE = "Credenciales inválidas"


class AuthService:

    def __init__(self, supabase: Client):
        self.auth_repository = AuthRepository(supabase)
        self.profile_repository = ProfileRepository(supabase)

    def register_user(self, user_data: UserRegister):

        try:
            auth_response = self.auth_repository.register_user(
                email=user_data.email,
                password=user_data.password
            )
        except AuthApiError as e:
            raise HTTPException(
                status_code=e.status,
                detail="User registration failed"
            )

        if not auth_response or not auth_response.user:
            raise HTTPException(
                status_code=400,
                detail="User registration failed"
            )

        user_id = auth_response.user.id

        try:
            self.profile_repository.create_profile(
                user_id=user_id,
                first_name=user_data.first_name,
                last_name=user_data.last_name
            )
        except Exception as e:
            try:
                self.auth_repository.delete_user(user_id)
            except Exception as rollback_error:
                logger.critical(f"Rollback failed: {rollback_error}")
            
            raise HTTPException(status_code=500, detail="Profile creation failed")

        return {
            "message": "User registered successfully",
            "user_id": user_id
        }
    
    def login(self, email: str, password: str) -> dict:
        try:
            response = self.auth_repository.sign_in_with_password(email, password)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_CREDENTIALS_MESSAGE,
            )

        session = getattr(response, "session", None)
        user = getattr(response, "user", None)

        if session is None or user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=INVALID_CREDENTIALS_MESSAGE,
            )

        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "user_id": user.id,
            "email": user.email,
        }

