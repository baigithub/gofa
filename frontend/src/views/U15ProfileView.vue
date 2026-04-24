<script setup lang="ts">
import AppNavBar from "../components/AppNavBar.vue";
import MobileFrame from "../components/MobileFrame.vue";
import { useAppStore } from "../stores/app";

const emit = defineEmits<{
  (event: "back-home"): void;
  (event: "go-runner"): void;
  (event: "go-admin"): void;
}>();

const appStore = useAppStore();

const profile = {
  name: "张同学",
  phone: "138****8888",
  level: "普通会员",
  score: 86,
};

const quickEntries = [
  { title: "常用地址", desc: "1号宿舍楼 / 图书馆 / 教学楼A" },
  { title: "我的优惠券", desc: "暂无可用优惠券" },
  { title: "客服中心", desc: "在线客服（9:00 - 22:00）" },
];
</script>

<template>
  <MobileFrame>
    <div class="page">
      <AppNavBar title="我的" :show-back="true" @back="emit('back-home')" />

      <section class="content">
        <el-card class="user-card" shadow="never">
          <div class="user-head">
            <div>
              <div class="name">{{ profile.name }}</div>
              <div class="phone">手机号：{{ profile.phone }}</div>
            </div>
            <el-tag type="primary" effect="dark" round>{{ profile.level }}</el-tag>
          </div>
          <el-divider />
          <div class="score">
            <span>信用分</span>
            <strong>{{ profile.score }}</strong>
          </div>
        </el-card>

        <el-card v-for="entry in quickEntries" :key="entry.title" class="entry-card" shadow="never">
          <div class="entry-title">{{ entry.title }}</div>
          <div class="entry-desc">{{ entry.desc }}</div>
        </el-card>
      </section>

      <footer class="footer">
        <div class="panel-actions" v-if="appStore.userRole === 'runner' || appStore.userRole === 'admin'">
          <el-button
            v-if="appStore.userRole === 'runner' || appStore.userRole === 'admin'"
            class="runner-btn"
            type="primary"
            size="large"
            round
            @click="emit('go-runner')"
          >
            进入跑腿端
          </el-button>
          <el-button
            v-if="appStore.userRole === 'admin'"
            class="admin-btn"
            type="danger"
            size="large"
            round
            @click="emit('go-admin')"
          >
            进入管理端
          </el-button>
        </div>
        <el-button class="home-btn" size="large" round @click="emit('back-home')">返回首页</el-button>
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
  display: grid;
  gap: var(--space-2);
}

.panel-actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.runner-btn,
.admin-btn,
.home-btn {
  width: 100%;
  min-height: 44px;
}

.runner-btn {
  border-color: rgba(64, 158, 255, 0.65);
  background: linear-gradient(135deg, #409eff, #2b7de9);
}

.admin-btn {
  border-color: rgba(245, 108, 108, 0.65);
  background: linear-gradient(135deg, #f56c6c, #d94b4b);
}

:deep(.el-divider--horizontal) {
  margin: 12px 0;
  border-top-color: rgba(123, 155, 232, 0.18);
}
</style>
