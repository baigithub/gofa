<script setup lang="ts">
import { computed } from "vue";
import AppNavBar from "../components/AppNavBar.vue";
import MobileFrame from "../components/MobileFrame.vue";
import { useAppStore } from "../stores/app";
import { getUserPhone } from "../core/auth";

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

const quickEntries = [
  { title: "今日收益", desc: "¥56.00" },
  { title: "本周单量", desc: "12 单" },
  { title: "历史订单", desc: "可查看" },
];
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

        <el-card v-for="entry in quickEntries" :key="entry.title" class="entry-card" shadow="never">
          <div class="entry-title">{{ entry.title }}</div>
          <div class="entry-desc">{{ entry.desc }}</div>
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
.page {
  min-height: 100%;
  display: grid;
  grid-template-rows: auto 1fr auto;
}

.content {
  padding: var(--space-4);
  display: grid;
  gap: var(--space-3);
  align-content: start;
  overflow: auto;
}

.user-card,
.entry-card {
  border: 1px solid rgba(123, 155, 232, 0.18);
  background: rgba(12, 18, 34, 0.55);
}

.user-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
}

.name {
  color: #f2f6ff;
  font-size: 20px;
  font-weight: 900;
  letter-spacing: 0.2px;
}

.phone {
  margin-top: 4px;
  color: rgba(167, 186, 227, 0.85);
}

.score {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: rgba(167, 186, 227, 0.9);
}

.score strong {
  color: #7ef0bf;
  font-size: 22px;
}

:deep(.vip-tag) {
  color: #fff7eb;
  border: 1px solid rgba(255, 158, 64, 0.45);
  background: linear-gradient(135deg, #ffb15c, #ff8a1f) !important;
}

.entry-title {
  color: #f2f6ff;
  font-weight: 700;
}

.entry-desc {
  margin-top: 6px;
  color: rgba(167, 186, 227, 0.85);
  font-size: 13px;
}

.footer {
  border-top: 1px solid rgba(123, 155, 232, 0.18);
  padding: var(--space-3) var(--space-4);
  background: rgba(8, 12, 24, 0.65);
}

.panel-actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.message-btn,
.home-btn {
  width: 100%;
  min-height: 44px;
}

.message-btn {
  border-color: rgba(64, 158, 255, 0.65);
  background: linear-gradient(135deg, #409eff, #2b7de9);
}

:deep(.el-divider--horizontal) {
  margin: 12px 0;
  border-top-color: rgba(123, 155, 232, 0.18);
}
</style>
