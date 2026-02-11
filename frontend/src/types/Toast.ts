export type ToastType = "success" | "warning" | "error";

export interface Toast {
    id: string;
    type: ToastType;
    title: string;
    message: string;
    duration?: number;
}
