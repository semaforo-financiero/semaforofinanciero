<script setup lang="ts">
import { reactive } from "vue";

import InputAutoFocus from "../atoms/InputAutoFocus.vue";
import Input from "../atoms/Input.vue";
import Link from "../atoms/Link.vue";
import TextButton from "../atoms/TextButton.vue";

import validateRegisterUserForm from "../../utils/validations/registerUserFormValidations";

const formData = reactive({
    name: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
});

const errors = reactive({
    name: "",
    lastName: "",
    email: "",
    password: "",
    confirmPassword: "",
});

const emit = defineEmits(["register", "goToLogin"]);

const clearErrors = () => {
    Object.keys(errors).forEach((key) => {
        errors[key as keyof typeof errors] = "";
    });
};

const register = () => {
    clearErrors();

    const validationErrors = validateRegisterUserForm(formData);

    if (Object.keys(validationErrors).length === 0) {
        emit("register", { ...formData });

        return;
    }

    Object.assign(errors, validationErrors);
};

const goToLogin = () => {
    emit("goToLogin");
};
</script>

<template>
    <div class="register-user-form">
        <div class="title">
            <h1>¡Crea una cuenta!</h1>
            <p>Y comienza a llevar una mejor gestión financiera</p>
        </div>

        <div class="form">
            <div class="form-input">
                <label for="name">Nombre(s):</label>
                <InputAutoFocus
                    v-model="formData.name"
                    id="name"
                    type="text"
                    placeholder="Nombre(s)"
                    :errorMessage="errors.name"
                />
            </div>

            <div class="form-input">
                <label for="lastName">Apellidos:</label>
                <Input
                    v-model="formData.lastName"
                    id="lastName"
                    type="text"
                    placeholder="Apellidos"
                    :errorMessage="errors.lastName"
                />
            </div>

            <div class="form-input">
                <label for="email">Correo electrónico:</label>
                <Input
                    v-model="formData.email"
                    id="email"
                    type="email"
                    placeholder="Correo electrónico"
                    :errorMessage="errors.email"
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
                />
            </div>

            <div class="form-input">
                <label for="confirmPassword">Confirmar contraseña:</label>
                <Input
                    v-model="formData.confirmPassword"
                    id="confirmPassword"
                    type="password"
                    placeholder="Confirmar contraseña"
                    :errorMessage="errors.confirmPassword"
                />
            </div>
        </div>

        <div class="buttons">
            <TextButton
                variant="primary"
                size="medium"
                @click="register"
                @enterKeyDown="register"
            >
                Registrarse
            </TextButton>
            <div class="redirect-login">
                ¿Ya tienes una cuenta?
                <Link @click="goToLogin" @enterKeyDown="goToLogin">
                    Inicia sesión
                </Link>
            </div>
        </div>
    </div>
</template>

<style scoped>
.register-user-form {
    display: flex;
    flex-direction: column;
    gap: 2rem;

    width: 80%;
    max-width: 50rem;
}

.title {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
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
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.redirect-login {
    display: flex;
    justify-content: center;
}
</style>
