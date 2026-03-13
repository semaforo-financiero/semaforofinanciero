from supabase import Client
import logging

logger = logging.getLogger(__name__)


class ExpenseSourceRepository:

    def __init__(self, supabase: Client):
        self.supabase = supabase

    def create(self, user_id: str, name: str, stability: str, is_debt: bool, description: str | None):
        try:
            return (
                self.supabase
                .table("expense_sources")
                .insert({
                    "user_id": user_id,
                    "name": name,
                    "stability": stability,
                    "is_debt": is_debt,
                    "description": description
                })
                .execute()
            )
        except Exception:
            logger.exception("Error creating expense source")
            raise

    def get_expense_sources_by_user(self, user_id: str):
        try:
            return (
                self.supabase
                .table("expense_sources")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
        except Exception:
            logger.exception("Error getting expense sources")
            raise

    def find_active_by_user_and_name(self, user_id: str, name: str):
        try:
            return (
                self.supabase
                .table("expense_sources")
                .select("id")
                .eq("name", name)
                .eq("user_id", user_id)
                .eq("is_active", True)
                .limit(1)
                .execute()
            )
        except Exception:
            logger.exception("Error getting expense source")
            raise

    def deactivate(self, expense_source_id: str, user_id: str):
        try:
            return (
                self.supabase
                .table("expense_sources")
                .update({"is_active": False})
                .eq("id", expense_source_id)
                .eq("user_id", user_id)
                .eq("is_active", True)
                .execute()
            )
        except Exception:
            logger.exception("Error deleting expense source")
            raise

    def get_by_id_and_user(self, expense_source_id: str, user_id: str):
        try:
            return (
                self.supabase
                .table("expense_sources")
                .select("id, user_id, is_active")
                .eq("id", expense_source_id)
                .eq("user_id", user_id)
                .eq("is_active", True)
                .limit(1)
                .execute()
            )
        except Exception:
            logger.exception("Error getting expense source by id and user")
            raise