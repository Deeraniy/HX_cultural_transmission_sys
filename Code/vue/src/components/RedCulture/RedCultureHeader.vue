<template>
  <div class="whole">
    <div class="total">
      <div class="left-container">
        <h2 class="fixed-title">{{ $t('hong-se-wen-hua-zhan-shi-jie-mian') }}</h2>
        <el-button class="back-btn" @click="goBack">{{ $t('fan-hui-0') }}</el-button>
      </div>
      <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          :ellipsis="false"
          @select="handleSelect"
      >
        <el-menu-item index="2">{{ $t('hong-se-ren-wu-zhan-shi') }}</el-menu-item>
        <el-menu-item index="3">{{ $t('zhi-wen-zhi-da') }}</el-menu-item>
        <el-menu-item index="4">{{ $t('zhi-shi-tu-pu') }}</el-menu-item>
        
      </el-menu>
    </div>
    <el-main>
      <Carousel v-if="activeIndex === '2'" class="carousel-container" />
      <RedCultureMain v-if="activeIndex === '3'" class="red-culture-main" />
      <KnowledgeGraph v-if="activeIndex === '4'" class="knowledge-graph" />
    </el-main>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import RedCultureMain from './RedCultureMain.vue';
import KnowledgeGraph from './KnowledgeGraph.vue';
import Carousel from "@/components/RedCulture/Carousel.vue";
import router from '@/router'
const goBack = () => {
  router.go(-1);
}
const activeIndex = ref('2')
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
  activeIndex.value = key;
}
</script>

<style scoped>
@import '@/assets/font/font.css';

.total {
  display: flex;
  align-items: center;
  background-image: url('@/assets/img_4.png');
  background-size: cover;
  background-position: center;
  border-bottom-left-radius: 30px;
  border-bottom-right-radius: 30px;
  padding: 0 20px;
  width: 100%;
  box-sizing: border-box;
  position: relative;
}

/* 创建一个左侧容器来包含标题和返回按钮 */
.left-container {
  display: flex;
  align-items: center;
  flex: 1;
}

.whole {
  background-image: url('@/assets/img2.png');
  background-color: #fff8f0;
  background-size: cover;
  background-position: center;
  min-height: 97vh;
  overflow-y: auto;
}

.el-main {
  padding: 20px 0px 0px 0px;
}

.fixed-title {
  color: #fff8f0;
  font-family: 'HelveticaNeue', serif;
  font-size: 34px;
  margin: 0;
  white-space: nowrap;
  margin-right: 20px; /* 在标题和返回按钮之间添加间距 */
}

.back-btn {
  font-family: 'HelveticaNeue', serif;
  background-color: transparent !important;
  color: #fff8f0 !important;
  border: none;
  font-size: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  padding-top: 20px; /* 移除内边距 */
  height: auto; /* 允许按钮高度自适应 */
}

.el-menu-demo {

  display: flex;
  justify-content: flex-end;
  background-color: transparent !important;
  box-shadow: none;
  border: none;
  margin-left: -200px;
}

.el-menu-item, .el-sub-menu {
  order: 1;
}

.workbench {
  order: 2;
  margin-left: 20px;
}

.el-menu-item, .el-sub-menu__title {
  color: #fff8f0 !important;
  font-size: 18px;
  font-family: 'HelveticaNeue', serif !important;
  padding: 0 15px !important;
}

.el-menu-item.is-active, .el-menu-item:hover, .el-sub-menu__title:hover {
  color: #ffd700 !important;
  background-color: rgba(255, 255, 255, 0.2) !important;
  border-bottom: 2px solid #ffd700;
}
</style>
