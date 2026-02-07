<script setup lang="ts">
const emit = defineEmits(["click", "enterKeyDown"]);

const handleClick = () => {
    emit("click");
};

const handleEnterKeyDown = () => {
    emit("enterKeyDown");
};
</script>

<template>
    <div class="link" tabindex="0">
        <a
            @click.prevent="handleClick"
            @keydown.enter.prevent="handleEnterKeyDown"
        >
            <slot />
        </a>
    </div>
</template>

<style scoped>
.link {
    display: flex;
    align-items: center;
    padding: 0 0.25rem;

    color: var(--primary-color-dark);
    cursor: pointer;
}

.link:focus {
    outline: 3px solid var(--primary-color-dark);
}

.link a {
    text-decoration: underline;
    color: inherit;
}

.link:hover a {
    color: var(--secondary-color-dark);
}
</style>
