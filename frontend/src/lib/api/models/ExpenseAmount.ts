class ExpenseAmount {
    id?: string;
    expense_source_id: string;
    amount: number | null;
    year: number;
    month: number;

    constructor(data: ExpenseAmount) {
        this.id = data.id;
        this.expense_source_id = data.expense_source_id;
        this.amount = data.amount;
        this.year = data.year;
        this.month = data.month;
    }
}

export default ExpenseAmount;
