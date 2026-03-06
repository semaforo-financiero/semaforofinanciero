<script setup lang="ts">
import { onMounted, ref } from "vue";

import api from "../lib/api";
import { useAuthStore } from "../stores/authStore";
import { toasterStore } from "../stores/toasterStore";
import { useRouter } from "vue-router";

import TwoPersons from "../assets/icons/TwoPersons.vue";
import House from "../assets/icons/House.vue";
import CurrencySimbol from "../assets/icons/CurrencySimbol.vue";
import Pulse from "../assets/icons/Pulse.vue";
import Shield from "../assets/icons/Shield.vue";
import PersonPlus from "../assets/icons/PersonPlus.vue";
import Spinner from "../components/atoms/Spinner.vue";
import type Invitation from "../lib/api/models/Invitation";

const authStore = useAuthStore();
const router = useRouter();

const familyName = ref("");
const isLoading = ref(false);
const invitations = ref<Invitation[]>([]);

const createFamily = async () => {
    if (!familyName.value.trim()) {
        return;
    }

    try {
        isLoading.value = true;

        const token = authStore.getAccessToken();

        await api.family.create(familyName.value.trim(), token || "");

        toasterStore.success(
            "Familia creada",
            "La familia se ha creado correctamente.",
        );

        router.push({ name: "family" });
    } catch (error) {
        toasterStore.error(
            "Error al crear la familia",
            "Por favor intenta nuevamente.",
        );
    } finally {
        isLoading.value = false;
    }
};

const getInvitations = async () => {
    try {
        const token = authStore.getAccessToken();

        if (!token) {
            throw new Error("No se encontró el token de autenticación");
        }

        invitations.value = await api.invitation.getAll(token);
    } catch (error) {
        toasterStore.error(
            "Error al cargar las invitaciones",
            "No se pudieron obtener las invitaciones pendientes. Por favor intenta de nuevo mas tarde.",
        );
    }
};

onMounted(() => {
    getInvitations();
});
</script>

<template>
    <div v-if="invitations.length > 0" class="invitations-container">
        <ul class="invitations-list">
            <li
                v-for="invitation in invitations"
                class="invitation-item"
                :key="invitation.id"
            >
                <p>
                    {{ invitation.invited_email }} te ha invitado a unirte a su
                    familia
                </p>
                <div class="actions-invitation">
                    <button class="accept-button" @click="">Aceptar</button>
                    <button class="decline-button" @click="">Rechazar</button>
                </div>
            </li>
        </ul>
    </div>

    <div class="family-view">
        <div class="family-info">
            <div class="family-info__icon-wrapper">
                <TwoPersons />
            </div>

            <h1 class="family-info__title">
                <span class="family-info__title-icon">
                    <House />
                </span>
                ¿Qué es una familia?
            </h1>

            <p class="family-info__description">
                En <strong>Semáforo Financiero</strong>, una familia es un grupo
                de usuarios que comparten sus finanzas y objetivos financieros.
                Al crear una familia, puedes invitar a tus seres queridos a
                unirse y colaborar en la gestión de sus finanzas.
            </p>

            <div class="family-info__features">
                <div class="family-info__feature">
                    <div class="family-info__feature-icon">
                        <CurrencySimbol />
                    </div>
                    <div class="family-info__feature-text">
                        <strong>Gastos compartidos</strong>
                        <span
                            >Gestiona los gastos del hogar de forma
                            conjunta</span
                        >
                    </div>
                </div>

                <div class="family-info__feature">
                    <div
                        class="family-info__feature-icon family-info__feature-icon--secondary"
                    >
                        <Pulse />
                    </div>
                    <div class="family-info__feature-text">
                        <strong>Metas financieras</strong>
                        <span>Establezcan objetivos y alcáncenlos juntos</span>
                    </div>
                </div>

                <div class="family-info__feature">
                    <div
                        class="family-info__feature-icon family-info__feature-icon--dark"
                    >
                        <Shield />
                    </div>
                    <div class="family-info__feature-text">
                        <strong>Estabilidad financiera</strong>
                        <span>Apóyense mutuamente en su camino financiero</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="create-family">
            <div class="create-family__header">
                <PersonPlus />
                <h2>Crear tu familia</h2>
            </div>

            <p class="create-family__subtitle">
                Dale un nombre a tu familia para comenzar a colaborar en sus
                finanzas.
            </p>

            <div class="create-family__form">
                <label class="create-family__label" for="familyName">
                    Nombre de la familia
                </label>

                <div class="create-family__input-wrapper">
                    <TwoPersons class="create-family__input-icon" />
                    <input
                        v-model="familyName"
                        id="familyName"
                        type="text"
                        class="create-family__input"
                        placeholder="Escribe el nombre de tu familia"
                        autofocus
                        autocomplete="off"
                    />
                </div>

                <button
                    class="create-family__button"
                    :class="{ 'create-family__button--loading': isLoading }"
                    :disabled="isLoading || !familyName.trim()"
                    @click="createFamily"
                >
                    <svg
                        v-if="!isLoading"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        stroke-width="2"
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        width="18"
                        height="18"
                    >
                        <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                        <circle cx="8.5" cy="7" r="4" />
                        <line x1="20" y1="8" x2="20" y2="14" />
                        <line x1="23" y1="11" x2="17" y2="11" />
                    </svg>

                    <Spinner v-else />

                    {{ isLoading ? "Creando familia..." : "Crear familia" }}
                </button>
            </div>

            <div class="create-family__bottom-bar">
                <div
                    class="create-family__bar-segment create-family__bar-segment--green"
                ></div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.family-view {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 2rem;
    max-width: 960px;
    margin: 2.5rem auto;
    padding: 0 1.5rem;
    overflow: hidden;
}

@media (min-width: 768px) {
    .family-view {
        flex-direction: row;
        align-items: flex-start;
        gap: 2.5rem;
        margin: 3.5rem auto;
    }
}

.family-info {
    position: relative;
    z-index: 1;
    flex: 1.2;
    background: var(--color-white, #fff);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    box-shadow:
        0 1px 3px rgba(0, 0, 0, 0.06),
        0 8px 24px rgba(0, 0, 0, 0.04);
    border: 1px solid rgba(0, 0, 0, 0.04);
}

.family-info__icon-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 56px;
    height: 56px;
    border-radius: 16px;
    background: linear-gradient(
        135deg,
        var(--primary-color, #43a047),
        var(--primary-color-light, #66bb6a)
    );
    color: var(--color-white, #fff);
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 12px rgba(67, 160, 71, 0.3);
}

.family-info__icon {
    width: 28px;
    height: 28px;
}

.family-info__title {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-color, #212121);
    margin-bottom: 1rem;
    line-height: 1.3;
}

.family-info__title-icon {
    display: flex;
    align-items: center;
    color: var(--primary-color, #43a047);
}

.family-info__description {
    font-size: 0.95rem;
    line-height: 1.65;
    color: var(--neutral-light, #6b7280);
    margin-bottom: 2rem;
}

.family-info__description strong {
    color: var(--primary-color-dark, #388e3c);
    font-weight: 600;
}

.family-info__features {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.family-info__feature {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 1rem;
    border-radius: 14px;
    background: var(--background-color, #f7f7f7);
    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.family-info__feature:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
}

.family-info__feature-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 42px;
    height: 42px;
    min-width: 42px;
    border-radius: 12px;
    background: rgba(67, 160, 71, 0.1);
    color: var(--primary-color, #43a047);
}

.family-info__feature-icon--secondary {
    background: rgba(0, 98, 133, 0.1);
    color: var(--secondary-color, #006285);
}

.family-info__feature-icon--dark {
    background: rgba(56, 142, 60, 0.1);
    color: var(--primary-color-dark, #388e3c);
}

.family-info__feature-text {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}

.family-info__feature-text strong {
    font-size: 0.9rem;
    font-weight: 600;
    color: var(--text-color, #212121);
}

.family-info__feature-text span {
    font-size: 0.82rem;
    color: var(--neutral-light, #6b7280);
    line-height: 1.4;
}

.create-family {
    position: relative;
    z-index: 1;
    flex: 0.8;
    background: var(--color-white, #fff);
    border-radius: 20px;
    padding: 2.5rem 2rem 0;
    box-shadow:
        0 1px 3px rgba(0, 0, 0, 0.06),
        0 8px 24px rgba(0, 0, 0, 0.04);
    border: 1px solid rgba(0, 0, 0, 0.04);
    overflow: hidden;
}

.create-family__header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 0.5rem;
}

.create-family__header-icon {
    color: var(--secondary-color, #006285);
}

.create-family__header h2 {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text-color, #212121);
}

.create-family__subtitle {
    font-size: 0.88rem;
    color: var(--neutral-light, #6b7280);
    line-height: 1.5;
    margin-bottom: 1.75rem;
}

.create-family__form {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.create-family__label {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-color, #212121);
}

.create-family__input-wrapper {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0 1rem;
    height: 48px;
    border-radius: 12px;
    border: 2px solid var(--color-gray-light, #dedede);
    background: var(--background-color, #f7f7f7);
    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}

.create-family__input-wrapper:focus-within {
    border-color: var(--primary-color, #43a047);
    box-shadow: 0 0 0 3px rgba(67, 160, 71, 0.15);
    background: var(--color-white, #fff);
}

.create-family__input-icon {
    color: var(--neutral-light, #6b7280);
    flex-shrink: 0;
}

.create-family__input-wrapper:focus-within .create-family__input-icon {
    color: var(--primary-color, #43a047);
}

.create-family__input {
    flex: 1;
    border: none;
    outline: none;
    background: transparent;
    font-size: 0.92rem;
    font-family: inherit;
    color: var(--text-color, #212121);
}

.create-family__input::placeholder {
    color: #b0b0b0;
}

.create-family__button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.6rem;
    width: 100%;
    height: 48px;
    margin-top: 0.5rem;
    margin-bottom: 2rem;
    border: none;
    border-radius: 12px;
    background: linear-gradient(
        135deg,
        var(--primary-color, #43a047),
        var(--primary-color-dark, #388e3c)
    );
    color: var(--color-white, #fff);
    font-size: 0.95rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition:
        transform 0.15s ease,
        box-shadow 0.2s ease,
        opacity 0.2s ease;
    box-shadow: 0 4px 14px rgba(67, 160, 71, 0.35);
}

.create-family__button:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(67, 160, 71, 0.45);
}

.create-family__button:active:not(:disabled) {
    transform: translateY(0);
}

.create-family__button:disabled {
    opacity: 0.55;
    cursor: not-allowed;
}

.create-family__button--loading {
    background: linear-gradient(
        135deg,
        var(--secondary-color, #006285),
        var(--secondary-color-dark, #004c6d)
    );
    box-shadow: 0 4px 14px rgba(0, 98, 133, 0.35);
}

.create-family__bottom-bar {
    display: flex;
    height: 5px;
    margin: 0 -2rem;
}

.create-family__bar-segment {
    flex: 1;
}

.create-family__bar-segment--green {
    background: var(--primary-color, #43a047);
}

.invitations-container {
    width: 100%;
    max-width: 960px;
    margin: 2rem auto;
    padding: 0 1.5rem;
}

.invitations-list {
    list-style: none;
    padding: 0;
    margin: 0 0 2rem 0;
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.invitation-item {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1.5rem;
    background: var(--color-white, #fff);
    border-radius: 16px;
    border: 2px solid var(--primary-color, #43a047);
    border-left: 10px solid var(--primary-color, #43a047);
    box-shadow:
        0 2px 8px rgba(67, 160, 71, 0.1),
        0 4px 16px rgba(0, 0, 0, 0.04);
    transition:
        transform 0.2s ease,
        box-shadow 0.2s ease;
}

.invitation-item:hover {
    transform: translateY(-2px);
    box-shadow:
        0 4px 12px rgba(67, 160, 71, 0.15),
        0 8px 24px rgba(0, 0, 0, 0.08);
}

.invitation-item p {
    margin: 0;
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text-color, #212121);
    line-height: 1.6;
}

.actions-invitation {
    display: flex;
    gap: 0.75rem;
    justify-content: flex-end;
    flex-wrap: wrap;
}

.accept-button,
.decline-button {
    padding: 0.6rem 1.5rem;
    border: none;
    border-radius: 10px;
    font-size: 0.85rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition:
        transform 0.15s ease,
        box-shadow 0.2s ease,
        opacity 0.2s ease;
    white-space: nowrap;
}

.accept-button {
    background: linear-gradient(
        135deg,
        var(--primary-color, #43a047),
        var(--primary-color-dark, #388e3c)
    );
    color: var(--color-white, #fff);
    box-shadow: 0 4px 12px rgba(67, 160, 71, 0.3);
}

.accept-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(67, 160, 71, 0.4);
}

.accept-button:active {
    transform: translateY(0);
}

.decline-button {
    background: var(--background-color, #f7f7f7);
    color: var(--text-color, #212121);
    border: 1.5px solid var(--color-gray-light, #dedede);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.decline-button:hover {
    background: var(--color-white, #fff);
    border-color: #c0c0c0;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.decline-button:active {
    transform: translateY(0);
}

@media (min-width: 768px) {
    .invitation-item {
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
    }

    .invitation-item p {
        flex: 1;
        margin: 0;
    }

    .actions-invitation {
        justify-content: flex-end;
        flex-shrink: 0;
    }
}
</style>
