import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/authStore";

import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Home from "../views/Home.vue";

const routes = [
    {
        path: "/",
        redirect: "/home",
    },
    {
        path: "/login",
        name: "login",
        component: Login,
        meta: { requiresGuest: true },
    },
    {
        path: "/register",
        name: "register",
        component: Register,
        meta: { requiresGuest: true },
    },
    {
        path: "/home",
        name: "home",
        component: Home,
        meta: { requiresAuth: true },
    },
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    
    if (!authStore.user) {
        authStore.loadSession();
    }

    const requiresAuth = to.meta.requiresAuth;
    const requiresGuest = to.meta.requiresGuest;
    const isAuthenticated = authStore.isAuthenticated;

    if (requiresAuth && !isAuthenticated) {
        next({ name: "login" });
    }
    else if (requiresGuest && isAuthenticated) {
        next({ name: "home" });
    }
    else {
        next();
    }
});

export default router;
