from supabase import Client
import logging

logger = logging.getLogger(__name__)

class FamilyRepository:
    def __init__(self, supabase: Client):
        self.supabase = supabase
    
    def create_family(self, name: str, user_id: str):
        try:
            return self.supabase.table("families").insert({
                "name": name,
                "created_by": user_id
            }).execute()
        except Exception:
            logger.exception("Error inserting family")
            raise
    
    def delete_family(self, family_id: str):
        try:
            return (
                self.supabase.table("familes")
                .delete()
                .eq("family_id", family_id)
                .execute()
            )
        except Exception:
            logger.exception("Unexpected error deleting family")
            raise

    def add_family_member(self, family_id: str, user_id: str, role: str):
        try:    
            return (
                self.supabase.table("family_members").insert({
                "family_id": family_id,
                "user_id": user_id,
                "role": role
                })
                .execute()
            )
        except Exception:
            logger.exception("Error inserting family member")

    def find_member_by_user(self, user_id: str):
        try:
            return (
                self.supabase.table("family_members")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
        except Exception:
            logger.exception("Error finding user member")