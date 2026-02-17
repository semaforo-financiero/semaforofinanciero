import { defineStore } from "pinia";
import { ref, computed } from "vue";

interface UserSession {
    userId: string;
    email: string;
    accessToken: string;
    refreshToken: string;
}

const AUTH_STORAGE_KEY = "auth_session";

export const useAuthStore = defineStore("auth", () => {
    const user = ref<UserSession | null>(null);

    const isAuthenticated = computed(() => user.value !== null);
    const userEmail = computed(() => user.value?.email ?? null);
    const userId = computed(() => user.value?.userId ?? null);

    function login(sessionData: UserSession) {
        user.value = sessionData;
        saveToStorage(sessionData);
    }

    function logout() {
        user.value = null;
        removeFromStorage();
    }

    function loadSession() {
        const stored = localStorage.getItem(AUTH_STORAGE_KEY);
        if (stored) {
            try {
                user.value = JSON.parse(stored);
            } catch (error) {
                console.error("Error loading session:", error);
                removeFromStorage();
            }
        }
    }

    function saveToStorage(sessionData: UserSession) {
        localStorage.setItem(AUTH_STORAGE_KEY, JSON.stringify(sessionData));
    }

    function removeFromStorage() {
        localStorage.removeItem(AUTH_STORAGE_KEY);
    }

    function getAccessToken(): string | null {
        return user.value?.accessToken ?? null;
    }

    return {
        user,
        isAuthenticated,
        userEmail,
        userId,
        login,
        logout,
        loadSession,
        getAccessToken,
    };
});
