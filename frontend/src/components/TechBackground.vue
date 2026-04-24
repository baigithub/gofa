<script setup lang="ts">
withDefaults(
  defineProps<{
    intensity?: "subtle" | "normal" | "strong";
  }>(),
  { intensity: "normal" },
);
</script>

<template>
  <div class="bg" :class="intensity">
    <div class="grid"></div>
    <div class="scan"></div>
    <div class="orb a"></div>
    <div class="orb b"></div>
    <div class="orb c"></div>
  </div>
</template>

<style scoped>
.bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
  border-radius: inherit;
  pointer-events: none;
}

.grid {
  position: absolute;
  inset: -20%;
  background-image:
    linear-gradient(rgba(120, 156, 255, 0.09) 1px, transparent 1px),
    linear-gradient(90deg, rgba(120, 156, 255, 0.09) 1px, transparent 1px);
  background-size: 22px 22px;
  transform: perspective(800px) rotateX(58deg) translateY(-10%);
  mask-image: radial-gradient(circle at center, #000 38%, transparent 78%);
  opacity: 0.9;
}

.scan {
  position: absolute;
  left: -30%;
  top: -10%;
  width: 160%;
  height: 22%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(72, 135, 255, 0.18),
    rgba(33, 203, 255, 0.12),
    transparent
  );
  transform: rotate(8deg);
  filter: blur(10px);
  animation: scan 5.8s linear infinite;
  opacity: 0.75;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(22px);
  opacity: 0.65;
  animation: float 6.8s ease-in-out infinite;
}

.orb.a {
  width: 180px;
  height: 180px;
  background: rgba(72, 135, 255, 0.42);
  top: -40px;
  right: -50px;
}

.orb.b {
  width: 170px;
  height: 170px;
  background: rgba(33, 203, 255, 0.22);
  bottom: -50px;
  left: -40px;
  animation-delay: -2.2s;
}

.orb.c {
  width: 140px;
  height: 140px;
  background: rgba(45, 207, 143, 0.18);
  top: 42%;
  left: -60px;
  animation-delay: -3.6s;
}

.subtle .grid {
  opacity: 0.55;
}
.subtle .scan {
  opacity: 0.45;
}
.subtle .orb {
  opacity: 0.42;
}

.strong .grid {
  opacity: 1;
}
.strong .scan {
  opacity: 0.9;
}
.strong .orb {
  opacity: 0.85;
}

@keyframes scan {
  0% {
    transform: translateX(-20%) rotate(8deg);
  }
  100% {
    transform: translateX(20%) rotate(8deg);
  }
}

@keyframes float {
  0%,
  100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-12px);
  }
}
</style>

