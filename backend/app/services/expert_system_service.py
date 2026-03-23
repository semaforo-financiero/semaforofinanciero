from __future__ import annotations


class ExpertSystemService:
    def evaluate_financial_risk(self, data: dict) -> dict:
        triggered_rules: list[dict] = []

        def add_rule(
            code: str,
            severity: str,
            score: int,
            message: str,
            recommendation: str,
        ) -> None:
            triggered_rules.append(
                {
                    "code": code,
                    "severity": severity,
                    "score": score,
                    "message": message,
                    "recommendation": recommendation,
                }
            )

        expense_ratio = data["expense_ratio"]
        savings = data["savings"]
        income = data["income"]
        debt_ratio = data["debt_ratio"]
        variable_income_sources_ratio = data["variable_income_sources_ratio"]
        fixed_expense_ratio = data["fixed_expense_ratio"]
        variable_expense_ratio = data["variable_expense_ratio"]
        months_analyzed = data["months_analyzed"]
        savings_ratio = data["savings_ratio"]
        employment_status = data["employment_status"]
        years_working = data["years_working"]

        if income <= 0 and data["expense"] > 0:
            add_rule(
                code="NO_INCOME_WITH_EXPENSES",
                severity="HIGH",
                score=40,
                message="Se detectaron gastos registrados sin ingresos suficientes en el periodo analizado.",
                recommendation="Registra todas las fuentes de ingreso activas y prioriza la cobertura de gastos esenciales.",
            )

        if expense_ratio >= 1:
            add_rule(
                code="EXPENSES_EXCEED_INCOME",
                severity="HIGH",
                score=35,
                message="Los egresos superan o igualan los ingresos del periodo.",
                recommendation="Reduce gastos no esenciales y renegocia obligaciones fijas o de deuda.",
            )
        elif expense_ratio >= 0.9:
            add_rule(
                code="HIGH_EXPENSE_RATIO",
                severity="MEDIUM",
                score=20,
                message="Los egresos consumen casi todo el ingreso disponible.",
                recommendation="Crea un presupuesto con limite maximo del 90% del ingreso para gastos.",
            )

        if savings < 0:
            add_rule(
                code="NEGATIVE_SAVINGS",
                severity="HIGH",
                score=25,
                message="El ahorro neto del periodo es negativo.",
                recommendation="Deten gastos postergables y define una meta minima de ahorro mensual.",
            )
        elif savings_ratio >= 0.2:
            add_rule(
                code="HEALTHY_SAVINGS",
                severity="LOW",
                score=-10,
                message="El usuario mantiene un nivel de ahorro saludable respecto a sus ingresos.",
                recommendation="Mantener el habito de ahorro y fortalecer el fondo de emergencia.",
            )

        if debt_ratio >= 0.4:
            add_rule(
                code="HIGH_DEBT_LOAD",
                severity="HIGH",
                score=20,
                message="La carga de deuda representa una proporcion elevada del ingreso.",
                recommendation="Prioriza la amortizacion de deudas y evita adquirir nuevas obligaciones.",
            )
        elif debt_ratio >= 0.25:
            add_rule(
                code="MODERATE_DEBT_LOAD",
                severity="MEDIUM",
                score=10,
                message="La deuda ocupa una parte relevante del ingreso mensual.",
                recommendation="Monitorea los pagos de deuda y define un plan de reduccion progresiva.",
            )

        if variable_income_sources_ratio >= 0.7:
            add_rule(
                code="HIGH_VARIABLE_INCOME_DEPENDENCY",
                severity="MEDIUM",
                score=15,
                message="La mayoria de los ingresos dependen de fuentes variables o inestables.",
                recommendation="Diversifica ingresos y busca mayor estabilidad en las fuentes principales.",
            )
        elif variable_income_sources_ratio == 0 and income > 0:
            add_rule(
                code="STABLE_INCOME_PROFILE",
                severity="LOW",
                score=-5,
                message="Las fuentes de ingreso registradas se perciben estables.",
                recommendation="Mantener actualizadas las fuentes de ingreso y conservar respaldo financiero.",
            )

        if fixed_expense_ratio >= 0.7:
            add_rule(
                code="HIGH_FIXED_EXPENSE_RATIO",
                severity="MEDIUM",
                score=15,
                message="Los gastos fijos comprometen una parte alta del ingreso.",
                recommendation="Evalua servicios recurrentes y reduce compromisos fijos cuando sea posible.",
            )

        if variable_expense_ratio >= 0.5:
            add_rule(
                code="HIGH_VARIABLE_EXPENSE_RATIO",
                severity="MEDIUM",
                score=15,
                message="Los gastos variables representan una proporcion alta del ingreso.",
                recommendation="Controla gastos discrecionales y define topes mensuales para consumos variables.",
            )
        elif 0 < variable_expense_ratio <= 0.2 and savings >= 0:
            add_rule(
                code="CONTROLLED_VARIABLE_EXPENSES",
                severity="LOW",
                score=-5,
                message="Los gastos variables se mantienen en un rango controlado.",
                recommendation="Mantener seguimiento de gastos variables para evitar aumentos graduales.",
            )

        if employment_status == "UNEMPLOYED":
            add_rule(
                code="UNEMPLOYED",
                severity="HIGH",
                score=25,
                message="El perfil socioeconomico indica desempleo.",
                recommendation="Prioriza liquidez, reduce gastos fijos y evita nuevas deudas mientras no haya ingresos estables.",
            )

        if years_working is not None and years_working <= 1:
            add_rule(
                code="LOW_WORK_EXPERIENCE",
                severity="LOW",
                score=5,
                message="La experiencia laboral reportada es baja, lo que puede afectar la estabilidad del ingreso.",
                recommendation="Fortalece el fondo de emergencia para cubrir posibles variaciones en ingresos.",
            )

        if months_analyzed < 3:
            add_rule(
                code="LOW_HISTORY",
                severity="LOW",
                score=5,
                message="El historial financiero analizado aun es corto para inferencias robustas.",
                recommendation="Registra al menos tres meses consecutivos de movimientos para mejorar la precision.",
            )

        score = max(sum(rule["score"] for rule in triggered_rules), 0)

        if score >= 60:
            risk = "HIGH"
        elif score >= 30:
            risk = "MEDIUM"
        else:
            risk = "LOW"

        recommendations: list[str] = []
        for rule in triggered_rules:
            recommendation = rule["recommendation"]
            if recommendation not in recommendations:
                recommendations.append(recommendation)

        return {
            "risk": risk,
            "score": score,
            "rules": triggered_rules,
            "recommendations": recommendations
        }
