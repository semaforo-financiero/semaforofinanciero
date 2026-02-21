from supabase import Client
import logging

logger = logging.getLogger(__name__)

class FamilyRepository:
    def __init__(self, supabase: Client):
        self.supabase = supabase
    
    def create_family(self, name: str, user_id: str):
        try:
            return self.supabase.table("families").insert({
                "name": name,
                "created_by": user_id
            }).execute()
        except Exception:
            logger.exception("Error inserting family")
            raise
    
    def delete_family(self, family_id: str):
        try:
            return (
                self.supabase.table("familes")
                .delete()
                .eq("family_id", family_id)
                .execute()
            )
        except Exception:
            logger.exception("Unexpected error deleting family")
            raise

    def add_family_member(self, family_id: str, user_id: str, role: str):
        try:    
            return (
                self.supabase.table("family_members").insert({
                "family_id": family_id,
                "user_id": user_id,
                "role": role
                })
                .execute()
            )
        except Exception:
            logger.exception("Error inserting family member")
            raise

    def find_member_by_user(self, user_id: str):
        try:
            return (
                self.supabase.table("family_members")
                .select("*")
                .eq("user_id", user_id)
                .execute()
            )
        except Exception:
            logger.exception("Error finding user member")
            raise
        
    def create_invitation(
        self,
        family_id: str,
        invited_by: str,
        invited_email: str,
        token: str,
        expires_at: str
    ):
        try:
            return (
                self.supabase
                .table("family_invitations")
                .insert({
                    "family_id": family_id,
                    "invited_by": invited_by,
                    "invited_email": invited_email,
                    "token": token,
                    "expires_at": expires_at
                })
                .execute()
            )
        except Exception:
            logger.exception("Error inserting invitation")
            raise
    
    def find_invitation_by_token(self, token: str):
        try:
            return (
                self.supabase.table("family_invitations")
                .select("*")
                .eq("token", token)
                .single()
                .execute()
            )
        except Exception:
            logger.exception("Error finding invitation by token")
            raise
    
    def update_invitation_status(self, token: str, status: str):
        try:
            return (
                self.supabase.table("family_invitations")
                .update({"status": status})
                .eq("token", token)
                .execute()
            )
        except Exception:
            logger.exception("Error updating invitation status")
            raise