<script setup lang="ts">
import StatusTag from "./StatusTag.vue";

defineProps<{
  type: string;
  from: string;
  to: string;
  amount: string;
  time: string;
  status: "待支付" | "待接单" | "已接单" | "配送中" | "已完成" | "已取消";
  actionText?: string;
}>();

const emit = defineEmits<{
  (event: "action"): void;
}>();
</script>

<template>
  <article class="order-card">
    <div class="row row-top">
      <strong>{{ type }}</strong>
      <StatusTag :status="status" />
    </div>
    <p class="route">{{ from }} -> {{ to }}</p>
    <div class="row row-bottom">
      <span>{{ time }}</span>
      <strong>{{ amount }}</strong>
    </div>
    <button v-if="actionText" class="action-btn" type="button" @click="emit('action')">
      {{ actionText }}
    </button>
  </article>
</template>

<style scoped>
.order-card {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  display: grid;
  gap: var(--space-2);
}

.row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.route {
  margin: 0;
  color: var(--color-text-secondary);
}

.row-bottom {
  color: var(--color-text-secondary);
}

.action-btn {
  justify-self: end;
  border: none;
  background: var(--color-primary);
  color: #fff;
  border-radius: var(--radius-sm);
  padding: 6px 12px;
  cursor: pointer;
}
</style>
