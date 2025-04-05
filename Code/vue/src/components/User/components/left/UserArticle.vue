<template>
  <div class="history-container">
    <!-- 标题区域 -->
    <div class="header-section">
      <div class="title-wrapper">
        <el-icon><Clock /></el-icon>
        <span class="main-title">浏览记录</span>
      </div>

      <!-- 控制面板 -->
      <div class="control-panel">
        <!-- 标签页 -->
        <div class="tabs-section">
          <el-button
              v-for="(tab, index) in tabs"
              :key="index"
              :class="['tab-button', { active: activeTab === tab }]"
              :type="activeTab === tab ? 'primary' : 'info'"
              text
              @click="selectTab(tab)"
          >
            {{ tab }}
          </el-button>
        </div>

        <!-- 搜索和管理按钮 -->
        <div class="action-section">
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
          <el-button type="danger" plain @click="clearSearch">
            <el-icon><Delete /></el-icon>
            清空历史
          </el-button>
          <el-button type="primary" plain @click="batchManage">
            <el-icon><Files /></el-icon>
            批量管理
          </el-button>
        </div>
      </div>
    </div>

    <!-- 时间线内容 -->
    <div class="timeline-container">
      <el-timeline>
        <el-timeline-item
            v-for="(article, index) in filteredList"
            :key="index"
            :timestamp="formatDate(article.history_time)"
            :type="getTimelineItemType(article.history_time)"
            placement="top"
        >
          <el-card class="timeline-card" shadow="hover">
            <div class="article-content">
              <!-- 添加图片展示 -->
              <div v-if="article.img_url" class="cover-image">
                <img :src="article.img_url" :alt="article.name" />
              </div>
              <h4 class="article-title">{{ article.name }}</h4>
              <p v-if="article.history_describe" class="article-description">
                {{ truncateDescription(article.history_describe) }}
              </p>
              <div class="article-footer">
                <el-tag effect="light" :type="getTagType(article.type)">
                  {{ typeMapping[article.type] || '其他' }}
                </el-tag>
                <div class="action-buttons">
                  <el-button text type="primary" @click="viewDetail(article)">
                    查看详情
                  </el-button>
                </div>
              </div>
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
    </div>
  </div>
</template>

<script setup>
import { getUserArticleList } from '@/apis/user';
import {computed, onMounted, ref} from "vue";
import { Clock, Search, Delete, Files, Timer } from '@element-plus/icons-vue';
import UserAPI from "@/api/user";
import { useRouter, useRoute } from 'vue-router';
import {useUserStore} from "@/stores/user.ts";
const articleList = ref([]);
const activeTab = ref('全部');
const tabs = ['全部', '美食', '文学', '风景', '民俗'];
const searchQuery = ref('');
const typeMapping = {
  literature: '文学',
  folk: '民俗',
  placeOfInterest: '风景',
  food: '美食'
};
// Methods
const selectTab = (tab) => {
  activeTab.value = tab;
};
const filteredList = computed(() => {
  const searchTerm = searchQuery.value.toLowerCase()

  return articleList.value
      .filter(article => {
        // 标签页过滤
        const tabMatch = activeTab.value === '全部' ||
            article.type === Object.keys(typeMapping).find(key => typeMapping[key] === activeTab.value)

        // 搜索过滤（标题和作者）
        const searchMatch = searchTerm === '' ||
            article.name.toLowerCase().includes(searchTerm) ||
            (article.author && article.author.toLowerCase().includes(searchTerm))

        return tabMatch && searchMatch
      })
      .sort((a, b) => new Date(b.history_time) - new Date(a.history_time))
})
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
};
const getTimelineItemType = (dateString) => {
  const now = new Date();
  const articleDate = new Date(dateString);
  const diffDays = Math.floor((now - articleDate) / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return 'primary';
  if (diffDays <= 7) return 'success';
  return 'info';
};
const truncateDescription = (desc) => {
  return desc.length > 100 ? desc.substring(0, 100) + '...' : desc;
};

// 新增标签类型映射
const getTagType = (type) => {
  const typeColors = {
    literature: 'warning',
    folk: 'success',
    placeOfInterest: '',
    food: 'danger'
  };
  return typeColors[type] || 'info';
};
const clearSearch = () => {
  searchQuery.value = '';
};

const batchManage = () => {
  console.log('Batch management triggered');
};

// 根据时间戳返回不同的类型
const userStore = useUserStore();

const getUserId = () => {
  // 首先从 userStore 中获取
  if (userStore.userId) {
    return userStore.userId;
  }

  // 如果 userStore 中没有，尝试从 localStorage 获取
  const userId = localStorage.getItem('userId');
  if (userId) {
    return userId;
  }

  // 如果都没有，返回 null
  console.warn('User ID is missing');
  return null;
};
const getHistory = () => {
  // 获取后端文章数据
  const userId = getUserId();
  UserAPI.GetUserHistory(userId).then(res => {
    articleList.value = res;
    console.log('获取历史记录成功')
    console.log(articleList.value)
  });
}
onMounted(() => {
  // 获取后端文章数据
  getHistory()

});

</script>

<style scoped>
.history-container {
  padding: 20px;
  max-width: 800px;
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
  border-bottom: 2px solid #ebeef5;
}

.main-title {
  margin-left: 10px;
  font-size: 22px;
  font-weight: 600;
  color: #303133;
}

.control-panel {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.tabs-section {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.tab-button {
  font-size: 14px;
  padding: 8px 16px;
}

.tab-button.active {
  font-weight: 600;
}

.action-section {
  display: flex;
  gap: 10px;
  align-items: center;
}

.search-input {
  width: 300px;
}

.timeline-container {
  padding: 20px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.timeline-card {
  margin-bottom: 10px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.timeline-card:hover {
  transform: translateY(-2px);
}

.article-content {
  padding: 10px;
}

.article-title {
  margin: 0 0 10px 0;
  font-size: 16px;
  color: #303133;
}

.article-description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 15px;
  line-height: 1.5;
}

.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid #ebeef5;
}

.duration {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #909399;
  font-size: 13px;
}

.action-buttons {
  display: flex;
  gap: 10px;
}

:deep(.el-timeline-item__node) {
  background-color: var(--el-color-primary);
}

:deep(.el-timeline-item__timestamp) {
  color: #909399;
  font-weight: 600;
}

/* 添加响应式布局 */
@media screen and (max-width: 768px) {
  .history-container {
    padding: 10px;
  }

  .action-section {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    width: 100%;
  }

  .timeline-container {
    padding: 10px;
  }
}
.cover-image {
  margin-bottom: 15px;

  img {
    width: 100%;
    max-height: 200px;
    object-fit: cover;
    border-radius: 4px;
  }
}

/* 调整底部布局 */
.article-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 15px;
  padding-top: 12px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .article-footer {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>
