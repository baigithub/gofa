<script setup lang="ts">
import { computed, ref } from "vue";
import { ElMessage } from "element-plus";
import AppButton from "../components/AppButton.vue";
import AppNavBar from "../components/AppNavBar.vue";
import { createOrder } from "../api/orders";
import { useAppStore } from "../stores/app";

const props = defineProps<{
  serviceType: "U03" | "U04" | "U05";
}>();

const emit = defineEmits<{
  (event: "back"): void;
  (event: "submit-pay", orderId: string): void;
}>();

const serviceName = computed(() => {
  if (props.serviceType === "U03") return "帮取快递";
  if (props.serviceType === "U04") return "帮买商品";
  return "万能跑腿";
});

const appStore = useAppStore();
const creatingOrder = ref(false);

const fee = computed(() => {
  return appStore.calcFee();
});

const orderType = computed(() => {
  if (props.serviceType === "U03") return "pickup" as const;
  if (props.serviceType === "U04") return "buy" as const;
  return "errand" as const;
});

const submitOrderAndPay = async () => {
  if (!appStore.userId) {
    ElMessage.error("请先登录后再下单");
    return;
  }
  if (creatingOrder.value) return;
  creatingOrder.value = true;
  try {
    const payload = {
      user_id: appStore.userId,
      order_type: orderType.value,
      pickup_address: "北门驿站",
      delivery_address: "1号宿舍楼",
      contact_phone: appStore.userPhone || "17800000000",
      remark: `${serviceName.value}下单`,
      amount_cents: Math.round(fee.value.total * 100),
    };
    console.info("[gofer] order.create.request", payload);
    const order = await createOrder(payload);
    console.info("[gofer] order.create.success", order);
    ElMessage.success("订单已创建，请完成支付");
    emit("submit-pay", order.id);
  } catch (error) {
    console.error("[gofer] order.create.failed", error);
    const msg = error instanceof Error ? error.message : "下单失败";
    ElMessage.error(msg);
  } finally {
    creatingOrder.value = false;
  }
};
</script>

<template>
  <main class="page">
    <section class="phone">
      <AppNavBar title="确认订单" :show-back="true" />

      <div class="content">
        <section class="card">
          <h3>配送信息</h3>
          <p>服务类型：{{ serviceName }}</p>
          <p>取货地址：北门驿站</p>
          <p>送达地址：1号宿舍楼</p>
          <p>联系电话：138****8888</p>
        </section>

        <section class="card">
          <h3>费用明细</h3>
          <div class="fee-row">
            <span>跑腿费</span>
            <span>¥{{ fee.base.toFixed(2) }}</span>
          </div>
          <div v-if="fee.goods > 0" class="fee-row">
            <span>商品预估</span>
            <span>¥{{ fee.goods.toFixed(2) }}</span>
          </div>
          <div class="fee-row">
            <span>加价费</span>
            <span>¥{{ fee.extra.toFixed(2) }}</span>
          </div>
          <div class="fee-row total">
            <span>实付金额</span>
            <strong>¥{{ fee.total.toFixed(2) }}</strong>
          </div>
        </section>
      </div>

      <footer class="footer">
        <p class="tip">提交即表示同意《跑腿服务协议》</p>
        <AppButton :disabled="creatingOrder" @click="submitOrderAndPay">{{ creatingOrder ? '提交中...' : '提交并支付' }}</AppButton>
        <AppButton variant="secondary" @click="emit('back')">返回修改</AppButton>
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
  overflow: auto;
}

.card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  padding: var(--space-4);
}

.card h3 {
  margin: 0 0 var(--space-3);
  font-size: var(--font-size-md);
}

.card p {
  margin: 0 0 var(--space-2);
  color: var(--color-text-secondary);
}

.fee-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: var(--space-2);
}

.total {
  margin-top: var(--space-2);
  padding-top: var(--space-2);
  border-top: 1px dashed var(--color-border);
}

.total strong {
  color: var(--color-primary);
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

.tip {
  margin: 0;
  color: var(--color-text-placeholder);
  font-size: var(--font-size-xs);
}
</style>
