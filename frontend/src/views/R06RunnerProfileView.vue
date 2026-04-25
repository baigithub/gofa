<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { ElMessage } from "element-plus";
import AppNavBar from "../components/AppNavBar.vue";
import MobileFrame from "../components/MobileFrame.vue";
import { useAppStore } from "../stores/app";
import { getUserPhone } from "../core/auth";
import { fetchRunnerDashboardStats, fetchRunnerHistoryOrders, type RunnerOrderItem } from "../api/runner";

const emit = defineEmits<{
  (event: "back-hall"): void;
  (event: "go-message"): void;
}>();

const appStore = useAppStore();

const profilePhone = computed(() => appStore.userPhone || getUserPhone() || "17800000011");
const profileNickname = computed(() => appStore.userNickname || "跑腿同学");

const profileLevel = computed(() => {
  if (appStore.userRole === "admin") return "管理员";
  if (appStore.userRole === "runner") return "跑腿员";
  return "普通用户";
});

const loading = ref(false);
const historyOrders = ref<RunnerOrderItem[]>([]);
const todayEarningsText = ref("¥0.00");
const weekOrdersText = computed(() => `${historyOrders.value.filter((o) => o.status === "completed").length} 单`);
const historyCountText = computed(() => `${historyOrders.value.length} 单`);

const statusText = (status: RunnerOrderItem["status"]) => {
  if (status === "pending_take") return "待接单";
  if (status === "accepted") return "已接单";
  if (status === "delivering") return "配送中";
  if (status === "completed") return "已完成";
  if (status === "cancelled") return "已取消";
  return "待支付";
};

const formatTime = (iso: string) => {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "--";
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  const h = String(d.getHours()).padStart(2, "0");
  const min = String(d.getMinutes()).padStart(2, "0");
  return `${m}-${day} ${h}:${min}`;
};

const loadRunnerData = async () => {
  if (!appStore.userId) return;
  loading.value = true;
  try {
    const [stats, history] = await Promise.all([
      fetchRunnerDashboardStats(appStore.userId),
      fetchRunnerHistoryOrders(appStore.userId),
    ]);
    todayEarningsText.value = `¥${(stats.today_earnings_cents / 100).toFixed(2)}`;
    historyOrders.value = history.slice(0, 3);
  } catch (error) {
    const msg = error instanceof Error ? error.message : "加载失败";
    ElMessage.warning(msg);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  void loadRunnerData();
});
</script>

<template>
  <MobileFrame>
    <div class="page">
      <AppNavBar title="我的" :show-back="true" @back="emit('back-hall')" />

      <section class="content">
        <el-card class="user-card" shadow="never">
          <div class="user-head">
            <div>
              <div class="name">{{ profileNickname }}</div>
              <div class="phone">手机号：{{ profilePhone }}</div>
            </div>
            <el-tag class="vip-tag" effect="dark" round>{{ profileLevel }}</el-tag>
          </div>
          <el-divider />
          <div class="score">
            <span>信用分</span>
            <strong>92</strong>
          </div>
        </el-card>

        <el-card class="entry-card" shadow="never">
          <div class="entry-title">今日收益</div>
          <div class="entry-desc">{{ todayEarningsText }}</div>
        </el-card>

        <el-card class="entry-card" shadow="never">
          <div class="entry-title">本周单量</div>
          <div class="entry-desc">{{ weekOrdersText }}</div>
        </el-card>

        <el-card class="entry-card" shadow="never">
          <div class="entry-title">历史订单</div>
          <div class="entry-desc">{{ loading ? '加载中...' : historyCountText }}</div>
          <div v-if="historyOrders.length" class="history-list">
            <button v-for="item in historyOrders" :key="item.id" class="history-item" type="button">
              <div class="history-left">
                <div class="history-status">{{ statusText(item.status) }}</div>
                <div class="history-time">{{ formatTime(item.updated_at) }}</div>
              </div>
              <div class="history-right">¥{{ (item.amount_cents / 100).toFixed(2) }}</div>
            </button>
          </div>
        </el-card>
      </section>

      <footer class="footer">
        <div class="panel-actions">
          <el-button class="message-btn" type="primary" size="large" round @click="emit('go-message')">消息窗口</el-button>
          <el-button class="home-btn" size="large" round @click="emit('back-hall')">返回大厅</el-button>
        </div>
      </footer>
    </div>
  </MobileFrame>
</template>

<style scoped>
.page { min-height: 100%; display: grid; grid-template-rows: auto 1fr auto; }
.content { padding: var(--space-4); display: grid; gap: var(--space-3); align-content: start; overflow: auto; }
.user-card,.entry-card { border: 1px solid rgba(123,155,232,.18); background: rgba(12,18,34,.55); }
.user-head { display:flex; align-items:center; justify-content:space-between; gap:var(--space-3); }
.name { color:#f2f6ff; font-size:20px; font-weight:900; }
.phone { margin-top:4px; color:rgba(167,186,227,.85); }
.score { display:flex; align-items:center; justify-content:space-between; color:rgba(167,186,227,.9); }
.score strong { color:#7ef0bf; font-size:22px; }
:deep(.vip-tag){ color:#fff7eb; border:1px solid rgba(255,158,64,.45); background:linear-gradient(135deg,#ffb15c,#ff8a1f)!important; }
.entry-title { color:#f2f6ff; font-weight:700; }
.entry-desc { margin-top:6px; color:rgba(167,186,227,.85); font-size:13px; }
.history-list { margin-top:10px; display:grid; gap:8px; }
.history-item { width:100%; border:1px solid rgba(123,155,232,.16); background:rgba(18,26,49,.6); border-radius:10px; padding:10px; display:flex; justify-content:space-between; align-items:center; }
.history-left { text-align:left; }
.history-status { color:#f2f6ff; font-size:13px; font-weight:700; }
.history-time { margin-top:2px; color:rgba(167,186,227,.75); font-size:12px; }
.history-right { color:#7ef0bf; font-weight:700; }
.footer { border-top:1px solid rgba(123,155,232,.18); padding:var(--space-3) var(--space-4); background:rgba(8,12,24,.65); }
.panel-actions { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:10px; }
.message-btn,.home-btn { width:100%; min-height:44px; }
.message-btn { border-color:rgba(64,158,255,.65); background:linear-gradient(135deg,#409eff,#2b7de9); }
:deep(.el-divider--horizontal) { margin:12px 0; border-top-color:rgba(123,155,232,.18); }
</style>
