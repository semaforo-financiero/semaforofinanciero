from supabase import Client
import logging

PROFILES_TABLE = "profiles"
SOCIOECONOMIC_PROFILES_TABLE = "socioeconomic_profiles"

logger = logging.getLogger(__name__)

class ProfileRepository:

    def __init__(self, supabase: Client):
        self.supabase = supabase

    def create_profile(self, user_id: str, first_name: str, last_name: str, email: str):
        try:
            return (
                self.supabase
                .table("profiles")
                .insert({
                    "id": user_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email
                })
                .execute()
            )
        except Exception:
            logger.exception("Error inserting profile")
            raise
    
    def get_profile_by_email(self, email: str):
        try:
            return (
                self.supabase
                .table("profiles")
                .select("*")
                .eq("email", email)
                .single()
                .execute()
            )
        except Exception:
            logger.exception("Error getting profile by email")
            raise


    def upsert_socioeconomic_profile(self, user_id: str, payload: dict) -> dict:
        data_to_save = {"id": user_id, **payload}

        response = (
            self.supabase.table("socioeconomic_profiles")
            .upsert(data_to_save)
            .execute()
        )

        rows = getattr(response, "data", None) or []
        if not rows:
            return data_to_save

        return rows[0]

    def get_basic_profile(self, user_id: str) -> dict | None:
        try:
            response = (
                self.supabase
                .table(PROFILES_TABLE)
                .select("id, first_name, last_name, email")
                .eq("id", user_id)
                .limit(1)
                .execute()
            )
        except Exception:
            logger.exception("Error selecting profile")
            raise

        rows = getattr(response, "data", None) or []
        return rows[0] if rows else None

    def get_socioeconomic_profile(self, user_id: str) -> dict | None:
        try:
            response = (
                self.supabase
                .table(SOCIOECONOMIC_PROFILES_TABLE)
                .select(
                    "id, age, years_working, gender, state, "
                    "employment_status, education_level, job_title"
                )
                .eq("id", user_id)
                .limit(1)
                .execute()
            )
        except Exception:
            logger.exception("Error selecting socioeconomic profile")
            raise

        rows = getattr(response, "data", None) or []
        return rows[0] if rows else None