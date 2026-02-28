<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";

import ProfileForm from "../components/molecules/ProfileForm.vue";
import api from "../lib/api";
import { useAuthStore } from "../stores/authStore";
import { toasterStore } from "../stores/toasterStore";

import type { StateMx } from "../types/State";
import type { Gender } from "../types/Gender";
import type { EducationLevel } from "../types/EducationLevel";
import type { EmploymentStatus } from "../types/EmploymentStatus";
import type { Job } from "../types/Job";
import type UserProfile from "../lib/api/models/UserProfile";

interface LocalUserProfile {
    id: string;
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
const authStore = useAuthStore();

const userProfile = ref<UserProfile | null>(null);
const user = ref<LocalUserProfile | null>(null);

const fetchUserData = async () => {
    try {
        const token = authStore.getAccessToken();

        if (!token) {
            throw new Error("No se encontró el token de autenticación");
        }

        userProfile.value = await api.profile.get(token);

        user.value = {
            id: userProfile.value.profile.id,
            name: userProfile.value.profile.first_name,
            email: userProfile.value.profile.email,
            age: userProfile.value.socioeconomic_profile?.age || null,
            gender: userProfile.value.socioeconomic_profile?.gender || null,
            state: userProfile.value.socioeconomic_profile?.state || null,
            antique:
                userProfile.value.socioeconomic_profile?.years_working || null,
            educationLevel:
                userProfile.value.socioeconomic_profile?.education_level ||
                null,
            employmentStatus:
                userProfile.value.socioeconomic_profile?.employment_status ||
                null,
            job: userProfile.value.socioeconomic_profile?.job_title || null,
        };
    } catch (error) {
        toasterStore.error(
            "Error al cargar el perfil",
            "Por favor inicia sesión nuevamente.",
        );
    }
};

const cancel = () => {
    router.push({ name: "home" });
};

const serializeUserProfile = (profile: LocalUserProfile) => {
    return {
        age: profile.age!,
        gender: profile.gender!,
        state: profile.state!,
        years_working: profile.antique!,
        education_level: profile.educationLevel!,
        employment_status: profile.employmentStatus!,
        job_title: profile.job!,
    };
};

const submit = async (updatedUser: LocalUserProfile) => {
    const token = authStore.getAccessToken();

    if (!token) {
        toasterStore.error(
            "Error al actualizar el perfil",
            "Por favor inicia sesión nuevamente.",
        );

        return;
    }

    try {
        await api.profile.update(token, serializeUserProfile(updatedUser));

        toasterStore.success(
            "Perfil actualizado",
            "Tu perfil ha sido actualizado correctamente.",
        );
    } catch (error) {
        toasterStore.error(
            "Error al actualizar el perfil",
            "Por favor intenta nuevamente.",
        );
    }
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
