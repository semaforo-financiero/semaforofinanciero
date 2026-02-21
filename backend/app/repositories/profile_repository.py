from supabase import Client
import logging

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


