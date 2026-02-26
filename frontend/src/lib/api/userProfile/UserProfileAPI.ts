import UserProfile from "../models/UserProfile";

class UserProfileAPI {
    async get(token: string): Promise<UserProfile> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/profile";

        try {
            const response = await fetch(url, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });

            const profile = await response.json();

            return new UserProfile(profile);
        } catch (error) {
            throw new Error("Error al obtener el perfil");
        }
    }

    async update(token: string, updatedProfile: any): Promise<void> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/profile";

        try {
            await fetch(url, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
                body: JSON.stringify(updatedProfile),
            });
        } catch (error) {
            console.log("ERROR API: ", error);
            throw new Error("Error al actualizar el perfil");
        }
    }
}

export default UserProfileAPI;
