<script setup lang="ts">
type Mode = "loading" | "empty" | "error";

withDefaults(
  defineProps<{
    mode: Mode;
    title?: string;
    description?: string;
    actionText?: string;
  }>(),
  {
    title: "",
    description: "",
    actionText: "",
  },
);

const emit = defineEmits<{
  (event: "action"): void;
}>();
</script>

<template>
  <div class="states">
    <el-skeleton v-if="mode === 'loading'" animated :rows="5" />

    <el-empty
      v-else-if="mode === 'empty'"
      :description="description || '暂无数据'"
      :image-size="80"
    >
      <el-button v-if="actionText" type="primary" @click="emit('action')">
        {{ actionText }}
      </el-button>
    </el-empty>

    <el-result
      v-else
      icon="error"
      :title="title || '请求失败'"
      :sub-title="description || '请稍后重试'"
    >
      <template #extra>
        <el-button v-if="actionText" type="primary" @click="emit('action')">
          {{ actionText }}
        </el-button>
      </template>
    </el-result>
  </div>
</template>

<style scoped>
.states {
  padding: 12px;
}
</style>

