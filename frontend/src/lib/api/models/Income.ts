enum STABILITY {
    VARIABLE = "VARIABLE",
    FIXED = "FIXED",
}

type Stability = `${STABILITY}`;

class Income {
    id?: string;
    name: string;
    stability: Stability;
    description: string;
    is_active?: boolean;
    user_id?: string;

    constructor(data: Income) {
        this.id = data.id;
        this.name = data.name;
        this.stability = data.stability;
        this.description = data.description;
        this.is_active = data.is_active;
        this.user_id = data.user_id;
    }
}

export default Income;
export { STABILITY, type Stability };
