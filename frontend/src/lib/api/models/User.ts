class User {
    private user_id?: string;
    private first_name?: string;
    private last_name?: string;
    private email: string;
    private password: string;
    private access_token?: string;
    private refresh_token?: string;

    constructor(data: User) {
        this.user_id = data.user_id;
        this.first_name = data.first_name;
        this.last_name = data.last_name;
        this.email = data.email;
        this.password = data.password;
        this.access_token = data.access_token;
        this.refresh_token = data.refresh_token;
    }

    get userId(): string | undefined {
        return this.user_id;
    }

    get firstName(): string | undefined {
        return this.first_name;
    }

    get lastName(): string | undefined {
        return this.last_name;
    }

    get userEmail(): string {
        return this.email;
    }

    get accessToken(): string | undefined {
        return this.access_token;
    }

    get refreshToken(): string | undefined {
        return this.refresh_token;
    }
}

export default User;
