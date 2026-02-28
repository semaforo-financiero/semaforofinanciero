import Family from "../models/Family";

class FamilyAPI {
    async create(name: string, token: string): Promise<string> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/families";

        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                name: name,
            }),
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(
                error.message || "Error en la creación de la familia",
            );
        }

        const family = await response.json();

        return family.id;
    }
}

export default FamilyAPI;
