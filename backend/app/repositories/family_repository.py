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
    
    def update_family(self, name: str, family_id: str):
        try:
            return (
                self.supabase
                .table("families")
                .update({"name": name})
                .eq("id", family_id)
                .execute()
            )
        except Exception:
            logger.exception("Error updating family")
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
        invited_user_id: str,
        invited_email: str
    ):
        try:
            return (
                self.supabase
                .table("family_invitations")
                .insert({
                    "family_id": family_id,
                    "invited_by": invited_by,
                    "invited_user_id": invited_user_id,
                    "invited_email": invited_email
                })
                .execute()
            )
        except Exception:
            logger.exception("Error inserting invitation")
            raise

    def find_pending_invitation(self, invited_user_id: str, family_id: str):
        try:
            return (
                self.supabase
                .table("family_invitations")
                .select("*")
                .eq("invited_user_id", invited_user_id)
                .eq("family_id", family_id)
                .eq("status", "pending")
                .execute()
            )
        except Exception:
            logger.exception("Error finding pending invitation")
            raise

    def accept_pending_invitation(self, user_id: str, family_id: str):
        try:
            return (
                self.supabase
                .table("family_invitations")
                .update({"status": "accepted"})
                .eq("invited_user_id", user_id)
                .eq("family_id", family_id)
                .eq("status", "pending")
                .execute()
            )
        except Exception:
            logger.exception("Error acepting pending invitation")
            raise
    
    def reject_pending_invitation(self, user_id: str, family_id: str):
        try:
            return (
                self.supabase
                .table("family_invitations")
                .update({"status": "rejected"})
                .eq("invited_user_id", user_id)
                .eq("family_id", family_id)
                .eq("status", "pending")
                .execute()
            )
        except Exception:
            logger.exception("Error rejecting pending invitation")
            raise
    
    def get_user_invitations(self, user_id: str):
        try:
            return (
                self.supabase
                .table("family_invitations")
                .select("*")
                .eq("invited_user_id", user_id)
                .execute()
            )
        except Exception:
            logger.exception("Error getting user invitations")
            raise

