<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import { toasterStore } from "../stores/toasterStore";

import Input from "../components/atoms/Input.vue";
import Select from "../components/atoms/Select.vue";
import TextButton from "../components/atoms/TextButton.vue";

import { STATE_OPTIONS } from "../types/State";
import { GENDER_OPTIONS } from "../types/Gender";
import { EDUCATION_LEVEL_OPTIONS } from "../types/EducationLevel";
import { EMPLOYMENT_STATUS_OPTIONS } from "../types/EmploymentStatus";
import { JOBS_OPTIONS } from "../types/Job";
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

const user = ref<User | null>(null);

const fetchUserData = async () => {
    // TODO: Fetch user data from API when endpoint is ready
    // and handle errors properly with toasterStore
    user.value = {
        name: "Manuel Rodriguez",
        email: "manuel.rodriguez@example.com",
        age: 30,
        gender: "MALE",
        state: "ESTADO_DE_MEXICO",
        antique: 5,
        educationLevel: "BACHELOR",
        employmentStatus: "EMPLOYED",
        job: "TECHNOLOGY",
    };
};

const hasWork = computed(() => {
    return (
        user.value?.employmentStatus === "EMPLOYED" ||
        user.value?.employmentStatus === "SELF_EMPLOYED"
    );
});

onMounted(() => {
    fetchUserData();
});

//HACER QUE LOS SELECTS E INPUTS SEAN CONTROLADOS Y PUEDAN GUARDAR LA INFORMACIÓN EN EL USUARIO, AUNQUE SEA SIMULADA, PARA PROBAR EL FUNCIONAMIENTO DE LOS COMPONENTES

//HACER QUE EL BOTON DE GUARDAR SE DESHABILITE SI NO HAY CAMBIOS EN LA INFORMACIÓN DEL USUARIO Y SE HABILITE CUANDO HAYA CAMBIOS

//HACER QUE LOS BOTONES DE GUARDAR Y VOLVER AL INICIO FUNCIONEN, EL DE VOLVER AL INICIO DEBE REDIRIGIR A LA PÁGINA PRINCIPAL Y EL DE GUARDAR DEBE MOSTRAR UN TOASTER DE ÉXITO SIMULANDO QUE SE GUARDÓ LA INFORMACIÓN CORRECTAMENTE

//HACER QUE LOS BOTONES ESTEN HASTA ABAJO DE LA PÁGINA Y NO SE MUEVAN CUANDO SE HAGA SCROLL, PARA QUE SIEMPRE ESTÉN A LA VISTA DEL USUARIO
</script>

<template>
    <div class="profile-view">
        <h1 class="title">
            Bienvenido, <span>{{ user?.name }}</span>
        </h1>
        <span class="subtitle">Información de perfil</span>

        <div class="line" />

        <section class="form">
            <div class="item">
                <label for="age">Edad:</label>
                <Input
                    id="age"
                    type="number"
                    placeholder="Ingresa tu edad"
                    :modelValue="user?.age"
                />
            </div>

            <div class="item">
                <label for="gender">Género:</label>
                <Select
                    id="gender"
                    placeholder="Selecciona tu género"
                    :modelValue="user?.gender"
                    :options="GENDER_OPTIONS"
                />
            </div>

            <div class="item">
                <label for="state">Estado:</label>
                <Select
                    id="state"
                    placeholder="Selecciona tu estado"
                    :modelValue="user?.state"
                    :options="STATE_OPTIONS"
                />
            </div>

            <div class="item">
                <label for="educationLevel">Ultimo nivel de estudios:</label>
                <Select
                    id="educationLevel"
                    placeholder="Selecciona tu ultimo nivel de estudios"
                    :modelValue="user?.educationLevel"
                    :options="EDUCATION_LEVEL_OPTIONS"
                />
            </div>

            <div class="item">
                <label for="employmentStatus">Situación laboral:</label>
                <Select
                    id="employmentStatus"
                    placeholder="Selecciona tu situación laboral"
                    :modelValue="user?.employmentStatus"
                    :options="EMPLOYMENT_STATUS_OPTIONS"
                />
            </div>

            <div v-if="hasWork" class="item">
                <label for="job">Empleo:</label>
                <Select
                    id="job"
                    placeholder="Selecciona la categoría de tu empleo"
                    :modelValue="user?.job"
                    :options="JOBS_OPTIONS"
                />
            </div>

            <div v-if="hasWork" class="item">
                <label for="antique">Antigüedad laboral en años:</label>
                <Input
                    id="antique"
                    type="number"
                    placeholder="Selecciona tu antigüedad laboral"
                    :modelValue="user?.antique"
                />
            </div>
        </section>
        <div class="buttons">
            <TextButton variant="secondary" size="medium">
                Volver al inicio
            </TextButton>
            <TextButton variant="primary" size="medium">
                Guardar cambios
            </TextButton>
        </div>
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

.form {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;

    width: 80%;

    margin: 1rem auto;
}

.item {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.buttons {
    display: flex;
    justify-self: right;
    gap: 1rem;

    width: 30rem;
}
</style>
