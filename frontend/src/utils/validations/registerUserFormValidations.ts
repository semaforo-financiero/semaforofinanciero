import type { RegisterUser } from "../../types/RegisterUser";

type ValidationErrors = {
    [K in keyof RegisterUser]?: string;
};

const validateRegisterUserForm = (data: RegisterUser): ValidationErrors => {
    const errors: ValidationErrors = {};
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!data.first_name || data.first_name.trim().length < 3) {
        errors.first_name = "El nombre debe tener al menos 3 caracteres.";
    }

    if (!data.last_name || data.last_name.trim().length < 3) {
        errors.last_name = "El apellido debe tener al menos 3 caracteres.";
    }

    if (!data.email || !emailRegex.test(data.email)) {
        errors.email = "La dirección de correo electrónico no es válida.";
    }

    if (!data.password || data.password.length < 6) {
        errors.password = "La contraseña debe tener al menos 6 caracteres.";
    }

    if (!data.confirm_password) {
        errors.confirm_password = "Debes confirmar la contraseña.";
    } else if (data.password !== data.confirm_password) {
        errors.confirm_password = "Las contraseñas no coinciden.";
    }

    return errors;
};

export default validateRegisterUserForm;
