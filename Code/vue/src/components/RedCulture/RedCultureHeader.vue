<template>
    <div class="whole">
      <div class="total">
        <h2 class="fixed-title">红色文化展示界面</h2>
        <el-button class="back-btn" @click="goBack">|返回</el-button>
        <el-menu
            :default-active="activeIndex"
            class="el-menu-demo"
            mode="horizontal"
            :ellipsis="false"
            @select="handleSelect"
        >
          <el-menu-item index="2">红色人物展示</el-menu-item>
          <el-menu-item index="3">智问智答</el-menu-item>
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
      </div>
      <el-main>
        <!-- 判断是否显示 Carousel 或 RedCultureMain -->
        <Carousel v-if="activeIndex === '2'" class="carousel-container" />
        <RedCultureMain v-if="activeIndex === '3'" class="red-culture-main" />
      </el-main>
    </div>
  </template>

  <script lang="ts" setup>
  import { ref } from 'vue'
  import RedCultureMain from './RedCultureMain.vue';
  import Carousel from "@/components/RedCulture/Carousel.vue";
  import router from '@/router'
  const goBack = () => {
    router.go(-1);  // 返回上一页
  }
  const activeIndex = ref('2')
  const handleSelect = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
    activeIndex.value = key;  // 更新 activeIndex
  }
  </script>

  <style>
  .back-btn {
    font-family: 'HelveticaNeue', serif;
    background-color: transparent !important;
    color: #fff8f0 !important;
    margin-bottom: 15px;
    border: none;
    font-size: 25px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-right: 720px; /* 给按钮添加右边距 */
    margin-top: 10px;
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
    min-width: 120px !important;
    padding: 0 15px !important;
  }

  .el-menu--popup .el-menu-item:hover,
  .el-menu .el-menu-item:hover {
    background: rgba(255, 255, 255, 0.3) !important;
    color: #ffd700 !important;
  }

  .el-popper__arrow {
    display: none !important;
  }

  /* 控制菜单宽度 */
  .el-menu--horizontal > .el-menu-item,
  .el-menu--horizontal > .el-sub-menu .el-sub-menu__title {
    min-width: auto !important;
    padding: 0 15px !important;
  }

  .el-menu--popup {
    min-width: 120px !important;
  }
  </style>

  <style scoped>
  @import '@/assets/font/font.css';

  .total {
    display: flex;
    align-items: center; /* 修改为center以便更好地对齐 */
    justify-content: space-between; /* 添加这个以确保标题和菜单的间距 */
    background-image: url('@/assets/img_4.png');
    background-size: cover;
    background-position: center;
    border-bottom-left-radius: 30px;
    border-bottom-right-radius: 30px;
    padding: 0 20px; /* 添加内边距 */
  }

  .whole {
    background-image: url('@/assets/img2.png');
    background-color: #fff8f0;
    background-size: cover;
    background-position: center;
  }

  .el-main {
    padding: 0;
  }

  .fixed-title {
    color: #fff8f0;
    font-family: 'HelveticaNeue', serif;
    font-size: 45px;
    margin: 0;
    white-space: nowrap; /* 防止标题换行 */
  }

  .el-menu-demo {
    display: flex;
    justify-content: flex-end;
    background-color: transparent !important;
    box-shadow: none;
    border: none;
    max-width: fit-content;
    margin-left: auto;
  }

  .el-menu-item {
    color: #fff8f0 !important;
    font-size: 20px;
    font-family: 'HelveticaNeue', serif !important;
    padding: 0 15px !important;
    min-width: auto !important;
  }

  .el-menu-item.is-active,
  .el-menu-item:hover {
    color: #ffd700 !important;
    background-color: rgba(255, 255, 255, 0.2) !important;
    border-bottom: 2px solid #ffd700;
  }

  :deep(.el-sub-menu__title) {
    color: #fff8f0 !important;
    background-color: transparent !important;
    font-family: 'HelveticaNeue', serif !important;
    padding: 0 15px !important;
    min-width: auto !important;
  }

  :deep(.el-sub-menu__title:hover),
  :deep(.el-sub-menu__title.is-active) {
    color: #ffd700 !important;
    background-color: rgba(255, 255, 255, 0.2) !important;
  }

  /* 控制子菜单宽度 */
  :deep(.el-menu--popup .el-menu-item) {
    min-width: 120px !important;
    padding: 0 15px !important;
  }
  /* 为了允许整体页面滚动，给 .whole 容器添加 overflow */
  .whole {
    background-image: url('@/assets/img2.png');
    background-color: #fff8f0;
    background-size: cover;
    background-position: center;
    min-height: 100vh; /* 确保页面至少填满整个视口 */
    overflow-y: auto; /* 允许纵向滚动 */
  }

  /* .total 的样式如果超出了屏幕，确保它的滚动也能启用 */
  .total {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background-image: url('@/assets/img_4.png');
    background-size: cover;
    background-position: center;
    border-bottom-left-radius: 30px;
    border-bottom-right-radius: 30px;
    padding: 0 20px;
    width: 100%; /* 确保宽度为 100% */
    box-sizing: border-box;
    overflow: hidden; /* 确保子元素不会溢出 */
    position: relative;
  }

  </style>
