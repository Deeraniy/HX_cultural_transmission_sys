<template>
  <div class="whole">
    <div class="total">
      <!-- 左侧大标题 -->
      <div class="menu-title">
        <h2>{{ $t('ying-shi-wen-xue-fen-xi') }}</h2>
      </div>
      <el-button :class="['back-btn', { 'right-position': locale === 'en' }]" @click="goBack">{{ $t('fan-hui-0') }}</el-button>

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
            {{ $t('zuo-pin-zong-lan') }}
          </template>
          <el-menu-item index="2-1">{{ $t('detail.literature.types.literature') }}</el-menu-item>
          <el-menu-item index="2-2">{{ $t('gu-dai-wen-xue') }}</el-menu-item>
          <el-menu-item index="2-3">{{ $t('detail.literature.types.newMedia') }}</el-menu-item>
          <el-menu-item index="2-4">{{ $t('detail.literature.types.performance') }}</el-menu-item>
        </el-sub-menu>
        <!-- <el-menu-item index="3">知识图谱</el-menu-item>
        <el-menu-item index="4">沉浸式故事体验</el-menu-item>
        <el-menu-item index="5">全球传播情况</el-menu-item>
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
        </el-sub-menu> -->
      </el-menu>
    </div>

    <el-main>
      <!-- 根据 activeIndex 显示不同的组件 -->
      <FilmLiterature v-if="activeIndex === '2-1'||activeIndex===null" />
      <PoemDisplay v-if="activeIndex === '2-2'" />
      <VideoDisplay v-if="activeIndex === '2-3'" />
      <ShowDisplay v-if="activeIndex === '2-4'" />
    </el-main>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import router from '@/router'
import FilmLiterature from "@/components/FilmLiterature/Literature/FilmLiterature.vue";
import PoemDisplay from "@/components/FilmLiterature/Literature/PoemDisplay.vue"; // 导入 PoemDisplay 组件
import VideoDisplay from "@/components/FilmLiterature/Literature/VideoDisplay.vue";
import ShowDisplay from "@/components/FilmLiterature/Literature/ShowDisplay.vue";
import { useI18n } from 'vue-i18n';

const { locale } = useI18n(); // 获取当前语言
const route = useRoute();
const activeIndex = ref(route.query.activeIndex || '2-1');

// 处理菜单选择
const handleSelect = (key: string) => {
  activeIndex.value = key;
};
const goBack = () => {
  router.go(-1);  // 返回上一页
}
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
.back-btn {
  font-family: 'HelveticaNeue', serif;
  background-color: transparent !important;
  color: #fff8f0 !important;
  margin-bottom: 15px;
  border: none;
  font-size: 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-right: 900px; /* 给按钮添加右边距 */
}

/* 英文模式下的右对齐 */
.right-position {
  margin-right: 500px; /* 右边距，保证按钮离右边有一定间距 */
}
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
  margin-right: 0px;
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
