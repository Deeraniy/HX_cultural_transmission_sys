<template>
  <div class="whole" :class="{ 'styled-font': fontStore.isStyled }">
    <div class="total">
      <!-- 左侧Logo -->
      <div class="logo">
        <img src="@/assets/444.png" alt="Logo" class="logo-image" />
      </div>
      <!-- 菜单区域 -->
      <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          :ellipsis="false"
          @select="handleSelect"
      >
        <!-- 作品总览菜单项 -->

        <el-sub-menu index="culture">
         <template #title>特色文化展示</template>
         <el-menu-item index="3">名胜古迹</el-menu-item>
         <el-menu-item index="4">影视文学</el-menu-item>
         <el-menu-item index="5">美食文化</el-menu-item>
         <el-menu-item index="6">非遗民俗</el-menu-item>
         <el-menu-item index="7">红色文化</el-menu-item>
       </el-sub-menu>
        <el-menu-item index="8">情感分析</el-menu-item>
        <el-menu-item index="9">个性推荐</el-menu-item>
        <el-menu-item index="10">宣传报告生成</el-menu-item>
        <el-menu-item index="11">全球传播情况</el-menu-item>
        <el-menu-item index="12">背景介绍</el-menu-item>
        <el-menu-item index="13">关于我们</el-menu-item>
      </el-menu>
      <!-- 右侧用户信息 -->
      <div class="user-info">
        <!-- 问候语 -->


        <!-- 语言选择 -->
        <el-dropdown trigger="click" @command="handleLanguageChange">
          <el-button type="primary">
            {{ language || '中文' }}
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="normal">系统字体</el-dropdown-item>
              <el-dropdown-item command="styled">风格字体</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <span class="greeting">{{ greeting }}</span>
        <!-- 用户头像下拉菜单 -->
        <el-dropdown v-if="userStore.isLoggedIn" trigger="click" @command="handleCommand">
          <div class="user-avatar">
            <img :src="userData.avatar || '@/assets/Video1.jpg'" alt="User Avatar" />
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">个人中心</el-dropdown-item>
              <el-dropdown-item command="logout">退出登录</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>

        <!-- 未登录时显示登录按钮 -->
        <el-button v-else type="text" @click="goToLogin">登录</el-button>
      </div>
    </div>

    <el-main>
      <!-- 根据 activeIndex 显示不同的组件 -->
      <index v-if="activeIndex===null" />
    </el-main>
  </div>
</template>

<script lang="ts" setup>
import {ref, watch, computed, onMounted} from 'vue';
import Index from "@/components/index.vue";
import PoemDisplay from "@/components/FilmLiterature/FilmLiteratureMain.vue"; // 导入 PoemDisplay 组件
import {ArrowDown} from "@element-plus/icons-vue";
import { useRouter, useRoute } from 'vue-router';
import { useUserStore } from '@/stores/user'
import UserAPI from '@/api/user'; // 导入UserAPI
import { useFontStore } from '@/stores/font'

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();
const fontStore = useFontStore()

// 设置 activeIndex 初始值为 '2-1'，这样组件会默认显示 FilmLiterature
// Sync the activeIndex with the route path
const activeIndex = ref<string | null>(null);

// Watch for route changes and update activeIndex
watch(
    () => route.path,
    (newPath) => {
      console.log("newPath", newPath)
      if (newPath === '/placeOfInterest') activeIndex.value = '3';
      else if (newPath === '/filmLiterature') activeIndex.value = '4';
      else if (newPath === '/food') activeIndex.value = '5';
      else activeIndex.value = null;
    }
);

// Set the initial activeIndex based on the current route
if (route.path === '/placeOfInterest') activeIndex.value = '3';
else if (route.path === '/filmLiterature') activeIndex.value = '4';
else if (route.path === '/food') activeIndex.value = '5';

const language = ref('中文');

// 获取问候语
const greeting = computed(() => {
  const hour = new Date().getHours();
  if (language.value === '中文') {
    if (hour < 6) return '凌晨好！';
    if (hour < 9) return '早上好！';
    if (hour < 12) return '上午好！';
    if (hour < 14) return '中午好！';
    if (hour < 17) return '下午好！';
    if (hour < 19) return '傍晚好！';
    if (hour < 22) return '晚上好！';
    return '夜深了！';
  } else {
    if (hour < 6) return 'Good Early Morning!';
    if (hour < 12) return 'Good Morning!';
    if (hour < 18) return 'Good Afternoon!';
    return 'Good Evening!';
  }
});

// 处理菜单选择
// Handle menu item select and navigate accordingly
const handleSelect = (key: string, keyPath: string[]) => {
  activeIndex.value = key;

  switch (key) {
    case '2':
      router.push('/index'); // 名胜古迹
      break;
    case '3':
      router.push('/placeOfInterest'); // 名胜古迹
      break;
    case '4':
      router.push('/filmLiterature'); // 影视文学
      break;
    case '5':
      router.push('/food'); // 美食文化
      break;
    case '6':
      router.push('/folkCustom'); // 美食文化
      break;
    case '7':
      router.push('/red'); // 美食文化
      break;
    case '8':
      router.push('/detail'); // 美食文化
      break;
    case '9':
      router.push('/recommend');
      break;
    case '10':
      router.push('/report');
      break;
    case '11':
      router.push('/globe');
      break;
    case '12':
      router.push('/background');
      break;
    case '13':
      router.push('/about');
      break;

      // Add more cases for other menu items if needed
    default:
      break;
  }
};

// 跳转到登录页
const goToLogin = () => {
  router.push('/login');
};

// 恢复处理用户下拉菜单命令
const handleCommand = (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/userHome/article');
      break;
    case 'logout':
      userStore.logout();
      router.push('/login');
      break;
  }
};

// 处理语言切换
const handleLanguageChange = (command) => {
  switch (command) {
    case 'normal':
      language.value = '系统字体';
      document.documentElement.setAttribute('data-font-style', 'normal');
      break;
    case 'styled':
      language.value = '风格字体';
      document.documentElement.setAttribute('data-font-style', 'styled');
      break;
  }
};

// 用户数据，包含头像
const userData = ref({
  username: '',
  avatar: new URL('@/assets/default-avatar.png', import.meta.url).href,  // 设置默认头像
  // ... 其他用户数据
});

// 获取用户信息
const getUserInfo = async () => {
  try {
    if (userStore.isLoggedIn && userStore.userId) {
      const res = await UserAPI.getUserFullInfo(userStore.userId);
      if (res && res.status === 'success' && res.data) {
        userData.value = {
          ...userData.value,
          avatar: res.data.avatar || new URL('@/assets/default-avatar.png', import.meta.url).href,
        };
      }
    }
  } catch (error) {
    console.error('获取用户信息失败:', error);
  }
};

// 在组件挂载时获取用户信息
onMounted(() => {
  if (userStore.isLoggedIn) {
    getUserInfo();
  }

  // 监听用户信息更新事件
  window.addEventListener('user-info-updated', getUserInfo);
});
</script>

<style>
:root {
  --el-menu-item-font-size: 20px !important;
  --el-font-size-base: 20px !important;
}

/* 全局样式覆盖 */
.el-menu,
.el-menu--horizontal,
.el-menu--popup,
.el-menu--popup-container,
.el-popper,
.el-sub-menu__popper {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
}

.el-menu-item,
.el-sub-menu,
.el-sub-menu__title {
  background: transparent !important;
}

.el-popper.is-light {
  background: transparent !important;
  border: none !important;
}

.el-menu--popup .el-menu-item,
.el-menu .el-menu-item {
  background: rgba(255, 255, 255, 0.2) !important;
  color: #fff8f0 !important;
}

.el-menu--popup .el-menu-item:hover,
.el-menu .el-menu-item:hover {
  background: rgba(255, 255, 255, 0.3) !important;
  color: #ffd700 !important;
}

.el-popper__arrow {
  display: none !important;
}

/* 新增的菜单项横向布局样式 */
.horizontal-submenu .el-menu-item {
  display: inline-block; /* 让菜单项横向排列 */
  margin-right: 20px; /* 为子菜单项之间添加间距 */
}

.horizontal-submenu .el-menu-item:last-child {
  margin-right: 0; /* 最后一个子项去除右边距 */
}

.horizontal-submenu .el-sub-menu__title {
  padding: 0 10px; /* 子菜单标题内边距 */
  cursor: pointer;
  white-space: nowrap;
}

/* 子菜单的弹出框样式 */
.horizontal-submenu .el-sub-menu__popper {
  display: none; /* 去除子菜单下拉显示 */
}
</style>

<style scoped>
@import '@/assets/font/font.css';

.total {
  display: flex;
  align-items: center;
  background-image: url('@/assets/img_4.png');
  background-size: cover;
  background-position: center;
  padding-right: 20px;
  justify-content: space-between;
}

.whole {
  margin-top: 0px;
  background-image: url('@/assets/img2.png');
  background-color: #fff8f0;
  background-size: cover;
  background-position: center;
}

.el-main {
  padding: 0;
}

/* 标题样式 */
.menu-title {
  transform: translateY(25px);
  color: #fff8f0;
  margin-right: 510px;
  font-family: 'HelveticaNeue', serif !important;
  font-size: 30px !important;
}

/* 系统字体时的标题样式 */
[data-font-style="normal"] .menu-title {
  font-family: var(--font-family-base) !important;
  font-size: 30px !important;
}

.el-menu-demo {
  margin-left: 50px;  /* 增加与logo的距离 */
  display: flex;
  justify-content: flex-start;
  background-color: transparent !important;
  box-shadow: none;
  border-bottom: none;
  flex: 1;
}

.el-menu-item {
  margin-right: 0px;
  padding: 0 15px;
  background-color: #B71C1C64 !important;
  color: #fff8f0 !important;
  height: 60px;  /* 确保菜单项高度足够 */
  line-height: 60px;  /* 垂直居中文字 */
}

.el-menu-item.is-active,
.el-menu-item:hover {
  color: #ffd700 !important;
  background-color: #B71C1C64 !important;
}

:deep(.el-sub-menu__title) {
  padding: 0 15px;
  color: #fff8f0 !important;
  background-color: #B71C1C64 !important;
  height: 60px;  /* 确保菜单项高度足够 */
  line-height: 60px;  /* 垂直居中文字 */
  white-space: nowrap;
  overflow: hidden;
  font-size: 20px !important;
  margin-right: -30px;
  text-overflow: ellipsis;
  cursor: pointer;
}

:deep(.el-sub-menu__icon-arrow) {
  display: none !important;
}

:deep(.el-sub-menu__title:hover),
:deep(.el-sub-menu__title.is-active) {
  color: #ffd700 !important;
  background-color: #B71C1C64 !important;
}

:deep(.el-sub-menu) {
  background-color: transparent !important;
}

/* 左侧Logo样式 */
.logo {
  flex: 0 0 40px;
  margin-left: 10px;
  display: flex;
  align-items: center;
}

.logo-image {
  width: 180%;
  height: auto;
  margin-left: 0;
}

/* 右侧用户信息 */
.user-info {
  display: flex;
  align-items: center;
  gap: 15px;  /* 增加元素间距 */
  margin-left: auto;
  margin-right: 0;
  z-index: 1;
}

.user-avatar {
  display: flex;
  align-items: center;
  cursor: pointer;
  white-space: nowrap;
}

.user-avatar img {
  width: 35px;
  height: 35px;
  object-fit: cover;
  border-radius: 50%;
}

.username {
  color: #fff8f0;
  font-family: 'HelveticaNeue', serif;
  font-size: 16px;
  white-space: nowrap;  /* 防止文字换行 */
}

.el-button.el-button--text {
  color: #fff8f0;
  font-family: 'HelveticaNeue', serif;
  font-size: 16px;
}

/* 修改下拉按钮样式 */
.el-dropdown .el-button {
  background-color: transparent;
  color: #fff8f0;
  border: none;
  font-family: 'HelveticaNeue', serif;
  font-size: 16px;
  padding: 0 10px;
}

.el-dropdown .el-button .el-icon--right {
  color: #fff8f0;
}

.greeting {
  color: #fff8f0;
  font-family: 'HelveticaNeue', serif;
  font-size: 16px;
  white-space: nowrap;
}

/* 为了确保其他需要保持特定大小的元素也不受影响，可以添加 data-preserve-font 属性 */
[data-preserve-font] {
  font-size: inherit !important;
  font-family: inherit !important;
}

.styled-font {
  font-family: 'HelveticaNeue', serif;
}

/* 非风格字体时的样式 */
.whole:not(.styled-font) {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* 子菜单的样式 */
:deep(.el-menu--popup) {
  min-width: 120px !important;
  background-color: rgba(183, 28, 28, 0.9) !important;
  border: none !important;
  padding: 0 !important;
}

:deep(.el-menu--popup .el-menu-item) {
  height: 50px !important;
  line-height: 50px !important;
  color: #fff8f0 !important;
  font-family: 'HelveticaNeue', serif !important;
  padding: 0 20px !important;
}

:deep(.el-menu--popup .el-menu-item:hover) {
  background-color: rgba(255, 255, 255, 0.1) !important;
  color: #ffd700 !important;
}

/* 添加新的样式规则来控制字体 */
[data-font-style="styled"] .el-menu-item,
[data-font-style="styled"] :deep(.el-sub-menu__title),
[data-font-style="styled"] :deep(.el-menu--popup .el-menu-item) {
  font-family: 'HelveticaNeue', serif !important;
  font-size: 20px !important;
}

[data-font-style="normal"] .el-menu-item,
[data-font-style="normal"] :deep(.el-sub-menu__title),
[data-font-style="normal"] :deep(.el-menu--popup .el-menu-item .el-font-size-base)  {
  font-family: var(--font-family-base) !important;
  font-size: 20px !important;
}

/* 确保下拉菜单的样式不受全局字体切换影响 */
:deep(.el-popper.is-light) {
  border: none !important;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1) !important;
}

:deep(.el-popper.is-light .el-menu--popup) {
  background-color: rgba(183, 28, 28, 0.9) !important;
}
</style>
