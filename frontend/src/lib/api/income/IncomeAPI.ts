import Income from "../models/Income";

class IncomeAPI {
    async create(income: Income, token: string): Promise<string> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/income-sources";

        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                name: income.name,
                stability: income.stability,
                description: income.description,
            }),
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(
                error.message || "Error en la creación del ingreso",
            );
        }

        const createdIncome = await response.json();

        return createdIncome.income_source_id;
    }

    async get(token: string): Promise<Income[]> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/income-sources";

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
                error.message || "Error en la obtención de los ingresos",
            );
        }

        const incomesData = await response.json();

        return incomesData.map((incomeData: Income) => new Income(incomeData));
    }

    async delete(incomeId: string, token: string): Promise<void> {
        const url =
            import.meta.env.VITE_API_BASE_URL +
            "api/income-sources/" +
            incomeId;

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
                error.message || "Error en la eliminación del ingreso",
            );
        }
    }
}

export default IncomeAPI;
