<script setup lang="ts">
import User from "../../assets/icons/User.vue";
import House from "../../assets/icons/House.vue";
import Family from "../../assets/icons/Family.vue";
</script>

<template>
    <aside class="sidebar">
        <nav>
            <ul>
                <li>
                    <span class="icon"><House /></span>
                    <router-link to="/">Inicio</router-link>
                </li>
                <li>
                    <span class="icon"><User /></span>
                    <router-link to="/profile">Perfil</router-link>
                </li>
                <li>
                    <span class="icon"><Family /></span>
                    <router-link to="/settings">Familia</router-link>
                </li>
            </ul>
        </nav>
    </aside>
</template>

<style scoped>
.sidebar {
    position: fixed;
    top: 4.5rem;
    left: 0;

    width: 4rem;
    height: 100vh;

    padding: 1rem;

    color: var(--secondary-color-dark);
    background-color: var(--color-white);

    overflow-x: hidden;

    transition: width 0.3s cubic-bezier(0.4, 0, 0.2, 1);

    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.2);

    z-index: 999;
}

.sidebar:hover {
    width: 15rem;
}

.sidebar ul {
    list-style: none;
    padding: 0;
    margin: 0;
}

.sidebar li {
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    height: 2.5rem;
}

.sidebar li:hover {
    background-color: var(--color-gray-light);
}

.icon {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 2rem;
    min-width: 2rem;
    height: 2rem;

    font-size: 1.2rem;
    stroke-width: 1.5;
}

.sidebar a {
    display: block;
    width: 100%;

    padding: 0.5rem 1rem;

    white-space: nowrap;

    text-decoration: none;
    font-weight: 600;
    color: var(--secondary-color-dark);

    transition: opacity 0.2s;
}

.sidebar a:visited {
    color: var(--secondary-color-dark);
}
</style>
