<script setup lang="ts">
import { reactive } from "vue";

import InputAutoFocus from "../atoms/InputAutoFocus.vue";
import Input from "../atoms/Input.vue";
import Link from "../atoms/Link.vue";
import TextButton from "../atoms/TextButton.vue";

type Props = {
    isLoading: boolean;
};

const props = defineProps<Props>();

const formData = reactive({
    email: "",
    password: "",
});

const errors = reactive({
    email: "",
    password: "",
});

const emit = defineEmits(["login", "goToRegister"]);

const login = () => {
    emit("login", { ...formData });
};

const goToRegister = () => {
    emit("goToRegister");
};
</script>

<template>
    <div class="login-form">
        <div class="title">
            <h1>¡Inicia sesión!</h1>
            <p>
                Accede a tu cuenta para disfrutar de todas las funcionalidades
                de nuestra aplicación.
            </p>
        </div>

        <div class="form">
            <div class="form-input">
                <label for="email">Correo electrónico:</label>
                <InputAutoFocus
                    v-model="formData.email"
                    id="email"
                    type="email"
                    placeholder="Correo electrónico"
                    :errorMessage="errors.email"
                    :disabled="props.isLoading"
                />
            </div>

            <div class="form-input">
                <label for="password">Contraseña:</label>
                <Input
                    v-model="formData.password"
                    id="password"
                    type="password"
                    placeholder="Contraseña"
                    :errorMessage="errors.password"
                    :disabled="props.isLoading"
                />
            </div>
        </div>

        <div class="buttons">
            <TextButton
                variant="primary"
                size="medium"
                :disabled="props.isLoading"
                @click="login"
            >
                {{ props.isLoading ? "Iniciando sesión..." : "Iniciar sesión" }}
            </TextButton>
            <div class="redirect-register">
                ¿Aún no tienes una cuenta?
                <Link @click="goToRegister"> Regístrate </Link>
            </div>
        </div>
    </div>
</template>

<style scoped>
.login-form {
    display: flex;
    flex-direction: column;
    gap: 2rem;

    min-width: 80%;
}

.title {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;

    width: 100%;
}

.title h1 {
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary-color-dark);
}

.title p {
    font-size: 1rem;
    color: var(--text-color);
}

.form {
    display: flex;
    flex-direction: column;

    width: 100%;
}

.form-input {
    display: flex;
    flex-direction: column;
}

.form-input label {
    font-weight: 600;
    margin-bottom: 0.5rem;
}

.form-input :not(label) {
    margin-left: 0.5rem;
}

.form-input:not(:last-child) {
    margin-bottom: 1.5rem;
}

.buttons {
    width: 100%;

    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.redirect-register {
    display: flex;
    justify-content: center;
}
</style>
