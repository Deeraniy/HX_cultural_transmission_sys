<script setup>
import { ref } from 'vue';
import { Lock, Key, Check, Warning } from '@element-plus/icons-vue';
import { useI18n } from 'vue-i18n';
import { ElMessage } from 'element-plus';

const { t } = useI18n();
const oldPassword = ref('');
const newPassword = ref('');
const confirmPassword = ref('');
const isCollapse = ref(true);
const loading = ref(false);

// 表单验证规则
const validatePass = (rule, value, callback) => {
  if (value === '') {
    callback(new Error(t('user.password.currentPasswordPlaceholder')));
  } else if (value.length < 6) {
    callback(new Error(t('user.password.requirementLength')));
  } else {
    callback();
  }
};

const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error(t('user.password.confirmPasswordPlaceholder')));
  } else if (value !== newPassword.value) {
    callback(new Error(t('user.password.mismatch')));
  } else {
    callback();
  }
};

const rules = {
  oldPassword: [{ validator: validatePass, trigger: 'blur' }],
  newPassword: [{ validator: validatePass, trigger: 'blur' }],
  confirmPassword: [{ validator: validatePass2, trigger: 'blur' }]
};

const formRef = ref(null);

// 提交表单
const handleSubmit = async () => {
  if (!formRef.value) return;

  try {
    await formRef.value.validate();
    loading.value = true;

    // 模拟API调用
    setTimeout(() => {
      ElMessage.success('密码修改成功');
      loading.value = false;
      // 重置表单
      formRef.value.resetFields();
      isCollapse.value = false;
    }, 1000);
  } catch (error) {
    console.error('表单验证失败:', error);
  }
};
</script>

<template>
  <div class="password-container">
    <el-card class="password-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <el-icon><Lock /></el-icon>
          <span>{{ t('user.password.title') }}</span>
        </div>
      </template>

      <el-collapse v-model="isCollapse" accordion>
        <el-collapse-item name="1">
          <template #title>
            <div class="collapse-title">
              <el-icon><Key /></el-icon>
              <span>{{ t('user.password.changePassword') }}</span>
            </div>
          </template>

          <div class="form-container">
            <el-form
                ref="formRef"
                :model="{ oldPassword, newPassword, confirmPassword }"
                :rules="rules"
                label-position="top"
            >
              <!-- 旧密码 -->
              <el-form-item
                  :label="t('user.password.currentPassword')"
                  prop="oldPassword"
                  class="password-item"
              >
                <el-input
                    v-model="oldPassword"
                    type="password"
                    :placeholder="t('user.password.currentPasswordPlaceholder')"
                    show-password
                    :prefix-icon="Lock"
                />
              </el-form-item>

              <!-- 新密码 -->
              <el-form-item
                  :label="t('user.password.newPassword')"
                  prop="newPassword"
                  class="password-item"
              >
                <el-input
                    v-model="newPassword"
                    type="password"
                    :placeholder="t('user.password.newPasswordPlaceholder')"
                    show-password
                    :prefix-icon="Lock"
                />
              </el-form-item>

              <!-- 确认密码 -->
              <el-form-item
                  :label="t('user.password.confirmPassword')"
                  prop="confirmPassword"
                  class="password-item"
              >
                <el-input
                    v-model="confirmPassword"
                    type="password"
                    :placeholder="t('user.password.confirmPasswordPlaceholder')"
                    show-password
                    :prefix-icon="Lock"
                />
              </el-form-item>

              <!-- 密码规则提示 -->
              <div class="password-tips">
                <el-alert
                    :title="t('user.password.requirements')"
                    type="info"
                    :closable="false"
                    show-icon
                >
                  <div class="tips-content">
                    <p>{{ t('user.password.requirementLength') }}</p>
                    <p>{{ t('user.password.requirementChars') }}</p>
                    <p>{{ t('user.password.requirementCommon') }}</p>
                  </div>
                </el-alert>
              </div>

              <!-- 提交按钮 -->
              <div class="form-actions">
                <el-button
                    type="primary"
                    :loading="loading"
                    @click="handleSubmit"
                >
                  <el-icon><Check /></el-icon>
                  {{ t('user.password.confirm') }}
                </el-button>
                <el-button @click="formRef?.resetFields()">
                  {{ t('user.password.reset') }}
                </el-button>
              </div>
            </el-form>
          </div>
        </el-collapse-item>
      </el-collapse>
    </el-card>
  </div>
</template>

<style scoped>
.password-container {
  padding: 20px;
  max-width: 500px;
  margin: 0 auto;
}

.password-card {
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.collapse-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
  color: #606266;
}

.form-container {
  padding: 20px 0;
}

.password-item {
  margin-bottom: 20px;
}

.password-tips {
  margin: 20px 0;
}

.tips-content {
  margin-top: 8px;
  font-size: 13px;
  color: #909399;
  line-height: 1.6;
}

.form-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 30px;
}

:deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #dcdfe6 inset;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #b71c1c inset;
}

:deep(.el-collapse-item__header) {
  font-size: 14px;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

/* 动画效果 */
.password-card {
  transition: all 0.3s ease;
}

.password-card:hover {
  transform: translateY(-2px);
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .password-container {
    padding: 10px;
  }

  .form-actions {
    flex-direction: column;
  }

  .form-actions .el-button {
    width: 100%;
  }
}
</style>
