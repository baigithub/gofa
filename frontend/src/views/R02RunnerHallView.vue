<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { ElButton, ElTag, ElAlert, ElIcon, ElMessage } from "element-plus";
import { Timer, Wallet } from "@element-plus/icons-vue";
import { useAppStore } from "../stores/app";
import { fetchRunnerDashboardStats, fetchHallOrders, acceptOrder, type RunnerDashboardStats, type RunnerOrderItem } from "../api/runner";
import OrderCard from "../components/OrderCard.vue";

const emit = defineEmits<{(event:"next"):void;(event:"back-home"):void;(event:"go-profile"):void;}>();
const appStore = useAppStore();
const stats = ref<RunnerDashboardStats | null>(null);
const hallOrders = ref<RunnerOrderItem[]>([]);

const isReviewing = computed(() => stats.value ? !stats.value.is_verified || stats.value.verification_status !== "approved" : false);
const todayEarnings = computed(() => `¥${((stats.value?.today_earnings_cents ?? 0) / 100).toFixed(2)}`);
const availableOrderCount = computed(() => stats.value?.available_order_count ?? hallOrders.value.length);
const statsHint = computed(() => (stats.value ? "数据已更新" : "正在同步数据"));

const typeLabel = (type: RunnerOrderItem["order_type"]) => {
  if (type === "pickup") return "帮取快递";
  if (type === "buy") return "帮买商品";
  return "万能跑腿";
};

const load = async () => {
  if (!appStore.userId) return;
  try {
    const [statsData, orders] = await Promise.all([
      fetchRunnerDashboardStats(appStore.userId),
      fetchHallOrders(),
    ]);
    stats.value = statsData;
    hallOrders.value = orders.filter((item) => item.status === "pending_take");
  } catch (error) {
    console.info("[gofer] load runner hall data failed", error);
  }
};

const onAccept = async (order: RunnerOrderItem) => {
  if (!appStore.userId) return;
  if (isReviewing.value) return;
  try {
    await acceptOrder(order.id, appStore.userId);
    ElMessage.success("接单成功");
    appStore.setActiveOrderId(order.id);
    emit("next");
  } catch (error) {
    const msg = error instanceof Error ? error.message : "接单失败";
    ElMessage.error(msg);
  }
};

onMounted(async () => {
  console.info("[gofer] mount R02RunnerHallView");
  await load();
});
</script>
<template>
  <main class="page">
    <section class="phone">
      <section class="hero">
        <div class="hero-bg"></div>
        <div class="hero-content">
          <div class="hero-top">
            <div class="brand-pill">RUNNER HUB</div>
            <el-tag type="success" effect="dark" round size="small">可接单</el-tag>
          </div>
          <h1>接单大厅</h1>
          <p>附近可接订单 · 抢单更快，收益更稳</p>
          <div class="stats">
            <div class="stat">
              <el-icon><Wallet /></el-icon>
              <div>
                <strong>{{ todayEarnings }}</strong>
                <span>今日收益</span>
              </div>
            </div>
            <div class="stat">
              <el-icon><Timer /></el-icon>
              <div>
                <strong>{{ availableOrderCount }}</strong>
                <span>可接订单</span>
              </div>
            </div>
          </div>
          <div class="stats-hint">{{ statsHint }}</div>
        </div>
      </section>

      <section class="notice-wrap">
        <el-alert
          v-if="isReviewing"
          title="您的认证还在审核中，请耐心等待～"
          type="warning"
          :closable="false"
          show-icon
        />
        <el-alert v-else title="优先接单距离近、时效紧的订单" type="info" :closable="false" show-icon />
      </section>

      <section class="list">
        <div class="section-head">
          <span class="section-title">可接订单</span>
          <span class="section-sub">实时数据</span>
        </div>

        <el-alert
          v-if="hallOrders.length === 0"
          title="当前暂无可接订单"
          type="info"
          :closable="false"
          show-icon
        />

        <OrderCard
          v-for="item in hallOrders"
          v-else
          :key="item.id"
          :type="typeLabel(item.order_type)"
          :from="item.pickup_address || '待补充'"
          :to="item.delivery_address || '待补充'"
          :amount="`¥${(item.amount_cents / 100).toFixed(2)}`"
          :time="'刚刚发布'"
          status="待接单"
          :action-text="isReviewing ? '审核中' : '立即接单'"
          @action="isReviewing ? undefined : onAccept(item)"
        />
      </section>

      <footer class="footer">
        <el-button type="primary" size="large" round @click="emit('go-profile')">我的</el-button>
        <el-button size="large" round @click="emit('back-home')">返回用户端</el-button>
      </footer>
    </section>
  </main>
</template>
<style scoped>
.page{min-height:100svh;display:grid;place-items:center;background:radial-gradient(circle at top,#1b2a52 0,#0b1120 42%,#070b14 100%)}
.phone{width:min(100vw,390px);min-height:100svh;display:grid;grid-template-rows:auto auto 1fr auto;background:linear-gradient(180deg,rgba(9,14,26,.92),rgba(10,16,30,.96));color:#eef4ff;box-shadow:0 20px 60px rgba(0,0,0,.35)}
.hero{position:relative;margin:16px 16px 0;padding:18px 16px 16px;border-radius:20px;overflow:hidden;border:1px solid rgba(123,155,232,.18);background:linear-gradient(135deg,rgba(47,125,255,.28),rgba(13,22,44,.78))}
.hero-bg{position:absolute;inset:-40px;background:radial-gradient(circle at 20% 20%,rgba(86,176,255,.45),transparent 30%),radial-gradient(circle at 80% 0%,rgba(47,125,255,.28),transparent 24%),radial-gradient(circle at 50% 100%,rgba(124,92,255,.18),transparent 28%);filter:blur(8px)}
.hero-content{position:relative;z-index:1}.hero-top{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px}.brand-pill{display:inline-flex;align-items:center;padding:6px 10px;border-radius:999px;background:rgba(255,255,255,.12);color:#dfeaff;font-size:12px;font-weight:700;letter-spacing:.8px}
h1{margin:0;font-size:24px;line-height:1.1;letter-spacing:.2px}p{margin:8px 0 0;color:rgba(231,239,255,.86)}
.stats{margin-top:14px;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}.stat{display:flex;align-items:center;gap:10px;padding:12px;border-radius:16px;background:rgba(9,15,29,.45);border:1px solid rgba(123,155,232,.14)}.stat :deep(.el-icon){font-size:18px;color:#8fc3ff}.stat strong{display:block;font-size:16px;color:#fff}.stat span{display:block;margin-top:2px;font-size:12px;color:rgba(199,214,243,.76)}.stats-hint{margin-top:10px;color:rgba(199,214,243,.72);font-size:12px}
.notice-wrap{padding:12px 16px 0}.list{padding:14px 16px;display:grid;align-content:start;gap:12px}.section-head{display:flex;align-items:baseline;justify-content:space-between;padding:0 2px}.section-title{font-size:14px;font-weight:800;color:#f4f8ff}.section-sub{font-size:12px;color:rgba(199,214,243,.7)}
.footer{border-top:1px solid rgba(123,155,232,.14);padding:12px 16px 14px;background:rgba(8,12,24,.72);display:grid;gap:10px}
:deep(.el-alert){border-radius:14px;background:rgba(24,38,64,.7);border-color:rgba(123,155,232,.16)}
:deep(.el-button){height:44px;font-weight:700}
:deep(.el-button--primary){background:linear-gradient(135deg,#2f7dff,#56b0ff);border:none;box-shadow:0 10px 24px rgba(47,125,255,.22)}
:deep(.el-button:not(.el-button--primary)){background:rgba(255,255,255,.04);border-color:rgba(123,155,232,.18);color:#e8f0ff}
</style>
