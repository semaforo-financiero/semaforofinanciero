from supabase import Client
from supabase_auth.errors import AuthApiError
from app.repositories.auth_repository import AuthRepository
from app.repositories.profile_repository import ProfileRepository
from app.models.schemas.user_schema import UserRegister
from app.core.exceptions import UserAlreadyExists, AuthError, ProfileCreationError
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
            code = getattr(e, "code", None)
            raw_msg = str(e)
            msg = raw_msg.lower()

            if code == "user_already_exists" or "already registered" in msg:
                raise UserAlreadyExists(
                    details={
                        "provider": "supabase",
                        "source_code": code,
                        "email": user_data.email,
                        "raw": raw_msg
                    }
                )

            raise AuthError(
                message="User registration failed",
                details={"source_code": code, "raw": raw_msg}
            )

        if not auth_response or not getattr(auth_response, "user", None):
            raise AuthError(message="User registration failed")

        user_id = auth_response.user.id

        try:
            self.profile_repository.create_profile(
                user_id=user_id,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                email=user_data.email
            )
        except Exception as e:
            try:
                self.auth_repository.delete_user(user_id)
            except Exception as rollback_error:
                logger.critical(f"Rollback failed: {rollback_error}")
            raise ProfileCreationError()

        return {
            "message": "User registered successfully",
            "user_id": user_id
        }
    
    def login(self, email: str, password: str) -> dict:
        try:
            response = self.auth_repository.sign_in_with_password(email, password)
        except Exception:
            raise AuthError(message=INVALID_CREDENTIALS_MESSAGE)

        session = getattr(response, "session", None)
        user = getattr(response, "user", None)

        if session is None or user is None:
            raise AuthError(message=INVALID_CREDENTIALS_MESSAGE)

        return {
            "access_token": session.access_token,
            "refresh_token": session.refresh_token,
            "user_id": user.id,
            "email": user.email,
        }

