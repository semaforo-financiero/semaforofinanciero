<script setup lang="ts">
import { toasterStore } from "../../stores/toasterStore";
import Toast from "../atoms/Toast.vue";

function handleClose(id: string) {
    toasterStore.remove(id);
}
</script>

<template>
    <div class="toast-container">
        <Toast
            v-for="toast in toasterStore.state.toasts"
            :key="toast.id"
            :toast="toast"
            @close="handleClose"
        />
    </div>
</template>

<style scoped>
.toast-container {
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    display: flex;
    flex-direction: column;
    pointer-events: none;
}

.toast-container > * {
    pointer-events: auto;
}
</style>
