<template>
  <div class="whole">
    <div class="total">
      <!-- 返回按钮 -->

      <h2 class="fixed-title">个性推荐界面</h2>
      <el-button class="back-btn" @click="goBack">| 返回</el-button>
      <el-menu
          :default-active="activeIndex"
          class="el-menu-demo"
          mode="horizontal"
          :ellipsis="false"
          @select="handleSelect"
      >
      </el-menu>
    </div>
    <el-main>
      <Recommend/>
    </el-main>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router';
import Recommend from "@/components/Recommend/RecommendPageMain.vue";

const activeIndex = ref('2')
const router = useRouter();

const handleSelect = (key: string, keyPath: string[]) => {
  console.log(key, keyPath)
};

// 返回上一页
const goBack = () => {
  // 直接导航到首页
  router.push('/index');
}
</script>

<style>
/* 返回按钮样式 */
.back-btn {
  font-family: 'HelveticaNeue', serif;
  background-color: transparent !important;
  color: #fff8f0 !important;
  border: none;
  font-size: 20px;
  padding: 10px 20px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  margin-right: 20px; /* 给按钮添加右边距 */
  margin-top: 10px;
}


.total {
  display: flex;
  align-items: center; /* 修改为center以便更好地对齐 */
  justify-content: space-between; /* 添加这个以确保标题和菜单的间距 */
  background-image: url('@/assets/img_4.png');
  background-size: cover;
  background-position: center;
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
  font-size: 34px;
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
  font-size: 18px;
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
</style>
