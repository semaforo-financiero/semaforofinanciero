import UserAPI from "./user/UserAPI";
import UserProfileAPI from "./userProfile/UserProfileAPI";

class API {
    user: UserAPI;
    profile: UserProfileAPI;

    constructor() {
        this.user = new UserAPI();
        this.profile = new UserProfileAPI();
    }
}

const api = new API();

export default api;
