<script setup lang="ts">
import { onMounted, ref } from "vue";
import { ElMessage } from "element-plus";
import AppNavBar from "../components/AppNavBar.vue";
import MobileFrame from "../components/MobileFrame.vue";
import AppStates from "../components/AppStates.vue";
import { fetchOrderById } from "../api/orders";
import { useAppStore } from "../stores/app";

const emit = defineEmits<{
  (event: "back-list"): void;
  (event: "go-pay"): void;
}>();

const appStore = useAppStore();
const loading = ref(false);
const loadFailed = ref(false);

const order = ref({
  id: "",
  serviceType: "",
  statusText: "待支付",
  statusDesc: "请在 15 分钟内完成支付，否则订单将自动取消",
  from: "—",
  to: "—",
  phoneMasked: "—",
  total: 0,
});

const mapOrderType = (type: string) => {
  if (type === "pickup") return "帮取快递";
  if (type === "buy") return "帮买商品";
  if (type === "errand") return "万能跑腿";
  return type;
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
    order.value = {
      id: item.id,
      serviceType: mapOrderType(item.order_type),
      statusText: item.status === "pending_pay" ? "待支付" : "订单状态已更新",
      statusDesc: item.status === "pending_pay" ? "请在 15 分钟内完成支付，否则订单将自动取消" : "订单已不在待支付状态",
      from: item.pickup_address || "—",
      to: item.delivery_address || "—",
      phoneMasked: maskPhone(item.contact_phone),
      total: (item.amount_cents ?? 0) / 100,
    };
    appStore.setActiveOrderId(item.id);
    appStore.setPendingOrderId(item.status === "pending_pay" ? item.id : null);
  } catch (e) {
    loadFailed.value = true;
    const msg = e instanceof Error ? e.message : "订单加载失败";
    ElMessage.error(msg);
  } finally {
    loading.value = false;
  }
};

onMounted(() => void loadOrder());
</script>

<template>
  <MobileFrame>
    <div class="page">
      <AppNavBar title="订单详情" :show-back="true" @back="emit('back-list')" />

      <section class="content">
        <AppStates v-if="loading" mode="loading" />
        <AppStates v-else-if="loadFailed" mode="error" title="订单加载失败" description="请返回订单列表重试" @action="loadOrder" />

        <template v-else>
          <el-card class="status-card" shadow="never">
            <div class="status-top">
              <div>
                <div class="status-title">{{ order.statusText }}</div>
                <div class="status-desc">{{ order.statusDesc }}</div>
              </div>
              <el-tag effect="dark" type="warning" round>待支付</el-tag>
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
              <span class="k">联系电话</span>
              <span class="v">{{ order.phoneMasked }}</span>
            </div>
          </el-card>

          <el-card class="fee-card" shadow="never">
            <div class="card-title">费用明细</div>
            <div class="total">
              <span>实付</span>
              <strong>¥{{ order.total.toFixed(2) }}</strong>
            </div>
          </el-card>
        </template>
      </section>

      <footer class="footer">
        <el-button class="primary" type="primary" size="large" round @click="emit('go-pay')">立即支付</el-button>
        <el-button class="secondary" size="large" round @click="emit('back-list')">返回订单列表</el-button>
      </footer>
    </div>
  </MobileFrame>
</template>

<style scoped>
.page { min-height: 100%; display: grid; grid-template-rows: auto 1fr auto; }
.content { padding: var(--space-4); display: grid; gap: var(--space-3); overflow: auto; }
.status-card,.info-card,.fee-card { border: 1px solid rgba(123,155,232,.18); background: rgba(12,18,34,.55); }
.status-top { display:flex; align-items:flex-start; justify-content:space-between; gap:var(--space-3); }
.status-title { font-weight:900; font-size:18px; color:#f2f6ff; }
.status-desc { margin-top:6px; color:rgba(167,186,227,.9); font-size:12px; }
.card-title { font-weight:800; color:#f2f6ff; margin-bottom:var(--space-3); }
.meta-row { display:flex; align-items:center; justify-content:space-between; gap:var(--space-3); padding:6px 0; }
.meta-row .k { color:rgba(167,186,227,.85); font-size:12px; }
.meta-row .v { color:#f2f6ff; font-size:13px; text-align:right; }
.mono { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
.route { display:grid; grid-template-columns:18px 1fr; gap:var(--space-2); align-items:start; padding:6px 0; }
.dot { width:10px; height:10px; border-radius:999px; margin-top:5px; }
.dot.from { background:#56b0ff; }
.dot.to { background:#7ef0bf; }
.place { color:#f2f6ff; font-weight:700; }
.hint { margin-top:2px; color:rgba(167,186,227,.8); font-size:12px; }
.total { margin-top:10px; padding-top:10px; border-top:1px dashed rgba(123,155,232,.22); display:flex; justify-content:space-between; }
.total strong { color:#7ef0bf; font-size:18px; }
.footer { border-top:1px solid rgba(123,155,232,.18); background:rgba(8,12,24,.65); padding:var(--space-3) var(--space-4); display:grid; gap:var(--space-2); }
.primary,.secondary{ width:100%; }
</style>
