import Expense from "../models/Expense";

class ExpenseAPI {
    async create(expense: Expense, token: string): Promise<string> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/expense-sources";

        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                name: expense.name,
                stability: expense.stability,
                is_debt: expense.is_debt,
                description: expense.description,
            }),
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.message || "Error en la creación del egreso");
        }

        const createdExpense = await response.json();

        return createdExpense.expense_source_id;
    }

    async get(token: string): Promise<Expense[]> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/expense-sources";

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
                error.message || "Error en la obtención de los egresos",
            );
        }

        const expensesData = await response.json();

        return expensesData.map(
            (expenseData: Expense) => new Expense(expenseData),
        );
    }

    async delete(expenseId: string, token: string): Promise<void> {
        const url =
            import.meta.env.VITE_API_BASE_URL +
            "api/expense-sources/" +
            expenseId;

        const response = await fetch(url, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(
                error.message || "Error en la eliminación del egreso",
            );
        }
    }
}

export default ExpenseAPI;
