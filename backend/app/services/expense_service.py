from fastapi import HTTPException
import logging

from app.models.schemas.expense_schema import ExpenseCreate
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.expense_source_repository import ExpenseSourceRepository

logger = logging.getLogger(__name__)


class ExpenseService:

    def __init__(self, supabase):
        self.repository = ExpenseRepository(supabase)
        self.expense_source_repository = ExpenseSourceRepository(supabase)

    def create_expense(self, user_id: str, data: ExpenseCreate):
        logger.info("Creating expense for user_id=%s", user_id)

        source = self.expense_source_repository.get_by_id_and_user(data.expense_source_id, user_id)

        if not source.data:
            logger.warning(
                "Expense source not found. user_id=%s expense_source_id=%s",
                user_id,
                data.expense_source_id
            )
            raise HTTPException(
                status_code=404,
                detail="Expense source not found"
            )

        response = self.repository.create(
            expense_source_id=data.expense_source_id,
            amount=data.amount,
            year=data.year,
            month=data.month
        )

        if not response.data:
            logger.error("Expense creation failed for user_id=%s", user_id)
            raise HTTPException(
                status_code=500,
                detail="Expense creation failed"
            )

        return {
            "message": "Expense created successfully",
            "expense_id": response.data[0]["id"]
        }

    def get_expenses(self, user_id: str):
        logger.info("Getting expenses for user_id=%s", user_id)
        response = self.repository.get_expenses_by_user(user_id)
        return response.data or []

    def update_expense_amount(self, user_id: str, expense_id: str, amount: float):
        logger.info("Updating expense amount. user_id=%s expense_id=%s", user_id, expense_id)

        existing = self.repository.get_by_id_and_user(expense_id, user_id)

        if not existing.data:
            logger.warning(
                "Expense not found. user_id=%s expense_id=%s",
                user_id,
                expense_id
            )
            raise HTTPException(
                status_code=404,
                detail="Expense not found"
            )

        response = self.repository.update_amount(
            expense_id=expense_id,
            amount=amount
        )

        if not response.data:
            logger.error(
                "Expense update failed. user_id=%s expense_id=%s",
                user_id,
                expense_id
            )
            raise HTTPException(
                status_code=500,
                detail="Expense update failed"
            )

        return {
            "message": "Expense amount updated successfully"
        }