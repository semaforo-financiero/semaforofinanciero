class Family {
    id?: string;
    name: string;

    constructor(data: Family) {
        this.id = data.id;
        this.name = data.name;
    }
}

export default Family;
