from fastapi import HTTPException
import logging
from app.models.schemas.income_source_schema import IncomeSourceCreate
from app.repositories.income_source_repository import IncomeSourceRepository

logger = logging.getLogger(__name__)

class IncomeSourceService:

    def __init__(self, supabase):
        self.repository = IncomeSourceRepository(supabase)


    def create_income_source(self, user_id: str, data: IncomeSourceCreate):

        name = data.name.strip()
        names = self.repository.find_active_by_user_and_name(user_id, name)
        if names.data:
            raise HTTPException(
                status_code=400,
                detail="Income source with this name already exists"
            )

        response = self.repository.create(
            user_id=user_id,
            name=name,
            stability=data.stability,
            description=data.description
        )

        if not response.data:
            raise HTTPException(
                status_code=500,
                detail="Income source creation failed"
            )

        return {
            "message": "Income source created successfully",
            "income_source_id": response.data[0]["id"]
        }


    def get_income_sources(self, user_id: str):

        response = self.repository.get_income_sources_by_user(user_id)

        return response.data or []
    

    def delete_income_source(self, user_id: str, income_source_id: str):

        response = self.repository.deactivate(income_source_id, user_id)

        if not response.data:
            raise HTTPException(
                status_code=404,
                detail="Income source not found"
            )

        return {"message": "Income source deleted successfully"}
