from fastapi import HTTPException
from supabase import Client
from app.repositories.family_repository import FamilyRepository
from app.models.schemas.family_schema import FamilyCreate
import logging

logger = logging.getLogger(__name__)

class FamilyService:

    def __init__(self, supabase: Client):
        self.family_repository = FamilyRepository(supabase)

    def create_family(self, user_id: str, family_data: FamilyCreate):

        existing = self.family_repository.find_member_by_user(user_id)
        if existing.data:
            raise HTTPException(
                status_code=400,
                detail="User already belongs to a family"
            )

        family_response = self.family_repository.create_family(
            name=family_data.name,
            user_id=user_id
        )

        if not family_response.data:
            raise HTTPException(
                status_code=500,
                detail="Family creation failed"
            )

        family_id = family_response.data[0]["id"]

        response = self.family_repository.add_family_member(
            family_id=family_id,
            user_id=user_id,
            role="admin"
        )
        if not response.data:
            logger.error(response)
            try:
                self.family_repository.delete_family(family_id)
            except Exception as rollback_error:
                logger.critical(f"Rollback failed: {rollback_error}")
            raise HTTPException(status_code=500, detail="Family creation failed")

        return {
            "message": "Family created successfully",
            "family_id": family_id
        }
