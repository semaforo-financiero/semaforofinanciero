<script setup lang="ts">
import { useRouter } from "vue-router";

import RegisterUserForm from "../components/molecules/RegisterUserForm.vue";

import type { RegisterUser } from "../types/RegisterUser";

const router = useRouter();

const handleRegister = (userData: RegisterUser) => {
    // TODO: Implement registration logic
};

const goToLogin = () => {
    router.push({ name: "login" });
};
</script>

<template>
    <div class="register-view">
        <div class="wallpaper">
            <img src="../assets/sf-logo.png" alt="Logo" />
        </div>
        <div class="register-form">
            <RegisterUserForm
                @register="handleRegister"
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
</style>
