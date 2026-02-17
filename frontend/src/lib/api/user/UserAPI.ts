import User from "../models/User";

class UserAPI {
    async register(userData: User): Promise<User> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/auth/register";

        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(userData),
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.message || "Error en el registro");
        }

        const user = await response.json();
        return new User(user);
    }

    async login(userData: User): Promise<User> {
        const url = import.meta.env.VITE_API_BASE_URL + "api/auth/login";

        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(userData),
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.message || "Error en el inicio de sesión");
        }

        const user = await response.json();
        return new User(user);
    }
}

export default UserAPI;
