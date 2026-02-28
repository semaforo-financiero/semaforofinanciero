<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

// TODO: Implementar lógica para verificar si el usuario tiene familia o no
const getFamily = () => {
    return false;
};

onMounted(() => {
    const hasFamily = getFamily();

    if (!hasFamily) {
        router.push({ name: "create-family" });
    }
});
</script>

<template>
    <!-- TODO: Crear vista de informacion de familia -->
</template>

<style scoped></style>
