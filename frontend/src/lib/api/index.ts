import UserAPI from "./user/UserAPI";

class API {
    user: UserAPI;

    constructor() {
        this.user = new UserAPI();
    }
}

const api = new API();

export default api;
