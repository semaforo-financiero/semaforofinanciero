<script setup lang="ts">
import { computed, nextTick, ref, watch, type Component } from "vue";

import Input from "./Input.vue";

type ModelValue = unknown;

type Content = string | Component;

interface Option {
    content: Content;
    value: ModelValue;
}

type Props = {
    modelValue: ModelValue;
    options: Option[];
    placeholder?: string;
};

const props = defineProps<Props>();

const emit = defineEmits(["update:modelValue"]);

const isOpen = ref(false);
const query = ref(getLabelFromValue(props.modelValue));
const inputRef = ref<{ inputElement: HTMLInputElement | null } | null>(null);
const focusedIndex = ref(-1);
const dropdownRef = ref<HTMLElement | null>(null);

const filteredOptions = computed(() => {
    if (!query.value) return props.options;

    const q = query.value.toLowerCase();

    return props.options.filter((option) =>
        typeof option.content === "string"
            ? option.content.toLowerCase().includes(q)
            : true,
    );
});

function getLabelFromValue(value: ModelValue): string {
    const option = props.options.find((o) => o.value === value);

    return option && typeof option.content === "string" ? option.content : "";
}

function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape") {
        isOpen.value = false;
        inputRef.value?.inputElement?.blur();
    } else if (event.key === "ArrowDown") {
        if (!isOpen.value) {
            isOpen.value = true;
            focusedIndex.value = 0;
            scrollToFocused();
        } else {
            focusedIndex.value =
                (focusedIndex.value + 1) % filteredOptions.value.length;
            scrollToFocused();
        }

        event.preventDefault();
    } else if (event.key === "ArrowUp") {
        if (!isOpen.value) {
            isOpen.value = true;
            focusedIndex.value = filteredOptions.value.length - 1;
            scrollToFocused();
        } else {
            focusedIndex.value =
                (focusedIndex.value - 1 + filteredOptions.value.length) %
                filteredOptions.value.length;
            scrollToFocused();
        }

        event.preventDefault();
    } else if (event.key === "Tab") {
        if (isOpen.value && filteredOptions.value.length > 0) {
            focusedIndex.value =
                (focusedIndex.value + 1) % filteredOptions.value.length;
            scrollToFocused();
            event.preventDefault();
        }
    } else if (event.key === "Enter") {
        if (
            isOpen.value &&
            focusedIndex.value >= 0 &&
            focusedIndex.value < filteredOptions.value.length
        ) {
            const option = filteredOptions.value[focusedIndex.value];

            if (option) {
                emit("update:modelValue", option.value);
            }

            isOpen.value = false;
            inputRef.value?.inputElement?.blur();
            event.preventDefault();
        }
    }
}

function scrollToFocused() {
    nextTick(() => {
        const dropdown = dropdownRef.value;

        if (!dropdown) return;

        const focusedItem = dropdown.querySelector(
            ".item.focused",
        ) as HTMLElement;

        if (focusedItem) {
            focusedItem.scrollIntoView({ block: "nearest" });
        }
    });
}

watch(isOpen, (val) => {
    if (val) {
        query.value = "";
    } else {
        focusedIndex.value = -1;
        query.value = getLabelFromValue(props.modelValue);
    }
});

watch(query, () => {
    focusedIndex.value = -1;
});

watch(
    () => props.modelValue,
    (val) => {
        query.value = getLabelFromValue(val);
    },
);
</script>

<template>
    <div class="select-container">
        <div class="input">
            <Input
                ref="inputRef"
                :modelValue="query"
                :placeholder="props.placeholder"
                @update:modelValue="query = $event"
                @focus="isOpen = true"
                @blur="isOpen = false"
                @keydown="handleKeydown"
            />
        </div>
        <div v-if="isOpen" ref="dropdownRef" class="dropdown">
            <ul class="list">
                <li
                    v-for="(option, index) in filteredOptions"
                    class="item"
                    :key="index"
                    :tabindex="0"
                    :class="{ focused: focusedIndex === index }"
                    @mousedown.prevent="
                        emit('update:modelValue', option.value);
                        isOpen = false;
                        inputRef?.inputElement?.blur();
                    "
                >
                    <template v-if="typeof option.content === 'string'">
                        {{ option.content }}
                    </template>
                    <template v-else>
                        <component :is="option.content" />
                    </template>
                </li>
            </ul>
        </div>
    </div>
</template>

<style scoped>
.select-container {
    position: relative;
    width: 100%;
}

.input {
    width: 100%;
}

.dropdown {
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    z-index: 9999;

    max-height: 16rem;
    overflow-y: auto;

    border: 1px solid var(--neutral-light);
    border-radius: 0.5rem;
    background-color: var(--color-white);

    margin-top: 0.5rem;
    padding: 0.25rem 0.5rem;
}

.list {
    list-style: none;
    margin: 0;
    padding: 0;
}

.item {
    padding: 0.5rem;
    cursor: pointer;

    border-radius: 0.25rem;
}

.item:hover {
    background-color: var(--color-gray-light);
}

.item.focused {
    outline: 3px solid var(--primary-color);
}
</style>
