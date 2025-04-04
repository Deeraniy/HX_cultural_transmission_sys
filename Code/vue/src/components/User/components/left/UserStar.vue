<script setup>
import {computed, onMounted, ref} from 'vue';
import { Star, Filter, Search, VideoPlay } from '@element-plus/icons-vue';
import UserAPI from "@/api/user";
import {useUserStore} from "@/stores/user.ts";

const userStore = useUserStore();
const starList = ref([]);
const searchQuery = ref('');
const activeTab = ref('全部');
const showMoreTabs = ref(false);

// 分类映射关系
const categoryMapping = {
  food: '特色美食',
  spot: '风景名胜',
  literature: '文学创作',
  folk: '非遗民俗'
};

// 标签配置
const tabs = ref(['最近收藏', '最多播放']);
const moreTabs = ref(['全部', ...Object.values(categoryMapping)]);

// 获取用户ID
const getUserId = () => {
  return userStore.userId || localStorage.getItem('userId') || null;
};

// 获取收藏数据
const getStar = () => {
  const userId = getUserId();
  if (!userId) return;

  UserAPI.GetUserStar(userId).then(res => {
    starList.value = res
        .filter(item => item.is_favorite) // 只显示收藏状态为true的
        .map(item => ({
          ...item,
          // 添加分类中文名称
          category: categoryMapping[item.theme_name] || '其他',
          // 生成示例图片URL（根据实际接口替换）
          image: `https://via.placeholder.com/150?text=${item.origin_id}`
        }));
  });
};

// 分类过滤 + 搜索过滤 + 排序
const filteredVideos = computed(() => {
  const searchTerm = searchQuery.value.toLowerCase();

  return starList.value
      .filter(item => {
        // 分类过滤
        const categoryMatch = activeTab.value === '全部' || item.category === activeTab.value;
        // 搜索过滤（搜索tag_name）
        const searchMatch = item.tag_name.toLowerCase().includes(searchTerm);

        return categoryMatch && searchMatch;
      })
      .sort((a, b) => {
        // 排序逻辑
        if (tabs.value[0] === '最近收藏') {
          // 按origin_id降序模拟时间排序（需要根据实际时间字段调整）
          return b.origin_id - a.origin_id;
        } else {
          // 按点击量排序
          return (b.total_clicks || 0) - (a.total_clicks || 0);
        }
      });
});

// 切换收藏状态
const toggleFavorite = async (item) => {
  try {
    // await UserAPI.UpdateFavorite({
    //   user_id: item.user_id,
    //   tag_id: item.tag_id,
    //   is_favorite: !item.is_favorite
    // });
    // 更新本地数据
    item.is_favorite = !item.is_favorite;
    starList.value = starList.value.filter(i => i.is_favorite);
  } catch (error) {
    console.error('更新收藏状态失败:', error);
  }
};

// 切换标签
const selectTab = (tab) => {
  activeTab.value = tab;
};

// 初始化
onMounted(getStar);
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
            @click="tabs = [tab, tabs[1 - index]]"
        >
          {{ tab }}
        </el-button>
        <el-button @click="showMoreTabs = !showMoreTabs" class="more-button">
          <el-icon><Filter /></el-icon>
          更多筛选
        </el-button>
      </div>

      <!-- 搜索框 -->
      <div class="search-section">
        <el-input
            v-model="searchQuery"
            placeholder="搜索标签名称"
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
          v-for="item in filteredVideos"
          :key="item.tag_id"
          class="video-card"
          shadow="hover"
      >
        <div class="video-content">
          <div class="video-thumbnail">
            <img :src="item.image" :alt="item.tag_name" />
            <div class="video-category">{{ item.category }}</div>
          </div>
          <div class="video-info">
            <h3 class="video-title">{{ item.tag_name }}</h3>
            <div class="video-stats">
              <el-tag size="small">播放: {{ item.total_clicks || 0 }}</el-tag>
              <el-tag size="small" type="success">点赞: {{ item.total_likes || 0 }}</el-tag>
            </div>
            <div class="video-actions">
              <el-button
                  type="danger"
                  plain
                  size="small"
                  @click="toggleFavorite(item)"
              >
                <el-icon><Star /></el-icon>
                {{ item.is_favorite ? '取消收藏' : '添加收藏' }}
              </el-button>
              <el-button type="primary" plain size="small">
                <el-icon><VideoPlay /></el-icon>
                查看详情
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
