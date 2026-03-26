import ExpenseAPI from "./expense/ExpenseAPI";
import ExpenseAmountAPI from "./expenseAmount/ExpenseAmountAPI";
import FamilyAPI from "./family/FamilyAPI";
import IncomeAPI from "./income/IncomeAPI";
import IncomeAmountAPI from "./incomeAmount/IncomeAmountAPI";
import InvitationAPI from "./invitations/InvitationAPI";
import RiskAPI from "./risk/RiskAPI";
import UserAPI from "./user/UserAPI";
import UserProfileAPI from "./userProfile/UserProfileAPI";

class API {
    user: UserAPI;
    profile: UserProfileAPI;
    family: FamilyAPI;
    invitation: InvitationAPI;
    income: IncomeAPI;
    expense: ExpenseAPI;
    incomeAmount: IncomeAmountAPI;
    expenseAmount: ExpenseAmountAPI;
    risk: RiskAPI;

    constructor() {
        this.user = new UserAPI();
        this.profile = new UserProfileAPI();
        this.family = new FamilyAPI();
        this.invitation = new InvitationAPI();
        this.income = new IncomeAPI();
        this.expense = new ExpenseAPI();
        this.incomeAmount = new IncomeAmountAPI();
        this.expenseAmount = new ExpenseAmountAPI();
        this.risk = new RiskAPI();
    }
}

const api = new API();

export default api;
