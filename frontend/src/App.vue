<script setup lang="ts">
import ToastContainer from "./components/organisms/ToastContainer.vue";
import MenuTop from "./components/molecules/MenuTop.vue";
import SidebarMenu from "./components/molecules/SidebarMenu.vue";

import { useAuthStore } from "./stores/authStore";
import { useRoute } from "vue-router";
import { computed } from "vue";

const authStore = useAuthStore();
const route = useRoute();

const isAuthenticated = computed(() => {
    return (
        authStore.isAuthenticated &&
        !["login", "register"].includes(String(route.name))
    );
});
</script>

<template>
    <template v-if="isAuthenticated">
        <MenuTop />
        <SidebarMenu />
    </template>
    <div :class="{ 'main-content': isAuthenticated }">
        <router-view />
        <ToastContainer />
    </div>
</template>

<style scoped>
.main-content {
    padding-top: 4.5rem;
    padding-left: 4rem;
}
</style>
