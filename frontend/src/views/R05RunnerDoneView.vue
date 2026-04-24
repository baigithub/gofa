<script setup lang="ts">
import AppButton from "../components/AppButton.vue";
const emit = defineEmits<{(event:"back-hall"):void;}>();
</script>
<template>
  <main class="page"><section class="phone">
    <section class="card"><h1>订单已完成</h1><p>本单收益：¥8.00</p><p>用户已确认收货</p></section>
    <footer class="footer"><AppButton @click="emit('back-hall')">返回接单大厅</AppButton></footer>
  </section></main>
</template>
<style scoped>
.page{min-height:100svh;display:grid;place-items:center}.phone{width:min(100vw,390px);min-height:100svh;display:grid;grid-template-rows:1fr auto;background:var(--color-bg)}
.card{margin:var(--space-4);background:var(--color-surface);border:1px solid var(--color-border);border-radius:var(--radius-md);padding:var(--space-4)}
h1{margin:0 0 var(--space-3);font-size:var(--font-size-lg)}p{margin:0 0 var(--space-2);color:var(--color-text-secondary)}
.footer{border-top:1px solid var(--color-border);padding:var(--space-3) var(--space-4);background:var(--color-surface)}
</style>
