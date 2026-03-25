import IncomeAmount from "../models/IncomeAmount";

class IncomeAmountAPI {
    async create(incomeAmount: IncomeAmount, token: string): Promise<string> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/income";

        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                income_source_id: incomeAmount.income_source_id,
                amount: incomeAmount.amount,
                year: incomeAmount.year,
                month: incomeAmount.month,
            }),
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(
                error.message || "Error en la creación del monto de ingreso",
            );
        }

        const createdIncome = await response.json();

        return createdIncome.income_source_id;
    }

    async get(token: string): Promise<IncomeAmount[]> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/income";

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
                    "Error en la obtención de los montos de ingresos",
            );
        }

        const incomesData = await response.json();

        return incomesData.map(
            (incomeAmountData: IncomeAmount) =>
                new IncomeAmount(incomeAmountData),
        );
    }

    async update(
        incomeAmountId: string,
        amount: number,
        token: string,
    ): Promise<void> {
        const url =
            import.meta.env.VITE_API_BASE_URL + "api/income/" + incomeAmountId;

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
                error.message ||
                    "Error en la actualización del monto de ingreso",
            );
        }
    }
}

export default IncomeAmountAPI;
