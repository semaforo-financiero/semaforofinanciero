<script setup lang="ts">
type Props = {
    modelValue?: string | number;
    errorMessage?: string;
};

const props = defineProps<Props>();

const emit = defineEmits(["update:modelValue"]);

defineOptions({
    inheritAttrs: false,
});

const handleInput = (event: Event) => {
    const target = event.target as HTMLInputElement;

    emit("update:modelValue", target.value);
};
</script>

<template>
    <input
        v-bind="$attrs"
        class="input"
        :value="modelValue"
        @input="handleInput"
    />
    <p v-if="props.errorMessage" class="error-message">
        {{ props.errorMessage }}
    </p>
</template>

<style scoped>
.input {
    width: 100%;
    padding: 0.5rem;

    font-size: 1rem;
    line-height: 1.5rem;

    border: 1px solid var(--neutral-light);
    border-radius: 0.5rem;
    background-color: var(--color-white);

    outline: none;
    appearance: none;
}

.input:focus {
    border: 1px solid transparent;
    outline: 3px solid var(--primary-color);
}

.error-message {
    margin-top: 0.125rem;

    font-size: 0.875rem;
    color: var(--color-red);
}
</style>
