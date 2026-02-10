class User {
    private user_id?: string;
    private first_name: string;
    private last_name: string;
    private email: string;
    private password: string;

    constructor(data: User) {
        this.user_id = data.user_id;
        this.first_name = data.first_name;
        this.last_name = data.last_name;
        this.email = data.email;
        this.password = data.password;
    }
}

export default User;
