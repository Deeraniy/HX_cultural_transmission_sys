<script setup>
import { useRouter } from 'vue-router';
import { ref } from 'vue';
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
</script>

<template>
  <div>
    <!-- 菜单组件 -->
    <el-menu class="card" background-color="#ffffff" text-color="#333" active-text-color="#409EFF" mode="vertical">
      <!-- 菜单项1: 浏览记录 -->
      <el-menu-item index="3" @click="jumpArticle">
        <el-icon>
          <Document />
        </el-icon>
        <template #title>浏览记录</template>
      </el-menu-item>

      <!-- 菜单项2: 收藏 -->
      <el-menu-item index="4" @click="jumpStar">
        <el-icon>
          <Star />
        </el-icon>
        <template #title>收藏</template>
      </el-menu-item>

      <!-- 菜单项3: 用户画像 -->
      <el-menu-item index="5" @click="jumpActivity">
        <el-icon>
          <DataAnalysis />
        </el-icon>
        <template #title>用户画像</template>
      </el-menu-item>

      <!-- 菜单项4: 关系上传 -->
      <el-menu-item index="6" @click="jumpUpload">
        <el-icon>
          <Upload />
        </el-icon>
        <template #title>关系上传</template>
      </el-menu-item>

      <!-- 菜单项5: 设置 -->
      <el-menu-item index="7" @click="jumpSet">
        <el-icon>
          <Setting />
        </el-icon>
        <template #title>设置</template>
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
}

.el-menu-item {
  padding: 10px 20px;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.el-menu-item:hover {
  background-color: #f4f4f4; /* 悬停背景色 */
}

.el-icon {
  font-size: 20px;
  margin-right: 15px;
}

/* 使菜单更具现代感，增加光滑的阴影效果 */
.el-menu {
  border: none;
  background-color: #fff;
  padding-top: 20px;
  padding-bottom: 20px;
}
</style>
