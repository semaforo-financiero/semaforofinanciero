import type { RegisterUser } from "../../types/RegisterUser";

type ValidationErrors = {
    [K in keyof RegisterUser]?: string;
};

const validateRegisterUserForm = (data: RegisterUser): ValidationErrors => {
    const errors: ValidationErrors = {};
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!data.name || data.name.trim().length < 3) {
        errors.name = "El nombre debe tener al menos 3 caracteres.";
    }

    if (!data.lastName || data.lastName.trim().length < 3) {
        errors.lastName = "El apellido debe tener al menos 3 caracteres.";
    }

    if (!data.email || !emailRegex.test(data.email)) {
        errors.email = "La dirección de correo electrónico no es válida.";
    }

    if (!data.password || data.password.length < 6) {
        errors.password = "La contraseña debe tener al menos 6 caracteres.";
    }

    if (!data.confirmPassword) {
        errors.confirmPassword = "Debes confirmar la contraseña.";
    } else if (data.password !== data.confirmPassword) {
        errors.confirmPassword = "Las contraseñas no coinciden.";
    }

    return errors;
};
export default validateRegisterUserForm;
