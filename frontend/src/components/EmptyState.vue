<script setup lang="ts">
defineProps<{
  title: string;
  description?: string;
  actionText?: string;
}>();
</script>

<template>
  <section class="empty-state">
    <h3>{{ title }}</h3>
    <p v-if="description">{{ description }}</p>
    <button v-if="actionText" type="button">{{ actionText }}</button>
  </section>
</template>

<style scoped>
.empty-state {
  text-align: center;
  padding: var(--space-8) var(--space-4);
  color: var(--color-text-secondary);
  border: 1px dashed var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
}

h3 {
  margin: 0 0 var(--space-2);
  color: var(--color-text-primary);
  font-size: var(--font-size-md);
}

p {
  margin: 0 0 var(--space-4);
}

button {
  border: none;
  background: var(--color-primary);
  color: #fff;
  border-radius: var(--radius-sm);
  padding: 6px 12px;
  cursor: pointer;
}
</style>
