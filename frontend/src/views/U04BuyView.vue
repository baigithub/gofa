<script setup lang="ts">
import { computed, reactive } from "vue";
import AppButton from "../components/AppButton.vue";
import AppNavBar from "../components/AppNavBar.vue";
import { useAppStore } from "../stores/app";

const emit = defineEmits<{
  (event: "back"): void;
  (event: "next"): void;
}>();

const appStore = useAppStore();

const form = reactive({
  buyAddress: "",
  deliveryAddress: "",
  itemList: "",
  estimatedAmount: "",
  deliveryTime: "",
  phone: "",
  remark: "",
});

const normalizedAmount = computed(() => {
  const raw = String(form.estimatedAmount ?? "").trim();
  // 允许输入：10 / 10.5 / ¥10 / 10元
  const cleaned = raw.replace(/[^\d.]/g, "");
  return Number.parseFloat(cleaned);
});

const canSubmit = computed(() => {
  const buyAddress = form.buyAddress.trim();
  const deliveryAddress = form.deliveryAddress.trim();
  const itemList = form.itemList.trim();
  const phone = form.phone.trim();
  return (
    buyAddress.length > 0 &&
    deliveryAddress.length > 0 &&
    itemList.length > 0 &&
    Number.isFinite(normalizedAmount.value) &&
    normalizedAmount.value > 0 &&
    /^1\d{10}$/.test(phone)
  );
});

const onNext = () => {
  if (!canSubmit.value) return;
  appStore.setBuyEstimatedAmount(normalizedAmount.value);
  emit("next");
};
</script>

<template>
  <main class="page">
    <section class="phone">
      <AppNavBar title="帮买商品" :show-back="true" />
      <form class="form">
        <label>购买地址<input v-model="form.buyAddress" placeholder="请输入商超/食堂位置" /></label>
        <label>送达地址<input v-model="form.deliveryAddress" placeholder="请选择宿舍/教学楼" /></label>
        <label>商品清单<input v-model="form.itemList" placeholder="例：矿泉水2瓶、面包1个" /></label>
        <label>商品预估金额（元）<input v-model="form.estimatedAmount" inputmode="decimal" placeholder="请输入预估金额（如 10 或 ¥10）" /></label>
        <label>期望送达时间<input v-model="form.deliveryTime" placeholder="尽快送达/指定时间" /></label>
        <label>联系电话<input v-model="form.phone" inputmode="numeric" maxlength="11" placeholder="请输入11位手机号" /></label>
        <label>备注<input v-model="form.remark" placeholder="可选，补充说明" /></label>
      </form>
      <footer class="footer">
        <AppButton :disabled="!canSubmit" @click="onNext">下一步</AppButton>
        <AppButton variant="secondary" @click="emit('back')">返回首页</AppButton>
      </footer>
    </section>
  </main>
</template>

<style scoped>
.page {
  min-height: 100svh;
  display: grid;
  place-items: center;
}

.phone {
  width: min(100vw, 390px);
  min-height: 100svh;
  background: var(--color-bg);
  display: grid;
  grid-template-rows: auto 1fr auto;
}

.form {
  padding: var(--space-4);
  display: grid;
  gap: var(--space-3);
  overflow: auto;
}

label {
  display: grid;
  gap: var(--space-2);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

input {
  height: 40px;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 0 var(--space-3);
  background: var(--color-surface);
}

.footer {
  position: sticky;
  bottom: 0;
  display: grid;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  background: var(--color-surface);
  border-top: 1px solid var(--color-border);
}
</style>
