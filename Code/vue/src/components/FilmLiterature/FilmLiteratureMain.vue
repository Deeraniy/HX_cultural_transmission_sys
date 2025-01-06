<template>
  <div class="whole">
    <div class="total">
      <!-- 左侧大标题 -->
      <div class="menu-title">
        <h2>影视文学分析</h2>
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
        <el-sub-menu index="2">
          <template #title>
            作品总览
          </template>
          <el-menu-item index="2-1">子菜单项 1</el-menu-item>
          <el-menu-item index="2-2">子菜单项 2</el-menu-item>
          <el-menu-item index="2-3">子菜单项 3</el-menu-item>
        </el-sub-menu>
        <el-menu-item index="3">知识图谱</el-menu-item>
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
        </el-sub-menu>
      </el-menu>
    </div>
    <el-main>
      <FilmLiterature />
    </el-main>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import FilmLiterature from "@/components/FilmLiterature/Literature/FilmLiterature.vue";

const activeIndex = ref('2');
const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath);
};
</script>

<style scoped>
@import '@/assets/font/font.css';

/* 样式区域 */

.total {
  display: flex;
  align-items: flex-end; /* 对齐底部 */
  background-image: url('@/assets/img_4.png');
  background-size: cover;
  background-position: center;
  padding-left: 20px;
}

.whole {
  margin-top: -70px;
  background-image: url('@/assets/img2.png');
  background-color: #fff8f0;
  background-size: cover;
  background-position: center;
}

.el-main {
  padding: 0;
}

.menu-title {
  transform: translateY(25px); /* 向下移动 25px */
  font-family: 'HelveticaNeue', serif;
  font-size: 30px;
  color: #fff8f0;
  margin-right: 510px; /* 给标题和菜单项之间添加间距 */
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
  color: #fff8f0 !important;
  font-size: 20px;
  font-family: 'HelveticaNeue', serif !important;
  border-bottom: none !important;
}

.el-menu-item.is-active,
.el-menu-item:hover {
  color: #ffd700 !important;
  background-color: rgba(255, 255, 255, 0.2) !important;
}

/* 使用深度选择器进行样式修改 */

:deep .el-sub-menu__title {
  color: #fff8f0 !important;
  background-color: transparent !important;
  font-family: 'HelveticaNeue', serif !important;
  font-size: 20px;
  padding: 0 10px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  cursor: pointer; /* 使其看起来像可点击的元素 */
}

/* 去掉箭头 */
:deep .el-sub-menu__icon-arrow {
  display: none !important;
}

/* 子菜单弹出层的样式 */
:deep .el-sub-menu__popper {
  background-color: transparent !important; /* 子菜单弹出层背景透明 */
  display: flex !important;
  flex-direction: row !important;
  padding: 0 !important;
}

/* 子菜单项的背景设置为透明 */
:deep .el-sub-menu__popper .el-menu-item {
  background-color: rgba(255, 255, 255, 0.2) !important;
}

/* 悬浮效果 */
:deep .el-sub-menu__title:hover,
:deep .el-sub-menu__title.is-active {
  color: #ffd700 !important;
  background-color: rgba(255, 255, 255, 0.2) !important;
}

/* 子菜单展开时的样式 */
:deep .el-sub-menu {
  background-color: rgba(255, 255, 255, 0.2) !important; /* 确保整个子菜单背景透明 */
}

</style>
