import FamilyAPI from "./family/FamilyAPI";
import IncomeAPI from "./income/IncomeAPI";
import InvitationAPI from "./invitations/InvitationAPI";
import UserAPI from "./user/UserAPI";
import UserProfileAPI from "./userProfile/UserProfileAPI";

class API {
    user: UserAPI;
    profile: UserProfileAPI;
    family: FamilyAPI;
    invitation: InvitationAPI;
    income: IncomeAPI;

    constructor() {
        this.user = new UserAPI();
        this.profile = new UserProfileAPI();
        this.family = new FamilyAPI();
        this.invitation = new InvitationAPI();
        this.income = new IncomeAPI();
    }
}

const api = new API();

export default api;
