<template>
  <div class="whole">
    <div class="total">
      <!-- 左侧Logo -->
      <div class="logo">
        <img src="@/assets/111.png" alt="Logo" class="logo-image" />
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
        <el-sub-menu index="2" class="horizontal-submenu">
          <template #title>
            首页
          </template>
          <el-menu-item index="2-1">文学</el-menu-item>
          <el-menu-item index="2-2">古代文学</el-menu-item>
          <el-menu-item index="2-3">新媒体艺术</el-menu-item>
          <el-menu-item index="2-4">表演艺术</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="3">名胜古迹</el-menu-item>
        <el-menu-item index="4">影视文学</el-menu-item>
        <el-menu-item index="5">美食文化</el-menu-item>
        <el-menu-item index="6">非遗民俗</el-menu-item>
        <el-menu-item index="7">红色文化</el-menu-item>
        <el-menu-item index="8">情感分析</el-menu-item>
        <el-menu-item index="9">全球传播情况</el-menu-item>
        <el-sub-menu index="1">
          <template #title>
            <span class="work">工作台</span>
          </template>
          <el-menu-item index="1-1">item one</el-menu-item>
          <el-menu-item index="1-2">item two</el-menu-item>
          <el-menu-item index="1-3">item three</el-menu-item>
          <el-sub-menu index="1-4">
            <template #title>item four</template>
            <el-menu-item index="1-4-1">item one</el-menu-item>
            <el-menu-item index="1-4-2">item two</el-menu-item>
            <el-menu-item index="1-4-3">item three</el-menu-item>
          </el-sub-menu>
        </el-sub-menu>
      </el-menu>
      <!-- 右侧用户信息 -->
      <div class="user-info">
        <!-- 语言选择 -->
        <el-dropdown trigger="click" >
          <el-button type="primary">
            {{ language || '语言' }} <el-icon class="el-icon--right"><arrow-down /></el-icon>
          </el-button>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="1">中文</el-dropdown-item>
              <el-dropdown-item command="2">English</el-dropdown-item>
              <el-dropdown-item command="3">日本語</el-dropdown-item>
              <el-dropdown-item command="4">일본어</el-dropdown-item>
              <el-dropdown-item command="5">Japonais</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <!-- 用户头像 -->
        <div class="user-avatar">
          <img src="@/assets/Video1.jpg" alt="User Avatar" />
        </div>
      </div>
    </div>

    <el-main>
      <!-- 根据 activeIndex 显示不同的组件 -->
      <index v-if="activeIndex === '2-1'||activeIndex===null" />
      <PoemDisplay v-if="activeIndex === '2-2'" />
      <VideoDisplay v-if="activeIndex === '2-3'" />
      <ShowDisplay v-if="activeIndex === '2-4'" />
    </el-main>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import Index from "@/components/index.vue";
import PoemDisplay from "@/components/FilmLiterature/Literature/PoemDisplay.vue"; // 导入 PoemDisplay 组件
import VideoDisplay from "@/components/FilmLiterature/Literature/VideoDisplay.vue";
import ShowDisplay from "@/components/FilmLiterature/Literature/ShowDisplay.vue";
import {ArrowDown} from "@element-plus/icons-vue";
// 设置 activeIndex 初始值为 '2-1'，这样组件会默认显示 FilmLiterature
const activeIndex = ref<'2-1' | '2-2' | 'null' | string>(null);
const language = ref('中文');
// 处理菜单选择
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
  activeIndex.value = key;  // 更新选中的菜单项
};
</script>

<style>
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
  align-items: flex-end;
  background-image: url('@/assets/img_4.png');
  background-size: cover;
  background-position: center;
  padding-left: 20px;
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

.menu-title {
  transform: translateY(25px);
  font-family: 'HelveticaNeue', serif;
  font-size: 40px;
  color: #fff8f0;
  margin-right: 510px;
}

.el-menu-demo {
  margin-left: 50px;
  display: flex;
  justify-content: flex-end;
  background-color: transparent !important;
  box-shadow: none;
  padding-top: 0;
  padding-bottom: 0;
  border-bottom: none;
  border-radius: 0;
}

.el-menu-item {
  margin-right: 0px;
  background-color: #B71C1C64 !important;
  color: #fff8f0 !important;
  font-size: 25px;
  font-family: 'HelveticaNeue', serif !important;
  border-bottom: none !important;
}

.el-menu-item.is-active,
.el-menu-item:hover {
  color: #ffd700 !important;
  background-color: #B71C1C64 !important;
}

:deep(.el-sub-menu__title) {
  color: #fff8f0 !important;
  background-color: #B71C1C64 !important;
  font-family: 'HelveticaNeue', serif !important;
  font-size: 25px;
  padding: 0 10px;
  white-space: nowrap;
  overflow: hidden;
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
}/* 左侧Logo样式 */
.logo {
  flex: 0 0 40px;
}

.logo-image {
  width: 100%;
  height: auto;
  margin-bottom: 5px;
}

/* 右侧用户信息 */
.user-info {
  display: flex;
  align-items: center;
  margin-left: auto;
  margin-bottom: 8px;
}

.user-avatar img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;

}

.language-select {
  margin-right: 10px;
  width: 120px;
}
/* 修改下拉按钮样式 */
.el-dropdown .el-button {
  background-color: transparent;  /* 金色背景 */
  color: #fff8f0;
  border: none;
  font-family: 'HelveticaNeue', serif;  /* 修改字体 */
  font-size: 20px;
  margin-right: 10px;
}

.el-dropdown .el-button .el-icon--right {
  color: #fff8f0 !important;  /* 强制将下拉符号的颜色设置为黑色 */
}

.el-dropdown .el-button .el-icon--right {
  color: white;  /* 确保右侧箭头图标颜色也为白色 */
}

</style>
