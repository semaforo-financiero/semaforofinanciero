type Severity = "HIGH" | "MEDIUM" | "LOW";

interface Rule {
    code: string;
    severity: Severity;
    score: number;
    message: string;
    recommendation: string;
}

interface Indicators {
    analysis_scope: string;
    income: number;
    expense: number;
    savings: number;
    expense_ratio: number;
    debt_expense_amount: number;
    debt_ratio: number;
    fixed_expense_amount: number;
    fixed_expense_ratio: number;
    variable_expense_amount: number;
    variable_expense_ratio: number;
    savings_ratio: number;
    months_analyzed: number;
    variable_income_sources_ratio: number;
    employment_status: string;
    years_working: number;
}

class Risk {
    risk: string;
    score: number;
    rules: Rule[];
    recommendations: string[];
    indicators: Indicators;
    data_mining: unknown;
    family_id?: number;
    family_name?: string;
    member_count?: number;

    constructor(data: Risk) {
        this.risk = data.risk;
        this.score = data.score;
        this.rules = data.rules;
        this.recommendations = data.recommendations;
        this.indicators = data.indicators;
        this.data_mining = data.data_mining;
        this.family_id = data.family_id;
        this.family_name = data.family_name;
        this.member_count = data.member_count;
    }
}

export default Risk;
export type { Rule, Indicators, Severity };
