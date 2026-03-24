import ExpenseAmount from "../models/ExpenseAmount";

class ExpenseAmountAPI {
    async create(expenseAmount: ExpenseAmount, token: string): Promise<string> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/expenses";

        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                expense_source_id: expenseAmount.expense_source_id,
                amount: expenseAmount.amount,
                year: expenseAmount.year,
                month: expenseAmount.month,
            }),
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(
                error.message || "Error en la creación del monto de gasto",
            );
        }

        const createdExpense = await response.json();

        return createdExpense.expense_source_id;
    }

    async get(token: string): Promise<ExpenseAmount[]> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/expenses";

        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(
                error.message ||
                    "Error en la obtención de los montos de gastos",
            );
        }

        const expensesData = await response.json();

        return expensesData.map(
            (expenseAmountData: ExpenseAmount) =>
                new ExpenseAmount(expenseAmountData),
        );
    }

    async update(
        expenseAmountId: string,
        amount: number,
        token: string,
    ): Promise<void> {
        const url =
            import.meta.env.VITE_API_BASE_URL +
            "api/expenses/" +
            expenseAmountId;

        const response = await fetch(url, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                amount: amount,
            }),
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(
                error.message || "Error en la actualización del monto de gasto",
            );
        }
    }
}

export default ExpenseAmountAPI;
