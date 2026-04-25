<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { ElMessage } from "element-plus";
import AppNavBar from "../components/AppNavBar.vue";
import MobileFrame from "../components/MobileFrame.vue";
import AppStates from "../components/AppStates.vue";
import { fetchOrderById } from "../api/orders";
import { useAppStore } from "../stores/app";

type DetailOrder = {
  id: string;
  serviceType: string;
  statusText: string;
  statusDesc: string;
  from: string;
  to: string;
  phoneMasked: string;
  goodsList: string;
  fee: { base: number; extra: number; goods: number; total: number };
};

const emit = defineEmits<{
  (event: "back-list"): void;
  (event: "contact-runner"): void;
}>();

const appStore = useAppStore();
const loading = ref(false);
const loadFailed = ref(false);
const order = ref<DetailOrder | null>(null);

const hasRunnerAccepted = computed(() => false);

const mapOrderType = (type: string) => {
  if (type === "pickup") return "帮取快递";
  if (type === "buy") return "帮买商品";
  if (type === "errand") return "万能跑腿";
  return type;
};

const mapOrderStatus = (status: string) => {
  if (status === "pending_take") return { text: "待接单", desc: "已支付成功，正在为你匹配跑腿员" };
  if (status === "accepted") return { text: "已接单", desc: "跑腿员已接单，正在赶来" };
  if (status === "delivering") return { text: "配送中", desc: "跑腿员正在配送，请保持电话畅通" };
  if (status === "completed") return { text: "已完成", desc: "订单已完成，欢迎再次下单" };
  return { text: "进行中", desc: "订单处理中" };
};

const maskPhone = (phone: string) => {
  if (!phone || phone.length < 7) return phone || "—";
  return `${phone.slice(0, 3)}****${phone.slice(-4)}`;
};

const loadOrder = async () => {
  const orderId = appStore.pendingOrderId || appStore.activeOrderId;
  if (!orderId || orderId === "latest") {
    loadFailed.value = true;
    return;
  }

  loading.value = true;
  loadFailed.value = false;
  try {
    const item = await fetchOrderById(orderId);
    const status = mapOrderStatus(item.status);
    const total = (item.amount_cents ?? 0) / 100;
    order.value = {
      id: item.id,
      serviceType: mapOrderType(item.order_type),
      statusText: status.text,
      statusDesc: status.desc,
      from: item.pickup_address || "—",
      to: item.delivery_address || "—",
      phoneMasked: maskPhone(item.contact_phone),
      goodsList: item.remark || "无",
      fee: { base: total, extra: 0, goods: 0, total },
    };
    appStore.setActiveOrderId(item.id);
  } catch (error) {
    loadFailed.value = true;
    const msg = error instanceof Error ? error.message : "订单加载失败";
    ElMessage.error(msg);
  } finally {
    loading.value = false;
  }
};

const onContactRunner = () => {
  if (!hasRunnerAccepted.value) {
    ElMessage.info("当前还没有跑腿员接单，先进入会话留言，接单后将收到回复。");
  }
  emit("contact-runner");
};

onMounted(() => void loadOrder());
</script>

<template>
  <MobileFrame>
    <div class="page">
      <AppNavBar title="订单详情" :show-back="true" @back="emit('back-list')" />

      <section class="content">
        <AppStates v-if="loading" mode="loading" />
        <AppStates v-else-if="loadFailed || !order" mode="error" title="订单加载失败" description="请返回订单列表重试" @action="loadOrder" />

        <template v-else>
          <el-card class="status-card" shadow="never">
            <div class="status-top">
              <div>
                <div class="status-title">{{ order.statusText }}</div>
                <div class="status-desc">{{ order.statusDesc }}</div>
              </div>
              <el-tag effect="dark" type="info" round>{{ order.statusText }}</el-tag>
            </div>
            <el-divider />
            <div class="meta-row">
              <span class="k">订单号</span>
              <span class="v mono">{{ order.id }}</span>
            </div>
            <div class="meta-row">
              <span class="k">服务类型</span>
              <span class="v">{{ order.serviceType }}</span>
            </div>
          </el-card>

          <el-card class="info-card" shadow="never">
            <div class="card-title">配送信息</div>
            <div class="route">
              <div class="dot from"></div>
              <div class="route-main">
                <div class="place">{{ order.from }}</div>
                <div class="hint">取货点</div>
              </div>
            </div>
            <div class="route">
              <div class="dot to"></div>
              <div class="route-main">
                <div class="place">{{ order.to }}</div>
                <div class="hint">送达点</div>
              </div>
            </div>
            <el-divider />
            <div class="meta-row">
              <span class="k">订单备注</span>
              <span class="v">{{ order.goodsList }}</span>
            </div>
            <div class="meta-row">
              <span class="k">联系电话</span>
              <span class="v">{{ order.phoneMasked }}</span>
            </div>
          </el-card>

          <el-card class="fee-card" shadow="never">
            <div class="card-title">费用明细</div>
            <div class="meta-row">
              <span class="k">订单金额</span>
              <span class="v">¥{{ order.fee.total.toFixed(2) }}</span>
            </div>
            <div class="total">
              <span>实付</span>
              <strong>¥{{ order.fee.total.toFixed(2) }}</strong>
            </div>
          </el-card>
        </template>
      </section>

      <footer class="footer">
        <el-button class="primary" type="primary" size="large" round @click="onContactRunner">联系跑腿员</el-button>
        <el-button class="secondary" size="large" round @click="emit('back-list')">返回订单列表</el-button>
      </footer>
    </div>
  </MobileFrame>
</template>

<style scoped>
.page {
  min-height: 100%;
  display: grid;
  grid-template-rows: auto 1fr auto;
}

.content {
  padding: var(--space-4);
  display: grid;
  gap: var(--space-3);
  overflow: auto;
}

.status-card,
.info-card,
.fee-card {
  border: 1px solid rgba(123, 155, 232, 0.18);
  background: rgba(12, 18, 34, 0.55);
}

.status-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-3);
}

.status-title {
  font-weight: 900;
  font-size: 18px;
  color: #f2f6ff;
  letter-spacing: 0.2px;
  text-shadow: 0 0 14px rgba(55, 143, 255, 0.18);
}

.status-desc {
  margin-top: 6px;
  color: rgba(167, 186, 227, 0.9);
  font-size: 12px;
  line-height: 1.35;
}

.card-title {
  font-weight: 800;
  color: #f2f6ff;
  margin-bottom: var(--space-3);
}

.meta-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  padding: 6px 0;
}

.meta-row .k {
  color: rgba(167, 186, 227, 0.85);
  font-size: 12px;
  white-space: nowrap;
}

.meta-row .v {
  color: #f2f6ff;
  font-size: 13px;
  text-align: right;
}

.mono {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
  opacity: 0.9;
}

.route {
  display: grid;
  grid-template-columns: 18px 1fr;
  gap: var(--space-2);
  align-items: start;
  padding: 6px 0;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
  margin-top: 5px;
  box-shadow: 0 0 0 4px rgba(47, 125, 255, 0.08);
}

.dot.from {
  background: #56b0ff;
}

.dot.to {
  background: #7ef0bf;
}

.place {
  color: #f2f6ff;
  font-weight: 700;
}

.hint {
  margin-top: 2px;
  color: rgba(167, 186, 227, 0.8);
  font-size: 12px;
}

.total {
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px dashed rgba(123, 155, 232, 0.22);
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: rgba(167, 186, 227, 0.95);
}

.total strong {
  color: #56b0ff;
  font-size: 18px;
  letter-spacing: 0.2px;
}

.footer {
  border-top: 1px solid rgba(123, 155, 232, 0.18);
  background: rgba(8, 12, 24, 0.65);
  padding: var(--space-3) var(--space-4);
  display: grid;
  gap: var(--space-2);
}

.primary,
.secondary {
  width: 100%;
}

:deep(.el-divider--horizontal) {
  margin: 12px 0;
  border-top-color: rgba(123, 155, 232, 0.18);
}
</style>
