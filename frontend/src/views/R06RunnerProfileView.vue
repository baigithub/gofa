<script setup lang="ts">
import { computed, onMounted, ref } from "vue";
import { ElMessage } from "element-plus";
import { uploadCredentialImage } from "../api/runner";

const emit = defineEmits<{
  (event: "back-hall"): void;
  (event: "go-message"): void;
}>();

const phone = ref("");
const studentNo = ref("");
const emergencyContact = ref("");
const credentialImages = ref<Array<{ name: string; url: string }>>([]);
const isUploading = ref(false);
const isSubmitting = ref(false);
const status = ref<"pending" | "approved" | "rejected">("pending");

const uploadHint = computed(() => (credentialImages.value.length ? `已选择 ${credentialImages.value.length} 张图片` : "上传各类认证图片"));
const statusText = computed(() => (status.value === "pending" ? "待认证" : status.value === "approved" ? "已通过" : "已拒绝"));

const onUploadChange = async (file: File) => {
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

const submitVerification = () => {
  if (!phone.value.trim() || !studentNo.value.trim()) {
    ElMessage.warning("请先填写手机号和学号");
    return;
  }
  if (credentialImages.value.length === 0) {
    ElMessage.warning("请先上传认证图片");
    return;
  }
  console.info("[gofer] submit runner verification", {
    phone: phone.value,
    studentNo: studentNo.value,
    imageCount: credentialImages.value.length,
  });
  isSubmitting.value = true;
  window.setTimeout(() => {
    ElMessage.success("认证材料已提交，等待管理员审核");
    status.value = "pending";
    isSubmitting.value = false;
  }, 500);
};

onMounted(() => {
  console.info("[gofer] mount R06RunnerProfileView");
});
</script>

<template>
  <main class="page">
    <section class="phone">
      <section class="card">
        <div class="section-badge">跑腿员认证页</div>
        <h1>跑腿员认证页</h1>
        <p>今日收益：¥56.00</p>
        <p>本周单量：12 单</p>
        <p>历史订单：可查看</p>
      </section>

      <section class="card">
        <div class="card-head">
          <h2>校园认证材料</h2>
          <span>{{ statusText }}</span>
        </div>
        <p class="desc">请确保手机号与学号信息真实有效，认证审核约 1-3 分钟。</p>

        <div class="form-grid">
          <el-input v-model="phone" placeholder="请输入11位手机号" maxlength="11" />
          <el-input v-model="studentNo" placeholder="请输入学号" maxlength="20" />
          <el-input v-model="emergencyContact" placeholder="请输入紧急联系人电话" maxlength="20" />
        </div>

        <el-upload
          class="upload-wrap"
          action="#"
          :show-file-list="false"
          :auto-upload="false"
          accept="image/*"
          :disabled="isUploading"
          :on-change="(file) => onUploadChange(file.raw as File)"
        >
          <button class="upload-btn" type="button" :disabled="isUploading">
            {{ isUploading ? '上传中...' : '上传认证图片' }}
          </button>
        </el-upload>

        <div v-if="credentialImages.length" class="preview-grid">
          <figure v-for="image in credentialImages" :key="image.url" class="preview-item">
            <img :src="image.url" :alt="image.name" />
            <figcaption>{{ image.name }}</figcaption>
          </figure>
        </div>

        <button class="submit-btn" type="button" :disabled="isSubmitting || isUploading" @click="submitVerification">
          {{ isSubmitting ? '提交中...' : '提交认证' }}
        </button>
      </section>

      <footer class="footer">
        <button class="primary" @click="emit('go-message')">消息窗口</button>
        <button @click="emit('back-hall')">返回大厅</button>
      </footer>
    </section>
  </main>
</template>

<style scoped>
.page { min-height: 100svh; display: grid; place-items: center; }
.phone { width: min(100vw, 390px); min-height: 100svh; display: grid; grid-template-rows: auto auto 1fr auto; gap: var(--space-3); background: var(--color-bg); }
.card { margin: 0 var(--space-4); background: var(--color-surface); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--space-4); }
.section-badge { display: inline-flex; align-items: center; margin-bottom: 10px; padding: 4px 8px; border-radius: 999px; background: rgba(0, 122, 255, 0.12); color: var(--color-primary); font-size: 12px; font-weight: 600; }
h1, h2 { margin: 0 0 var(--space-3); font-size: var(--font-size-lg); }
.card-head { display: flex; justify-content: space-between; gap: var(--space-2); align-items: baseline; }
.card-head span, .desc, p { color: var(--color-text-secondary); margin: 0; }
.desc { margin-bottom: var(--space-3); line-height: 1.5; }
.form-grid { display: grid; gap: 10px; margin-bottom: var(--space-3); }
.upload-wrap { width: 100%; }
.upload-btn { width: 100%; height: 40px; border: 1px dashed var(--color-primary); border-radius: var(--radius-sm); background: rgba(0, 122, 255, 0.05); color: var(--color-primary); }
.preview-grid { margin-top: var(--space-3); display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--space-2); }
.preview-item { margin: 0; border: 1px solid var(--color-border); border-radius: var(--radius-sm); overflow: hidden; background: #fff; }
.preview-item img { width: 100%; aspect-ratio: 1 / 1; object-fit: cover; display: block; }
.preview-item figcaption { padding: var(--space-2); font-size: 12px; color: var(--color-text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.submit-btn { width: 100%; height: 40px; margin-top: var(--space-3); border: 1px solid var(--color-primary); border-radius: var(--radius-sm); background: rgba(0, 122, 255, 0.08); color: var(--color-primary); }
.footer { border-top: 1px solid var(--color-border); padding: var(--space-3) var(--space-4); background: var(--color-surface); display: grid; gap: var(--space-2); }
button { width: 100%; height: 40px; border: 1px solid var(--color-border); border-radius: var(--radius-sm); background: #fff; }
.primary { border-color: var(--color-primary); color: var(--color-primary); }
.upload-btn:disabled,
.submit-btn:disabled { opacity: 0.7; cursor: not-allowed; }
:deep(.el-textarea__inner),
:deep(.el-input__wrapper) { background: #fff; border-color: var(--color-border); }
</style>
