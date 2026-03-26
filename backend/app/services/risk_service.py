from __future__ import annotations

from fastapi import HTTPException
from supabase import Client
import numpy as np

from app.models.schemas.financial_snapshot_schema import FinancialSnapshotCreate
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.family_repository import FamilyRepository
from app.repositories.financial_snapshot_repository import FinancialSnapshotRepository
from app.repositories.income_repository import IncomeRepository
from app.repositories.profile_repository import ProfileRepository
from app.services.data_mining_service import DataMiningService
from app.services.expert_system_service import ExpertSystemService


class RiskService:
    def __init__(self, supabase: Client):
        self.income_repository = IncomeRepository(supabase)
        self.expense_repository = ExpenseRepository(supabase)
        self.family_repository = FamilyRepository(supabase)
        self.profile_repository = ProfileRepository(supabase)
        self.snapshot_repository = FinancialSnapshotRepository(supabase)

        self.expert_system_service = ExpertSystemService()
        self.data_mining_service = DataMiningService()

    def _get_nested_source(self, item: dict, key: str) -> dict:
        source = item.get(key)
        if isinstance(source, list):
            return source[0] if source else {}
        return source or {}

    def _normalize_employment_status(self, socioeconomic_profile: dict | None) -> str:
        if not socioeconomic_profile:
            return "UNKNOWN"
        return str(socioeconomic_profile.get("employment_status") or "UNKNOWN").upper()

    def _extract_years_working(self, socioeconomic_profile: dict | None) -> int | None:
        if not socioeconomic_profile:
            return None
        years_working = socioeconomic_profile.get("years_working")
        return int(years_working) if years_working is not None else None

    def _build_financial_profile(
        self,
        incomes: list[dict],
        expenses: list[dict],
        socioeconomic_profiles: list[dict] | None = None,
        analysis_scope: str = "USER",
    ) -> dict:
        total_income = sum(float(income.get("amount") or 0) for income in incomes)
        total_expense = sum(float(expense.get("amount") or 0) for expense in expenses)

        debt_expense_amount = 0.0
        fixed_expense_amount = 0.0
        variable_expense_amount = 0.0
        monthly_data = {}

        unique_income_sources = {
            income.get("income_source_id")
            for income in incomes
            if income.get("income_source_id")
        }

        variable_income_sources = {
            income.get("income_source_id")
            for income in incomes
            if str(self._get_nested_source(income, "income_sources").get("stability") or "").upper() == "VARIABLE"
        }

        income_periods = {
            (income.get("year"), income.get("month"))
            for income in incomes
            if income.get("year") is not None and income.get("month") is not None
        }

        expense_periods = {
            (expense.get("year"), expense.get("month"))
            for expense in expenses
            if expense.get("year") is not None and expense.get("month") is not None
        }

        for income in incomes:
            key = (income.get("year"), income.get("month"))
            monthly_data.setdefault(key, {"income": 0, "expense": 0})
            monthly_data[key]["income"] += float(income.get("amount") or 0)

        for expense in expenses:
            key = (expense.get("year"), expense.get("month"))
            monthly_data.setdefault(key, {"income": 0, "expense": 0})
            amount = float(expense.get("amount") or 0)
            monthly_data[key]["expense"] += amount
            source = self._get_nested_source(expense, "expense_sources")
            stability = str(source.get("stability") or "").upper()


            if bool(source.get("is_debt")):
                debt_expense_amount += amount

            if stability == "FIXED":
                fixed_expense_amount += amount
            elif stability == "VARIABLE":
                variable_expense_amount += amount

        savings = total_income - total_expense
        expense_ratio = total_expense / total_income if total_income > 0 else float(total_expense > 0)
        debt_ratio = debt_expense_amount / total_income if total_income > 0 else float(debt_expense_amount > 0)
        fixed_expense_ratio = fixed_expense_amount / total_income if total_income > 0 else float(fixed_expense_amount > 0)
        variable_expense_ratio = (
            variable_expense_amount / total_income if total_income > 0 else float(variable_expense_amount > 0)
        )
        savings_ratio = savings / total_income if total_income > 0 else 0.0
        months_analyzed = len(income_periods | expense_periods)
        total_income_sources = len(unique_income_sources)

        variable_income_sources_ratio = (
            len(variable_income_sources) / total_income_sources
            if total_income_sources > 0 else 0
        )

        normalized_profiles = socioeconomic_profiles or []
        employment_statuses = [
            self._normalize_employment_status(profile) for profile in normalized_profiles
        ]

        years_working_values = []
        for profile in normalized_profiles:
            years_working_value = self._extract_years_working(profile)
            if years_working_value is not None:
                years_working_values.append(years_working_value)

        employment_status = "UNKNOWN"
        if "UNEMPLOYED" in employment_statuses:
            employment_status = "UNEMPLOYED"
        elif "EMPLOYED" in employment_statuses:
            employment_status = "EMPLOYED"
        elif employment_statuses:
            employment_status = employment_statuses[0]

        years_working = min(years_working_values) if years_working_values else None
        incomes_list = [v["income"] for v in monthly_data.values()]
        
        income_variability = (
            np.std(incomes_list) / np.mean(incomes_list)
            if len(incomes_list) > 1 and np.mean(incomes_list) > 0 else 0
        )
        
        months_with_deficit = sum(
            1 for v in monthly_data.values() if v["expense"] > v["income"]
        )
        deficit_ratio = (
            months_with_deficit / len(monthly_data)
            if monthly_data else 0
        )

        expenses_list = [v["expense"] for v in monthly_data.values()]
        expense_trend = (
            expenses_list[-1] - expenses_list[0]
            if len(expenses_list) > 1 else 0
        )

        return {
            "analysis_scope": analysis_scope,
            "income": round(total_income, 2),
            "expense": round(total_expense, 2),
            "expense_ratio": round(expense_ratio, 4),
            "savings": round(savings, 2),
            "savings_ratio": round(savings_ratio, 4),
            "debt_expense_amount": round(debt_expense_amount, 2),
            "debt_ratio": round(debt_ratio, 4),
            "fixed_expense_amount": round(fixed_expense_amount, 2),
            "fixed_expense_ratio": round(fixed_expense_ratio, 4),
            "variable_expense_amount": round(variable_expense_amount, 2),
            "variable_expense_ratio": round(variable_expense_ratio, 4),
            "months_analyzed": months_analyzed,
            "variable_income_sources_ratio": round(variable_income_sources_ratio, 4),
            "employment_status": employment_status,
            "years_working": years_working,
            "income_variability": round(income_variability, 4),
            "deficit_ratio": round(deficit_ratio, 4),
            "expense_trend": round(expense_trend, 2),
        }

    def _save_snapshot(
        self,
        profile: dict,
        expert_result: dict,
        user_id: str | None = None,
        family_id: str | None = None,
    ) -> None:
        snapshot = FinancialSnapshotCreate(
            user_id=user_id,
            family_id=family_id,
            analysis_scope=profile["analysis_scope"],
            income=profile["income"],
            expense=profile["expense"],
            savings=profile["savings"],
            expense_ratio=profile["expense_ratio"],
            debt_expense_amount=profile["debt_expense_amount"],
            debt_ratio=profile["debt_ratio"],
            fixed_expense_amount=profile["fixed_expense_amount"],
            fixed_expense_ratio=profile["fixed_expense_ratio"],
            variable_expense_amount=profile["variable_expense_amount"],
            variable_expense_ratio=profile["variable_expense_ratio"],
            savings_ratio=profile["savings_ratio"],
            months_analyzed=profile["months_analyzed"],
            variable_income_sources_ratio=profile["variable_income_sources_ratio"],
            employment_status=profile["employment_status"],
            years_working=profile["years_working"],
            income_variability=profile["income_variability"],
            deficit_ratio=profile["deficit_ratio"],
            expense_trend=profile["expense_trend"],
            expert_risk=expert_result["risk"],
            expert_score=expert_result["score"],
        )
        self.snapshot_repository.create_snapshot(snapshot)

    def _combine_risk_results(self, expert_result: dict, mining_result: dict | None) -> dict:
        if not mining_result:
            return {
                **expert_result,
                "data_mining": None,
            }

        expert_score = expert_result["score"]
        mining_risk = str(mining_result["predicted_risk"]).upper()
        confidence = float(mining_result["confidence"])

        mining_score_map = {
            "LOW": 10,
            "MEDIUM": 35,
            "HIGH": 65,
        }

        mining_score = mining_score_map.get(mining_risk, 0)

        final_score = round((expert_score * 0.7) + (mining_score * 0.3 * confidence))
        final_score = max(final_score, 0)

        if final_score >= 60:
            final_risk = "HIGH"
        elif final_score >= 30:
            final_risk = "MEDIUM"
        else:
            final_risk = "LOW"

        return {
            "risk": final_risk,
            "score": final_score,
            "rules": expert_result["rules"],
            "recommendations": expert_result["recommendations"],
            "data_mining": mining_result,
        }

    def _build_response(
        self,
        profile: dict,
        result: dict,
        family_data: dict | None = None,
        member_count: int | None = None,
    ) -> dict:
        response = {
            "risk": result["risk"],
            "score": result["score"],
            "rules": result["rules"],
            "recommendations": result["recommendations"],
            "indicators": profile,
            "data_mining": result.get("data_mining"),
        }

        if family_data:
            response["family_id"] = family_data["id"]
            response["family_name"] = family_data["name"]
            response["member_count"] = member_count or 0

        return response

    def get_user_risk(self, user_id: str):
        incomes_res = self.income_repository.get_incomes_by_user(user_id)
        expenses_res = self.expense_repository.get_expenses_by_user(user_id)
        socioeconomic_profile = self.profile_repository.get_socioeconomic_profile(user_id)

        incomes = incomes_res.data or []
        expenses = expenses_res.data or []

        profile = self._build_financial_profile(
            incomes=incomes,
            expenses=expenses,
            socioeconomic_profiles=[socioeconomic_profile] if socioeconomic_profile else [],
            analysis_scope="USER",
        )

        expert_result = self.expert_system_service.evaluate_financial_risk(profile)

        self._save_snapshot(
            profile=profile,
            expert_result=expert_result,
            user_id=user_id,
        )

        mining_result = self.data_mining_service.predict_risk(profile)
        final_result = self._combine_risk_results(expert_result, mining_result)

        return self._build_response(
            profile=profile,
            result=final_result,
        )

    def get_family_risk(self, user_id: str):
        family = self.family_repository.get_family_by_user(user_id)
        if not family:
            raise HTTPException(status_code=404, detail="Family not found")

        members = family["members"]
        all_incomes: list[dict] = []
        all_expenses: list[dict] = []
        socioeconomic_profiles: list[dict] = []

        for member in members:
            member_id = member["user_id"]

            incomes_res = self.income_repository.get_incomes_by_user(member_id)
            expenses_res = self.expense_repository.get_expenses_by_user(member_id)
            socioeconomic_profile = self.profile_repository.get_socioeconomic_profile(member_id)

            all_incomes.extend(incomes_res.data or [])
            all_expenses.extend(expenses_res.data or [])

            if socioeconomic_profile:
                socioeconomic_profiles.append(socioeconomic_profile)

        profile = self._build_financial_profile(
            incomes=all_incomes,
            expenses=all_expenses,
            socioeconomic_profiles=socioeconomic_profiles,
            analysis_scope="FAMILY",
        )

        expert_result = self.expert_system_service.evaluate_financial_risk(profile)

        self._save_snapshot(
            profile=profile,
            expert_result=expert_result,
            family_id=family["id"],
        )

        mining_result = self.data_mining_service.predict_risk(profile)
        final_result = self._combine_risk_results(expert_result, mining_result)

        return self._build_response(
            profile=profile,
            result=final_result,
            family_data=family,
            member_count=len(members),
        )