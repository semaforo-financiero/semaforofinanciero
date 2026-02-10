<script setup lang="ts">
import { useRouter } from "vue-router";
import { ref } from "vue";

import RegisterUserForm from "../components/molecules/RegisterUserForm.vue";
import api from "../lib/api";
import User from "../lib/api/models/User";
import { toasterStore } from "../stores/toasterStore";

const isLoading = ref(false);

const router = useRouter();

const goToLogin = () => {
    router.push({ name: "login" });
};

const registerUser = async (userData: User) => {
    try {
        isLoading.value = true;

        await api.user.register(userData);

        toasterStore.success(
            "¡Registro exitoso!",
            "Tu cuenta ha sido creada. Ahora inicia sesión.",
        );

        goToLogin();
    } catch (error) {
        toasterStore.error(
            "Error en el registro",
            "No se pudo crear la cuenta. Intenta nuevamente",
        );
    } finally {
        isLoading.value = false;
    }
};
</script>

<template>
    <div class="register-view">
        <div class="wallpaper">
            <img src="../assets/sf-logo.png" alt="Logo" />
        </div>
        <div class="register-form">
            <RegisterUserForm
                :isLoading="isLoading"
                @register="registerUser"
                @goToLogin="goToLogin"
            />
        </div>
    </div>
</template>

<style scoped>
.register-view {
    display: flex;

    height: 100vh;
    width: 100vw;
}

.wallpaper,
.register-form {
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

.register-form {
    display: flex;
    justify-content: center;
    align-items: center;
}

@media (max-width: 1024px) {
    .wallpaper {
        max-width: 40%;
    }

    .register-form {
        max-width: 60%;
    }

    .wallpaper img {
        max-width: 60%;
    }
}

@media (max-width: 768px) {
    .register-view {
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

    .register-form {
        max-width: 100%;
    }
}
</style>
