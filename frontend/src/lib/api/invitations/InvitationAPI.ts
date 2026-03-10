import Invitation from "../models/Invitation";

class InvitationAPI {
    async getAll(token: string): Promise<Invitation[]> {
        try {
            const url =
                import.meta.env.VITE_API_BASE_URL + "api/families/invitations";

            const response = await fetch(url, {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            const invitationsData = await response.json();

            return invitationsData.map(
                (invitationData: Invitation) => new Invitation(invitationData),
            );
        } catch (error: any) {
            throw {
                status: error.status,
                message: error.message || "Error al obtener invitaciones",
            };
        }
    }

    async accept(token: string, familyId: string): Promise<void> {
        try {
            const url =
                import.meta.env.VITE_API_BASE_URL + `api/families/accept`;

            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ family_id: familyId }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw {
                    status: response.status,
                    message:
                        errorData.message || "Error al aceptar la invitación",
                };
            }
        } catch (error: any) {
            throw {
                status: error.status,
                message: error.message || "Error al aceptar la invitación",
            };
        }
    }

    async reject(token: string, familyId: string): Promise<void> {
        try {
            const url =
                import.meta.env.VITE_API_BASE_URL + `api/families/reject`;

            await fetch(url, {
                method: "PATCH",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify({ family_id: familyId }),
            });
        } catch (error: any) {
            throw {
                status: error.status,
                message: error.message || "Error al rechazar la invitación",
            };
        }
    }
}

export default InvitationAPI;
