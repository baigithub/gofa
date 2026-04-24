<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { ElMessage } from "element-plus";
import { useAppStore } from "../stores/app";
import AppNavBar from "../components/AppNavBar.vue";
import MobileFrame from "../components/MobileFrame.vue";
import { fetchOrderChats, sendOrderChat } from "../api/runner";

const emit = defineEmits<{
  (event: "back-profile"): void;
}>();

const appStore = useAppStore();
const input = ref("");
const messages = computed(() => appStore.chatMessages);

const syncChats = async () => {
  try {
    const list = await fetchOrderChats(appStore.activeOrderId);
    appStore.chatMessages = list.map((item) => ({
      id: item.id,
      sender: item.sender_role === "runner" ? "runner" : "user",
      text: item.content,
      time: new Date(item.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    }));
  } catch {
    // 保留本地会话作为兜底
  }
};

onMounted(() => {
  void syncChats();
});

const send = () => {
  const text = input.value.trim();
  if (!text) return;
  appStore.pushChatMessage("runner", text);
  if (appStore.userId) {
    void sendOrderChat(appStore.activeOrderId, {
      sender_user_id: appStore.userId,
      sender_role: "runner",
      content: text,
    })
      .then(() => syncChats())
      .catch(() => ElMessage.warning("回复已本地保存，后端同步失败"));
  }
  input.value = "";
};
</script>

<template>
  <MobileFrame>
    <div class="page">
      <AppNavBar title="跑腿员消息窗口" :show-back="true" @back="emit('back-profile')" />

      <section class="list">
        <el-empty v-if="messages.length === 0" description="暂无用户消息" />
        <div v-for="msg in messages" :key="msg.id" class="row" :class="msg.sender">
          <div class="bubble">
            <p>{{ msg.text }}</p>
            <span>{{ msg.time }}</span>
          </div>
        </div>
      </section>

      <footer class="footer">
        <el-input v-model="input" placeholder="回复用户..." maxlength="100" @keyup.enter="send" />
        <el-button type="primary" round @click="send">回复</el-button>
      </footer>
    </div>
  </MobileFrame>
</template>

<style scoped>
.page { min-height: 100%; display: grid; grid-template-rows: auto 1fr auto; }
.list { padding: var(--space-4); overflow: auto; display: grid; gap: var(--space-2); align-content: start; }
.row { display: flex; }
.row.runner { justify-content: flex-end; }
.row.user, .row.system { justify-content: flex-start; }
.bubble { max-width: 86%; border: 1px solid rgba(123, 155, 232, 0.2); border-radius: 12px; padding: 8px 10px; background: rgba(14, 22, 44, 0.65); }
.row.runner .bubble { background: rgba(126, 240, 191, 0.2); border-color: rgba(126, 240, 191, 0.45); }
.bubble p { margin: 0; color: #f2f6ff; line-height: 1.4; }
.bubble span { display: block; margin-top: 4px; font-size: 11px; color: rgba(167, 186, 227, 0.85); text-align: right; }
.footer { border-top: 1px solid rgba(123, 155, 232, 0.18); background: rgba(8, 12, 24, 0.65); padding: var(--space-3) var(--space-4); display: grid; grid-template-columns: 1fr auto; gap: var(--space-2); }
</style>
