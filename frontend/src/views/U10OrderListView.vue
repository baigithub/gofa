<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from "vue";
import AppNavBar from "../components/AppNavBar.vue";
import OrderCard from "../components/OrderCard.vue";
import AppStates from "../components/AppStates.vue";
import MobileFrame from "../components/MobileFrame.vue";
import { fetchOrders, type BackendOrderItem } from "../api/orders";
import { useAppStore } from "../stores/app";

const appStore = useAppStore();

type OrderStatus = "待支付" | "待接单" | "已接单" | "配送中" | "已完成";
type TabKey = "全部" | "待支付" | "进行中" | "已完成";
type UiOrder = {
  id: string;
  type: string;
  from: string;
  to: string;
  amount: string;
  time: string;
  createdAt: string;
  status: OrderStatus;
};

const emit = defineEmits<{
  (event: "back-home"): void;
  (event: "open-detail", page: "U11" | "U12" | "U13"): void;
}>();

const currentTab = ref<TabKey>("全部");
const isLoading = ref(false);
const isError = ref(false);

const tabs: { key: TabKey; label: string }[] = [
  { key: "全部", label: "全部" },
  { key: "待支付", label: "待支付" },
  { key: "进行中", label: "进行中" },
  { key: "已完成", label: "已完成" },
];

const orders = ref<UiOrder[]>([]);
const listRef = ref<HTMLElement | null>(null);
const pageSize = 4;
const visibleCount = ref(pageSize);

const typeLabelMap: Record<BackendOrderItem["order_type"], string> = {
  pickup: "帮取快递",
  buy: "帮买商品",
  errand: "万能跑腿",
};

const statusLabelMap: Record<BackendOrderItem["status"], OrderStatus> = {
  pending_pay: "待支付",
  pending_take: "待接单",
  accepted: "已接单",
  delivering: "配送中",
  completed: "已完成",
  cancelled: "已完成",
};

const formatTime = (iso: string) => {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "未知时间";
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  const h = String(d.getHours()).padStart(2, "0");
  const min = String(d.getMinutes()).padStart(2, "0");
  return `${m}-${day} ${h}:${min}`;
};

const toUiOrder = (item: BackendOrderItem): UiOrder => ({
  id: item.id,
  type: typeLabelMap[item.order_type],
  from: item.pickup_address || "待补充",
  to: item.delivery_address || "待补充",
  amount: `¥${(item.amount_cents / 100).toFixed(2)}`,
  time: formatTime(item.created_at),
  createdAt: item.created_at,
  status: statusLabelMap[item.status],
});

const loadOrders = async () => {
  isLoading.value = true;
  isError.value = false;
  try {
    const list = await fetchOrders(appStore.userId ?? undefined);
    orders.value = list
      .map(toUiOrder)
      .sort((a, b) => new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime());
    visibleCount.value = pageSize;
    await nextTick();
    if (listRef.value) listRef.value.scrollTop = 0;
  } catch {
    isError.value = true;
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  void loadOrders();
});

const filteredOrders = computed(() => {
  if (currentTab.value === "全部") return orders.value;
  if (currentTab.value === "待支付") return orders.value.filter((o) => o.status === "待支付");
  if (currentTab.value === "进行中")
    return orders.value.filter((o) => ["待接单", "已接单", "配送中"].includes(o.status));
  return orders.value.filter((o) => o.status === "已完成");
});

const visibleOrders = computed(() => filteredOrders.value.slice(0, visibleCount.value));

const canLoadMore = computed(() => visibleOrders.value.length < filteredOrders.value.length);

const loadMore = () => {
  if (!canLoadMore.value) return;
  visibleCount.value = Math.min(visibleCount.value + pageSize, filteredOrders.value.length);
};

watch(currentTab, async () => {
  visibleCount.value = pageSize;
  await nextTick();
  if (listRef.value) listRef.value.scrollTop = 0;
});

const counts = computed(() => {
  const all = orders.value.length;
  const pendingPay = orders.value.filter((o) => o.status === "待支付").length;
  const inProgress = orders.value.filter((o) => ["待接单", "已接单", "配送中"].includes(o.status)).length;
  const done = orders.value.filter((o) => o.status === "已完成").length;
  return { all, pendingPay, inProgress, done };
});

const actionText = (status: OrderStatus) => {
  if (status === "待支付") return "去支付";
  if (status === "已完成") return "再来一单";
  return "查看详情";
};

const openDetail = (status: OrderStatus) => {
  if (status === "待支付") emit("open-detail", "U11");
  else if (status === "已完成") emit("open-detail", "U13");
  else emit("open-detail", "U12");
};
</script>

<template>
  <MobileFrame>
    <div class="page">
      <AppNavBar title="订单" :show-back="true" @back="emit('back-home')" />

      <section class="toolbar">
        <el-card class="summary" shadow="never">
          <div class="summary-row">
            <div class="summary-left">
              <div class="summary-title">订单总览</div>
              <div class="summary-sub">快速筛选并跟踪履约进度</div>
            </div>
            <el-tag effect="dark" type="info" round size="small">V1</el-tag>
          </div>

          <div class="stats">
            <div class="stat">
              <div class="k">全部</div>
              <div class="v">{{ counts.all }}</div>
            </div>
            <div class="stat">
              <div class="k">待支付</div>
              <div class="v accent">{{ counts.pendingPay }}</div>
            </div>
            <div class="stat">
              <div class="k">进行中</div>
              <div class="v">{{ counts.inProgress }}</div>
            </div>
            <div class="stat">
              <div class="k">已完成</div>
              <div class="v">{{ counts.done }}</div>
            </div>
          </div>
        </el-card>

        <div class="seg">
          <el-button
            v-for="t in tabs"
            :key="t.key"
            size="small"
            round
            :type="currentTab === t.key ? 'primary' : 'default'"
            plain
            @click="currentTab = t.key"
          >
            {{ t.label }}
          </el-button>
        </div>
      </section>

      <section ref="listRef" class="list">
        <AppStates v-if="isLoading" mode="loading" />
        <AppStates
          v-else-if="isError"
          mode="error"
          title="加载失败"
          description="网络开小差了，请稍后重试"
          action-text="重试"
          @action="loadOrders"
        />
        <AppStates v-else-if="filteredOrders.length === 0" mode="empty" description="当前没有符合条件的订单" />
        <OrderCard
          v-else
          v-for="order in visibleOrders"
          :key="order.id"
          :type="order.type"
          :from="order.from"
          :to="order.to"
          :amount="order.amount"
          :time="order.time"
          :status="order.status"
          :action-text="actionText(order.status)"
          @action="openDetail(order.status)"
        />
        <div v-if="!isLoading && !isError && canLoadMore" class="load-more">
          <el-button size="small" round @click="loadMore">点击加载更多</el-button>
        </div>
        <p v-else-if="!isLoading && !isError && filteredOrders.length > 0" class="load-tip done">已显示全部</p>
      </section>

      <footer class="footer">
        <el-button class="home-btn" size="large" round @click="emit('back-home')">返回首页</el-button>
      </footer>
    </div>
  </MobileFrame>
</template>

<style scoped>
.page {
  min-height: 100%;
  display: grid;
  grid-template-rows: auto auto 1fr auto;
}

.toolbar {
  padding: var(--space-4);
  display: grid;
  gap: var(--space-3);
}

.summary {
  border: 1px solid rgba(123, 155, 232, 0.18);
  background: rgba(12, 18, 34, 0.55);
}

.summary-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  margin-bottom: var(--space-3);
}

.summary-title {
  font-weight: 800;
  color: #f2f6ff;
  letter-spacing: 0.2px;
}

.summary-sub {
  margin-top: 2px;
  color: rgba(167, 186, 227, 0.85);
  font-size: 12px;
}

.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-2);
}

.stat {
  padding: 10px 10px;
  border-radius: 12px;
  border: 1px solid rgba(123, 155, 232, 0.18);
  background: rgba(18, 26, 49, 0.75);
}

.stat .k {
  color: rgba(167, 186, 227, 0.9);
  font-size: 11px;
}

.stat .v {
  margin-top: 6px;
  font-size: 18px;
  font-weight: 700;
  color: #f2f6ff;
}

.stat .v.accent {
  color: #7ef0bf;
}

.seg {
  display: flex;
  gap: var(--space-2);
  overflow: auto;
  padding-bottom: 2px;
}

.seg :deep(.el-button) {
  border-color: rgba(123, 155, 232, 0.24);
  background: rgba(18, 26, 49, 0.55);
  color: #cfe0ff;
}

.seg :deep(.el-button--primary.is-plain) {
  background: linear-gradient(90deg, rgba(47, 125, 255, 0.3), rgba(86, 176, 255, 0.22));
  border-color: rgba(108, 162, 255, 0.55);
  color: #edf4ff;
}

.list {
  padding: var(--space-4);
  display: grid;
  gap: var(--space-3);
  align-content: start;
  overflow: auto;
}

.load-tip {
  margin: 2px 0 0;
  text-align: center;
  color: rgba(167, 186, 227, 0.85);
  font-size: 12px;
}

.load-tip.done {
  color: rgba(136, 155, 198, 0.85);
}

.load-more {
  display: grid;
  place-items: center;
  padding: 2px 0 0;
}

.footer {
  border-top: 1px solid rgba(123, 155, 232, 0.18);
  background: rgba(8, 12, 24, 0.65);
  padding: var(--space-3) var(--space-4);
}

.home-btn {
  width: 100%;
}
</style>
