import type { EducationLevel } from "../../../types/EducationLevel";
import type { EmploymentStatus } from "../../../types/EmploymentStatus";
import type { Gender } from "../../../types/Gender";
import type { Job } from "../../../types/Job";
import type { StateMx } from "../../../types/State";

interface Profile {
    id: string;
    first_name: string;
    last_name: string;
    email: string;
}

interface SocioeconomicProfile {
    id: string;
    age: number;
    years_working: number;
    gender: Gender;
    state: StateMx;
    employment_status: EmploymentStatus;
    education_level: EducationLevel;
    job_title: Job;
}

class UserProfile {
    profile: Profile;
    socioeconomic_profile: SocioeconomicProfile | null;

    constructor(data: UserProfile) {
        this.profile = data.profile;
        this.socioeconomic_profile = data.socioeconomic_profile;
    }
}

export default UserProfile;
