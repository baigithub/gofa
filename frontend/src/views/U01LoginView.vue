<script setup lang="ts">
import { computed, ref } from "vue";
import { ElMessage } from "element-plus";
import MobileFrame from "../components/MobileFrame.vue";
import { login, sendCode } from "../api/auth";

const emit = defineEmits<{
  (event: "login-success", payload?: { role: "user" | "runner" | "admin"; token: string; userId: string }): void;
}>();

const phone = ref("");
const code = ref("");
const isRunner = ref(false);
const sendingCode = ref(false);
const submitting = ref(false);

const isPhoneValid = computed(() => /^1\d{10}$/.test(phone.value));
const canSubmit = computed(() => isPhoneValid.value && code.value.length === 6);

const onSendCode = async () => {
  if (!isPhoneValid.value) {
    ElMessage.warning("请输入正确的手机号");
    return;
  }

  sendingCode.value = true;
  try {
    await sendCode(phone.value);
    ElMessage.success("验证码已发送");
  } catch (error) {
    const message = error instanceof Error ? error.message : "发送失败，请稍后重试";
    ElMessage.error(message);
  } finally {
    sendingCode.value = false;
  }
};

const submit = async () => {
  if (!canSubmit.value) return;

  submitting.value = true;
  try {
    const result = await login({ phone: phone.value, code: code.value });
    if (isRunner.value && result.role !== "runner" && result.role !== "admin") {
      ElMessage.warning("该账号未分配跑腿员角色，请联系管理员在「管理员面板」中设置");
      return;
    }
    ElMessage.success("登录成功");
    emit("login-success", result);
  } catch (error) {
    const message = error instanceof Error ? error.message : "登录失败，请稍后重试";
    ElMessage.error(message);
  } finally {
    submitting.value = false;
  }
};

const scanLogin = () => {
  if (submitting.value) return;
  // 原型约定：扫码即管理员（17800000000）
  submitting.value = true;
  void login({ phone: "17800000000", code: "123456" })
    .then((result) => {
      ElMessage.success("微信扫码登录成功（管理员）");
      emit("login-success", result);
    })
    .catch((error) => {
      const message = error instanceof Error ? error.message : "扫码登录失败，请稍后重试";
      ElMessage.error(message);
    })
    .finally(() => {
      submitting.value = false;
    });
};
</script>

<template>
  <MobileFrame>
    <header class="brand">
      <p class="tag">GOFER CAMPUS</p>
      <h1>校园跑腿登录</h1>
    </header>

    <el-card class="card" shadow="never">
      <el-form label-position="top">
        <el-form-item label="手机号">
          <el-input v-model="phone" maxlength="11" placeholder="请输入手机号" clearable />
        </el-form-item>

        <el-form-item label="验证码">
          <div class="code-row">
            <el-input v-model="code" maxlength="6" placeholder="请输入 6 位验证码" clearable />
            <el-button class="ghost-btn" :loading="sendingCode" @click="onSendCode">获取验证码</el-button>
          </div>
        </el-form-item>
        <el-form-item>
          <el-checkbox v-model="isRunner" :disabled="submitting || sendingCode">是否跑腿员</el-checkbox>
        </el-form-item>
      </el-form>

      <el-button class="primary-btn" :disabled="!canSubmit" :loading="submitting" @click="submit">登录/注册</el-button>
      <el-divider content-position="center">OR</el-divider>
      <el-button class="wechat-btn" :loading="submitting" @click="scanLogin">微信扫码登录</el-button>

      <p class="tips">未注册手机号将自动创建账号</p>
      <p class="agreement">登录即表示同意《用户协议》《隐私政策》</p>
    </el-card>
  </MobileFrame>
</template>

<style scoped>
.brand {
  margin-top: 8px;
  margin-bottom: 12px;
  text-align: center;
}

.tag {
  margin: 0 0 var(--space-2);
  font-size: 11px;
  letter-spacing: 2px;
  color: #8fb7ff;
}

.brand h1 {
  margin: 0 0 var(--space-2);
  font-size: 22px;
  color: #f2f6ff;
  text-shadow: 0 0 14px rgba(55, 143, 255, 0.4);
}

.brand p {
  margin: 0;
  color: #9fb0cf;
}

.card {
  padding: 6px;
}

.code-row {
  display: grid;
  grid-template-columns: 1fr 110px;
  gap: var(--space-2);
}

.tips {
  margin: 0;
  color: #8ea1c9;
  font-size: var(--font-size-xs);
}

.divider {
  text-align: center;
  color: #6e83b2;
  font-size: var(--font-size-xs);
  letter-spacing: 1px;
}

.wechat-login {
  width: 100%;
  height: 40px;
  border-radius: var(--radius-sm);
  border: 1px solid #2dcf8f;
  background: linear-gradient(180deg, rgba(26, 180, 117, 0.2), rgba(26, 180, 117, 0.08));
  color: #7ef0bf;
  font-size: var(--font-size-sm);
  cursor: pointer;
}

.agreement {
  margin: 0;
  color: #60749e;
  font-size: var(--font-size-xs);
  text-align: center;
}

:deep(.el-form-item) {
  margin-bottom: 14px;
}

:deep(.el-form-item__label) {
  color: #b9c7e8;
}

:deep(.el-input__wrapper) {
  background: rgba(18, 26, 49, 0.9);
  border: 1px solid rgba(123, 155, 232, 0.35);
  box-shadow: none;
}

:deep(.el-input__inner) {
  color: #f4f7ff;
}

:deep(.el-divider__text) {
  background: transparent;
  color: #6e83b2;
}

.primary-btn,
.wechat-btn,
.ghost-btn {
  width: 100%;
}

.primary-btn,
.wechat-btn {
  height: 40px;
}

.ghost-btn {
  height: 40px;
}

.primary-btn {
  background: linear-gradient(90deg, #2f7dff, #56b0ff);
  border: none;
}

.ghost-btn {
  border-color: #4a8dff;
  color: #9ec2ff;
  background: rgba(67, 124, 255, 0.12);
}

.wechat-btn {
  border-color: #2dcf8f;
  color: #7ef0bf;
  background: rgba(26, 180, 117, 0.12);
}

:deep(.el-checkbox__label) {
  color: rgba(167, 186, 227, 0.9);
}
</style>
