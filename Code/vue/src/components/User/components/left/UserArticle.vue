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
            v-for="(article, index) in virtualArticles"
            :key="index"
            :timestamp="article.timestamp"
            :type="getTimelineItemType(article.timestamp)"
        >
          <el-card class="timeline-card" shadow="hover">
            <div class="article-content">
              <h4 class="article-title">{{ article.title }}</h4>
              <p class="article-description">{{ article.description }}</p>
              <div class="article-footer">
                <span class="duration">
                  <el-icon><Timer /></el-icon>
                  观看时长: {{ article.viewDuration }}
                </span>
                <div class="action-buttons">
                  <el-button text type="primary">继续观看</el-button>
                  <el-button text type="danger">删除记录</el-button>
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
import { onMounted, ref } from "vue";
import { Clock, Search, Delete, Files, Timer } from '@element-plus/icons-vue';

const articleList = ref([]);
const activeTab = ref('全部');
const tabs = ['全部', '美食', '文学', '风景', '民俗'];
const searchQuery = ref('');

// Methods
const selectTab = (tab) => {
  activeTab.value = tab;
};

const clearSearch = () => {
  searchQuery.value = '';
};

const batchManage = () => {
  console.log('Batch management triggered');
};

// 根据时间戳返回不同的类型
const getTimelineItemType = (timestamp) => {
  if (timestamp === '今天') return 'primary'
  if (timestamp === '近一周') return 'success'
  return 'info'
}

onMounted(() => {
  // 获取后端文章数据
  getUserArticleList().then(res => {
    articleList.value = res.data.pageInfo.list;
    console.log(articleList.value)
  });
});

const virtualArticles = [
  {
    timestamp: '今天',
    title: '探索美食：亚洲街头小吃',
    description: '一起探索亚洲最具代表性的街头小吃，享受独特的美味和风味。',
    viewDuration: '5:30',
  },
  {
    timestamp: '近一周',
    title: '文学的力量：如何写出打动人心的故事',
    description: '通过一些经典的故事，分析如何构建感人的情节。',
    viewDuration: '6:45',
  },
  {
    timestamp: '近一周',
    title: '风景画的魅力：一探自然与艺术的结合',
    description: '了解风景画艺术背后的历史和技巧，感受大自然的美丽。',
    viewDuration: '4:15',
  },
  {
    timestamp: '一周前',
    title: '民俗探秘：揭秘中国传统节日的背后故事',
    description: '了解中国各大传统节日的历史与文化背景。',
    viewDuration: '7:00',
  },
  {
    timestamp: '一周前',
    title: '科技未来：人工智能的应用与挑战',
    description: '深入探讨人工智能技术如何改变我们的工作和生活。',
    viewDuration: '8:20',
  }
];
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
</style>
