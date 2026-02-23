<script setup lang="ts">
import { computed, onMounted, ref } from "vue";

import Input from "../../components/atoms/Input.vue";
import Select from "../../components/atoms/Select.vue";
import TextButton from "../../components/atoms/TextButton.vue";
import Warning from "../../assets/icons/Warning.vue";

import { STATE_OPTIONS } from "../../types/State";
import { GENDER_OPTIONS } from "../../types/Gender";
import { EDUCATION_LEVEL_OPTIONS } from "../../types/EducationLevel";
import { EMPLOYMENT_STATUS_OPTIONS } from "../../types/EmploymentStatus";
import { JOBS_OPTIONS } from "../../types/Job";

import type { StateMx } from "../../types/State";
import type { Gender } from "../../types/Gender";
import type { EducationLevel } from "../../types/EducationLevel";
import type { EmploymentStatus } from "../../types/EmploymentStatus";
import type { Job } from "../../types/Job";

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

type Props = {
    userProfileData: User;
};

const props = defineProps<Props>();
const emit = defineEmits(["submit", "cancel"]);

const user = ref<User | null>(null);

const hasWork = computed(() => {
    return (
        user.value?.employmentStatus === "EMPLOYED" ||
        user.value?.employmentStatus === "SELF_EMPLOYED"
    );
});

const thereAreChanges = computed(() => {
    return JSON.stringify(user.value) !== JSON.stringify(props.userProfileData);
});

const hasNullField = computed(() => {
    if (!user.value) {
        return false;
    }

    const requiredFields: (keyof User)[] = [
        "name",
        "email",
        "age",
        "gender",
        "state",
        "educationLevel",
        "employmentStatus",
    ];

    if (hasWork.value) {
        requiredFields.push("job", "antique");
    }

    return requiredFields.some((field) => user.value![field] === null);
});

const updateValue = (field: keyof User, value: unknown) => {
    if (user.value) {
        if (field === "age" || field === "antique") {
            (user.value as Record<string, unknown>)[field] =
                value === "" ? null : Number(value);
        } else {
            (user.value as Record<string, unknown>)[field] = value;
        }
    }
};

const handleGoHome = () => {
    emit("cancel");
};

const submit = () => {
    emit("submit", user.value);
};

onMounted(() => {
    user.value = JSON.parse(JSON.stringify(props.userProfileData));
});
</script>

<template>
    <section class="form">
        <div v-if="hasNullField" class="warning">
            <Warning />
            <p>
                Por favor, completa todos los campos para poder hacer uso del
                sistema
            </p>
        </div>

        <div class="item">
            <label for="age">Edad:</label>
            <Input
                id="age"
                type="number"
                placeholder="Ingresa tu edad"
                :modelValue="user?.age"
                @update:modelValue="updateValue('age', $event)"
            />
        </div>

        <div class="item">
            <label for="gender">Género:</label>
            <Select
                id="gender"
                placeholder="Selecciona tu género"
                :modelValue="user?.gender"
                :options="GENDER_OPTIONS"
                @update:modelValue="updateValue('gender', $event)"
            />
        </div>

        <div class="item">
            <label for="state">Estado:</label>
            <Select
                id="state"
                placeholder="Selecciona tu estado"
                :modelValue="user?.state"
                :options="STATE_OPTIONS"
                @update:modelValue="updateValue('state', $event)"
            />
        </div>

        <div class="item">
            <label for="educationLevel">Ultimo nivel de estudios:</label>
            <Select
                id="educationLevel"
                placeholder="Selecciona tu ultimo nivel de estudios"
                :modelValue="user?.educationLevel"
                :options="EDUCATION_LEVEL_OPTIONS"
                @update:modelValue="updateValue('educationLevel', $event)"
            />
        </div>

        <div class="item">
            <label for="employmentStatus">Situación laboral:</label>
            <Select
                id="employmentStatus"
                placeholder="Selecciona tu situación laboral"
                :modelValue="user?.employmentStatus"
                :options="EMPLOYMENT_STATUS_OPTIONS"
                @update:modelValue="updateValue('employmentStatus', $event)"
            />
        </div>

        <div v-if="hasWork" class="item">
            <label for="job">Empleo:</label>
            <Select
                id="job"
                placeholder="Selecciona la categoría de tu empleo"
                :modelValue="user?.job"
                :options="JOBS_OPTIONS"
                @update:modelValue="updateValue('job', $event)"
            />
        </div>

        <div v-if="hasWork" class="item">
            <label for="antique">Antigüedad laboral en años:</label>
            <Input
                id="antique"
                type="number"
                placeholder="Selecciona tu antigüedad laboral"
                :modelValue="user?.antique"
                @update:modelValue="updateValue('antique', $event)"
            />
        </div>
    </section>
    <div class="buttons">
        <TextButton variant="secondary" size="medium" @click="handleGoHome">
            Volver al inicio
        </TextButton>
        <TextButton
            variant="primary"
            size="medium"
            :disabled="!thereAreChanges"
            @click="submit"
        >
            Guardar cambios
        </TextButton>
    </div>
</template>

<style scoped>
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

    margin-top: 5rem;
    margin-right: 1rem;
}

.warning {
    grid-column: 1 / -1;
    display: flex;
    align-items: center;
    gap: 0.5rem;

    color: var(--color-red);
}
</style>
