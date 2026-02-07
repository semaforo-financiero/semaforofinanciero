<script setup lang="ts">
type Props = {
    variant: "primary" | "secondary";
    size: "small" | "medium" | "large";
    disabled?: boolean;
};

const props = defineProps<Props>();

const emit = defineEmits(["click", "enterKeyDown"]);
</script>

<template>
    <button
        class="text-button"
        :class="[props.variant, props.size]"
        :disabled="props.disabled"
        @click="$emit('click')"
        @keydown.enter="$emit('enterKeyDown')"
    >
        <slot />
    </button>
</template>

<style scoped>
.text-button {
    width: 100%;
    padding: 0.5rem;

    border-radius: 0.5rem;
    border: none;
    cursor: pointer;
}

.text-button:disabled {
    cursor: not-allowed;
    opacity: 0.5;
}

.text-button:focus {
    outline: 3px solid var(--primary-color-dark);
}

.text-button.primary {
    color: var(--color-white);
    background-color: var(--primary-color);
}

.text-button.primary:hover {
    background-color: var(--primary-color-dark);
}

.text-button.secondary {
    background-color: transparent;
    border: 1px solid var(--primary-color);
}

.text-button.secondary:hover {
    background-color: var(--color-gray-light);
}

.text-button.small {
    font-size: 1rem;
}

.text-button.medium {
    font-size: 1.25rem;
}

.text-button.large {
    font-size: 1.5rem;
}
</style>
