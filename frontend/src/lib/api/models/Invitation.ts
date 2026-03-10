class Invitation {
    readonly id: string;
    readonly family_id: string;
    readonly invited_by: string;
    readonly invited_user_id: string;
    readonly invited_email: string;
    readonly invited_by_email: string;
    readonly status: string;
    readonly created_at: string;

    constructor(data: Invitation) {
        this.id = data.id;
        this.family_id = data.family_id;
        this.invited_by = data.invited_by;
        this.invited_user_id = data.invited_user_id;
        this.invited_email = data.invited_email;
        this.invited_by_email = data.invited_by_email;
        this.status = data.status;
        this.created_at = data.created_at;
    }
}

export default Invitation;
