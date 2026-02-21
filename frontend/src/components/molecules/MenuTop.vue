<script setup lang="ts">
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/authStore";

const router = useRouter();
const authStore = useAuthStore();

const handleLogout = () => {
    authStore.logout();
    router.push({ name: "login" });
};
</script>

<template>
    <header>
        <nav>
            <div class="logo-container">
                <router-link to="/">
                    <img
                        src="../../assets/sf-logo.png"
                        alt="Logo"
                        class="logo"
                    />
                </router-link>
            </div>
            <ul class="menu-links">
                <li><router-link to="/home">Inicio</router-link></li>
                <li><router-link to="/profile">Perfil</router-link></li>
                <li>
                    <router-link to="/logout" @click.prevent="handleLogout"
                        >Cerrar sesión</router-link
                    >
                </li>
            </ul>
        </nav>
    </header>
</template>

<style scoped>
header {
    position: fixed;

    display: flex;
    align-items: center;

    width: 100%;
    height: 4.5rem;

    padding: 0 1.5rem 0 0.75rem;

    color: var(--secondary-color-dark);
    background-color: var(--color-white);
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2);
}

nav {
    display: flex;
    align-items: center;
    justify-content: space-between;

    width: 100%;
}

.logo-container {
    display: flex;
    align-items: center;
}

.logo {
    height: 2.5rem;
    width: auto;

    display: block;
}

.menu-links {
    display: flex;
    align-items: center;
    gap: 24px;

    margin: 0;
    padding: 0;

    list-style: none;
}

.menu-links li {
    display: flex;
    align-items: center;
}

a {
    color: inherit;
    text-decoration: none;
    font-weight: bold;
}

a:visited {
    color: inherit;
    text-decoration: none;
}

a.router-link-exact-active {
    border-bottom: 2px solid var(--primary-color-light);
}
</style>
