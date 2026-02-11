<script setup lang="ts">
import { computed } from "vue";
import type { Toast } from "../../types/Toast";

const props = defineProps<{
    toast: Toast;
}>();

const emit = defineEmits<{
    close: [id: string];
}>();

const borderColorClass = computed(() => {
    switch (props.toast.type) {
        case "success":
            return "border-green-500";
        case "warning":
            return "border-yellow-500";
        case "error":
            return "border-red-500";
        default:
            return "border-gray-500";
    }
});

function handleClose() {
    emit("close", props.toast.id);
}
</script>

<template>
    <div class="toast" :class="borderColorClass">
        <div class="toast-content">
            <h4 class="toast-title">{{ toast.title }}</h4>
            <p class="toast-message">{{ toast.message }}</p>
        </div>
        <button class="toast-close" @click="handleClose" aria-label="Cerrar">
            ✕
        </button>
    </div>
</template>

<style scoped>
.toast {
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    padding: 16px;
    margin-bottom: 12px;
    min-width: 320px;
    max-width: 420px;
    border-bottom: 4px solid;
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    animation: slideIn 0.3s ease-out;
    position: relative;
}

.toast-content {
    flex: 1;
    margin-right: 12px;
}

.toast-title {
    margin: 0 0 4px 0;
    font-size: 16px;
    font-weight: 600;
    color: #1a1a1a;
}

.toast-message {
    margin: 0;
    font-size: 14px;
    color: #666;
    line-height: 1.4;
}

.toast-close {
    background: none;
    border: none;
    color: #999;
    cursor: pointer;
    font-size: 20px;
    line-height: 1;
    padding: 0;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 4px;
    transition: all 0.2s;
    flex-shrink: 0;
}

.toast-close:hover {
    background: #f5f5f5;
    color: #666;
}

.border-green-500 {
    border-bottom-color: #22c55e;
}

.border-yellow-500 {
    border-bottom-color: #eab308;
}

.border-red-500 {
    border-bottom-color: #ef4444;
}

@keyframes slideIn {
    from {
        transform: translateX(100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}
</style>
