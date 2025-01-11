<template>
  <div class="whole">
    <div class="total">
      <!-- 左侧大标题 -->
      <div class="menu-title">
        <h2>美食文化分析</h2>
      </div>

      <!-- 菜单区域 -->
      <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          :ellipsis="false"
          @select="handleSelect"
      >
        <!-- 首页菜单项 -->
        <el-menu-item index="1">首页</el-menu-item>
        <!-- 美食专区菜单项 -->
        <el-menu-item index="2">美食专区</el-menu-item>
        <!-- 传播效果分析菜单项 -->
        <el-menu-item index="3">传播效果分析</el-menu-item>
      </el-menu>
    </div>

    <el-main>
<!--       根据 activeIndex 显示不同的组件 -->
      <HomePageMain v-if="activeIndex === '1' || activeIndex === null" />
      <FoodPage v-if="activeIndex === '2'" />
      <PropagationPage v-if="activeIndex === '3'" />
    </el-main>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import HomePageMain from "@/components/Food/HomePageMain.vue";
import FoodPage from "@/components/Food/FoodPage.vue"; // 这是美食专区组件
import PropagationPage from "@/components/Food/PropagationPage.vue";
import FoodDetailPage from "@/components/Food/FoodDetailPage.vue";
// 这是传播效果分析组件

// 设置 activeIndex 初始值为 '1'，这样组件会默认显示首页
const activeIndex = ref('1')
import { useRouter } from 'vue-router';
const router = useRouter();
const navItems = [
  { index: '1', link: '/food' },
  { index: '2', link: '/food/detail' },
  { index: '3', link: '/food/propagation' },
];
// 处理菜单选择
const handleSelect = (key: string) => {
  activeIndex.value = key;
 /* router.push(navItems[Number(key) - 1].link)// 更新选中的菜单项*/
};
</script>

<style>


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
  transform: translateY(25px);
  font-family: 'HelveticaNeue', serif;
  font-size: 30px;
  color: #fff8f0;
  margin-right: 810px;
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
