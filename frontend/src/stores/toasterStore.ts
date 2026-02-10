import { reactive } from "vue";
import type { Toast, ToastType } from "../types/Toast";

interface ToasterState {
    toasts: Toast[];
}

const state = reactive<ToasterState>({
    toasts: [],
});

let toastIdCounter = 0;

function generateId(): string {
    return `toast-${Date.now()}-${toastIdCounter++}`;
}

function addToast(
    type: ToastType,
    title: string,
    message: string,
    duration: number = 5000,
) {
    const id = generateId();
    const toast: Toast = {
        id,
        type,
        title,
        message,
        duration,
    };

    state.toasts.push(toast);

    setTimeout(() => {
        removeToast(id);
    }, duration);

    return id;
}

function removeToast(id: string) {
    const index = state.toasts.findIndex((t) => t.id === id);
    if (index !== -1) {
        state.toasts.splice(index, 1);
    }
}

export const toasterStore = {
    state,
    success(title: string, message: string, duration?: number) {
        return addToast("success", title, message, duration);
    },
    warning(title: string, message: string, duration?: number) {
        return addToast("warning", title, message, duration);
    },
    error(title: string, message: string, duration?: number) {
        return addToast("error", title, message, duration);
    },
    remove(id: string) {
        removeToast(id);
    },
};
