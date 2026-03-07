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
}

export default InvitationAPI;
