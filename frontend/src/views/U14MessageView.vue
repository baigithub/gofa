<script setup lang="ts">
import AppNavBar from "../components/AppNavBar.vue";
import AppStates from "../components/AppStates.vue";
import { ref } from "vue";
import MobileFrame from "../components/MobileFrame.vue";

const emit = defineEmits<{
  (event: "back-home"): void;
}>();

const messages = [
  { title: "支付成功", content: "你的订单已支付成功，正在等待接单", time: "刚刚" },
  { title: "接单成功", content: "跑腿员小王已接单，正在前往取货", time: "10分钟前" },
  { title: "送达通知", content: "你的订单已送达，请确认收货", time: "昨天" },
];

const isLoading = ref(false);
const unreadCount = ref(2);
</script>

<template>
  <MobileFrame>
    <div class="page">
      <AppNavBar title="消息中心" :show-back="true" @back="emit('back-home')" />

      <section class="toolbar">
        <el-card class="summary" shadow="never">
          <div class="summary-row">
            <div>
              <div class="summary-title">通知总览</div>
              <div class="summary-sub">系统、履约、支付消息统一汇总</div>
            </div>
            <el-tag type="danger" effect="dark" round>未读 {{ unreadCount }}</el-tag>
          </div>
        </el-card>
      </section>

      <section class="list">
        <AppStates v-if="isLoading" mode="loading" />
        <AppStates v-else-if="messages.length === 0" mode="empty" description="暂无消息通知" />
        <el-card v-for="msg in messages" :key="msg.title + msg.time" class="item" shadow="never">
          <div class="item-head">
            <h3>{{ msg.title }}</h3>
            <el-tag size="small" effect="dark" type="info" round>{{ msg.time }}</el-tag>
          </div>
          <p>{{ msg.content }}</p>
        </el-card>
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
}

.summary-title {
  color: #f2f6ff;
  font-weight: 800;
}

.summary-sub {
  margin-top: 4px;
  color: rgba(167, 186, 227, 0.85);
  font-size: 12px;
}

.list {
  padding: 0 var(--space-4) var(--space-4);
  display: grid;
  gap: var(--space-3);
  align-content: start;
  overflow: auto;
}

.item {
  border: 1px solid rgba(123, 155, 232, 0.18);
  background: rgba(12, 18, 34, 0.55);
}

.item-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-2);
}

.item h3 {
  margin: 0;
  color: #f2f6ff;
  font-size: 15px;
}

.item p {
  margin: var(--space-2) 0 0;
  color: rgba(167, 186, 227, 0.9);
  line-height: 1.45;
}

.footer {
  border-top: 1px solid rgba(123, 155, 232, 0.18);
  padding: var(--space-3) var(--space-4);
  background: rgba(8, 12, 24, 0.65);
}

.home-btn {
  width: 100%;
}
</style>
