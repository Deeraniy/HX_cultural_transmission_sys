<script setup>
import {computed, ref} from 'vue';
import { Clock, Star } from '@element-plus/icons-vue';

// 假设这部分数据从后端获取

const activeTab = ref('全部');
const tabs = ['最近收藏', '最多播放'];
const showMoreTabs = ref(false);
const moreTabs=['全部','特色美食','非遗民俗','风景名胜','文学创作']
const videos = ref([
  {
    id: 1,
    title: '探索世界的美丽风景',
    description: '带你领略各地的自然风光和人文景观。',
    category: '风景名胜',
    image: 'https://via.placeholder.com/150',
    isFavorite: false,
  },
  {
    id: 2,
    title: '传统美食的魅力',
    description: '探索全球各地的美食文化。',
    category: '特色美食',
    image: 'https://via.placeholder.com/150',
    isFavorite: false,
  },
  // 更多视频数据...
]);
const filteredVideos = computed(() => {
  if (activeTab.value === '全部') {
    return videos.value;
  }
  return videos.value.filter(video => video.category === activeTab.value);
});
// 切换收藏状态
const toggleMoreTabs = () => {
  showMoreTabs.value = !showMoreTabs.value;
};
const toggleFavorite = (video) => {
  video.isFavorite = !video.isFavorite;
};
const  selectTab = (tab) => {
  activeTab.value = tab;
};
</script>

<template>
  <div>
    <div>
      <el-icon style="font-size: 20px;"><Star /></el-icon>
      <el-text class="mainTitle">视频收藏</el-text>
    </div>
    <div class="container" style="display: flex">
      <!-- Tabs Section -->
      <div class="tabs">
        <el-button
            v-for="(tab, index) in tabs"
            :key="index"
            :class="['tab', { active: activeTab === tab }]"
            @click="selectTab(tab)"
        >
          {{ tab }}
        </el-button>
        <el-button @click="toggleMoreTabs">更多筛选</el-button>
      </div>

      <!-- Search Section -->
      <div class="search-section">
        <input
            type="text"
            v-model="searchQuery"
            placeholder="搜索标题/up主昵称"
            class="search-input"
        />

      </div>
    </div>
    <div class="moreTabs" v-if="showMoreTabs">
      <el-button
          v-for="(tab, index) in moreTabs"
          :key="index"
          :class="['tab', { active: activeTab === tab }]"
          @click="selectTab(tab)"
      >
        {{ tab }}
      </el-button>
    </div>

    <!-- 收藏的视频列表 -->
    <div class="articleContent">
<!--      收藏的视频列表-->


        <div
            v-for="video in filteredVideos"
            :key="video.id"
            class="video-item"
        >
          <img :src="video.image" alt="视频封面" style="max-width: 200px" />
          <div class="video-info" style="width: 700px">
            <div class="video-title">{{ video.title }}</div>
            <div class="video-description">{{ video.description }}</div>
            <el-button>
              取消收藏
            </el-button>
          </div>

        </div>












    </div>
  </div>
</template>

<style scoped>
.mainTitle {
  margin-left: 30px;
  font-size: 18px;
  color: #000;
  font-weight: bolder;
}

.video-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 10px 0;
}

.video-title {
  font-size: 16px;
  color: #333;
}

.el-button {
  font-size: 14px;
}
</style>
