from supabase import Client
import logging

logger = logging.getLogger(__name__)

class IncomeSourceRepository:

    def __init__(self, supabase: Client):
        self.supabase = supabase


    def create(self, user_id: str, name: str, stability: str, description: str | None):
        try:
            return (
                self.supabase
                .table("income_sources")
                .insert({
                    "user_id": user_id,
                    "name": name,
                    "stability": stability,
                    "description": description
                })
                .execute()
            )
        except Exception:
            logger.exception("Error creating income source")
            raise


    def get_income_sources_by_user(self, user_id: str):
        try:
            return (
                self.supabase
                .table("income_sources")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
        except Exception:
            logger.exception("Error getting income sources")
            raise
    
    def find_active_by_user_and_name(self, user_id: str, name: str):
        try:
            return (
                self.supabase
                .table("income_sources")
                .select("id")
                .eq("name",  name)
                .eq("user_id",  user_id)
                .eq("is_active", True)
                .limit(1)
                .execute()
            )
        except Exception:
            logger.exception("Error getting income source")
            raise


    def deactivate(self, income_source_id: str, user_id: str):
        try:
            return (
                self.supabase
                .table("income_sources")
                .update({"is_active": False})
                .eq("id", income_source_id)
                .eq("user_id", user_id)
                .eq("is_active", True)
                .execute()
            )
        except Exception:
            logger.exception("Error deleting income source")
            raise
