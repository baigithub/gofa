<script setup lang="ts">
import { computed, ref, watch } from "vue";
import { ElMessage } from "element-plus";
import AppNavBar from "../components/AppNavBar.vue";
import MobileFrame from "../components/MobileFrame.vue";
import { submitRunnerVerification, uploadCredentialImage } from "../api/runner";

const props = defineProps<{
  userId: string | null;
  userPhone: string | null;
}>();

const emit = defineEmits<{
  (event: "next"): void;
  (event: "back-home"): void;
}>();

const phone = ref("");
const studentNo = ref("");
const emergencyContact = ref("");
const credentialImages = ref<Array<{ name: string; url: string }>>([]);
const fileInput = ref<HTMLInputElement | null>(null);
const isUploading = ref(false);
const isSubmitting = ref(false);

watch(
  () => props.userPhone,
  (value) => {
    if (value && !phone.value) phone.value = value;
  },
  { immediate: true },
);

const resolvedUserId = computed(() => props.userId || props.userPhone || "");

const canSubmit = computed(() => {
  const phoneValue = phone.value.trim();
  const studentNoValue = studentNo.value.trim();
  const emergencyContactValue = emergencyContact.value.trim();
  return /^1\d{10}$/.test(phoneValue) && studentNoValue.length >= 6 && credentialImages.value.length > 0 && emergencyContactValue.length > 0;
});

const openFilePicker = () => {
  fileInput.value?.click();
};

const onFileSelected = async (event: Event) => {
  const input = event.target as HTMLInputElement;
  const file = input.files?.[0];
  input.value = "";
  if (!file) return;
  if (!file.type.startsWith("image/")) {
    ElMessage.warning("请选择图片文件");
    return;
  }
  isUploading.value = true;
  try {
    const result = await uploadCredentialImage(file);
    credentialImages.value = [...credentialImages.value, { name: result.filename, url: result.url }];
    ElMessage.success("图片已上传到 uploadfile");
  } catch (error) {
    const msg = error instanceof Error ? error.message : "上传失败";
    ElMessage.error(msg);
  } finally {
    isUploading.value = false;
  }
};

const submit = async () => {
  if (!canSubmit.value) {
    ElMessage.warning("请完整填写认证信息后再提交");
    return;
  }
  if (!resolvedUserId.value) {
    ElMessage.error("缺少当前登录用户信息，请先登录");
    return;
  }
  isSubmitting.value = true;
  console.info("[gofer] submit runner verification", {
    userId: resolvedUserId.value,
    phone: phone.value,
    studentNo: studentNo.value,
    emergencyContact: emergencyContact.value,
    imageCount: credentialImages.value.length,
  });
  try {
    await submitRunnerVerification({
      user_id: resolvedUserId.value,
      student_no: studentNo.value.trim(),
      credential_images: credentialImages.value.map((image) => image.url),
    });
    ElMessage.success("认证材料已提交，等待管理员审核");
    emit("next");
  } catch (error) {
    const msg = error instanceof Error ? error.message : "提交失败";
    ElMessage.error(msg);
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<template>
  <MobileFrame>
    <div class="page">
      <AppNavBar title="跑腿认证页" :show-back="true" @back="emit('back-home')" />

      <section class="content">
        <el-card class="hero" shadow="never">
          <div class="hero-row">
            <div>
              <div class="hero-title">认证后可接单</div>
              <div class="hero-sub">完成基础认证后，开通接单大厅与收益面板</div>
            </div>
            <el-tag type="warning" effect="dark" round>待认证</el-tag>
          </div>
          <el-divider />
          <el-alert
            title="请确保手机号与学号信息真实有效，认证审核约 1-3 分钟"
            type="info"
            :closable="false"
            show-icon
          />
        </el-card>

        <el-card class="form-card" shadow="never">
          <el-form label-position="top">
            <el-form-item label="手机号">
              <el-input v-model="phone" maxlength="11" inputmode="numeric" placeholder="请输入11位手机号" clearable />
            </el-form-item>

            <el-form-item label="学号">
              <el-input v-model="studentNo" placeholder="请输入学号" clearable />
            </el-form-item>

            <el-form-item label="校园认证材料">
              <input ref="fileInput" class="hidden-input" type="file" accept="image/*" @change="onFileSelected" />
              <button class="upload-btn" type="button" :disabled="isUploading" @click="openFilePicker">
                {{ isUploading ? '上传中...' : '上传认证图片' }}
              </button>
            </el-form-item>

            <el-form-item label="紧急联系人">
              <el-input v-model="emergencyContact" placeholder="请输入紧急联系人电话" clearable />
            </el-form-item>
          </el-form>

          <div v-if="credentialImages.length" class="preview-grid">
            <figure v-for="image in credentialImages" :key="image.url" class="preview-item">
              <img :src="image.url" :alt="image.name" />
              <figcaption>{{ image.name }}</figcaption>
            </figure>
          </div>
        </el-card>
      </section>

      <footer class="footer">
        <div class="footer-actions">
          <el-button class="primary" type="primary" size="large" round :disabled="!canSubmit || isSubmitting || isUploading" @click="submit">提交认证</el-button>
          <el-button class="secondary" size="large" round @click="emit('back-home')">返回用户端</el-button>
        </div>
      </footer>
    </div>
  </MobileFrame>
</template>

<style scoped>
.page {
  min-height: 100%;
  display: grid;
  grid-template-rows: auto 1fr auto;
}

.hidden-input { display: none; }
.preview-grid { margin-top: 12px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }
.preview-item { margin: 0; border: 1px solid rgba(123, 155, 232, 0.18); border-radius: 10px; overflow: hidden; background: rgba(12, 18, 34, 0.35); }
.preview-item img { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; display: block; }
.preview-item figcaption { padding: 8px; font-size: 12px; color: rgba(167, 186, 227, 0.9); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.upload-btn {
  width: 100%;
  height: 46px;
  border: 1px solid rgba(64, 158, 255, 0.7);
  border-radius: 14px;
  background: linear-gradient(135deg, rgba(47, 125, 255, 0.18), rgba(86, 176, 255, 0.12));
  color: #dfeaff;
  font-size: 14px;
  font-weight: 700;
  letter-spacing: 0.2px;
  box-shadow: 0 8px 20px rgba(47, 125, 255, 0.12);
  transition: transform 0.16s ease, box-shadow 0.16s ease, filter 0.16s ease;
}
.upload-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 10px 24px rgba(47, 125, 255, 0.18);
  filter: brightness(1.05);
}
.upload-btn:active {
  transform: translateY(0);
  box-shadow: 0 6px 16px rgba(47, 125, 255, 0.12);
}

.content {
  padding: var(--space-4);
  display: grid;
  gap: var(--space-3);
  overflow: auto;
}

.hero,
.form-card {
  border: 1px solid rgba(123, 155, 232, 0.18);
  background: rgba(12, 18, 34, 0.55);
}

.hero-row {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-3);
}

.hero-title {
  color: #f2f6ff;
  font-size: 18px;
  font-weight: 900;
  letter-spacing: 0.2px;
}

.hero-sub {
  margin-top: 6px;
  color: rgba(167, 186, 227, 0.9);
  font-size: 12px;
  line-height: 1.35;
}

.footer {
  border-top: 1px solid rgba(123, 155, 232, 0.18);
  background: rgba(8, 12, 24, 0.65);
  padding: var(--space-3) var(--space-4);
}

.footer-actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 10px;
}

.primary,
.secondary {
  width: 100%;
}

:deep(.el-form-item) {
  margin-bottom: 14px;
}

:deep(.el-form-item__label) {
  color: #b9c7e8;
}
</style>
