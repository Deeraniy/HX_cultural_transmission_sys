<script setup>
import { computed, ref } from 'vue';
import { Star, Filter, Search, VideoPlay } from '@element-plus/icons-vue';

// 假设这部分数据从后端获取
const searchQuery = ref('');
const activeTab = ref('全部');
const tabs = ['最近收藏', '最多播放'];
const showMoreTabs = ref(false);
const moreTabs = ['全部', '特色美食', '非遗民俗', '风景名胜', '文学创作'];
const videos = ref([
  {
    id: 1,
    title: '探索世界的美丽风景',
    description: '带你领略各地的自然风光和人文景观。这是一段较长的描述文字，用来测试多行文本的显示效果。',
    category: '风景名胜',
    image: 'https://via.placeholder.com/150',
    isFavorite: true,
  },
  {
    id: 2,
    title: '传统美食的魅力',
    description: '探索全球各地的美食文化。了解不同地区的特色菜品和烹饪技巧。',
    category: '特色美食',
    image: 'https://via.placeholder.com/150',
    isFavorite: true,
  },
  {
    id: 3,
    title: '非遗文化传承',
    description: '探索中国传统非物质文化遗产，传承千年文明。',
    category: '非遗民俗',
    image: 'https://via.placeholder.com/150',
    isFavorite: true,
  },
]);

const filteredVideos = computed(() => {
  if (activeTab.value === '全部') {
    return videos.value;
  }
  return videos.value.filter(video => video.category === activeTab.value);
});

const toggleMoreTabs = () => {
  showMoreTabs.value = !showMoreTabs.value;
};

const toggleFavorite = (video) => {
  video.isFavorite = !video.isFavorite;
};

const selectTab = (tab) => {
  activeTab.value = tab;
};
</script>

<template>
  <div class="favorite-container">
    <!-- 标题区域 -->
    <div class="header-section">
      <div class="title-wrapper">
        <el-icon><Star /></el-icon>
        <span class="main-title">视频收藏</span>
      </div>
    </div>

    <!-- 控制面板 -->
    <div class="control-panel">
      <!-- 主要标签 -->
      <div class="main-tabs">
        <el-button
            v-for="(tab, index) in tabs"
            :key="index"
            :type="activeTab === tab ? 'primary' : 'default'"
            :class="['tab-button', { active: activeTab === tab }]"
            @click="selectTab(tab)"
        >
          {{ tab }}
        </el-button>
        <el-button @click="toggleMoreTabs" class="more-button">
          <el-icon><Filter /></el-icon>
          更多筛选
        </el-button>
      </div>

      <!-- 搜索框 -->
      <div class="search-section">
        <el-input
            v-model="searchQuery"
            placeholder="搜索标题/up主昵称"
            class="search-input"
            clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
    </div>

    <!-- 更多标签 -->
    <div v-if="showMoreTabs" class="more-tabs">
      <el-button
          v-for="(tab, index) in moreTabs"
          :key="index"
          :type="activeTab === tab ? 'primary' : 'default'"
          text
          :class="['more-tab-button', { active: activeTab === tab }]"
          @click="selectTab(tab)"
      >
        {{ tab }}
      </el-button>
    </div>

    <!-- 视频列表 -->
    <div class="video-list">
      <el-card
          v-for="video in filteredVideos"
          :key="video.id"
          class="video-card"
          shadow="hover"
      >
        <div class="video-content">
          <div class="video-thumbnail">
            <img :src="video.image" :alt="video.title" />
            <div class="video-category">{{ video.category }}</div>
          </div>
          <div class="video-info">
            <h3 class="video-title">{{ video.title }}</h3>
            <p class="video-description">{{ video.description }}</p>
            <div class="video-actions">
              <el-button type="danger" plain size="small" @click="toggleFavorite(video)">
                <el-icon><Star /></el-icon>
                取消收藏
              </el-button>
              <el-button type="primary" plain size="small">
                <el-icon><VideoPlay /></el-icon>
                观看视频
              </el-button>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.favorite-container {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.header-section {
  margin-bottom: 30px;
}

.title-wrapper {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #ebeef5;
}

.main-title {
  margin-left: 10px;
  font-size: 24px;
  font-weight: 600;
  color: #303133;
}

.control-panel {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 15px;
}

.main-tabs {
  display: flex;
  gap: 10px;
  align-items: center;
}

.search-section {
  width: 300px;
}

.more-tabs {
  background-color: #f8f9fa;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.video-list {
  display: grid;
  gap: 20px;
}

.video-card {
  border-radius: 12px;
  transition: all 0.3s ease;
}

.video-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.video-content {
  display: flex;
  gap: 20px;
}

.video-thumbnail {
  position: relative;
  width: 200px;
  height: 150px;
  overflow: hidden;
  border-radius: 8px;
}

.video-thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-category {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: rgba(0, 0, 0, 0.6);
  color: #fff;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.video-info {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.video-title {
  margin: 0 0 10px;
  font-size: 18px;
  color: #303133;
  font-weight: 500;
}

.video-description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 15px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-actions {
  margin-top: auto;
  display: flex;
  gap: 10px;
}

/* 响应式布局 */
@media screen and (max-width: 768px) {
  .control-panel {
    flex-direction: column;
    align-items: stretch;
  }

  .search-section {
    width: 100%;
  }

  .video-content {
    flex-direction: column;
  }

  .video-thumbnail {
    width: 100%;
  }

  .video-actions {
    flex-wrap: wrap;
  }
}

/* 动画效果 */
.more-tabs-enter-active,
.more-tabs-leave-active {
  transition: all 0.3s ease;
}

.more-tabs-enter-from,
.more-tabs-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>
