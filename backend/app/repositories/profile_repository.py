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

