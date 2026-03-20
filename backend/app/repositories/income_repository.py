from supabase import Client
from uuid import UUID

class IncomeRepository:
    def __init__(self, supabase: Client):
        self.supabase = supabase
    
    def create_income(self, income_source_id: UUID, amount: float, year: int, month: int):
        return (
            self.supabase
            .table("incomes")
            .insert({
                "income_source_id": str(income_source_id),
                "amount": amount,
                "year": year,
                "month": month
            })
            .execute()
        )
    
    def get_incomes_by_user(self, user_id: str):
        return (
            self.supabase
            .table("incomes")
            .select("*, income_sources!incomes_income_source_id_fk(user_id, name, is_active, stability)")
            .eq("income_sources.user_id", user_id)
            .execute()
        )
    
    def find_income(self, income_id: str):
        return (
            self.supabase
            .table("incomes")
            .select("*")
            .eq("id", income_id)
            .execute()
        )

    
    def update_income(self, income_id, payload: dict):

        return (
            self.supabase
            .table("incomes")
            .update(payload)
            .eq("id", income_id)
            .execute()
        )


