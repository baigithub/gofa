<script setup lang="ts">
import MobileFrame from "../components/MobileFrame.vue";

const emit = defineEmits<{
  (event: "go-service", service: "U03" | "U04" | "U05"): void;
  (event: "go-page", page: "U10" | "U14" | "U15"): void;
}>();

const serviceCards = [
  { key: "U03", title: "帮取快递", desc: "快速取件送到宿舍" },
  { key: "U04", title: "帮买商品", desc: "超市零食饮料代买" },
  { key: "U05", title: "万能跑腿", desc: "自定义跑腿需求" },
] as const;
</script>

<template>
  <MobileFrame>
    <header class="head">
      <div class="left">
        <p class="tag">CONTROL PANEL</p>
        <h1>首页</h1>
      </div>
      <el-tag class="campus" effect="dark" type="primary" round>北校区</el-tag>
    </header>

    <el-card class="search-card" shadow="never">
      <el-input placeholder="搜索服务或问题" clearable>
        <template #prefix>
          <span class="prefix-dot"></span>
        </template>
      </el-input>
    </el-card>

    <section class="grid">
      <el-card v-for="card in serviceCards" :key="card.title" class="svc" shadow="never">
        <div class="svc-top">
          <h2>{{ card.title }}</h2>
          <el-tag size="small" effect="dark" type="info" round>V1</el-tag>
        </div>
        <p>{{ card.desc }}</p>
        <el-button class="go" type="primary" @click="emit('go-service', card.key)">立即下单</el-button>
      </el-card>
    </section>

    <el-alert
      class="notice"
      title="高峰期配送时效可能延长，请提前下单"
      type="info"
      :closable="false"
      show-icon
    />

    <nav class="bottom">
      <el-button text class="active">首页</el-button>
      <el-button text @click="emit('go-page', 'U10')">订单</el-button>
      <el-button text @click="emit('go-page', 'U14')">消息</el-button>
      <el-button text @click="emit('go-page', 'U15')">我的</el-button>
    </nav>
  </MobileFrame>
</template>

<style scoped>
.head {
  display: flex;
  justify-content: space-between;
  align-items: end;
  margin-top: 6px;
  margin-bottom: 10px;
}

.tag {
  margin: 0;
  font-size: 11px;
  letter-spacing: 2px;
  color: #8fb7ff;
}

h1 {
  margin: 2px 0 0;
  font-size: 22px;
  color: #f2f6ff;
  text-shadow: 0 0 14px rgba(55, 143, 255, 0.35);
}

.campus {
  border-color: rgba(122, 155, 231, 0.35);
}

.search-card {
  margin-bottom: 12px;
}

.prefix-dot {
  width: 8px;
  height: 8px;
  display: inline-block;
  border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, #56b0ff, #2f7dff);
  box-shadow: 0 0 10px rgba(86, 176, 255, 0.45);
}

.grid {
  display: grid;
  gap: 12px;
}

.svc :deep(.el-card__body) {
  padding: 14px;
}

.svc-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.svc h2 {
  margin: 0;
  color: #f2f6ff;
  font-size: 16px;
}

.svc p {
  margin: 0 0 10px;
  color: #9fb0cf;
}

.go {
  width: 100%;
}

.notice {
  margin-top: 12px;
}

.bottom {
  margin-top: auto;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  border-top: 1px solid rgba(122, 155, 231, 0.18);
  padding-top: 10px;
  gap: 6px;
}

.bottom :deep(.el-button) {
  color: #9fb0cf;
}

.bottom .active {
  color: #56b0ff;
  font-weight: 700;
}
</style>
