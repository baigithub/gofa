<script setup lang="ts">
import { ref } from "vue";
import AppButton from "../components/AppButton.vue";
import AppNavBar from "../components/AppNavBar.vue";

const props = defineProps<{
  amount: number;
}>();

const emit = defineEmits<{
  (event: "back"): void;
  (event: "pay-success"): void;
  (event: "pay-failed"): void;
}>();

const paying = ref(false);

const submitPay = async () => {
  if (paying.value) return;
  paying.value = true;
  await new Promise((resolve) => setTimeout(resolve, 800));
  paying.value = false;
  // 模拟支付结果：70% 成功，30% 失败
  const isSuccess = Math.random() < 0.7;
  if (isSuccess) {
    emit("pay-success");
    return;
  }
  emit("pay-failed");
};
</script>

<template>
  <main class="page">
    <section class="phone">
      <AppNavBar title="收银台" :show-back="true" />

      <section class="content">
        <article class="card">
          <p class="label">订单号</p>
          <p class="value">202604230001</p>
          <p class="label">支付金额</p>
          <p class="amount">¥{{ amount.toFixed(2) }}</p>
        </article>

        <article class="card">
          <h3>支付方式</h3>
          <label class="pay-item">
            <input checked type="radio" name="pay-type" />
            <span>微信支付</span>
          </label>
          <p class="hint">V1 仅支持微信支付</p>
        </article>
      </section>

      <footer class="footer">
        <AppButton :disabled="paying" @click="submitPay">
          {{ paying ? "支付中..." : "立即支付" }}
        </AppButton>
        <AppButton variant="secondary" @click="emit('pay-failed')">取消支付</AppButton>
        <AppButton variant="secondary" @click="emit('back')">返回确认页</AppButton>
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
  display: grid;
  grid-template-rows: auto 1fr auto;
  background: var(--color-bg);
}

.content {
  padding: var(--space-4);
  display: grid;
  gap: var(--space-3);
}

.card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  padding: var(--space-4);
}

.label {
  margin: 0 0 var(--space-1);
  color: var(--color-text-secondary);
  font-size: var(--font-size-xs);
}

.value {
  margin: 0 0 var(--space-3);
}

.amount {
  margin: 0;
  color: var(--color-primary);
  font-size: var(--font-size-lg);
  font-weight: 700;
}

h3 {
  margin: 0 0 var(--space-3);
  font-size: var(--font-size-md);
}

.pay-item {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.hint {
  margin: var(--space-2) 0 0;
  color: var(--color-text-placeholder);
  font-size: var(--font-size-xs);
}

.footer {
  position: sticky;
  bottom: 0;
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
  padding: var(--space-3) var(--space-4);
  display: grid;
  gap: var(--space-2);
}
</style>
