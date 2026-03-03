from fastapi import HTTPException
from supabase import Client
from app.repositories.family_repository import FamilyRepository
from app.repositories.profile_repository import ProfileRepository
from app.models.schemas.family_schema import FamilyCreate
from app.models.schemas.family_schema import FamilyUpdate
from app.models.schemas.family_schema import FamilyInviteCreate
import logging

logger = logging.getLogger(__name__)

class FamilyService:

    def __init__(self, supabase: Client):
        self.family_repository = FamilyRepository(supabase)
        self.profile_repository = ProfileRepository(supabase)

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
    def delete_family(self, user_id: str):

        existing = self.family_repository.find_member_by_user(user_id)
        if not existing.data:
            raise HTTPException(
                status_code=404,
                detail="User has no family"
            )
        
        user = existing.data[0]
        if user["role"] != "admin":
            raise HTTPException(403, "Only admin can delete family")
        
        family_id = user["family_id"]
        
        try:
            response = self.family_repository.delete_family(family_id)
        except Exception:
            raise HTTPException(500, "Delete failed")
        
        if not response.data:
            raise HTTPException(404, "Family not found")
            
        return {
            "message": "Family deleted successfully"
        }
    
    def update_family(self, user_id: str, family_data: FamilyUpdate):
        member = self.family_repository.find_member_by_user(user_id)
        if not member.data:
            raise HTTPException(404, "User has no family")
        
        if member.data[0]["role"] != "admin":
            raise HTTPException(403, "Only admin can edit family")
        
        family_id = member.data[0]["family_id"]

        response = self.family_repository.update_family(family_data.name, family_id)
        
        if not response.data:
            raise HTTPException(500, "Update failed")
        
        return {
            "message": "Family updated",
            "family_id": family_id
        }
    
    def get_family(self, user_id: str):
        if not user_id:
            raise HTTPException(401, "Invalid user")
        result = self.family_repository.get_family_by_user(user_id)

        if not result:
            raise HTTPException(404, "Family not found")

        return result

    
    def invite_member(self, user_id: str, invite_data: FamilyInviteCreate):

        member = self.family_repository.find_member_by_user(user_id)

        if not member.data:
            raise HTTPException(400, "User has no family")

        if member.data[0]["role"] != "admin":
            raise HTTPException(403, "Only admin can invite")

        family_id = member.data[0]["family_id"]

        try:
            invited = self.profile_repository.get_profile_by_email(invite_data.email)
        except Exception:
            raise HTTPException(404, "Invited user not registered")

        invited_id = invited.data.get("id")

        existing_member = self.family_repository.find_member_by_user(invited_id)
        if existing_member.data:
            raise HTTPException(400, "User already in family")

        existing_inv = self.family_repository.find_pending_invitation(invited_id, family_id)
        if existing_inv.data:
            raise HTTPException(400, "Invitation already pending")

        response = self.family_repository.create_invitation(
            family_id=family_id,
            invited_by=user_id,
            invited_user_id=invited_id,
            invited_email=invite_data.email
        )

        if not response.data:
            raise HTTPException(500, "Invitation failed")

        return {"message": "Invitation created", "family_id": family_id}
    
    def remove_member(self, actor_id: str, target_id: str):

        actor = self.family_repository.find_member_by_user(actor_id)

        if not actor.data:
            raise HTTPException(404, "Actor has no family")

        actor_member = actor.data[0]
        family_id = actor_member["family_id"]
        actor_role = actor_member["role"]

        target = self.family_repository.find_member_by_user(target_id)

        if not target.data:
            raise HTTPException(404, "Target not in family")

        target_member = target.data[0]

        if target_member["family_id"] != family_id:
            raise HTTPException(403, "Different family")

        if actor_id != target_id and actor_role != "admin":
            raise HTTPException(403, "Only admin can remove others")

        if actor_id == target_id and actor_role == "admin":
            raise HTTPException(400, "Admin cannot remove himself")

        self.family_repository.delete_family_member(target_id)

        return {"message": "Member removed"}

    
    def accept_invitation(self, user_id: str, family_id: str):

        existing = self.family_repository.find_member_by_user(user_id)
        if existing.data:
            raise HTTPException(400, "User already in family")

        invitation = self.family_repository.accept_pending_invitation(
            user_id=user_id,
            family_id=family_id
        )

        if not invitation.data:
            raise HTTPException(404, "Pending invitation not found or already processed")

        response = self.family_repository.add_family_member(
            family_id=family_id,
            user_id=user_id,
            role="member"
        )

        if not response.data:
            raise HTTPException(500, "Failed to join family")

        return {"message": "Joined family", "family_id": family_id}
    
    def reject_invitation(self, user_id: str, family_id: str):

        existing = self.family_repository.find_member_by_user(user_id)
        if existing.data:
            raise HTTPException(400, "User already in a family")

        invitation = self.family_repository.reject_pending_invitation(
            user_id=user_id,
            family_id=family_id
        )

        if not invitation.data:
            raise HTTPException(404, "Pending invitation not found or already processed")

        return {"message": "Invitation rejected", "family_id": family_id}
    
    def list_user_invitations(self, user_id: str):
        if not user_id:
            raise HTTPException(401, "Invalid user")
        response = self.family_repository.get_user_invitations(user_id)
        return response.data if response.data else []


