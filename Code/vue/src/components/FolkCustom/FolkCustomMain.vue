<template>
  <div class="whole">
    <div class="total">
      <!-- 左侧大标题 -->
      <div class="menu-title">
        <h2>非遗民俗分析</h2>
      </div>
      <el-button class="back-btn" @click="goBack">|返回</el-button>
      <!-- 菜单区域 -->
      <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          :ellipsis="false"
          @select="handleSelect"
      ><!--开启vue-router模式-->

        <!-- 首页菜单项 -->
        <el-menu-item index="2">首页</el-menu-item> <!--index配置跳转路径-->
        <!-- 美食专区菜单项 -->
        <el-menu-item index="3">传播效果</el-menu-item>
        <!-- 传播效果分析菜单项 -->
        <!-- <el-menu-item index="4">情感分析</el-menu-item> -->
      </el-menu>
    </div>

    <el-main>
      <FolkCustom v-if="activeIndex === '2'" class="carousel-container" />
      <FolkCustomInfluence v-if="activeIndex === '3'" class="red-culture-main" />
      <FolkSentimentAnalyze v-if="activeIndex === '4'" class="red-culture-main" />
    </el-main>
  </div>
</template>

<script lang="ts" setup>
import FolkCustom from "@/components/FolkCustom/FolkCustom.vue";
import FolkCustomInfluence from "@/components/FolkCustom/FolkCustomInfluence.vue";
import FolkSentimentAnalyze from "@/components/FolkCustom/FolkSentimentAnalyze.vue";
import router from '@/router'
import Carousel from "@/components/RedCulture/Carousel.vue";
import RedCultureMain from "@/components/RedCulture/RedCultureMain.vue";
import { ref, onMounted, nextTick } from 'vue'
// 导入背景图片
import backgroundImage from '@/assets/img_4.png';

const goBack = () => {
  // 使用 router.back() 返回上一页
  router.back();
}

const activeIndex = ref('2')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
  activeIndex.value = key;  // 更新 activeIndex
}

// 在组件挂载时确保顶栏样式正确
onMounted(() => {
  nextTick(() => {
    // 强制刷新顶栏样式
    const totalElement = document.querySelector('.total');
    if (totalElement) {
      // 使用类型断言告诉 TypeScript 这是一个 HTMLElement
      const htmlElement = totalElement as HTMLElement;
      
      // 触发重排以刷新样式
      htmlElement.style.display = 'none';
      void htmlElement.offsetWidth;
      htmlElement.style.display = 'flex';
      
      // 确保背景图片正确加载 - 使用导入的图片
      htmlElement.style.backgroundImage = `url(${backgroundImage})`;
    }
  });
});
</script>

<style>

.back-btn {
  font-family: 'HelveticaNeue', serif;
  background-color: transparent !important;
  color: #fff8f0 !important;
  margin-bottom: 15px;
  border: none;
  font-size: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-right: 850px; /* 给按钮添加右边距 */
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
  margin-right: 180px; /* 为子菜单项之间添加间距 */
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
  margin-top: -55px;
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
  font-size: 24px;
  color: #fff8f0;
  margin-right: 30px;
  margin-bottom: 10px;
}

.el-menu-demo {
  margin-right: 0px;
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
  font-size: 20px;
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
  font-size: 20px;
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
}
</style>
