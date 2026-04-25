<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { ElMessage } from "element-plus";
import AppNavBar from "../components/AppNavBar.vue";
import AppStates from "../components/AppStates.vue";
import MobileFrame from "../components/MobileFrame.vue";
import {
  deleteRole,
  fetchAdminOrders,
  fetchRoles,
  fetchRunnerVerifications,
  fetchUsers,
  resetUserPassword,
  reviewRunnerVerification,
  setRoleEnabled,
  setUserEnabled,
  setUserRole,
  type AdminOrderItem,
  type RoleItem,
  type RunnerVerificationItem,
  type UserItem,
} from "../api/admin";
import { useAppStore } from "../stores/app";

const emit = defineEmits<{ (event: "back"): void }>();

const appStore = useAppStore();
const currentTab = ref<"users" | "roles" | "orders" | "runner-review">("users");
const isLoading = ref(false);
const isError = ref(false);
const users = ref<UserItem[]>([]);
const roles = ref<RoleItem[]>([]);
const orders = ref<AdminOrderItem[]>([]);
const runnerReviews = ref<RunnerVerificationItem[]>([]);
const currentUserPage = ref(1);
const currentOrderPage = ref(1);
const currentReviewPage = ref(1);
const imagePreviewVisible = ref(false);
const previewImageUrl = ref("");
const USER_PAGE_SIZE = 4;
const PAGE_SIZE = 2;

const adminUserId = computed(() => appStore.userId ?? "");

const load = async () => {
  if (!adminUserId.value) {
    ElMessage.error("缺少管理员身份，请重新扫码登录");
    return;
  }
  isLoading.value = true;
  isError.value = false;
  try {
    const [userResult, roleResult, orderResult, runnerReviewResult] = await Promise.allSettled([
      fetchUsers(adminUserId.value),
      fetchRoles(adminUserId.value),
      fetchAdminOrders(adminUserId.value),
      fetchRunnerVerifications(adminUserId.value),
    ]);

    if (userResult.status === "fulfilled") users.value = userResult.value;
    if (roleResult.status === "fulfilled") roles.value = roleResult.value;
    if (orderResult.status === "fulfilled") orders.value = orderResult.value;
    if (runnerReviewResult.status === "fulfilled") {
      runnerReviews.value = runnerReviewResult.value;
      console.info(
        "[gofer] admin.runnerReviews.loaded",
        runnerReviewResult.value.map((item) => ({
          id: item.id,
          user_id: item.user_id,
          phone: item.phone,
          student_no: item.student_no,
          verification_status: item.verification_status,
        })),
      );
    } else {
      runnerReviews.value = [];
      console.error("[gofer] admin.runnerReviews.load_failed", runnerReviewResult.reason);
      ElMessage.warning("跑腿员审核列表加载失败，已隐藏该页数据");
    }

    if (userResult.status === "rejected" || roleResult.status === "rejected" || orderResult.status === "rejected") {
      throw userResult.status === "rejected"
        ? userResult.reason
        : roleResult.status === "rejected"
          ? roleResult.reason
          : orderResult.status === "rejected"
            ? orderResult.reason
            : new Error("加载失败");
    }

    currentUserPage.value = 1;
    currentOrderPage.value = 1;
    currentReviewPage.value = 1;
  } catch (e) {
    isError.value = true;
    const msg = e instanceof Error ? e.message : "加载失败";
    ElMessage.error(msg);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => void load());

const roleType = (role: UserItem["role"]) => {
  if (role === "admin") return "danger";
  if (role === "runner") return "warning";
  return "primary";
};

const roleLabel = (role: UserItem["role"]) => {
  if (role === "admin") return "管理员";
  if (role === "runner") return "跑腿员";
  if (role === "user") return "用户";
  const found = roles.value.find((item) => item.code === role);
  return found?.name ?? role;
};

const verificationStatusLabel = (status: string) => {
  if (status === "pending") return "待审核";
  if (status === "approved") return "已通过";
  if (status === "rejected") return "已拒绝";
  return status;
};

const approveReview = async (item: RunnerVerificationItem) => {
  if (!adminUserId.value) return;
  try {
    await reviewRunnerVerification(adminUserId.value, item.id, { approve: true });
    ElMessage.success("已通过审核");
    await load();
  } catch (e) {
    const msg = e instanceof Error ? e.message : "操作失败";
    ElMessage.error(msg);
  }
};

const rejectReview = async (item: RunnerVerificationItem) => {
  if (!adminUserId.value) return;
  try {
    await reviewRunnerVerification(adminUserId.value, item.id, { approve: false, rejection_reason: "资料不符合要求" });
    ElMessage.success("已拒绝审核");
    await load();
  } catch (e) {
    const msg = e instanceof Error ? e.message : "操作失败";
    ElMessage.error(msg);
  }
};

const openPreview = (url: string) => {
  previewImageUrl.value = url;
  imagePreviewVisible.value = true;
};

const updateRole = async (u: UserItem, role: UserItem["role"]) => {
  if (!adminUserId.value) return;
  if (u.role === role) return;
  try {
    await setUserRole(adminUserId.value, u.id, role);
    u.role = role;
    ElMessage.success(`已设置为：${roleLabel(role)}`);
  } catch (e) {
    const msg = e instanceof Error ? e.message : "设置失败";
    ElMessage.error(msg);
  }
};

const switchUserRole = async (u: UserItem) => {
  const enabledRoles = roles.value.filter((r) => r.is_enabled);
  if (enabledRoles.length === 0) {
    ElMessage.warning("暂无可用角色");
    return;
  }
  const currentIndex = enabledRoles.findIndex((r) => r.code === u.role);
  const nextIndex = currentIndex >= 0 ? (currentIndex + 1) % enabledRoles.length : 0;
  await updateRole(u, enabledRoles[nextIndex].code);
};

const sortedUsers = computed(() => {
  return [...users.value].sort((a, b) => {
    const ta = a.created_at ? new Date(a.created_at).getTime() : 0;
    const tb = b.created_at ? new Date(b.created_at).getTime() : 0;
    return tb - ta;
  });
});

const pagedUsers = computed(() => {
  const start = (currentUserPage.value - 1) * USER_PAGE_SIZE;
  return sortedUsers.value.slice(start, start + USER_PAGE_SIZE);
});

const hasNextUserPage = computed(() => currentUserPage.value * USER_PAGE_SIZE < sortedUsers.value.length);

const goNextUserPage = () => {
  if (!hasNextUserPage.value) return;
  currentUserPage.value += 1;
};

const userPageLabel = computed(() => {
  if (sortedUsers.value.length === 0) return "第 0 / 0 页";
  const totalPages = Math.ceil(sortedUsers.value.length / USER_PAGE_SIZE);
  return `第 ${currentUserPage.value} / ${totalPages} 页`;
});

const toggleUserEnabled = async (u: UserItem) => {
  if (!adminUserId.value) return;
  try {
    const nextEnabled = !u.is_enabled;
    await setUserEnabled(adminUserId.value, u.id, nextEnabled);
    u.is_enabled = nextEnabled;
    ElMessage.success(nextEnabled ? "用户已启用" : "用户已禁用");
  } catch (e) {
    const msg = e instanceof Error ? e.message : "操作失败";
    ElMessage.error(msg);
  }
};

const resetPassword = async (u: UserItem) => {
  if (!adminUserId.value) return;
  try {
    const result = await resetUserPassword(adminUserId.value, u.id);
    ElMessage.success(`重置成功，临时密码(验证码)：${result.temp_password}`);
  } catch (e) {
    const msg = e instanceof Error ? e.message : "重置失败";
    ElMessage.error(msg);
  }
};

const toggleRoleEnabled = async (role: RoleItem) => {
  if (!adminUserId.value) return;
  try {
    const updated = await setRoleEnabled(adminUserId.value, role.id, !role.is_enabled);
    role.is_enabled = updated.is_enabled;
    ElMessage.success(updated.is_enabled ? "角色已启用" : "角色已禁用");
  } catch (e) {
    const msg = e instanceof Error ? e.message : "操作失败";
    ElMessage.error(msg);
  }
};

const removeRole = async (role: RoleItem) => {
  if (!adminUserId.value) return;
  try {
    await deleteRole(adminUserId.value, role.id);
    ElMessage.success("角色已删除");
    await load();
  } catch (e) {
    const msg = e instanceof Error ? e.message : "删除失败";
    ElMessage.error(msg);
  }
};

const formatTime = (value: string | null) => {
  if (!value) return "—";
  const d = new Date(value);
  if (Number.isNaN(d.getTime())) return value;
  return d.toLocaleString();
};

const sortedOrders = computed(() => {
  return [...orders.value].sort((a, b) => {
    const ta = a.required_completed_at ? new Date(a.required_completed_at).getTime() : 0;
    const tb = b.required_completed_at ? new Date(b.required_completed_at).getTime() : 0;
    return tb - ta;
  });
});

const sortedRunnerReviews = computed(() => {
  return [...runnerReviews.value].sort((a, b) => {
    const ta = a.created_at ? new Date(a.created_at).getTime() : 0;
    const tb = b.created_at ? new Date(b.created_at).getTime() : 0;
    return tb - ta;
  });
});

const pagedOrders = computed(() => {
  const start = (currentOrderPage.value - 1) * PAGE_SIZE;
  return sortedOrders.value.slice(start, start + PAGE_SIZE);
});

const pagedRunnerReviews = computed(() => {
  const start = (currentReviewPage.value - 1) * PAGE_SIZE;
  return sortedRunnerReviews.value.slice(start, start + PAGE_SIZE);
});

const hasNextPage = computed(() => currentOrderPage.value * PAGE_SIZE < sortedOrders.value.length);
const hasNextReviewPage = computed(() => currentReviewPage.value * PAGE_SIZE < sortedRunnerReviews.value.length);

const goNextPage = () => {
  if (!hasNextPage.value) return;
  currentOrderPage.value += 1;
};

const goNextReviewPage = () => {
  if (!hasNextReviewPage.value) return;
  currentReviewPage.value += 1;
};

const orderPageLabel = computed(() => {
  if (sortedOrders.value.length === 0) return "第 0 / 0 页";
  const totalPages = Math.ceil(sortedOrders.value.length / PAGE_SIZE);
  return `第 ${currentOrderPage.value} / ${totalPages} 页`;
});

const reviewPageLabel = computed(() => {
  if (sortedRunnerReviews.value.length === 0) return "第 0 / 0 页";
  const totalPages = Math.ceil(sortedRunnerReviews.value.length / PAGE_SIZE);
  return `第 ${currentReviewPage.value} / ${totalPages} 页`;
});

</script>

<template>
  <MobileFrame>
    <div class="page">
      <AppNavBar title="管理面板" :show-back="true" @back="emit('back')" />

      <section class="content">
        <el-card class="intro" shadow="never">
          <div class="intro-top">
            <div>
              <div class="title">管理面板</div>
              <div class="sub">管理用户、角色、订单和跑腿员认证审核</div>
            </div>
            <el-tag effect="dark" type="danger" round size="small">ADMIN</el-tag>
          </div>
          <el-divider />
          <el-button size="small" round @click="load">刷新列表</el-button>
        </el-card>

        <AppStates v-if="isLoading" mode="loading" />
        <AppStates
          v-else-if="isError"
          mode="error"
          title="加载失败"
          description="请检查后端服务或网络"
          action-text="重试"
          @action="load"
        />
        <template v-else>
          <el-tabs v-model="currentTab" class="compact-tabs">
            <el-tab-pane label="用户管理" name="users" />
            <el-tab-pane label="角色管理" name="roles" />
            <el-tab-pane label="订单总览" name="orders" />
            <el-tab-pane label="跑腿审核" name="runner-review" />
          </el-tabs>

          <template v-if="currentTab === 'users'">
            <AppStates v-if="pagedUsers.length === 0" mode="empty" description="暂无用户" />
            <template v-else>
              <div class="user-list">
                <el-card v-for="u in pagedUsers" :key="u.id" class="user-card user-card-pretty" shadow="hover">
                  <div class="user-line user-line-top user-line-inline">
                    <div class="phone-wrap">
                      <el-tag class="user-prefix-tag" type="info" effect="plain" round size="small">用户</el-tag>
                      <div class="phone">{{ u.phone }}</div>
                    </div>
                    <el-tag class="role-switch" :type="roleType(u.role)" effect="plain" round @click="switchUserRole(u)">
                      角色：{{ roleLabel(u.role) }}
                    </el-tag>
                  </div>
                  <div class="user-line user-line-bottom user-line-inline">
                    <div class="meta-line">
                      <span class="meta-label">状态</span>
                      <el-tag :type="u.is_enabled ? 'success' : 'info'" effect="plain" round>
                        {{ u.is_enabled ? "启用中" : "已禁用" }}
                      </el-tag>
                    </div>
                    <div class="action-group">
                      <el-button size="small" round :type="u.is_enabled ? 'danger' : 'success'" plain @click="toggleUserEnabled(u)">
                        {{ u.is_enabled ? "禁用" : "启用" }}
                      </el-button>
                      <el-button size="small" round type="warning" plain @click="resetPassword(u)">重置密码</el-button>
                    </div>
                  </div>
                </el-card>
              </div>
              <div class="order-pager">
                <span class="pager-text">{{ userPageLabel }}</span>
                <div class="pager-actions">
                  <el-button size="small" round type="primary" :disabled="currentUserPage === 1" @click="currentUserPage -= 1">上一页</el-button>
                  <el-button size="small" round type="primary" :disabled="!hasNextUserPage" @click="goNextUserPage">下一页</el-button>
                </div>
              </div>
            </template>
          </template>

          <template v-else-if="currentTab === 'roles'">
            <AppStates v-if="roles.length === 0" mode="empty" description="暂无角色" />
            <el-card v-for="r in roles" v-else :key="r.id" class="user-card" shadow="never">
              <div class="row">
                <div class="left">
                  <div class="phone">{{ r.name }}（{{ r.code }}）</div>
                  <div class="id">{{ r.description || "无描述" }}</div>
                </div>
                <el-tag :type="r.is_enabled ? 'success' : 'info'" effect="dark" round>{{ r.is_enabled ? "启用" : "禁用" }}</el-tag>
              </div>
              <div class="actions">
                <el-button size="small" round :type="r.is_enabled ? 'warning' : 'success'" plain @click="toggleRoleEnabled(r)">
                  {{ r.is_enabled ? "禁用" : "启用" }}
                </el-button>
                <el-button size="small" round type="danger" plain @click="removeRole(r)">删除</el-button>
              </div>
            </el-card>
          </template>

          <template v-else-if="currentTab === 'orders'">
            <AppStates v-if="pagedOrders.length === 0" mode="empty" description="暂无订单" />
            <template v-else>
              <div class="order-grid">
                <el-card v-for="item in pagedOrders" :key="item.order_id" class="order-item" shadow="never">
                  <div class="order-line"><span>发起人</span><strong>{{ item.initiator }}</strong></div>
                  <div class="order-line"><span>跑腿人</span><strong>{{ item.runner }}</strong></div>
                  <div class="order-line"><span>内容</span><strong>{{ item.order_content }}</strong></div>
                  <div class="order-line"><span>状态</span><strong>{{ item.status }}</strong></div>
                  <div class="order-line"><span>要求时间</span><strong>{{ formatTime(item.required_completed_at) }}</strong></div>
                  <div class="order-line"><span>送达时间</span><strong>{{ formatTime(item.completed_at) }}</strong></div>
                </el-card>
              </div>
              <div class="order-pager">
                <span class="pager-text">{{ orderPageLabel }}</span>
                <el-button size="small" round type="primary" :disabled="!hasNextPage" @click="goNextPage">下一页</el-button>
              </div>
            </template>
          </template>

          <template v-else-if="currentTab === 'runner-review'">
            <AppStates v-if="pagedRunnerReviews.length === 0" mode="empty" description="暂无待审核跑腿员" />
            <template v-else>
              <div class="review-grid">
                <el-card v-for="item in pagedRunnerReviews" :key="item.id" class="review-item" shadow="never">
                  <div class="review-line"><span>手机号</span><strong>{{ item.phone }}</strong></div>
                  <div class="review-line"><span>学号</span><strong>{{ item.student_no || '—' }}</strong></div>
                  <div class="review-line"><span>状态</span><strong>{{ verificationStatusLabel(item.verification_status) }}</strong></div>
                  <div class="review-line review-image-line">
                    <span>校园材料图片</span>
                    <div class="credential-thumb-wrap" v-if="item.credential_images?.length">
                      <img
                        class="credential-thumb"
                        :src="item.credential_images[0]"
                        alt="校园材料图片"
                        @click="openPreview(item.credential_images[0])"
                      />
                      <span class="credential-hint">点击放大</span>
                    </div>
                    <strong v-else>暂无</strong>
                  </div>
                  <div class="actions review-actions">
                    <el-button size="small" round type="success" plain @click="approveReview(item)">通过</el-button>
                    <el-button size="small" round type="danger" plain @click="rejectReview(item)">拒绝</el-button>
                  </div>
                </el-card>
              </div>
              <div class="order-pager">
                <span class="pager-text">{{ reviewPageLabel }}</span>
                <el-button size="small" round type="primary" :disabled="!hasNextReviewPage" @click="goNextReviewPage">下一页</el-button>
              </div>
            </template>
          </template>
        </template>
      </section>

      <el-dialog v-model="imagePreviewVisible" width="92%" top="8vh" append-to-body>
        <img class="preview-dialog-image" :src="previewImageUrl" alt="校园材料大图" />
      </el-dialog>
    </div>
  </MobileFrame>
</template>

<style scoped>
.page {
  min-height: 100%;
  display: grid;
  grid-template-rows: auto 1fr;
}

.content {
  padding: var(--space-3);
  display: grid;
  gap: var(--space-2);
  align-content: start;
  overflow: auto;
}

.intro,
.user-card {
  border: 1px solid rgba(123, 155, 232, 0.18);
  background: rgba(12, 18, 34, 0.55);
}

.compact-tabs :deep(.el-tabs__header) {
  margin: 0 0 8px;
}

.compact-tabs :deep(.el-tabs__nav-wrap::after) {
  height: 1px;
}

.compact-tabs :deep(.el-tabs__item) {
  padding: 0 10px;
  height: 34px;
  line-height: 34px;
  font-size: 12px;
}

.table-card {
  border: 1px solid rgba(123, 155, 232, 0.18);
  background: rgba(12, 18, 34, 0.55);
}

.user-card-pretty {
  border-color: rgba(96, 126, 199, 0.22);
  border-radius: 14px;
  background: linear-gradient(180deg, rgba(16, 24, 44, 0.78), rgba(12, 19, 36, 0.7));
  box-shadow: 0 6px 20px rgba(5, 10, 20, 0.22);
}

.user-line {
  width: 100%;
}

.user-line-top,
.user-line-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.user-line-top {
  min-height: 26px;
}

.user-line-bottom {
  margin-top: 10px;
  margin-bottom: 10px;
}

.user-line-inline {
  flex-wrap: nowrap;
}

.meta-line {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.meta-label {
  color: rgba(167, 186, 227, 0.8);
  font-size: 12px;
  flex-shrink: 0;
}

.action-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.user-divider {
  margin: 10px 0 12px;
  border-color: rgba(124, 154, 228, 0.14);
}

.user-list {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}

.order-grid,
.review-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--space-3);
}

.user-card,
.order-item,
.review-item {
  border: 1px solid rgba(123, 155, 232, 0.18);
  background: rgba(12, 18, 34, 0.55);
}

.order-line,
.review-line {
  display: grid;
  grid-template-columns: 64px 1fr;
  gap: 8px;
  align-items: start;
  margin-bottom: 6px;
  color: rgba(167, 186, 227, 0.9);
}

.order-line:last-child,
.review-line:last-child {
  margin-bottom: 0;
}

.order-line strong,
.review-line strong {
  color: #f2f6ff;
  font-weight: 600;
  word-break: break-word;
}

.review-image-line {
  align-items: center;
}

.credential-thumb-wrap {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 6px;
}

.credential-thumb {
  width: 64px;
  height: 64px;
  object-fit: cover;
  border-radius: 10px;
  border: 1px solid rgba(123, 155, 232, 0.2);
  cursor: zoom-in;
  background: rgba(10, 14, 26, 0.45);
}

.credential-hint {
  font-size: 11px;
  color: rgba(167, 186, 227, 0.78);
}

.preview-dialog-image {
  width: 100%;
  max-height: 72vh;
  object-fit: contain;
  display: block;
}

.order-pager {
  margin-top: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.pager-actions {
  display: flex;
  gap: 8px;
  flex-wrap: nowrap;
}

.pager-text {
  color: rgba(167, 186, 227, 0.9);
  font-size: 12px;
}

.intro-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.title {
  color: #f2f6ff;
  font-weight: 900;
  font-size: 16px;
}

.sub {
  margin-top: 4px;
  color: rgba(167, 186, 227, 0.85);
  font-size: 11px;
  line-height: 1.35;
}

.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
}

.phone {
  color: #ecf3ff;
  font-weight: 700;
  font-size: 15px;
  line-height: 1.2;
  letter-spacing: 0.2px;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.phone-wrap {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
}

.user-prefix-tag {
  flex-shrink: 0;
}

.second-line-grid {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  align-items: center;
  gap: 12px;
}

.second-line-item {
  display: flex;
  align-items: center;
}

.second-line-left {
  justify-content: center;
}

.second-line-center,
.second-line-right {
  justify-content: center;
}


.id {
  margin-top: 4px;
  color: rgba(167, 186, 227, 0.75);
  font-size: 12px;
  word-break: break-all;
}

.role-switch {
  cursor: pointer;
  transition: all 0.18s ease;
}

.role-switch:hover {
  transform: translateY(-1px);
  filter: brightness(1.08);
}

.actions {
  margin-top: 10px;
  display: flex;
  gap: var(--space-2);
  flex-wrap: wrap;
}

.review-actions {
  margin-top: 12px;
}

.actions :deep(.el-button) {
  border-color: rgba(123, 155, 232, 0.24);
  background: rgba(18, 26, 49, 0.55);
  color: #cfe0ff;
}

:deep(.user-card-pretty .el-tag) {
  font-weight: 500;
  border-color: rgba(123, 155, 232, 0.3);
  background: rgba(20, 30, 56, 0.42);
}

:deep(.user-card-pretty .el-button--warning.is-plain) {
  border-color: rgba(255, 181, 110, 0.24);
  color: #ffd8ad;
  background: rgba(255, 181, 110, 0.1);
}

:deep(.user-card-pretty .el-button--danger.is-plain) {
  border-color: rgba(255, 122, 122, 0.24);
  color: #ffc0c0;
  background: rgba(255, 122, 122, 0.1);
}

:deep(.user-card-pretty .el-button--success.is-plain) {
  border-color: rgba(88, 215, 170, 0.24);
  color: #baf5df;
  background: rgba(88, 215, 170, 0.1);
}

:deep(.user-card-pretty .el-button) {
  min-width: 82px;
  letter-spacing: 0.2px;
}

:deep(.el-tabs__item) {
  color: #cfe0ff;
}

:deep(.el-table) {
  --el-table-bg-color: rgba(12, 18, 34, 0.35);
  --el-table-tr-bg-color: rgba(12, 18, 34, 0.35);
  --el-table-header-bg-color: rgba(18, 26, 49, 0.7);
  --el-table-border-color: rgba(123, 155, 232, 0.2);
  --el-table-text-color: #e7efff;
}
</style>

