<script setup lang="ts">
import { onMounted, ref } from "vue";

type Props = {
    modelValue?: string | number;
    errorMessage?: string;
};

const props = defineProps<Props>();

const emit = defineEmits(["update:modelValue"]);

const inputAutoFocus = ref<HTMLInputElement | null>(null);

defineOptions({
    inheritAttrs: false,
});

const handleInput = (event: Event) => {
    const target = event.target as HTMLInputElement;
    emit("update:modelValue", target.value);
};

onMounted(() => {
    inputAutoFocus.value?.focus();
});
</script>

<template>
    <input
        v-bind="$attrs"
        ref="inputAutoFocus"
        class="input-auto-focus"
        :value="modelValue"
        @input="handleInput"
    />
    <p v-if="props.errorMessage" class="error-message">
        {{ props.errorMessage }}
    </p>
</template>

<style scoped>
.input-auto-focus {
    display: flex;
    flex-direction: column;

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

.input-auto-focus:focus {
    border: 1px solid transparent;
    outline: 3px solid var(--primary-color);
}

.error-message {
    margin-top: 0.125rem;

    font-size: 0.875rem;
    color: var(--color-red);
}
</style>
