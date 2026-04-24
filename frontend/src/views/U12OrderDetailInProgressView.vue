<script setup lang="ts">
import { ElMessage } from "element-plus";
import AppNavBar from "../components/AppNavBar.vue";
import MobileFrame from "../components/MobileFrame.vue";

const emit = defineEmits<{
  (event: "back-list"): void;
  (event: "contact-runner"): void;
}>();

const order = {
  id: "20260423-002",
  serviceType: "帮买商品",
  statusText: "待接单",
  statusDesc: "已支付成功，正在为你匹配跑腿员",
  from: "一食堂",
  to: "图书馆",
  phoneMasked: "138****8888",
  goodsList: "矿泉水 2 瓶 / 面包 1 个",
  fee: { base: 8, extra: 2, goods: 50, total: 60 },
};

const hasRunnerAccepted = false;

const onContactRunner = () => {
  if (!hasRunnerAccepted) {
    ElMessage.info("当前还没有跑腿员接单，先进入会话留言，接单后将收到回复。");
  }
  emit("contact-runner");
};
</script>

<template>
  <MobileFrame>
    <div class="page">
      <AppNavBar title="订单详情" :show-back="true" @back="emit('back-list')" />

      <section class="content">
        <el-card class="status-card" shadow="never">
          <div class="status-top">
            <div>
              <div class="status-title">{{ order.statusText }}</div>
              <div class="status-desc">{{ order.statusDesc }}</div>
            </div>
            <el-tag effect="dark" type="info" round>待接单</el-tag>
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
              <div class="hint">购买点</div>
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
            <span class="k">商品清单</span>
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
            <span class="k">跑腿费</span>
            <span class="v">¥{{ order.fee.base.toFixed(2) }}</span>
          </div>
          <div class="meta-row">
            <span class="k">商品预估</span>
            <span class="v">¥{{ order.fee.goods.toFixed(2) }}</span>
          </div>
          <div class="meta-row">
            <span class="k">加价费</span>
            <span class="v">¥{{ order.fee.extra.toFixed(2) }}</span>
          </div>
          <div class="total">
            <span>实付</span>
            <strong>¥{{ order.fee.total.toFixed(2) }}</strong>
          </div>
        </el-card>
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
