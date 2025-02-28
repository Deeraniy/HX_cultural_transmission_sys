<template>
  <div class="login-container">
    <div class="login-box">
      <div class="logo">
        <img src="@/assets/login/hunan.jpg" alt="logo" />
      </div>
      <h1>湖湘文化数智化传播系统</h1>
      <!-- 登录表单 -->
      <form v-if="!isRegister" @submit.prevent="handleLogin">
        <div class="input-group">
          <label for="username">用户名</label>
          <input
              type="text"
              id="username"
              v-model="username"
              placeholder="请输入用户名"
              required
          />
        </div>
        <div class="input-group">
          <label for="password">密码</label>
          <input
              type="password"
              id="password"
              v-model="password"
              placeholder="请输入密码"
              required
          />
        </div>
        <div class="submit-btn">
          <button type="submit">登录</button>
        </div>
      </form>

      <!-- 注册表单 -->
      <form v-if="isRegister" @submit.prevent="handleRegister">
        <div class="input-group">
          <label for="register-username">用户名</label>
          <input
              type="text"
              id="register-username"
              v-model="registerUsername"
              placeholder="请输入用户名"
              required
          />
        </div>
        <div class="input-group">
          <label for="register-password">密码</label>
          <input
              type="password"
              id="register-password"
              v-model="registerPassword"
              placeholder="请输入密码"
              required
          />
        </div>
        <div class="input-group">
          <label for="register-confirm-password">确认密码</label>
          <input
              type="password"
              id="register-confirm-password"
              v-model="registerConfirmPassword"
              placeholder="请确认密码"
              required
          />
        </div>
        <div class="submit-btn">
          <button type="submit">注册</button>
        </div>
      </form>

      <div class="links">
        <a href="#" v-if="!isRegister" @click.prevent="handleForgotPassword">忘记密码？</a>
        <a href="#" @click.prevent="toggleForm">{{ isRegister ? '已有账户？登录' : '没有账户？注册' }}</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import {
  provinceAndCityData,
  pcTextArr,
  regionData,
  pcaTextArr,
  codeToText,
} from "element-china-area-data";

const router = useRouter();

const username = ref('');
const password = ref('');
const isRegister = ref(false);
const registerUsername = ref('');
const registerPassword = ref('');
const registerConfirmPassword = ref('');

// 登录处理
const handleLogin = () => {
  if (username.value && password.value) {
    console.log('Logging in with:', username.value, password.value);
    router.push('/index');
  } else {
    alert('请输入用户名和密码');
  }
};

// 注册处理
const handleRegister = () => {
  if (registerPassword.value !== registerConfirmPassword.value) {
    alert('密码和确认密码不一致');
    return;
  }

  if (registerUsername.value && registerPassword.value) {
    console.log('Registering with:', registerUsername.value, registerPassword.value);
    router.push('/dashboard');
  } else {
    alert('请输入用户名和密码');
  }
};

// 忘记密码处理
const handleForgotPassword = () => {
  router.push('/forgot-password');
};

// 切换表单
const toggleForm = () => {
  isRegister.value = !isRegister.value;
};
</script>


<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.5) url('@/assets/login/city.png') no-repeat center center;
  background-size: cover;
}

.login-box {
  background-color: #fff;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

.logo img {
  width: 80px;
  height: auto;
  margin-bottom: 20px;
}

h1 {
  font-family: "KaiTi", "楷体", serif;
  font-size: 24px;
  color: #d9534f; /* 故宫红 */
  margin-bottom: 30px;
}

.input-group {
  margin-bottom: 20px;
  text-align: left;
}

.input-group label {
  font-size: 14px;
  color: #555;
}

.input-group input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.submit-btn button {
  width: 100%;
  padding: 12px;
  background-color: #d9534f;
  border: none;
  border-radius: 4px;
  color: #fff;
  font-size: 16px;
  cursor: pointer;
}

.submit-btn button:hover {
  background-color: #c9302c;
}

.links {
  margin-top: 15px;
  font-size: 14px;
}

.links a {
  color: #d9534f;
  text-decoration: none;
  margin: 0 10px;
}

.links a:hover {
  text-decoration: underline;
}
</style>
