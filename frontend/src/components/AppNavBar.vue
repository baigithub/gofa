<script setup lang="ts">
const props = defineProps<{
  title: string;
  showBack?: boolean;
}>();

const emit = defineEmits<{
  (event: "back"): void;
}>();
</script>

<template>
  <header class="nav-bar">
    <button
      v-if="props.showBack"
      class="back-btn"
      type="button"
      aria-label="返回"
      @click="emit('back')"
    >
      <span class="chev" aria-hidden="true">‹</span>
    </button>
    <h1 class="title">{{ title }}</h1>
    <span class="right-slot" aria-hidden="true"></span>
  </header>
</template>

<style scoped>
.nav-bar {
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  padding: 10px var(--space-4);
  border-bottom: 1px solid rgba(123, 155, 232, 0.16);
  background: linear-gradient(180deg, rgba(14, 22, 44, 0.78), rgba(8, 12, 24, 0.32));
  backdrop-filter: blur(8px);
}

.back-btn {
  width: 34px;
  height: 34px;
  display: grid;
  place-items: center;
  border-radius: 999px;
  border: 1px solid rgba(123, 155, 232, 0.22);
  background: rgba(18, 26, 49, 0.62);
  color: #dbe7ff;
  cursor: pointer;
  box-shadow: 0 0 0 1px rgba(47, 125, 255, 0.08) inset, 0 10px 30px rgba(0, 0, 0, 0.25);
  transition: transform 120ms ease, border-color 120ms ease, background 120ms ease;
}

.back-btn:active {
  transform: translateY(1px);
}

.chev {
  font-size: 20px;
  line-height: 1;
  transform: translateY(-1px);
}

.title {
  margin: 0;
  font-size: 16px;
  font-weight: 800;
  letter-spacing: 0.2px;
  color: #f2f6ff;
  text-shadow: 0 0 14px rgba(55, 143, 255, 0.24);
}

.right-slot {
  width: 34px;
  height: 34px;
}
</style>
