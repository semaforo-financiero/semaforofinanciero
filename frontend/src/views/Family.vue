<script setup lang="ts">
import { ref, onMounted, computed } from "vue";

import api from "../lib/api";
import { useAuthStore } from "../stores/authStore";
import { toasterStore } from "../stores/toasterStore";
import type Family from "../lib/api/models/Family";
import type { Member } from "../lib/api/models/Family";

import House from "../assets/icons/House.vue";
import TwoPersons from "../assets/icons/TwoPersons.vue";
import Calendar from "../assets/icons/Calendar.vue";
import PaperFly from "../assets/icons/PaperFly.vue";
import Spinner from "../components/atoms/Spinner.vue";
import Trash from "../assets/icons/Trash.vue";
import PersonPlus from "../assets/icons/PersonPlus.vue";
import { useRouter } from "vue-router";

const authStore = useAuthStore();
const router = useRouter();

const family = ref<Family | null>(null);
const isLoading = ref(true);
const inviteEmail = ref("");
const isInviting = ref(false);
const removingMemberId = ref<string | null>(null);
const showInviteForm = ref(false);

const memberCount = computed(() => family.value?.members?.length);

const getInitials = (name: string) => {
    return name
        .split(" ")
        .map((n) => n[0])
        .join("")
        .toUpperCase()
        .slice(0, 2);
};

const getAvatarColor = (name: string) => {
    const colors = [
        { bg: "rgba(67, 160, 71, 0.12)", text: "#388e3c" },
        { bg: "rgba(0, 98, 133, 0.12)", text: "#006285" },
        { bg: "rgba(102, 187, 106, 0.15)", text: "#2e7d32" },
        { bg: "rgba(0, 76, 109, 0.12)", text: "#004c6d" },
        { bg: "rgba(56, 142, 60, 0.12)", text: "#1b5e20" },
    ];

    const index = name.charCodeAt(0) % colors.length;

    return colors[index];
};

const fetchFamily = async () => {
    isLoading.value = true;

    try {
        const token = authStore.getAccessToken();

        if (!token) {
            throw new Error("No se encontró el token de autenticación");
        }

        family.value = await api.family.getFamily(token);
    } catch (error) {
        router.push({ name: "create-family" });
    } finally {
        isLoading.value = false;
    }
};

const inviteMember = async () => {
    if (!inviteEmail.value.trim()) return;

    try {
        isInviting.value = true;
        const token = authStore.getAccessToken();

        if (!token) {
            throw new Error("No se encontró el token de autenticación");
        }

        await api.family.inviteMember(inviteEmail.value.trim(), token);

        toasterStore.success(
            "Miembro invitado",
            `Invitación enviada a ${inviteEmail.value}`,
        );

        inviteEmail.value = "";
    } catch (error) {
        switch (error) {
            case "404":
                toasterStore.error(
                    "Usuario no encontrado",
                    "No se encontró un usuario con ese correo. Verifica que el correo sea correcto e intenta de nuevo.",
                );
                break;
            case "400":
                toasterStore.error(
                    "Usuario ya invitado",
                    "Este usuario ya ha sido invitado a la familia o ya es miembro. Verifica el correo e intenta de nuevo.",
                );
                break;
            default:
                toasterStore.error(
                    "Error al invitar al miembro",
                    "No se pudo invitar al miembro a la familia. Por favor intenta de nuevo mas tarde.",
                );
                break;
        }
    } finally {
        isInviting.value = false;
    }
};

const removeMember = async (member: Member) => {
    if (member.role === "admin") return;

    try {
        const token = authStore.getAccessToken();

        if (!token) {
            throw new Error("No se encontró el token de autenticación");
        }

        await api.family.removeMember(member.user_id, token);

        if (family.value) {
            family.value.members = family.value.members?.filter(
                (m) => m.user_id !== member.user_id,
            );
        }

        toasterStore.success(
            "Miembro eliminado",
            `${member.first_name} ha sido eliminado de la familia.`,
        );
    } catch (error) {
        toasterStore.error(
            "Error al eliminar al miembro",
            `No se pudo eliminar a ${member.first_name} de la familia. Por favor intenta de nuevo mas tarde.`,
        );
    }
};

onMounted(() => {
    fetchFamily();
});
</script>

<template>
    <div class="family-view">
        <template v-if="isLoading">
            <div class="skeleton-card">
                <div class="skeleton skeleton--title"></div>
                <div class="skeleton skeleton--text"></div>
                <div class="skeleton skeleton--text skeleton--short"></div>
                <div
                    v-for="i in 3"
                    class="skeleton skeleton--member"
                    :key="i"
                ></div>
            </div>
        </template>

        <template v-else-if="family">
            <div class="family-header">
                <div class="family-header__top">
                    <div class="family-header__icon-wrapper">
                        <House />
                    </div>
                    <div class="family-header__info">
                        <h1 class="family-header__name">{{ family.name }}</h1>
                        <p class="family-header__meta">
                            <TwoPersons width="16" height="16" />
                            {{ memberCount }}
                            {{ memberCount === 1 ? "miembro" : "miembros" }}
                            <span class="family-header__separator">|</span>
                            <Calendar />
                            Creada el
                            {{
                                new Date(
                                    family.created_at || new Date(),
                                ).toLocaleDateString("es-MX", {
                                    year: "numeric",
                                    month: "long",
                                    day: "numeric",
                                })
                            }}
                        </p>
                    </div>
                </div>

                <div class="family-header__accent">
                    <div
                        class="family-header__accent-segment family-header__accent-segment--green"
                    />
                </div>
            </div>

            <div class="family-content">
                <div class="members-card">
                    <div class="members-card__header">
                        <div class="members-card__header-left">
                            <TwoPersons width="24" height="24" />
                            <h2>Miembros</h2>
                        </div>
                        <button
                            class="members-card__invite-toggle"
                            @click="showInviteForm = !showInviteForm"
                        >
                            <template v-if="!showInviteForm">+</template>
                            {{ showInviteForm ? "Cancelar" : "Invitar" }}
                        </button>
                    </div>

                    <Transition name="slide">
                        <div v-if="showInviteForm" class="invite-form">
                            <div class="invite-form__inner">
                                <p class="invite-form__label">
                                    Ingresa el correo del usuario que deseas
                                    invitar
                                </p>
                                <div class="invite-form__row">
                                    <div class="invite-form__input-wrapper">
                                        @
                                        <input
                                            v-model="inviteEmail"
                                            type="email"
                                            class="invite-form__input"
                                            placeholder="correo@ejemplo.com"
                                            @keyup.enter="inviteMember"
                                        />
                                    </div>
                                    <button
                                        class="invite-form__button"
                                        :disabled="
                                            isInviting || !inviteEmail.trim()
                                        "
                                        @click="inviteMember"
                                    >
                                        <PaperFly v-if="!isInviting" />
                                        <Spinner v-else />
                                        {{
                                            isInviting
                                                ? "Enviando..."
                                                : "Enviar"
                                        }}
                                    </button>
                                </div>
                            </div>
                        </div>
                    </Transition>

                    <div class="members-list">
                        <TransitionGroup name="member">
                            <div
                                v-for="member in family.members"
                                class="member-row"
                                :key="member.user_id"
                                :class="{
                                    'member-row--removing':
                                        removingMemberId === member.user_id,
                                }"
                            >
                                <div class="member-row__left">
                                    <div
                                        class="member-row__avatar"
                                        :style="{
                                            backgroundColor: getAvatarColor(
                                                member.first_name!,
                                            )!.bg,
                                            color: getAvatarColor(
                                                member.first_name!,
                                            )!.text,
                                        }"
                                    >
                                        {{ getInitials(member.first_name!) }}
                                    </div>
                                    <div class="member-row__info">
                                        <div class="member-row__name-row">
                                            <span class="member-row__name">
                                                {{ member.first_name }}
                                            </span>
                                            <span
                                                v-if="member.role === 'admin'"
                                                class="member-row__badge"
                                            >
                                                Admin
                                            </span>
                                        </div>
                                        <span class="member-row__email">{{
                                            member.email
                                        }}</span>
                                    </div>
                                </div>
                                <button
                                    v-if="member.role !== 'admin'"
                                    class="member-row__remove"
                                    :disabled="
                                        removingMemberId === member.user_id
                                    "
                                    @click="removeMember(member)"
                                    :title="`Eliminar a ${member.first_name}`"
                                >
                                    <Trash
                                        v-if="
                                            removingMemberId !== member.user_id
                                        "
                                    />
                                    <Spinner v-else />
                                </button>
                            </div>
                        </TransitionGroup>
                    </div>

                    <div
                        v-if="family.members?.length === 0"
                        class="members-empty"
                    >
                        <div class="members-empty__icon">
                            <PersonPlus width="40" height="40" />
                        </div>
                        <p class="members-empty__text">
                            Aun no hay miembros en tu familia
                        </p>
                        <p class="members-empty__sub">
                            Invita a tus seres queridos usando su correo
                            electronico
                        </p>
                    </div>
                </div>
            </div>
        </template>
    </div>
</template>

<style scoped>
.family-view {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    max-width: 720px;
    margin: 2.5rem auto;
    padding: 0 1.5rem;
}

.blob {
    position: fixed;
    width: 500px;
    height: 500px;
    z-index: 0;
    pointer-events: none;
}

.blob--top-right {
    top: -120px;
    right: -120px;
}

.blob--bottom-left {
    bottom: -150px;
    left: -150px;
}

.alert {
    position: relative;
    z-index: 2;
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.85rem 1.15rem;
    border-radius: 12px;
    font-size: 0.88rem;
    font-weight: 500;
    line-height: 1.4;
}

.alert--success {
    background: rgba(67, 160, 71, 0.08);
    border: 1px solid rgba(67, 160, 71, 0.2);
    color: var(--primary-color-dark, #388e3c);
}

.alert--error {
    background: rgba(211, 47, 47, 0.06);
    border: 1px solid rgba(211, 47, 47, 0.18);
    color: #c62828;
}

.alert__close {
    margin-left: auto;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 24px;
    height: 24px;
    border: none;
    background: transparent;
    color: inherit;
    cursor: pointer;
    border-radius: 6px;
    opacity: 0.6;
    transition: opacity 0.15s;
}

.alert__close:hover {
    opacity: 1;
}

.alert-enter-active,
.alert-leave-active {
    transition: all 0.3s ease;
}

.alert-enter-from,
.alert-leave-to {
    opacity: 0;
    transform: translateY(-8px);
}

.family-header {
    position: relative;
    z-index: 1;
    background: var(--color-white, #fff);
    border-radius: 20px;
    padding: 2rem 2rem 0;
    box-shadow:
        0 1px 3px rgba(0, 0, 0, 0.06),
        0 8px 24px rgba(0, 0, 0, 0.04);
    border: 1px solid rgba(0, 0, 0, 0.04);
    overflow: hidden;
}

.family-header__top {
    display: flex;
    align-items: center;
    gap: 1.25rem;
    padding-bottom: 1.75rem;
}

.family-header__icon-wrapper {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 56px;
    height: 56px;
    min-width: 56px;
    border-radius: 16px;
    background: linear-gradient(
        135deg,
        var(--primary-color, #43a047),
        var(--primary-color-light, #66bb6a)
    );
    color: var(--color-white, #fff);
    box-shadow: 0 4px 12px rgba(67, 160, 71, 0.3);
}

.family-header__info {
    display: flex;
    flex-direction: column;
    gap: 0.35rem;
}

.family-header__name {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text-color, #212121);
    line-height: 1.25;
}

.family-header__meta {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    font-size: 0.82rem;
    color: var(--neutral-light, #6b7280);
    flex-wrap: wrap;
}

.family-header__separator {
    opacity: 0.3;
    margin: 0 0.15rem;
}

.family-header__accent {
    display: flex;
    height: 4px;
    margin: 0 -2rem;
}

.family-header__accent-segment {
    flex: 1;
}

.family-header__accent-segment--green {
    background: var(--primary-color, #43a047);
}

.family-header__accent-segment--blue {
    background: var(--secondary-color, #006285);
}

.family-header__accent-segment--green-light {
    background: var(--primary-color-light, #66bb6a);
}

.members-card {
    position: relative;
    z-index: 1;
    background: var(--color-white, #fff);
    border-radius: 20px;
    box-shadow:
        0 1px 3px rgba(0, 0, 0, 0.06),
        0 8px 24px rgba(0, 0, 0, 0.04);
    border: 1px solid rgba(0, 0, 0, 0.04);
    overflow: hidden;
}

.members-card__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.5rem 2rem;
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.members-card__header-left {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    color: var(--text-color, #212121);
}

.members-card__header-left h2 {
    font-size: 1.1rem;
    font-weight: 700;
}

.members-card__invite-toggle {
    display: flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.5rem 1rem;
    border: 2px solid var(--primary-color, #43a047);
    border-radius: 10px;
    background: transparent;
    color: var(--primary-color, #43a047);
    font-size: 0.85rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition: all 0.2s ease;
}

.members-card__invite-toggle:hover {
    background: var(--primary-color, #43a047);
    color: var(--color-white, #fff);
}

.icon-rotate {
    transform: rotate(45deg);
    transition: transform 0.25s ease;
}

.invite-form {
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    overflow: hidden;
}

.invite-form__inner {
    padding: 1.5rem 2rem;
    background: rgba(67, 160, 71, 0.03);
}

.invite-form__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    border-radius: 10px;
    background: rgba(0, 98, 133, 0.08);
    color: var(--secondary-color, #006285);
    margin-bottom: 0.75rem;
}

.invite-form__label {
    font-size: 0.88rem;
    color: var(--neutral-light, #6b7280);
    margin-bottom: 0.85rem;
    line-height: 1.4;
}

.invite-form__row {
    display: flex;
    gap: 0.75rem;
}

@media (max-width: 540px) {
    .invite-form__row {
        flex-direction: column;
    }
}

.invite-form__input-wrapper {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0 1rem;
    height: 44px;
    border-radius: 10px;
    border: 2px solid var(--color-gray-light, #dedede);
    background: var(--color-white, #fff);
    transition:
        border-color 0.2s ease,
        box-shadow 0.2s ease;
}

.invite-form__input-wrapper:focus-within {
    border-color: var(--secondary-color, #006285);
    box-shadow: 0 0 0 3px rgba(0, 98, 133, 0.12);
}

.invite-form__input-icon {
    color: var(--neutral-light, #6b7280);
    flex-shrink: 0;
}

.invite-form__input-wrapper:focus-within .invite-form__input-icon {
    color: var(--secondary-color, #006285);
}

.invite-form__input {
    flex: 1;
    border: none;
    outline: none;
    background: transparent;
    font-size: 0.9rem;
    font-family: inherit;
    color: var(--text-color, #212121);
}

.invite-form__input::placeholder {
    color: #b0b0b0;
}

.invite-form__button {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    padding: 0 1.5rem;
    height: 44px;
    border: none;
    border-radius: 10px;
    background: linear-gradient(
        135deg,
        var(--secondary-color, #006285),
        var(--secondary-color-dark, #004c6d)
    );
    color: var(--color-white, #fff);
    font-size: 0.88rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    transition:
        transform 0.15s ease,
        box-shadow 0.2s ease,
        opacity 0.2s ease;
    box-shadow: 0 4px 12px rgba(0, 98, 133, 0.3);
    white-space: nowrap;
}

.invite-form__button:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 6px 16px rgba(0, 98, 133, 0.4);
}

.invite-form__button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.slide-enter-active {
    transition: all 0.3s ease;
    max-height: 200px;
}

.slide-leave-active {
    transition: all 0.25s ease;
    max-height: 200px;
}

.slide-enter-from,
.slide-leave-to {
    opacity: 0;
    max-height: 0;
}

.members-list {
    padding: 0.5rem 0;
}

.member-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem 2rem;
    transition:
        background 0.15s ease,
        opacity 0.3s ease;
}

.member-row:hover {
    background: rgba(0, 0, 0, 0.015);
}

.member-row--removing {
    opacity: 0.4;
    pointer-events: none;
}

.member-row__left {
    display: flex;
    align-items: center;
    gap: 1rem;
    min-width: 0;
}

.member-row__avatar {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 44px;
    height: 44px;
    min-width: 44px;
    border-radius: 12px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 0.5px;
}

.member-row__info {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
    min-width: 0;
}

.member-row__name-row {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.member-row__name {
    font-size: 0.92rem;
    font-weight: 600;
    color: var(--text-color, #212121);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.member-row__badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.15rem 0.55rem;
    border-radius: 6px;
    background: rgba(67, 160, 71, 0.1);
    color: var(--primary-color-dark, #388e3c);
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    white-space: nowrap;
}

.member-row__email {
    font-size: 0.82rem;
    color: var(--neutral-light, #6b7280);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.member-row__remove {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border: none;
    border-radius: 10px;
    background: transparent;
    color: var(--neutral-light, #6b7280);
    cursor: pointer;
    transition: all 0.15s ease;
    flex-shrink: 0;
}

.member-row__remove:hover:not(:disabled) {
    background: rgba(211, 47, 47, 0.08);
    color: #c62828;
}

.member-row__remove:disabled {
    cursor: not-allowed;
}

.member-enter-active,
.member-leave-active {
    transition: all 0.3s ease;
}

.member-enter-from {
    opacity: 0;
    transform: translateX(-16px);
}

.member-leave-to {
    opacity: 0;
    transform: translateX(16px);
}

.members-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 3rem 2rem;
    text-align: center;
}

.members-empty__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 72px;
    height: 72px;
    border-radius: 20px;
    background: rgba(0, 98, 133, 0.06);
    color: var(--secondary-color, #006285);
    margin-bottom: 1.25rem;
}

.members-empty__text {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-color, #212121);
    margin-bottom: 0.35rem;
}

.members-empty__sub {
    font-size: 0.85rem;
    color: var(--neutral-light, #6b7280);
    line-height: 1.4;
}

.spinner {
    animation: spin 1s linear infinite;
}

@keyframes spin {
    from {
        transform: rotate(0deg);
    }
    to {
        transform: rotate(360deg);
    }
}

.skeleton-card {
    position: relative;
    z-index: 1;
    background: var(--color-white, #fff);
    border-radius: 20px;
    padding: 2rem;
    box-shadow:
        0 1px 3px rgba(0, 0, 0, 0.06),
        0 8px 24px rgba(0, 0, 0, 0.04);
    border: 1px solid rgba(0, 0, 0, 0.04);
    display: flex;
    flex-direction: column;
    gap: 1.25rem;
}

.skeleton {
    border-radius: 8px;
    background: linear-gradient(
        90deg,
        rgba(0, 0, 0, 0.04) 25%,
        rgba(0, 0, 0, 0.08) 50%,
        rgba(0, 0, 0, 0.04) 75%
    );
    background-size: 200% 100%;
    animation: shimmer 1.5s ease-in-out infinite;
}

.skeleton--title {
    height: 28px;
    width: 55%;
}

.skeleton--text {
    height: 16px;
    width: 80%;
}

.skeleton--short {
    width: 40%;
}

.skeleton--member {
    height: 56px;
    width: 100%;
    border-radius: 12px;
}

@keyframes shimmer {
    0% {
        background-position: -200% 0;
    }
    100% {
        background-position: 200% 0;
    }
}
</style>
