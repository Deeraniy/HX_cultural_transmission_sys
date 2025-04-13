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
        <!-- 首页按钮 -->
        <el-menu-item index="1">{{ t('menu.home') }}</el-menu-item>

        <!-- 作品总览菜单项 -->
        <el-sub-menu index="culture">
         <template #title>{{ t('menu.culture') }}</template>
         <el-menu-item index="3">{{ t('menu.places') }}</el-menu-item>
         <el-menu-item index="4">{{ t('menu.film') }}</el-menu-item>
         <el-menu-item index="5">{{ t('menu.food') }}</el-menu-item>
         <el-menu-item index="6">{{ t('menu.folk') }}</el-menu-item>
         <el-menu-item index="7">{{ t('menu.red') }}</el-menu-item>
       </el-sub-menu>
        <el-menu-item index="8">{{ t('menu.sentiment') }}</el-menu-item>
        <el-menu-item index="9">{{ t('menu.recommend') }}</el-menu-item>
        <el-menu-item index="10">{{ t('menu.report') }}</el-menu-item>
        <el-menu-item index="11">{{ t('menu.global') }}</el-menu-item>
        <el-menu-item index="12">{{ t('menu.background') }}</el-menu-item>
        <el-menu-item index="13">{{ t('menu.about') }}</el-menu-item>
      </el-menu>
      <!-- 右侧用户信息 -->
      <div class="user-info">
        <!-- 语言选择 -->
        <el-dropdown trigger="click" @command="handleLanguageChange">
          <el-button type="primary">
            {{ currentLanguage }}
            <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="zh">中文</el-dropdown-item>
              <el-dropdown-item command="en">English</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <!-- 只在中文模式下显示问候语 -->
        <span v-if="locale === 'zh'" class="greeting">{{ greeting }}</span>
        <!-- 用户头像下拉菜单 -->
        <el-dropdown v-if="userStore.isLoggedIn" trigger="click" @command="handleCommand">
          <div class="user-avatar">
            <img :src="userData.avatar || '@/assets/Video1.jpg'" alt="User Avatar" />
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">{{ t('user.profile.title') }}</el-dropdown-item>
              <el-dropdown-item command="logout">{{ t('user.logout') }}</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>

        <!-- 未登录时显示登录按钮 -->
        <el-button v-else type="text" @click="goToLogin">{{ t('user.login') }}</el-button>
      </div>
    </div>

    <el-main>
      <!-- 根据 activeIndex 显示不同的组件 -->
      <index v-if="activeIndex===null" />
      <router-view/>
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
import BackgroundIntro from "@/components/Background/BackgroundIntro.vue";
import AboutUs from "@/components/About/AboutUs.vue";
import { useI18n } from 'vue-i18n';

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();
const fontStore = useFontStore()
const { t, locale } = useI18n();

// 设置 activeIndex 初始值为 '2-1'，这样组件会默认显示 FilmLiterature
// Sync the activeIndex with the route path
const activeIndex = ref<string | null>(null);

// Watch for route changes and update activeIndex
watch(
    () => route.path,
    (newPath) => {
      console.log("newPath", newPath)
      if (newPath === '/') activeIndex.value = '1';
      else if (newPath === '/placeOfInterest') activeIndex.value = '3';
      else if (newPath === '/filmLiterature') activeIndex.value = '4';
      else if (newPath === '/food') activeIndex.value = '5';
      else if (newPath==='/index/background') activeIndex.value = '12'
      else if (newPath==='/index/about') activeIndex.value = '13'
      else activeIndex.value = null;
    }
);

// Set the initial activeIndex based on the current route
if (route.path === '/') activeIndex.value = '1';
else if (route.path === '/placeOfInterest') activeIndex.value = '3';
else if (route.path === '/filmLiterature') activeIndex.value = '4';
else if (route.path === '/food') activeIndex.value = '5'
else if (route.path==='/index/background') activeIndex.value = '12'
else if (route.path==='/index/about') activeIndex.value = '13'
else activeIndex.value = null;

// 当前语言显示
const currentLanguage = computed(() => {
  return locale.value === 'zh' ? '中文' : 'English';
});

// 处理语言切换
const handleLanguageChange = (command: string) => {
  locale.value = command;
  // 保存语言设置到本地存储
  localStorage.setItem('language', command);
    // 刷新页面
    window.location.reload();  // 刷新页面
};

// 获取问候语
const greeting = computed(() => {
  const hour = new Date().getHours();
  if (hour < 6) return '凌晨好！';
  if (hour < 9) return '早上好！';
  if (hour < 12) return '上午好！';
  if (hour < 14) return '中午好！';
  if (hour < 17) return '下午好！';
  if (hour < 19) return '傍晚好！';
  if (hour < 22) return '晚上好！';
  return '夜深了！';
});

// 处理菜单选择
// Handle menu item select and navigate accordingly
const handleSelect = (key: string, keyPath: string[]) => {
  activeIndex.value = key;

  switch (key) {
    case '1':
      router.push('/index'); // 首页
      break;
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
      router.push('/index/background');
      break;
    case '13':
      router.push('/index/about');
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

// 在组件挂载时初始化语言设置
onMounted(() => {
  // 从本地存储获取语言设置
  const savedLanguage = localStorage.getItem('language');
  if (savedLanguage) {
    locale.value = savedLanguage;
  }
  
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
  margin-left: 30px;  /* 增加与logo的距离 */
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
  margin-left: 0px;
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
