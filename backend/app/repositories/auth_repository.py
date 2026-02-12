from supabase import Client
from supabase_auth.errors import AuthApiError
import logging

logger = logging.getLogger(__name__)

class AuthRepository:

    def __init__(self, supabase: Client):
        self.supabase = supabase

    def register_user(self, email: str, password: str):
        try:
            return self.supabase.auth.sign_up({
                "email": email,
                "password": password,
            })
        except AuthApiError as e:
            logger.warning(f"Supabase Auth error: {e}")
            raise
        except Exception:
            logger.exception("Unexpected error in register_user")
            raise

    def sign_in_with_password(self, email: str, password: str):
        try:
            return self.supabase.auth.sign_in_with_password({                
                "email": email, "password": password
            })
        except AuthApiError as e:
            logger.warning(f"Supabase Auth error: {e}")
            raise
        except Exception:
            logger.exception("Unexpected error in sign_in_with_password")
            raise


