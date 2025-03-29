<script setup>
import { useRouter, useRoute } from 'vue-router';
import { ref, onMounted, watch } from 'vue';
// 导入图标
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
  ChatLineSquare,
  Flag,
  DataAnalysis,
  Star,
  Upload
} from '@element-plus/icons-vue';

// 使用路由
const router = useRouter();
const route = useRoute();

// 监听按钮状态
const createArticle = () => {
  router.push({ path: '/editor' });
};

const jumpEmpty = () => {
  router.push({ path: '/empty' });
};

const jumpUserHome = () => {
  router.push({ path: '/userHome' });
};

const jumpTags = () => {
  router.push({ path: '/userHome/tags' });
};

const jumpSet = () => {
  router.push({ path: '/userHome/profile' });
};

const jumpProfile = () => {
  router.push({ path: '/userHome/profile' });
};

const jumpArticle = () => {
  router.push({ path: '/userHome/article' });
};

const jumpUpload = () => {
  router.push({ path: '/userHome/upload' });
};

const jumpStar = () => {
  router.push({ path: '/userHome/star' });
};

const jumpActivity = () => {
  router.push({ path: '/userHome/activity' });
};

const activeIndex = ref('');

// 根据当前路由设置激活的菜单项
const setActiveMenu = () => {
  const path = route.path;
  switch (path) {
    case '/userHome/article':
      activeIndex.value = '3';
      break;
    case '/userHome/star':
      activeIndex.value = '4';
      break;
    case '/userHome/activity':
      activeIndex.value = '5';
      break;
    case '/userHome/upload':
      activeIndex.value = '6';
      break;
    case '/userHome/profile':
      activeIndex.value = '7';
      break;
    default:
      activeIndex.value = '';
  }
};

// 监听路由变化
watch(() => route.path, () => {
  setActiveMenu();
}, { immediate: true });

onMounted(() => {
  setActiveMenu();
});

// 修改菜单点击处理函数
const handleMenuClick = (index) => {
  switch (index) {
    case '3':
      router.push('/userHome/article');
      break;
    case '4':
      router.push('/userHome/star');
      break;
    case '5':
      router.push('/userHome/activity');
      break;
    case '6':
      router.push('/userHome/upload');
      break;
    case '7':
      router.push('/userHome/profile');
      break;
  }
};
</script>

<template>
  <div>
    <!-- 菜单组件 -->
    <el-menu 
      class="card" 
      background-color="#ffffff"
      :default-active="activeIndex"
      :router="true"
      mode="vertical"
      @select="handleMenuClick"
    >
      <!-- 菜单项1: 浏览记录 -->
      <el-menu-item index="3">
        <el-icon>
          <Document />
        </el-icon>
        <span class="menu-text">浏览记录</span>
      </el-menu-item>

      <!-- 菜单项2: 收藏 -->
      <el-menu-item index="4">
        <el-icon>
          <Star />
        </el-icon>
        <span class="menu-text">收藏</span>
      </el-menu-item>

      <!-- 菜单项3: 用户画像 -->
      <el-menu-item index="5">
        <el-icon>
          <DataAnalysis />
        </el-icon>
        <span class="menu-text">用户画像</span>
      </el-menu-item>

      <!-- 菜单项4: 关系上传 -->
      <el-menu-item index="6">
        <el-icon>
          <Upload />
        </el-icon>
        <span class="menu-text">关系上传</span>
      </el-menu-item>

      <!-- 菜单项5: 设置 -->
      <el-menu-item index="7">
        <el-icon>
          <Setting />
        </el-icon>
        <span class="menu-text">设置</span>
      </el-menu-item>
    </el-menu>
  </div>
</template>

<style scoped>
.card {
  width: 220px;
  min-height: 200px;
  border-radius: 10px;
  box-shadow: 0 2px 15px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}

/* 修改菜单项样式 */
:deep(.el-menu-item) {
  background-color: #fff;
  color: #000000 !important;
  padding: 10px 20px;
  font-size: 16px;
  transition: all 0.3s ease;
  
  /* 确保所有子元素都继承颜色 */
  * {
    color: #000000 !important;
    transition: all 0.3s ease;
  }
}

/* 菜单文字样式 */
.menu-text {
  color: #000000 !important;
  font-weight: 500;
}

/* 图标样式 */
:deep(.el-icon) {
  color: #000000 !important;
  font-size: 20px;
  margin-right: 15px;
}

/* 悬停效果 */
:deep(.el-menu-item:hover) {
  background-color: #f4f4f4 !important;
  
  * {
    color: #b71c1c !important;
  }
}

/* 选中状态 */
:deep(.el-menu-item.is-active) {
  background-color: #ecf5ff !important;
  
  * {
    color: #b71c1c !important;
  }
  &:not(:hover) {
    background-color: transparent !important;
    * {
      color: #000000 !important;
    }
  }
}

/* 使菜单更具现代感，增加光滑的阴影效果 */
.el-menu {
  border: none;
  background-color: #fff !important;
  padding-top: 20px;
  padding-bottom: 20px;
  border-radius: 10px;
}

/* 确保容器有白色背景 */
.el-menu-vertical-demo {
  background-color: #fff;
}
</style>
