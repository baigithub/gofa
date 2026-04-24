<script setup lang="ts">
import AppButton from "../components/AppButton.vue";

const emit = defineEmits<{
  (event: "view-order"): void;
  (event: "go-home"): void;
}>();
</script>

<template>
  <main class="page">
    <section class="phone">
      <section class="card">
        <div class="icon success">✓</div>
        <h1>支付成功</h1>
        <p>订单已支付，等待跑腿员接单</p>
      </section>

      <footer class="footer">
        <AppButton @click="emit('view-order')">查看订单</AppButton>
        <AppButton variant="secondary" @click="emit('go-home')">返回首页</AppButton>
      </footer>
    </section>
  </main>
</template>

<style scoped>
.page {
  min-height: 100svh;
  display: grid;
  place-items: center;
}

.phone {
  width: min(100vw, 390px);
  min-height: 100svh;
  background: var(--color-bg);
  display: grid;
  grid-template-rows: 1fr auto;
}

.card {
  margin: auto var(--space-4);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-6) var(--space-4);
  text-align: center;
}

.icon {
  width: 56px;
  height: 56px;
  margin: 0 auto var(--space-3);
  border-radius: 50%;
  display: grid;
  place-items: center;
  color: #fff;
  font-size: 28px;
  font-weight: 700;
}

.success {
  background: var(--color-status-finished);
}

h1 {
  margin: 0 0 var(--space-2);
  font-size: var(--font-size-lg);
}

p {
  margin: 0;
  color: var(--color-text-secondary);
}

.footer {
  border-top: 1px solid var(--color-border);
  padding: var(--space-3) var(--space-4);
  display: grid;
  gap: var(--space-2);
  background: var(--color-surface);
}
</style>
