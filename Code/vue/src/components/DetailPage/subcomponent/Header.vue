<template>
  <div class="button-container">
    <!-- 返回按钮和标题 -->
    <el-page-header @back="onBack" class="header" style="color: #fff8f0;font-size: 30px">
      <template #content>
        <span class="title" style="font-size: 30px">{{ title }}</span>
      </template>
    </el-page-header>

    <!-- 添加搜索框和下拉列表 -->
    <div class="header-actions">
      <!-- 下拉列表 -->
      <el-dropdown trigger="click" @command="handleCommand">
        <el-button class="custom-button">
          {{ selectedType || '文化类型' }} <el-icon class="el-icon--right"><arrow-down /></el-icon>
        </el-button>
        <template #dropdown>
          <el-dropdown-menu>
            <el-dropdown-item command="1">名胜古迹</el-dropdown-item>
            <el-dropdown-item command="2">影视文学</el-dropdown-item>
            <el-dropdown-item command="3">美食文化</el-dropdown-item>
            <el-dropdown-item command="4">非遗民俗</el-dropdown-item>
            <el-dropdown-item command="5">红色文化</el-dropdown-item>
          </el-dropdown-menu>
        </template>
      </el-dropdown>

      <!-- 搜索框部分 -->
      <el-input
        v-model="searchQuery"
        placeholder="请输入搜索内容"
        style="width: 200px; margin-left: 20px;"
        clearable
        @keyup.enter="handleSearch"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute, useRouter } from "vue-router";
import { ArrowDown } from '@element-plus/icons-vue';

const route = useRoute();
const router = useRouter();

const searchQuery = ref('');
const selectedType = ref('');
const title = ref('');

// 监听 URL 变化，自动更新标题
const updateTitleFromRoute = () => {
  title.value = decodeURIComponent(route.query.name || '默认标题');
};

onMounted(updateTitleFromRoute);
watch(() => route.query.name, updateTitleFromRoute);

// 处理下拉选择
const handleCommand = (command) => {
  const typeMap = {
    '1': '名胜古迹',
    '2': '影视文学',
    '3': '美食文化',
    '4': '非遗民俗',
    '5': '红色文化'
  };
  selectedType.value = typeMap[command];

  // 更新 URL 参数
  updateURL({ type: command });
};

// 处理搜索
const handleSearch = () => {
  if (searchQuery.value.trim()) {
    updateURL({ search: searchQuery.value.trim() });
    searchQuery.value = ''; // 清空搜索框
  }
};

// 更新 URL
const updateURL = (newParams) => {
  router.push({
    path: route.path,
    query: {
      ...route.query,
      ...newParams
    }
  });
};

const onBack = () => {
  router.go(-1);
};
</script>

<style scoped>
@import '@/assets/font/font.css';

.button-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
  background-image: url('@/assets/img_4.png');
  background-size: cover;
  background-position: center;
  border-bottom-left-radius: 30px;
  border-bottom-right-radius: 30px;
  position: relative;
}

.title {
  color: #fff8f0;
  font-family: 'HelveticaNeue', serif;
  font-size: 20px;
  font-weight: bold;
}

.header-actions {
  margin-right: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex: 1;
}

.custom-button {
  font-size: 14px !important;
  border: 2px solid #f1ce5b !important;
  padding: 5px 5px !important;
  border-radius: 5px !important;
  background: #fff8f0 !important;
  color: black !important;
  font-family: 'HelveticaNeue', serif !important;
  transition: all 0.3s !important;
  height: 35px !important;
  width: 120px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
}

.custom-button:hover {
  background: #FFC107 !important;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
  border-radius: 5px !important;
  border-color: #f1ce5b !important;
}
</style>
