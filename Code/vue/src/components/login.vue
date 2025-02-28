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

<script>
export default {
  data() {
    return {
      username: '',        // 登录时的用户名
      password: '',        // 登录时的密码
      isRegister: false,   // 控制显示登录还是注册表单
      registerUsername: '', // 注册时的用户名
      registerPassword: '', // 注册时的密码
      registerConfirmPassword: '', // 注册时的确认密码
    };
  },
  methods: {
    // 登录处理
    handleLogin() {
      if (this.username && this.password) {
        console.log('Logging in with:', this.username, this.password);
        this.$router.push('/dashboard'); // 登录成功后跳转到仪表盘
      } else {
        alert('请输入用户名和密码');
      }
    },

    // 注册处理
    handleRegister() {
      // 检查密码是否匹配
      if (this.registerPassword !== this.registerConfirmPassword) {
        alert('密码和确认密码不一致');
        return;
      }

      if (this.registerUsername && this.registerPassword) {
        console.log('Registering with:', this.registerUsername, this.registerPassword);
        this.$router.push('/dashboard'); // 注册成功后跳转到仪表盘
      } else {
        alert('请输入用户名和密码');
      }
    },

    // 忘记密码处理
    handleForgotPassword() {
      // 假设跳转到忘记密码页面
      this.$router.push('/forgot-password');
    },

    // 切换表单
    toggleForm() {
      this.isRegister = !this.isRegister;
    },
  },
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
