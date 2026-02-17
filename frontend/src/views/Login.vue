<script setup lang="ts">
import { useRouter } from "vue-router";
import { ref } from "vue";

import LoginForm from "../components/molecules/LoginForm.vue";
import api from "../lib/api";
import { toasterStore } from "../stores/toasterStore";
import { useAuthStore } from "../stores/authStore";

import type User from "../lib/api/models/User";

const isLoading = ref(false);

const router = useRouter();
const authStore = useAuthStore();

const goToRegister = () => {
    router.push({ name: "register" });
};

const login = async (loginData: User) => {
    try {
        isLoading.value = true;

        const userLogged = await api.user.login(loginData);

        authStore.login({
            userId: userLogged.userId!,
            email: userLogged.userEmail,
            accessToken: userLogged.accessToken!,
            refreshToken: userLogged.refreshToken!,
        });

        toasterStore.success(
            "¡Inicio de sesión exitoso!",
            "Has iniciado sesión correctamente.",
        );

        router.push({ name: "home" });
    } catch (error) {
        toasterStore.error(
            "Error en el inicio de sesión",
            "No se pudo iniciar sesión. Intenta nuevamente",
        );
    } finally {
        isLoading.value = false;
    }
};
</script>

<template>
    <div class="login-view">
        <div class="wallpaper">
            <img src="../assets/sf-logo.png" alt="Logo" />
        </div>
        <div class="login-form">
            <LoginForm
                :isLoading="isLoading"
                @login="login"
                @goToRegister="goToRegister"
            />
        </div>
    </div>
</template>

<style scoped>
.login-view {
    display: flex;

    height: 100vh;
    width: 100vw;
}

.wallpaper,
.login-form {
    flex: 1;
    max-width: 50%;
}

.wallpaper {
    display: flex;
    justify-content: center;
    align-items: center;

    background-image: linear-gradient(
        180deg,
        var(--secondary-color-dark) 10%,
        var(--secondary-color-light) 90%
    );

    box-shadow: 3px 0 35px 1px rgba(0, 0, 0, 0.5);
}

.wallpaper img {
    max-width: 50%;
    filter: drop-shadow(0 2px 20px rgba(0, 0, 0, 0.3));
}

.login-form {
    display: flex;
    justify-content: center;
    align-items: center;
}

@media (max-width: 1024px) {
    .wallpaper {
        max-width: 40%;
    }

    .login-form {
        max-width: 60%;
    }

    .wallpaper img {
        max-width: 60%;
    }
}

@media (max-width: 768px) {
    .login-view {
        flex-direction: column;
    }

    .wallpaper {
        max-width: 100%;
        max-height: 15vh;

        box-shadow: 0 3px 20px rgba(0, 0, 0, 0.3);
    }

    .wallpaper img {
        max-height: 100%;
    }

    .login-form {
        margin: auto;
        max-width: 90%;
    }
}
</style>
