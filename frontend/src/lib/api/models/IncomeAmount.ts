class IncomeAmount {
    id?: string;
    income_source_id: string;
    amount: number | null;
    year: number;
    month: number;

    constructor(data: IncomeAmount) {
        this.id = data.id;
        this.income_source_id = data.income_source_id;
        this.amount = data.amount;
        this.year = data.year;
        this.month = data.month;
    }
}

export default IncomeAmount;
