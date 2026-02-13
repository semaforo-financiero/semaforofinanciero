<script setup lang="ts">
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/authStore";

const router = useRouter();
const authStore = useAuthStore();

const handleLogout = () => {
    authStore.logout();
    router.push({ name: "login" });
};
</script>

<template>
    <div class="home-view">
        <div class="header">
            <h1>Semáforo Financiero</h1>
            <button @click="handleLogout" class="logout-btn">
                Cerrar Sesión
            </button>
        </div>
        <div class="content">
            <div class="welcome-card">
                <h2>¡Bienvenido!</h2>
                <p class="user-info">
                    <strong>Email:</strong> {{ authStore.userEmail }}
                </p>
                <p class="user-info">
                    <strong>ID:</strong> {{ authStore.userId }}
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.home-view {
    min-height: 100vh;
    background: linear-gradient(
        135deg,
        var(--secondary-color-light) 0%,
        var(--secondary-color-dark) 100%
    );
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem 3rem;
    background: rgba(255, 255, 255, 0.95);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header h1 {
    color: var(--secondary-color-dark);
    margin: 0;
    font-size: 1.8rem;
}

.logout-btn {
    padding: 0.75rem 1.5rem;
    background: var(--secondary-color-dark);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.logout-btn:hover {
    background: var(--secondary-color-light);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.content {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: calc(100vh - 100px);
    padding: 2rem;
}

.welcome-card {
    background: white;
    padding: 3rem;
    border-radius: 16px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    max-width: 600px;
    width: 100%;
}

.welcome-card h2 {
    color: var(--secondary-color-dark);
    margin: 0 0 2rem 0;
    font-size: 2rem;
    text-align: center;
}

.user-info {
    margin: 1rem 0;
    font-size: 1.1rem;
    color: #333;
    padding: 1rem;
    background: #f5f5f5;
    border-radius: 8px;
}

.user-info strong {
    color: var(--secondary-color-dark);
}

@media (max-width: 768px) {
    .header {
        padding: 1rem 1.5rem;
        flex-direction: column;
        gap: 1rem;
    }

    .header h1 {
        font-size: 1.5rem;
    }

    .welcome-card {
        padding: 2rem;
    }

    .welcome-card h2 {
        font-size: 1.5rem;
    }
}
</style>
