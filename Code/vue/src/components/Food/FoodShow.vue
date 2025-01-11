<template>
  <div class="whole">
    <div class="total">
      <!-- 左侧大标题 -->
      <div class="menu-title">
        <h2>美食文化分析</h2>
      </div>

      <!-- 菜单区域 -->
      <el-menu
          class="el-menu-demo"
          mode="horizontal"
          :ellipsis="false"
          :router="true"
      ><!--开启vue-router模式-->

        <!-- 首页菜单项 -->
        <el-menu-item index="/food/home">首页</el-menu-item> <!--index配置跳转路径-->
        <!-- 美食专区菜单项 -->
        <el-menu-item index="/food/detail">美食专区</el-menu-item>
        <!-- 传播效果分析菜单项 -->
        <el-menu-item index="/food/propagation">传播效果分析</el-menu-item>
      </el-menu>
    </div>

    <el-main>
      <router-view/>
    </el-main>
  </div>
</template>

<script lang="ts" setup>
// 这是传播效果分析组件
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
