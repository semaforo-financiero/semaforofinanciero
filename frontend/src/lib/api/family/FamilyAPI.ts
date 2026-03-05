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

    async getFamily(token: string): Promise<Family> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/families";

        const response = await fetch(url, {
            method: "GET",
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(
                error.message ||
                    "Error al obtener la información de la familia",
            );
        }

        const familyData = await response.json();

        return new Family(familyData);
    }

    async inviteMember(email: string, token: string): Promise<void> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/families/invite";

        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${token}`,
            },
            body: JSON.stringify({
                email: email,
            }),
        });

        if (!response.ok) {
            throw new Error(response.status.toString());
        }
    }

    async removeMember(userId: string, token: string): Promise<void> {
        const url =
            import.meta.env.VITE_API_BASE_URL +
            `api/families/members/${userId}`;

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
                error.message || "Error al eliminar al miembro de la familia",
            );
        }
    }
}

export default FamilyAPI;
