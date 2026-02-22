<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import ProfileForm from "../components/molecules/ProfileForm.vue";

import type { StateMx } from "../types/State";
import type { Gender } from "../types/Gender";
import type { EducationLevel } from "../types/EducationLevel";
import type { EmploymentStatus } from "../types/EmploymentStatus";
import type { Job } from "../types/Job";

// TODO: Change this to a real user object when model (from gateway) is ready
interface User {
    name: string;
    email: string;
    age: number | null;
    gender: Gender | null;
    state: StateMx | null;
    antique: number | null;
    educationLevel: EducationLevel | null;
    employmentStatus: EmploymentStatus | null;
    job: Job | null;
}

const router = useRouter();

const user = ref<User>();

const fetchUserData = async () => {
    // TODO: Fetch user data from API when endpoint is ready
    // and handle errors properly with toasterStore
    user.value = {
        name: "Manuel Rodriguez",
        email: "manuel.rodriguez@example.com",
        age: null,
        gender: "MALE",
        state: "ESTADO_DE_MEXICO",
        antique: 5,
        educationLevel: "BACHELOR",
        employmentStatus: "EMPLOYED",
        job: "TECHNOLOGY",
    };
};

const cancel = () => {
    router.push({ name: "home" });
};

const submit = (updatedUser: User) => {
    // TODO: Send updated user data to API when endpoint is ready
};

onMounted(() => {
    fetchUserData();
});
</script>

<template>
    <div class="profile-view">
        <h1 class="title">
            Bienvenido, <span>{{ user?.name }}</span>
        </h1>

        <span class="subtitle">Información de perfil</span>

        <div class="line" />

        <template v-if="user">
            <ProfileForm
                :userProfileData="user"
                @cancel="cancel"
                @submit="submit"
            />
        </template>
    </div>
</template>

<style scoped>
.profile-view {
    padding: 1.5rem;
}

.title {
    font-size: 1.5rem;
    font-weight: bold;

    margin-bottom: 0.5rem;
}

.title span {
    color: var(--primary-color-dark);
}

.subtitle {
    color: var(--text-color);
}

.line {
    width: 95%;
    height: 1px;

    margin: 1rem auto;

    background-color: var(--secondary-color-dark);
}
</style>
