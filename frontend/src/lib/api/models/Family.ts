interface Member {
    user_id: string;
    role: string;
    first_name?: string;
    last_name?: string;
    email?: string;
}

class Family {
    id?: string;
    name: string;
    created_by?: string;
    created_at?: string;
    members?: Member[];

    constructor(data: Family) {
        this.id = data.id;
        this.name = data.name;
        this.created_by = data.created_by;
        this.created_at = data.created_at;
        this.members = data.members;
    }
}

export default Family;
export type { Member };
