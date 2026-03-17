import { type Stability } from "./Income";

class Expense {
    id?: string;
    name: string;
    stability: Stability;
    is_debt?: boolean;
    description: string;
    is_active?: boolean;
    user_id?: string;

    constructor(data: Expense) {
        this.id = data.id;
        this.name = data.name;
        this.stability = data.stability;
        this.is_debt = data.is_debt;
        this.description = data.description;
        this.is_active = data.is_active;
        this.user_id = data.user_id;
    }
}

export default Expense;
