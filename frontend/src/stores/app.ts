import { defineStore } from "pinia";

export type ViewKey =
  | "U01"
  | "U02"
  | "U03"
  | "U04"
  | "U05"
  | "U06"
  | "U07"
  | "U08"
  | "U09"
  | "U10"
  | "U11"
  | "U12"
  | "U13"
  | "U14"
  | "U15"
  | "U16"
  | "U17"
  | "R01"
  | "R02"
  | "R03"
  | "R04"
  | "R05"
  | "R06"
  | "R07";

export type ServiceType = "U03" | "U04" | "U05";
export type PayStatus = "idle" | "success" | "failed";
export type UserRole = "user" | "runner" | "admin";
export type ChatSender = "user" | "runner" | "system";

export type ChatMessage = {
  id: string;
  sender: ChatSender;
  text: string;
  time: string;
};

export const useAppStore = defineStore("app", {
  state: () => ({
    currentView: "U01" as ViewKey,
    selectedService: "U03" as ServiceType,
    buyEstimatedAmount: 0,
    orderAmount: 10,
    payStatus: "idle" as PayStatus,
    userRole: "user" as UserRole,
    userId: null as string | null,
    userPhone: null as string | null,
    userNickname: null as string | null,
    activeOrderId: "latest",
    pendingOrderId: null as string | null,
    chatMessages: [] as ChatMessage[],
  }),
  actions: {
    setView(view: ViewKey) {
      this.currentView = view;
    },
    selectService(service: ServiceType) {
      this.selectedService = service;
      this.currentView = service;
    },
    setBuyEstimatedAmount(amountYuan: number) {
      this.buyEstimatedAmount = Number.isFinite(amountYuan) ? amountYuan : 0;
    },
    calcFee() {
      const base = 8;
      const extra = 2;
      const goods = this.selectedService === "U04" ? this.buyEstimatedAmount : 0;
      return { base, extra, goods, total: base + extra + goods };
    },
    goPay() {
      const fee = this.calcFee();
      this.orderAmount = fee.total;
      this.currentView = "U07";
      this.payStatus = "idle";
    },
    setPendingOrderId(orderId: string | null) {
      this.pendingOrderId = orderId;
    },
    markPaySuccess() {
      this.payStatus = "success";
      this.currentView = "U08";
    },
    markPayFailed() {
      this.payStatus = "failed";
      this.currentView = "U09";
    },
    setRole(role: UserRole) {
      this.userRole = role;
    },
    setUserId(userId: string | null) {
      this.userId = userId;
    },
    setUserPhone(userPhone: string | null) {
      this.userPhone = userPhone;
    },
    setUserNickname(userNickname: string | null) {
      this.userNickname = userNickname;
    },
    clearAccount() {
      this.userId = null;
      this.userPhone = null;
      this.userNickname = null;
      this.userRole = "user";
    },
    setActiveOrderId(orderId: string) {
      this.activeOrderId = orderId || "latest";
    },
    ensureChatSeed() {
      if (this.chatMessages.length > 0) return;
      this.chatMessages.push({
        id: "seed-1",
        sender: "system",
        text: "会话已创建，可与跑腿员沟通取货和送达细节。",
        time: "刚刚",
      });
    },
    pushChatMessage(sender: ChatSender, text: string) {
      const content = text.trim();
      if (!content) return;
      this.chatMessages.push({
        id: `${Date.now()}-${Math.random().toString(16).slice(2, 8)}`,
        sender,
        text: content,
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      });
    },
    contactRunnerFromUser() {
      this.ensureChatSeed();
      this.pushChatMessage("user", "你好，我这边订单已支付，请问大概多久可以接单？");
      this.setActiveOrderId("latest");
      this.currentView = "U16";
    },
  },
});

