from fastapi import HTTPException, status
from supabase import Client

from app.repositories.profile_repository import ProfileRepository


PROFILE_NOT_FOUND_MESSAGE = "Perfil no encontrado"
PROFILE_UPSERT_FAILED_MESSAGE = "No se pudo guardar el perfil socioeconómico"
PROFILE_GET_FAILED_MESSAGE = "No se pudo obtener el perfil"


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
        
    def get_full_profile(self, user_id: str) -> dict:
        try:
            profile = self.profile_repository.get_basic_profile(user_id)
            if profile is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=PROFILE_NOT_FOUND_MESSAGE,
                )

            socioeconomic_profile = self.profile_repository.get_socioeconomic_profile(user_id)

            return {
                "profile": profile,
                "socioeconomic_profile": socioeconomic_profile,
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{PROFILE_GET_FAILED_MESSAGE}: {str(e)}",
            )