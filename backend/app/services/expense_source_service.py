from fastapi import HTTPException
import logging

from app.models.schemas.expense_source_schema import ExpenseSourceCreate
from app.repositories.expense_source_repository import ExpenseSourceRepository

logger = logging.getLogger(__name__)


class ExpenseSourceService:

    def __init__(self, supabase):
        self.repository = ExpenseSourceRepository(supabase)

    def create_expense_source(self, user_id: str, data: ExpenseSourceCreate):
        name = data.name.strip()

        names = self.repository.find_active_by_user_and_name(user_id, name)
        if names.data:
            raise HTTPException(
                status_code=400,
                detail="Expense source with this name already exists"
            )

        response = self.repository.create(
            user_id=user_id,
            name=name,
            stability=data.stability,
            is_debt=data.is_debt,
            description=data.description
        )

        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Expense source creation failed"
            )

        return {
            "message": "Expense source created successfully",
            "expense_source_id": response.data[0]["id"]
        }

    def get_expense_sources(self, user_id: str):
        response = self.repository.get_expense_sources_by_user(user_id)
        return response.data or []

    def delete_expense_source(self, user_id: str, expense_source_id: str):
        response = self.repository.deactivate(expense_source_id, user_id)

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Expense source not found"
            )

        return {"message": "Expense source deleted successfully"}