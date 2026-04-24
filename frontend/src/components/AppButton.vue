<script setup lang="ts">
withDefaults(
  defineProps<{
    variant?: "primary" | "secondary";
    disabled?: boolean;
  }>(),
  {
    variant: "primary",
    disabled: false,
  },
);
</script>

<template>
  <button class="app-button" :class="variant" :disabled="disabled" type="button">
    <slot />
  </button>
</template>

<style scoped>
.app-button {
  width: 100%;
  height: 40px;
  border-radius: var(--radius-sm);
  font-size: var(--font-size-sm);
  cursor: pointer;
}

.primary {
  border: none;
  color: #fff;
  background: var(--color-primary);
}

.primary:active {
  background: var(--color-primary-pressed);
}

.secondary {
  border: 1px solid var(--color-border);
  color: var(--color-text-primary);
  background: var(--color-surface);
}

.app-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
