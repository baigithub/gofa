<script setup lang="ts">
import TechBackground from "./TechBackground.vue";

withDefaults(
  defineProps<{
    title?: string;
    showTechBg?: boolean;
    dark?: boolean;
  }>(),
  {
    title: "",
    showTechBg: true,
    dark: true,
  },
);
</script>

<template>
  <main class="outer">
    <section class="frame" :class="{ 'mobile-dark': dark }">
      <TechBackground v-if="showTechBg" intensity="normal" />
      <div class="inner">
        <slot />
      </div>
    </section>
  </main>
</template>

<style scoped>
.outer {
  min-height: 100svh;
  display: grid;
  place-items: center;
  background: #fff;
  padding: 18px;
}

.frame {
  position: relative;
  width: min(92vw, 390px);
  min-height: min(88svh, 780px);
  border-radius: 22px;
  overflow: hidden;
  border: 1px solid rgba(122, 155, 231, 0.22);
  background: radial-gradient(circle at 20% 20%, rgba(25, 45, 90, 0.9), rgba(8, 14, 29, 0.96) 58%, rgba(6, 10, 20, 0.98));
  box-shadow: 0 22px 48px rgba(2, 6, 18, 0.52);
}

.inner {
  position: relative;
  z-index: 1;
  height: 100%;
  padding: 18px;
  display: grid;
}
</style>

