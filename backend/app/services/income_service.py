from fastapi import HTTPException
from supabase import Client
from app.models.schemas.income_schema import CreateIncomeRequest
from app.models.schemas.income_schema import UpdateIncomeRequest
from app.repositories.income_repository import IncomeRepository
from app.repositories.income_source_repository import IncomeSourceRepository

class IncomeService:

    def __init__(self, supabase: Client):
        self.income_repository = IncomeRepository(supabase)
        self.income_source_repository = IncomeSourceRepository(supabase)

    def create_income(self, user_id: str, data: CreateIncomeRequest):

        source = self.income_source_repository.find_income_source(data.income_source_id)

        if not source.data or source.data[0]["user_id"] != user_id:
            raise HTTPException(404, "Income source not found")

        response = self.income_repository.create_income(
            data.income_source_id, 
            data.amount, 
            data.year, 
            data.month
        )

        return response.data[0]

    def get_user_incomes(self, user_id: str):

        response = self.income_repository.get_incomes_by_user(user_id)

        return response.data or []
    
    def update_income(self, user_id: str, income_id: str, data: UpdateIncomeRequest):

        update_data = data.model_dump(exclude_unset=True)

        if not update_data:
            raise HTTPException(400, "No data provided to update")

        income = self.income_repository.find_income(income_id)

        if not income.data:
            raise HTTPException(404, "Income not found")

        income_source_id = income.data[0]["income_source_id"]

        income_source = self.income_source_repository.find_income_source(income_source_id)

        if not income_source.data or income_source.data[0]["user_id"] != user_id:
            raise HTTPException(404, "Income not found")

        response = self.income_repository.update_income(income_id, update_data)

        if not response.data:
            raise HTTPException(404, "Income not found")

        return response.data[0]


