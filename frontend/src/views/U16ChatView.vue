<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { ElMessage } from "element-plus";
import { useAppStore } from "../stores/app";
import AppNavBar from "../components/AppNavBar.vue";
import MobileFrame from "../components/MobileFrame.vue";
import { fetchOrderChats, sendOrderChat } from "../api/runner";

const emit = defineEmits<{
  (event: "back"): void;
}>();

const appStore = useAppStore();
const input = ref("");

const messages = computed(() => appStore.chatMessages);

const syncChats = async () => {
  try {
    const list = await fetchOrderChats(appStore.activeOrderId);
    appStore.chatMessages = list.map((item) => ({
      id: item.id,
      sender: item.sender_role === "runner" ? "runner" : item.sender_role === "admin" ? "system" : "user",
      text: item.content,
      time: new Date(item.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    }));
  } catch {
    // 原型兜底：接口异常时继续显示本地消息
  }
};

onMounted(() => {
  void syncChats();
});

const send = () => {
  const text = input.value.trim();
  if (!text) return;
  appStore.pushChatMessage("user", text);
  if (appStore.userId) {
    void sendOrderChat(appStore.activeOrderId, {
      sender_user_id: appStore.userId,
      sender_role: "user",
      content: text,
    })
      .then(() => syncChats())
      .catch(() => ElMessage.warning("消息已本地保存，后端同步失败"));
  }
  input.value = "";
};
</script>

<template>
  <MobileFrame>
    <div class="page">
      <AppNavBar title="联系跑腿员" :show-back="true" @back="emit('back')" />

      <section class="list">
        <el-empty v-if="messages.length === 0" description="暂无会话消息" />
        <div v-for="msg in messages" :key="msg.id" class="row" :class="msg.sender">
          <div class="bubble">
            <p>{{ msg.text }}</p>
            <span>{{ msg.time }}</span>
          </div>
        </div>
      </section>

      <footer class="footer">
        <el-input v-model="input" placeholder="输入消息内容..." maxlength="100" @keyup.enter="send" />
        <el-button type="primary" round @click="send">发送</el-button>
      </footer>
    </div>
  </MobileFrame>
</template>

<style scoped>
.page { min-height: 100%; display: grid; grid-template-rows: auto 1fr auto; }
.list { padding: var(--space-4); overflow: auto; display: grid; gap: var(--space-2); align-content: start; }
.row { display: flex; }
.row.user { justify-content: flex-end; }
.row.runner, .row.system { justify-content: flex-start; }
.bubble { max-width: 86%; border: 1px solid rgba(123, 155, 232, 0.2); border-radius: 12px; padding: 8px 10px; background: rgba(14, 22, 44, 0.65); }
.row.user .bubble { background: rgba(47, 125, 255, 0.25); border-color: rgba(108, 162, 255, 0.45); }
.bubble p { margin: 0; color: #f2f6ff; line-height: 1.4; }
.bubble span { display: block; margin-top: 4px; font-size: 11px; color: rgba(167, 186, 227, 0.85); text-align: right; }
.footer { border-top: 1px solid rgba(123, 155, 232, 0.18); background: rgba(8, 12, 24, 0.65); padding: var(--space-3) var(--space-4); display: grid; grid-template-columns: 1fr auto; gap: var(--space-2); }
</style>
