from supabase import create_client, Client
from app.core.settings import settings

import logging

logger = logging.getLogger(__name__)

def get_supabase_client() -> Client:
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise ValueError("Supabase environment variables not configured")

    try:
        return create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY
        )
    except Exception:
        logger.exception("Error creating Supabase client")
        raise


