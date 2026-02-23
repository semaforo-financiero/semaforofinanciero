from fastapi import HTTPException, status
from supabase import Client

from app.repositories.profile_repository import ProfileRepository


PROFILE_UPSERT_FAILED_MESSAGE = "No se pudo guardar el perfil socioeconómico"


class ProfileService:
    def __init__(self, supabase: Client):
        self.profile_repository = ProfileRepository(supabase)

    def upsert_socioeconomic_profile(self, user_id: str, payload: dict) -> dict:
        try:
            return self.profile_repository.upsert_socioeconomic_profile(user_id, payload)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{PROFILE_UPSERT_FAILED_MESSAGE}: {str(e)}",
            )