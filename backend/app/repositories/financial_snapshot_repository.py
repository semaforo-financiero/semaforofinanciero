from __future__ import annotations

from supabase import Client

from app.models.schemas.financial_snapshot_schema import FinancialSnapshotCreate


class FinancialSnapshotRepository:
    TABLE_NAME = "financial_snapshots"

    def __init__(self, supabase: Client):
        self.supabase = supabase

    def create_snapshot(self, snapshot: FinancialSnapshotCreate):
        payload = snapshot.model_dump()
        return self.supabase.table(self.TABLE_NAME).insert(payload).execute()

    def get_all_snapshots(self):
        return self.supabase.table(self.TABLE_NAME).select("*").execute()

    def get_snapshots_by_user(self, user_id: str):
        return (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )

    def get_snapshots_by_family(self, family_id: str):
        return (
            self.supabase
            .table(self.TABLE_NAME)
            .select("*")
            .eq("family_id", family_id)
            .order("created_at", desc=True)
            .execute()
        )