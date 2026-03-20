from supabase import Client
import logging

logger = logging.getLogger(__name__)


class ExpenseRepository:

    def __init__(self, supabase: Client):
        self.supabase = supabase

    def create(self, expense_source_id: str, amount: float, year: int, month: int):
        try:
            return (
                self.supabase
                .table("expenses")
                .insert({
                    "expense_source_id": expense_source_id,
                    "amount": amount,
                    "year": year,
                    "month": month
                })
                .execute()
            )
        except Exception:
            logger.exception("Error creating expense")
            raise

    def get_expenses_by_user(self, user_id: str):
        try:
            return (
                self.supabase
                .table("expenses")
                .select("*, expense_sources!inner!expenses_expense_source_id_fkey(user_id, name, is_active, is_debt, stability)")
                .eq("expense_sources.user_id", user_id)
                .execute()
            )
        except Exception:
            logger.exception("Error getting expenses")
            raise

    def get_by_id_and_user(self, expense_id: str, user_id: str):
        try:
            return (
                self.supabase
                .table("expenses")
                .select("*, expense_sources!inner(user_id, name, is_active, is_debt, stability)")
                .eq("id", expense_id)
                .eq("expense_sources.user_id", user_id)
                .eq("expense_sources.is_active", True)
                .limit(1)
                .execute()
            )
        except Exception:
            logger.exception("Error getting expense by id")
            raise

    def update_amount(self, expense_id: str, amount: float):
        try:
            return (
                self.supabase
                .table("expenses")
                .update({
                "amount": amount
                })
                .eq("id", expense_id)
                .execute()
        )
        except Exception:
            logger.exception("Error updating expense amount")
            raise
