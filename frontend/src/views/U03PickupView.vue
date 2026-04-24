<script setup lang="ts">
import { computed, reactive } from "vue";
import AppButton from "../components/AppButton.vue";
import AppNavBar from "../components/AppNavBar.vue";

const emit = defineEmits<{
  (event: "back"): void;
  (event: "next"): void;
}>();

const form = reactive({
  pickupAddress: "",
  deliveryAddress: "",
  courierCompany: "",
  pickupCode: "",
  deliveryTime: "",
  phone: "",
  remark: "",
});

const canSubmit = computed(
  () =>
    form.pickupAddress &&
    form.deliveryAddress &&
    form.courierCompany &&
    form.pickupCode &&
    /^1\d{10}$/.test(form.phone),
);
</script>

<template>
  <main class="page">
    <section class="phone">
      <AppNavBar title="帮取快递" :show-back="true" />
      <form class="form">
        <label>取件地址<input v-model="form.pickupAddress" placeholder="请选择快递站点" /></label>
        <label>送达地址<input v-model="form.deliveryAddress" placeholder="请选择宿舍/教学楼" /></label>
        <label>快递公司<input v-model="form.courierCompany" placeholder="请输入快递公司" /></label>
        <label>取件码<input v-model="form.pickupCode" placeholder="请输入取件码" /></label>
        <label>期望送达时间<input v-model="form.deliveryTime" placeholder="尽快送达/指定时间" /></label>
        <label>联系电话<input v-model="form.phone" maxlength="11" placeholder="请输入手机号" /></label>
        <label>备注<input v-model="form.remark" placeholder="可选，补充说明" /></label>
      </form>
      <footer class="footer">
        <AppButton :disabled="!canSubmit" @click="emit('next')">下一步</AppButton>
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
