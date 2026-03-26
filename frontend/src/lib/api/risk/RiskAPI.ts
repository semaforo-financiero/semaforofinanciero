import Risk from "../models/Risk";

class RiskAPI {
    async getByUser(token: string): Promise<Risk> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/risk/user";

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
                    "Error en la obtención de los riesgos financieros del usuario",
            );
        }

        const riskData = await response.json();

        return new Risk(riskData);
    }

    async getByFamily(token: string): Promise<Risk> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/risk/family";

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
                    "Error en la obtención de los riesgos financieros de la familia",
            );
        }

        const riskData = await response.json();

        return new Risk(riskData);
    }
}

export default RiskAPI;
