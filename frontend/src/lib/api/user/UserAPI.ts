import User from "../models/User";

class UserAPI {
    async register(userData: User): Promise<User> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/auth/register";

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(userData),
            });

            const user = await response.json();

            return new User(user);
        } catch (error) {
            throw error;
        }
    }
}

export default UserAPI;
