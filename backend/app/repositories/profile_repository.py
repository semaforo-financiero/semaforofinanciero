from supabase import Client
import logging

logger = logging.getLogger(__name__)

class ProfileRepository:

    def __init__(self, supabase: Client):
        self.supabase = supabase

    def create_profile(self, user_id: str, first_name: str, last_name: str):
        try:
            return (
                self.supabase
                .table("profiles")
                .insert({
                    "id": user_id,
                    "first_name": first_name,
                    "last_name": last_name
                })
                .execute()
            )
        except Exception:
            logger.exception("Error inserting profile")
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
