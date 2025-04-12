<script setup>
import {computed, onMounted, ref} from 'vue';
import { Star, Filter, Search, VideoPlay } from '@element-plus/icons-vue';
import UserAPI from "@/api/user";
import {useUserStore} from "@/stores/user.ts";
import { ElMessage } from 'element-plus';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();
const userStore = useUserStore();
const starList = ref([]);
const searchQuery = ref('');
const activeTab = ref(t('user.star.categories.all'));
const showMoreTabs = ref(false);

// 分类映射关系
const categoryMapping = {
  food: t('user.star.categories.food'),
  spot: t('user.star.categories.spot'),
  literature: t('user.star.categories.literature'),
  folk: t('user.star.categories.folk')
};

// 标签配置
const tabs = ref([t('user.star.recentFavorites'), t('user.star.mostViewed')]);
const moreTabs = ref([t('user.star.categories.all'), ...Object.values(categoryMapping)]);

// 获取用户ID
const getUserId = () => {
  return userStore.userId || localStorage.getItem('userId') || null;
};

// 获取收藏数据
const getStar = () => {
  const userId = getUserId();
  if (!userId) return;

  UserAPI.GetUserStar(userId).then(res => {
    console.log("收藏数据原始响应:", res);
    
    const uniqueItemMap = new Map();
    
    res.filter(item => item.is_favorite).forEach(item => {
      const key = item.tag_id || (item.name + item.theme_name);
      if (!uniqueItemMap.has(key)) {
        uniqueItemMap.set(key, item);
      }
    });
    
    starList.value = Array.from(uniqueItemMap.values())
        .map(item => {
          console.log("处理单个收藏项:", item);
          
          let imageUrl = item.img_url;
          if (!imageUrl && item.theme_name === 'spot') {
            imageUrl = item.image_url || item.cover_img || '/placeholder.jpg';
          } else if (!imageUrl && item.theme_name === 'literature') {
            imageUrl = '/litcover.jpg';
          } else if (!imageUrl && item.theme_name === 'food') {
            imageUrl = '/foodcover.jpg';
          } else if (!imageUrl && item.theme_name === 'folk') {
            imageUrl = '/folkcover.jpg';
          }
          
          if (!imageUrl) {
            imageUrl = '/defaultcover.jpg';
          }
          
          return {
            ...item,
            category: categoryMapping[item.theme_name] || t('user.star.categories.other'),
            image: imageUrl
          };
        });
    
    console.log("处理后的收藏列表:", starList.value);
  }).catch(err => {
    console.error("获取收藏数据失败:", err);
  });
};

// 分类过滤 + 搜索过滤 + 排序
const filteredVideos = computed(() => {
  const searchTerm = searchQuery.value.toLowerCase();

  return starList.value
      .filter(item => {
        const categoryMatch = activeTab.value === t('user.star.categories.all') || item.category === activeTab.value;
        const searchMatch = item.tag_name.toLowerCase().includes(searchTerm);

        return categoryMatch && searchMatch;
      })
      .sort((a, b) => {
        if (tabs.value[0] === t('user.star.recentFavorites')) {
          return b.origin_id - a.origin_id;
        } else {
          return (b.total_clicks || 0) - (a.total_clicks || 0);
        }
      });
});

// 切换收藏状态
const toggleFavorite = async (item) => {
  try {
    await UserAPI.UpdateFavorite({
      user_id: getUserId(),
      tag_id: item.tag_id,
      is_favorite: 0
    });
    
    starList.value = starList.value.filter(i => i.tag_id !== item.tag_id);
    
    ElMessage.success(t('user.star.messages.removeSuccess'));
  } catch (error) {
    console.error('更新收藏状态失败:', error);
    ElMessage.error(t('user.star.messages.removeError'));
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
        <span class="main-title">{{ t('user.star.title') }}</span>
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
          {{ t('user.star.moreFilter') }}
        </el-button>
      </div>

      <!-- 搜索框 -->
      <div class="search-section">
        <el-input
            v-model="searchQuery"
            :placeholder="t('user.star.search')"
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
              <el-tag size="small">{{ t('user.star.stats.views') }}: {{ item.total_clicks || 0 }}</el-tag>
              <el-tag size="small" type="success">{{ t('user.star.stats.likes') }}: {{ item.total_likes || 0 }}</el-tag>
            </div>
            <div class="video-actions">
              <el-button
                  type="danger"
                  plain
                  size="small"
                  @click="toggleFavorite(item)"
              >
                <el-icon><Star /></el-icon>
                {{ item.is_favorite ? t('user.star.actions.removeFavorite') : t('user.star.actions.addFavorite') }}
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
