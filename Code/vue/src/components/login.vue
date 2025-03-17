<template>
  <div class="login-container">
    <div class="login-box">
      <div class="form-container">
        <!-- Logo和标题 -->
        <div class="brand">
          <div class="logo">
            <img src="@/assets/333.png" alt="logo" />
          </div>
          <h1 class="title">湖湘文化数智化传播系统</h1>
          <p class="subtitle">数联万里湖湘 · 智汇千年文脉</p>
        </div>
        <!-- 登录表单 -->
        <el-form
            v-if="!isRegister"
            ref="loginFormRef"
            :model="loginForm"
            :rules="loginRules"
            @submit.prevent="handleLogin"
        >
          <el-form-item prop="username">
            <el-input
                v-model="loginForm.username"
                :prefix-icon="User"
                placeholder="请输入用户名"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
                v-model="loginForm.password"
                :prefix-icon="Lock"
                type="password"
                placeholder="请输入密码"
                show-password
            />
          </el-form-item>

          <div class="remember-forgot">
            <el-checkbox v-model="rememberMe" class="remember-text">记住我</el-checkbox>
            <a class="forgot-link" @click="handleForgotPassword">忘记密码？</a>
          </div>

          <div class="button-wrapper">
            <el-button
                type="primary"
                class="submit-btn"
                :loading="loading"
                @click="handleLogin"
            >
              登录
            </el-button>
          </div>
        </el-form>

        <!-- 注册表单 -->
        <el-form
            v-else
            ref="registerFormRef"
            :model="registerForm"
            :rules="registerRules"
            @submit.prevent="handleRegister"
        >
          <el-form-item prop="username">
            <el-input
                v-model="registerForm.username"
                :prefix-icon="User"
                placeholder="请输入用户名"
            />
          </el-form-item>

          <el-form-item prop="password">
            <el-input
                v-model="registerForm.password"
                :prefix-icon="Lock"
                type="password"
                placeholder="请输入密码"
                show-password
            />
          </el-form-item>

          <!-- 年龄和性别放在同一行 -->
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item prop="age">
                <el-input
                    v-model.number="registerForm.age"
                    :prefix-icon="Calendar"
                    type="number"
                    placeholder="请输入年龄"
                />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item prop="sex">
                <el-select v-model="registerForm.sex" placeholder="请选择性别" style="width: 100%">
                  <el-option label="男" value="male" />
                  <el-option label="女" value="female" />
                  <el-option label="其他" value="other" />
                </el-select>
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item prop="region" label="所在地区">
            <el-cascader
                v-model="registerForm.region"
                :options="regionData"
                placeholder="请选择所在地区"
            />
          </el-form-item>

          <div class="button-wrapper">
            <el-button
                type="primary"
                class="submit-btn"
                :loading="loading"
                @click="handleRegister"
            >
              注册
            </el-button>
          </div>
        </el-form>

        <!-- 切换表单 -->
        <div class="form-switch">
          <p>
            {{ isRegister ? '已有账号？' : '还没有账号？' }}
            <a @click="toggleForm">
              {{ isRegister ? '立即登录' : '立即注册' }}
            </a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { User, Lock, Calendar } from '@element-plus/icons-vue';
import { regionData } from 'element-china-area-data';
import { ElMessage } from 'element-plus';
import UserAPI from '@/api/user';

const router = useRouter();
const loading = ref(false);
const isRegister = ref(false);
const rememberMe = ref(false);

// 登录表单
const loginFormRef = ref(null);
const loginForm = reactive({
  username: '',
  password: ''
});

// 注册表单
const registerFormRef = ref(null);
const registerForm = reactive({
  username: '',
  password: '',
  age: '',
  sex: 'other' as 'male' | 'female' | 'other',
  region: [] as any[],
  avatar: ''
});

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于 6 个字符', trigger: 'blur' }
  ]
};

const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能小于 6 个字符', trigger: 'blur' }
  ],
  age: [
    { required: true, message: '请输入年龄', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value === '') {
          callback(new Error('请输入年龄'))
        } else {
          const age = parseInt(value)
          if (isNaN(age)) {
            callback(new Error('年龄必须为数字'))
          } else if (age < 0 || age > 150) {
            callback(new Error('年龄必须在 0 到 150 之间'))
          } else {
            callback()
          }
        }
      },
      trigger: 'blur'
    }
  ],
  sex: [
    { required: true, message: '请选择性别', trigger: 'change' }
  ],
  region: [
    { required: true, message: '请选择所在地区', trigger: 'change' }
  ]
};

// 修改响应类型定义
interface ApiResponse {
  status: string;
  msg: string;
  user_id: number;
  username: string;
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return;

  try {
    await loginFormRef.value.validate();
    loading.value = true;

    const loginData = {
      username: loginForm.username,
      password: loginForm.password
    };

    try {
      const response = await UserAPI.loginAPI(loginData);
      console.log('Login response:', response);

      if (response.status === "success") {
        ElMessage.success('登录成功');
        
        localStorage.setItem('userId', String(response.user_id));
        localStorage.setItem('username', response.username);
        
        if (rememberMe.value) {
          localStorage.setItem('rememberMe', 'true');
        }
        
        router.push('/index');
      } else {
        ElMessage.error(response.msg || '登录失败');
      }
    } catch (error) {
      console.error('Login error:', error);
      ElMessage.error('登录失败，请稍后重试');
    }
  } catch (error) {
    console.error('表单验证失败:', error);
  } finally {
    loading.value = false;
  }
};

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return;

  try {
    await registerFormRef.value.validate();
    loading.value = true;

    const regionValue = registerForm.region[registerForm.region.length - 1];

    const registerData = {
      username: registerForm.username,
      password: registerForm.password,
      age: parseInt(registerForm.age) || 0,
      sex: registerForm.sex,
      location: regionValue || '',  // 确保有默认值
      avatar: registerForm.avatar
    };

    try {
      const response = await UserAPI.registerAPI(registerData);
      console.log('Registration response:', response);

      if (!response) {
        throw new Error('注册失败：服务器无响应');
      }

      ElMessage.success('注册成功');
      isRegister.value = false;  // 切换到登录界面

    } catch (error: any) {
      console.error('Registration error details:', error);
      ElMessage.error(error.message || '注册失败，请稍后重试');
    }
  } finally {
    loading.value = false;
  }
};

// 处理忘记密码
const handleForgotPassword = () => {
  router.push('/forgot-password');
};

// 切换表单
const toggleForm = () => {
  isRegister.value = !isRegister.value;
  // 重置表单
  if (isRegister.value) {
    loginFormRef.value?.resetFields();
  } else {
    registerFormRef.value?.resetFields();
  }
};
</script>

<style scoped>
@import '@/assets/font/font.css';

.login-container {
  font-family: 'HelveticaNeue',serif;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.3)),
  url('@/assets/login/city.png') no-repeat center center;
  background-size: cover;
}

.login-box {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  padding-left: 40px;
  padding-right: 40px;
  padding-top: 20px;
  padding-bottom: 20px;
  width: 100%;
  max-width: 420px;
  margin: 20px;
}

.brand {
  text-align: center;
  margin-bottom: 40px;
}

.logo img {
  width: 80px;
  height: 80px;
  object-fit: cover;
}

.title {
  font-family: 'HelveticaNeue',serif;
  font-size: 38px;
  color: #b71c1c;
  letter-spacing: 2px;
}

.subtitle {
  color: #8c8c8c;
  font-family: 'HelveticaNeue',serif;
  font-size: 18px;
}

.form-container {
  margin-top: 20px;
}

:deep(.el-input__wrapper) {
  box-shadow: 0 0 0 1px #d9d9d9 inset;
  padding: 12px;
  border-radius: 8px;
}

:deep(.el-input__inner) {
  height: 20px;
  font-family: 'HelveticaNeue', serif;
  font-size: 16px;
}

:deep(.el-input__inner::placeholder) {
  font-family: 'HelveticaNeue', serif;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 1px #b71c1c inset;
}

.remember-forgot {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 20px 0;
  font-size: 16px;
}

.remember-text {
  font-size: 16px;
}

:deep(.el-checkbox__label) {
  font-size: 16px;
}

.forgot-link {
  color: #b71c1c;
  cursor: pointer;
  font-size: 16px;
}

.forgot-link:hover {
  text-decoration: underline;
}

.button-wrapper {
  display: flex;
  justify-content: center;
  width: 100%;
}

.submit-btn {
  width: 30%;
  padding: 12px;
  font-size: 20px;
  background: #b71c1c;
  font-family: 'HelveticaNeue',serif;
  border: none;
}

.submit-btn:hover {
  background: #d32f2f;
}

.form-switch {
  text-align: center;
  margin-top: 20px;
  color: #8c8c8c;
  font-size: 16px;
}

.form-switch a {
  color: #b71c1c;
  cursor: pointer;
  font-weight: 500;
}

.form-switch a:hover {
  text-decoration: underline;
}

/* 动画效果 */
.login-box {
  animation: slideUp 0.5s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式布局 */
@media (max-width: 480px) {
  .login-box {
    margin: 10px;
    padding: 20px;
  }

  .title {
    font-size: 24px;
  }
}

/* 统一所有输入框的基础样式 */
:deep(.el-input__wrapper),
:deep(.el-select .el-input__wrapper) {
    height: 44px;  /* 设置统一高度 */
    line-height: 44px;
    box-sizing: border-box;
}

/* 专门调整性别选择框 */
:deep(.el-select) {
    width: 100%;
    height: 44px;
}

:deep(.el-select .el-input) {
    height: 44px;
}

:deep(.el-select .el-input__wrapper) {
    height: 44px !important;
}

:deep(.el-select .el-input__inner) {
    height: 44px !important;
    line-height: 44px !important;
}

/* 调整下拉选项的样式 */
:deep(.el-select-dropdown__item) {
    height: 44px;
    line-height: 44px;
}

/* 确保所有表单项容器高度一致 */
.el-form-item {
    margin-bottom: 20px;
    height: 44px;
}

:deep(.el-form-item__content) {
    height: 44px;
    line-height: 44px;
}

/* 移除行间距 */
.el-row {
    margin-bottom: 0;
}

/* 调整列间距 */
.el-col {
    padding: 0 10px;
}
</style>
