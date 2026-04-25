<script setup lang="ts">
import { defineAsyncComponent, watch } from "vue";
import { storeToRefs } from "pinia";
import { clearAuth, setAuth } from "./core/auth";
import { fetchRunnerDashboardStats } from "./api/runner";
import { useAppStore } from "./stores/app";

const U01LoginView = defineAsyncComponent(() => import("./views/U01LoginView.vue"));
const U02HomeView = defineAsyncComponent(() => import("./views/U02HomeView.vue"));
const U03PickupView = defineAsyncComponent(() => import("./views/U03PickupView.vue"));
const U04BuyView = defineAsyncComponent(() => import("./views/U04BuyView.vue"));
const U05ErrandView = defineAsyncComponent(() => import("./views/U05ErrandView.vue"));
const U06ConfirmOrderView = defineAsyncComponent(() => import("./views/U06ConfirmOrderView.vue"));
const U07CashierView = defineAsyncComponent(() => import("./views/U07CashierView.vue"));
const U08PaySuccessView = defineAsyncComponent(() => import("./views/U08PaySuccessView.vue"));
const U09PayFailedView = defineAsyncComponent(() => import("./views/U09PayFailedView.vue"));
const U10OrderListView = defineAsyncComponent(() => import("./views/U10OrderListView.vue"));
const U11OrderDetailPendingPayView = defineAsyncComponent(() => import("./views/U11OrderDetailPendingPayView.vue"));
const U12OrderDetailInProgressView = defineAsyncComponent(() => import("./views/U12OrderDetailInProgressView.vue"));
const U13OrderDetailFinishedView = defineAsyncComponent(() => import("./views/U13OrderDetailFinishedView.vue"));
const U14MessageView = defineAsyncComponent(() => import("./views/U14MessageView.vue"));
const U15ProfileView = defineAsyncComponent(() => import("./views/U15ProfileView.vue"));
const U16ChatView = defineAsyncComponent(() => import("./views/U16ChatView.vue"));
const U17AdminPanelView = defineAsyncComponent(() => import("./views/U17AdminPanelView.vue"));
const R01RunnerLoginView = defineAsyncComponent(() => import("./views/R01RunnerLoginView.vue"));
const R02RunnerHallView = defineAsyncComponent(() => import("./views/R02RunnerHallView.vue"));
const R03RunnerOrderDetailView = defineAsyncComponent(() => import("./views/R03RunnerOrderDetailView.vue"));
const R04RunnerDeliveringView = defineAsyncComponent(() => import("./views/R04RunnerDeliveringView.vue"));
const R05RunnerDoneView = defineAsyncComponent(() => import("./views/R05RunnerDoneView.vue"));
const R06RunnerProfileView = defineAsyncComponent(() => import("./views/R06RunnerProfileView.vue"));
const R07RunnerMessageView = defineAsyncComponent(() => import("./views/R07RunnerMessageView.vue"));

const appStore = useAppStore();
const { currentView, selectedService, orderAmount } = storeToRefs(appStore);

watch(
  currentView,
  (view) => {
    console.info(`[gofer] currentView=${view}`);
  },
  { immediate: true },
);

const goService = (service: "U03" | "U04" | "U05") => {
  appStore.selectService(service);
};

const goPay = (orderId?: string) => {
  if (orderId) appStore.setPendingOrderId(orderId);
  appStore.goPay();
};

const onPayFailed = () => {
  appStore.markPayFailed();
};

const onPaySuccess = () => {
  appStore.markPaySuccess();
};

const onViewOrder = () => {
  // 支付成功后先进入待接单详情，避免误导为“配送中”
  appStore.setView("U12");
};

const onGoOrder = () => {
  // 支付失败后回到待支付订单详情，支持重新支付
  appStore.setView("U11");
};

const onOpenRecentOrder = (payload: { orderId: string; status: string }) => {
  appStore.setActiveOrderId(payload.orderId);
  if (payload.status === "pending_pay") {
    appStore.setPendingOrderId(payload.orderId);
    appStore.setView("U11");
    return;
  }
  if (payload.status === "completed" || payload.status === "cancelled") {
    appStore.setView("U13");
    return;
  }
  appStore.setView("U12");
};

const onUserLogin = (payload?: { role?: "user" | "runner" | "admin"; token?: string; userId?: string; phone?: string; nickname?: string | null }) => {
  const role = payload?.role ?? "user";
  console.info("[gofer] login.success", {
    role,
    userId: payload?.userId ?? null,
    phone: payload?.phone ?? null,
    nickname: payload?.nickname ?? null,
  });
  setAuth(role, payload?.token, payload?.userId, payload?.phone);
  appStore.setRole(role);
  appStore.setUserId(payload?.userId ?? null);
  appStore.setUserPhone(payload?.phone ?? null);
  appStore.setUserNickname(payload?.nickname ?? null);
  appStore.setView("U02");
};

const onGoRunner = async () => {
  setAuth("runner", undefined, appStore.userId ?? undefined, appStore.userPhone ?? undefined);
  appStore.setRole("runner");

  if (!appStore.userId) {
    appStore.setView("R01");
    return;
  }

  try {
    const stats = await fetchRunnerDashboardStats(appStore.userId);
    if (stats.is_verified && stats.verification_status === "approved") {
      appStore.setView("R02");
      return;
    }
  } catch (error) {
    console.info("[gofer] check runner verification status failed", error);
  }

  appStore.setView("R01");
};

const onLogout = () => {
  clearAuth();
  appStore.clearAccount();
  appStore.setView("U01");
  console.info("[gofer] logout.success");
};

const onContactRunner = () => {
  appStore.contactRunnerFromUser();
};

</script>

<template>
  <U01LoginView v-if="currentView === 'U01'" @login-success="onUserLogin" />
  <U02HomeView
    v-else-if="currentView === 'U02'"
    @go-service="goService"
    @go-page="appStore.setView($event)"
    @open-recent-order="onOpenRecentOrder"
  />
  <U03PickupView v-else-if="currentView === 'U03'" @back="appStore.setView('U02')" @next="appStore.setView('U06')" />
  <U04BuyView v-else-if="currentView === 'U04'" @back="appStore.setView('U02')" @next="appStore.setView('U06')" />
  <U05ErrandView v-else-if="currentView === 'U05'" @back="appStore.setView('U02')" @next="appStore.setView('U06')" />
  <U06ConfirmOrderView
    v-else-if="currentView === 'U06'"
    :service-type="selectedService"
    @back="appStore.setView(selectedService)"
    @submit-pay="goPay"
  />
  <U07CashierView
    v-else-if="currentView === 'U07'"
    :amount="orderAmount"
    :order-id="appStore.pendingOrderId"
    @back="appStore.setView('U06')"
    @pay-failed="onPayFailed"
    @pay-success="onPaySuccess"
  />
  <U08PaySuccessView
    v-else-if="currentView === 'U08'"
    @view-order="onViewOrder"
    @go-home="appStore.setView('U02')"
  />
  <U09PayFailedView
    v-else-if="currentView === 'U09'"
    @retry="appStore.setView('U07')"
    @go-order="onGoOrder"
  />
  <U10OrderListView
    v-else-if="currentView === 'U10'"
    @back-home="appStore.setView('U02')"
    @open-detail="appStore.setView($event)"
  />
  <U11OrderDetailPendingPayView
    v-else-if="currentView === 'U11'"
    @back-list="appStore.setView('U10')"
    @go-pay="appStore.setView('U07')"
  />
  <U12OrderDetailInProgressView
    v-else-if="currentView === 'U12'"
    @back-list="appStore.setView('U10')"
    @contact-runner="onContactRunner"
  />
  <U13OrderDetailFinishedView
    v-else-if="currentView === 'U13'"
    @back-list="appStore.setView('U10')"
    @again="appStore.setView('U02')"
  />
  <U14MessageView v-else-if="currentView === 'U14'" @back-home="appStore.setView('U02')" />
  <U15ProfileView
    v-else-if="currentView === 'U15'"
    @back-home="appStore.setView('U02')"
    @go-runner="onGoRunner"
    @go-admin="appStore.setView('U17')"
    @logout="onLogout"
  />
  <U16ChatView v-else-if="currentView === 'U16'" @back="appStore.setView('U12')" />
  <U17AdminPanelView v-else-if="currentView === 'U17'" @back="appStore.setView('U15')" />
  <R01RunnerLoginView
    v-else-if="currentView === 'R01'"
    :user-id="appStore.userId"
    :user-phone="appStore.userPhone"
    @next="appStore.setView('R02')"
    @back-home="appStore.setView('U02')"
  />
  <R02RunnerHallView
    v-else-if="currentView === 'R02'"
    @next="appStore.setView('R03')"
    @go-profile="appStore.setView('R06')"
    @back-home="appStore.setView('U02')"
  />
  <R03RunnerOrderDetailView v-else-if="currentView === 'R03'" @next="appStore.setView('R04')" @back="appStore.setView('R02')" />
  <R04RunnerDeliveringView v-else-if="currentView === 'R04'" @next="appStore.setView('R05')" @back="appStore.setView('R03')" />
  <R05RunnerDoneView v-else-if="currentView === 'R05'" @back-hall="appStore.setView('R02')" />
  <R06RunnerProfileView
    v-else-if="currentView === 'R06'"
    @back-hall="appStore.setView('R02')"
    @go-message="appStore.setView('R07')"
  />
  <R07RunnerMessageView v-else @back-profile="appStore.setView('R06')" />
</template>
