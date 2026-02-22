from fastapi import HTTPException
from supabase import Client
from app.repositories.family_repository import FamilyRepository
from app.models.schemas.family_schema import FamilyCreate
from app.models.schemas.family_schema import FamilyInviteCreate
import uuid
from datetime import datetime, timedelta, timezone
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
    
    def invite_member(self, user_id: str, invite_data: FamilyInviteCreate):
        member = self.family_repository.find_member_by_user(user_id)

        if not member.data:
            raise HTTPException(400, "User has no family")
        
        family_id = member.data[0]["family_id"]

        token = str(uuid.uuid4())
        expires_at = (datetime.now(timezone.utc) + timedelta(days=2)).isoformat()

        response = self.family_repository.create_invitation(
            family_id=family_id,
            invited_by=user_id,
            invited_email=invite_data.email,
            token=token,
            expires_at=expires_at
        )

        if not response.data:
            raise HTTPException(500, "Invitation failed")
        
        return {
            "message": "Invitation created",
            "token": token
        }
    
    def accept_invitation(self, user_id: str, token: str):
        invitation = self.family_repository.find_invitation_by_token(token)
        
        if not invitation.data:
            raise HTTPException(404, "Invitation not found")

        invite = invitation.data

        if invite.get("status") != "pending":
            raise HTTPException("Invitation already proccesed")
        
        if datetime.fromisoformat(invite.get("expires_at")) < datetime.now(timezone.utc):
            raise HTTPException(400, "Invitation expired")
        
        existing = self.family_repository.find_member_by_user(user_id)
        
        if existing.data:
            raise HTTPException(400, "User already in family")
        
        response = self.family_repository.add_family_member(
            family_id=invite.get("family_id"),
            user_id=user_id,
            role="member"
        )

        if not response.data:
            raise HTTPException(500, "Failed to join family")
        
        self.family_repository.update_invitation_status(token, "accepted")

        return {"message": "Joined family"}