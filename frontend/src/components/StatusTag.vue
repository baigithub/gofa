<script setup lang="ts">
import { computed } from "vue";

const props = defineProps<{
  status:
    | "待支付"
    | "待接单"
    | "已接单"
    | "配送中"
    | "已完成"
    | "已取消";
}>();

const className = computed(() => {
  switch (props.status) {
    case "待支付":
      return "pending-pay";
    case "待接单":
      return "pending-take";
    case "已接单":
      return "pending-take";
    case "配送中":
      return "delivering";
    case "已完成":
      return "finished";
    case "已取消":
      return "cancelled";
    default:
      return "cancelled";
  }
});
</script>

<template>
  <span class="status-tag" :class="className">{{ status }}</span>
</template>

<style scoped>
.status-tag {
  display: inline-block;
  font-size: var(--font-size-xs);
  padding: 2px var(--space-2);
  border-radius: 999px;
  color: #fff;
}

.pending-pay {
  background: var(--color-status-pending-pay);
}

.pending-take {
  background: var(--color-status-pending-take);
}

.delivering {
  background: var(--color-status-delivering);
}

.finished {
  background: var(--color-status-finished);
}

.cancelled {
  background: var(--color-status-cancelled);
}
</style>
