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
              :style="activeTab === tab ? {color: '#fff', backgroundColor: '#b71c1c', borderColor: '#b71c1c'} : {color: '#b71c1c'}"
              @click="selectTab(tab)"
          >
            {{ tab }}
          </el-button>
        </div>

        <!-- 搜索和管理按钮 -->
        <div class="action-section">
          <el-input
              v-model="searchQuery"
              placeholder="搜索标题"
              class="search-input"
              clearable
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <!-- 暂时注释清空历史按钮
          <el-button type="danger" plain @click="showClearConfirm" style="background-color: #fff; color: #b71c1c; border-color: #b71c1c; font-size: 12px;">
            <el-icon><Delete /></el-icon>
            清空历史
          </el-button>
          -->
          <!-- 暂时注释批量管理按钮
          <el-button type="primary" plain @click="toggleBatchMode" style="background-color: #fff; color: #b71c1c; border-color: #b71c1c; font-size: 12px;">
            <el-icon><Files /></el-icon>
            {{ isBatchMode ? '完成' : '批量管理' }}
          </el-button>
          -->
        </div>
      </div>
    </div>

    <!-- 时间线内容 -->
    <div class="timeline-container">
      <!-- 暂时注释批量操作区域
      <div v-if="isBatchMode" class="batch-actions">
        <el-button type="danger" @click="deleteSelected" :disabled="selectedItems.length === 0" 
          style="background-color: #b71c1c; border-color: #b71c1c;">
          删除选中项 ({{ selectedItems.length }})
        </el-button>
        <el-button @click="selectAll" style="color: #b71c1c; border-color: #b71c1c;">
          {{ isAllSelected ? '取消全选' : '全选' }}
        </el-button>
      </div>
      -->
      
      <el-timeline>
        <el-timeline-item
            v-for="(article, index) in paginatedArticles"
            :key="index"
            :timestamp="formatDate(article.history_time)"
            :type="getTimelineItemType(article.history_time)"
            placement="top"
        >
          <el-card class="timeline-card" shadow="hover">
            <div class="article-content">
              <!-- 暂时注释批量选择复选框 
              <el-checkbox 
                v-if="isBatchMode"
                v-model="article.isSelected"
                @change="updateSelectedItems"
                class="batch-checkbox"
              ></el-checkbox>
              -->
              
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
                  <el-button text :style="{color: '#b71c1c'}" @click="viewDetail(article)">
                    查看详情
                  </el-button>
                </div>
              </div>
            </div>
          </el-card>
        </el-timeline-item>
      </el-timeline>
      
      <!-- 分页控件 -->
      <div class="pagination-container">
        <el-pagination
          v-model:currentPage="currentPage"
          :page-size="pageSize"
          :total="filteredList.length"
          layout="prev, pager, next, jumper"
          @current-change="handlePageChange"
          background
          hide-on-single-page
        />
      </div>
    </div>
    
    <!-- 详情弹窗 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="selectedArticle?.name || '详情'"
      width="60%"
      :close-on-click-modal="true"
      :show-close="true"
      class="detail-dialog"
    >
      <div v-if="selectedArticle" class="article-detail">
        <div v-if="selectedArticle.img_url" class="detail-image">
          <img :src="selectedArticle.img_url" :alt="selectedArticle.name" />
        </div>
        <h3 class="detail-title">{{ selectedArticle.name }}</h3>
        <el-tag class="detail-tag" effect="light" :type="getTagType(selectedArticle.type)">
          {{ typeMapping[selectedArticle.type] || '其他' }}
        </el-tag>
        <p class="detail-time">浏览时间: {{ formatDate(selectedArticle.history_time) }}</p>
        <div class="detail-description">
          <h4>概述</h4>
          <div class="scrollable-content">
            <p>{{ formatDetailDescription(selectedArticle.history_describe) }}</p>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { getUserArticleList } from '@/apis/user';
import {computed, onMounted, ref} from "vue";
import { Clock, Search, Delete, Files, Timer } from '@element-plus/icons-vue';
import UserAPI from "@/api/user";
import { useRouter, useRoute } from 'vue-router';
import {useUserStore} from "@/stores/user.ts";
import { ElMessage, ElMessageBox } from 'element-plus';

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

// 详情弹窗相关
const detailDialogVisible = ref(false);
const selectedArticle = ref(null);

// 批量管理相关
const isBatchMode = ref(false);
const selectedItems = ref([]);
const isAllSelected = computed(() => {
  return paginatedArticles.value.length > 0 && 
         selectedItems.value.length === paginatedArticles.value.length;
});

// Methods
const selectTab = (tab) => {
  activeTab.value = tab;
  currentPage.value = 1; // 切换标签时重置为第一页
};

// 添加分页相关变量
const currentPage = ref(1);
const pageSize = ref(5);

// 格式化日期函数修改，更详细的时间格式
const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });
};

// 查看详情函数
const viewDetail = (article) => {
  selectedArticle.value = article;
  detailDialogVisible.value = true;
};

// 修改筛选逻辑，确保同一标签只显示最新的一条记录
const filteredList = computed(() => {
  const searchTerm = searchQuery.value.toLowerCase()
  
  // 首先根据标签页和搜索词筛选
  let filtered = articleList.value
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
  
  // 去重处理，只保留每个name的最新记录
  const uniqueArticles = [];
  const nameSet = new Set();
  
  filtered.forEach(article => {
    if (!nameSet.has(article.name)) {
      nameSet.add(article.name);
      uniqueArticles.push(article);
    }
  });
  
  return uniqueArticles;
})

// 计算当前页的数据
const paginatedArticles = computed(() => {
  const startIndex = (currentPage.value - 1) * pageSize.value;
  const endIndex = startIndex + pageSize.value;
  return filteredList.value.slice(startIndex, endIndex);
});

// 计算总页数
const totalPages = computed(() => {
  return Math.ceil(filteredList.value.length / pageSize.value);
});

// 页码变化处理函数
const handlePageChange = (newPage) => {
  currentPage.value = newPage;
};

// 时间线项目类型
const getTimelineItemType = (dateString) => {
  const now = new Date();
  const articleDate = new Date(dateString);
  const diffDays = Math.floor((now - articleDate) / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return 'primary';
  if (diffDays <= 7) return 'success';
  return 'info';
};

const truncateDescription = (desc) => {
  if (!desc) return '';
  
  // 如果描述长度超过限制，进行截断
  if (desc.length > 100) {
    // 截取前100个字符
    const truncated = desc.substring(0, 100);
    return truncated + '...';
  }
  
  // 即使不需要截断，也检查整段话的最后一个字符是否是标点符号
  const lastChar = desc[desc.length - 1];
  if (lastChar === '。' || lastChar === '？' || lastChar === '！' || 
      lastChar === '.' || lastChar === '?' || lastChar === '!' ||
      lastChar === '…' || lastChar === ';' || lastChar === '；') {
    // 如果已经以标点符号结尾，直接返回
    return desc;
  } else {
    // 如果不是以标点符号结尾，添加省略号
    return desc + '...';
  }
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

// 切换批量管理模式
const toggleBatchMode = () => {
  isBatchMode.value = !isBatchMode.value;
  if (!isBatchMode.value) {
    // 退出批量模式时清空选中项
    selectedItems.value = [];
    paginatedArticles.value.forEach(item => {
      item.isSelected = false;
    });
  }
};

// 更新选中项
const updateSelectedItems = () => {
  selectedItems.value = paginatedArticles.value
    .filter(item => item.isSelected)
    .filter(item => item.id !== undefined && item.id !== null && !isNaN(Number(item.id)));
  
  // 如果有无效ID的记录被选中，给出警告
  const invalidItems = paginatedArticles.value
    .filter(item => item.isSelected && (item.id === undefined || item.id === null || isNaN(Number(item.id))));
  
  if (invalidItems.length > 0) {
    console.warn('有选中项缺少有效ID，这些项将被忽略:', invalidItems);
  }
};

// 全选/取消全选
const selectAll = () => {
  const newState = !isAllSelected.value;
  paginatedArticles.value.forEach(item => {
    item.isSelected = newState;
  });
  updateSelectedItems();
};

// 删除选中项
const deleteSelected = async () => {
  if (selectedItems.value.length === 0) return;
  
  try {
    const userId = getUserId();
    if (!userId) {
      ElMessage.warning('请先登录');
      return;
    }
    
    // 收集所有要删除的项，按照是否有临时ID分为两组
    const selectedItemsData = selectedItems.value;
    
    // 处理前端本地删除
    // 从本地数据中移除被删除的项
    articleList.value = articleList.value.filter(item => 
      !selectedItemsData.some(selected => selected.id === item.id)
    );
    
    // 重置选中状态
    selectedItems.value = [];
    
    // 从服务器删除历史记录
    try {
      // 确保ID是数字类型
      const numericUserId = Number(userId);
      
      // 获取可能的历史时间，用于复合匹配
      const historyTimes = selectedItemsData.map(item => item.history_time);
      
      // 如果历史记录没有ID，则使用其他字段组合进行删除
      await UserAPI.DeleteUserHistoryByCompositeKey(numericUserId, {
        history_times: historyTimes
      });
      
      ElMessage.success('删除成功');
    } catch (error) {
      console.error('服务器删除失败，但本地删除已完成:', error);
      ElMessage.warning('部分删除可能未在服务器端完成，请刷新页面确认');
    }
    
    // 如果当前页没有数据了，且不是第一页，则回到上一页
    if (paginatedArticles.value.length === 0 && currentPage.value > 1) {
      currentPage.value--;
    }
  } catch (error) {
    console.error('删除失败:', error);
    ElMessage.error('删除失败，请重试');
  }
};

// 显示清空确认对话框
const showClearConfirm = () => {
  ElMessageBox.confirm(
    '确定要清空全部浏览历史记录吗？此操作不可恢复。',
    '警告',
    {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
      confirmButtonClass: 'el-button--danger',
      cancelButtonClass: 'el-button--info',
    }
  )
  .then(() => {
    clearAllHistory();
  })
  .catch(() => {
    ElMessage.info('已取消清空操作');
  });
};

// 清空所有历史
const clearAllHistory = async () => {
  try {
    const userId = getUserId();
    if (!userId) {
      ElMessage.warning('请先登录');
      return;
    }
    
    console.log('准备清空历史记录', { userId });
    
    // 确保ID是数字类型
    const numericUserId = Number(userId);
    
    // 先清空本地数据，确保UI立即响应
    articleList.value = [];
    
    // 调用清空历史API
    try {
      await UserAPI.ClearUserHistory(numericUserId);
      ElMessage.success('已清空全部历史记录');
    } catch (error) {
      console.error('服务器清空历史失败，但本地已清空:', error);
      ElMessage.warning('历史记录已在本地清空，但可能未在服务器端完成，请刷新页面确认');
    }
  } catch (error) {
    console.error('清空历史失败:', error);
    ElMessage.error('清空历史失败，请重试');
  }
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
  if (!userId) {
    ElMessage.warning('请先登录以查看浏览历史');
    return;
  }
  
  const numericUserId = Number(userId);
  
  UserAPI.GetUserHistory(numericUserId).then(res => {
    // 检查和处理响应数据，确保每个项目都有有效的ID
    if (Array.isArray(res)) {
      // 为每条记录添加自动生成的ID
      articleList.value = res.map((item, index) => {
        // 如果后端返回的数据中没有id字段，则使用index作为临时id
        const tempId = index + 1; // 使用索引+1作为临时ID
        
        if (item.id === undefined || item.id === null) {
          console.warn(`历史记录缺少ID字段，已添加临时ID ${tempId}:`, item);
        }
        
        return {
          ...item,
          id: item.id !== undefined && item.id !== null ? Number(item.id) : tempId
        };
      });
      
      console.log('获取历史记录成功，处理后数据:', articleList.value);
    } else {
      console.error('历史记录数据格式错误:', res);
      articleList.value = [];
    }
  }).catch(error => {
    console.error('获取历史记录失败:', error);
    ElMessage.error('获取历史记录失败，请重试');
    articleList.value = [];
  });
};
onMounted(() => {
  // 获取后端文章数据
  getHistory()

});

const formatDetailDescription = (desc) => {
  if (!desc) return '暂无描述';
  
  // 在详情弹窗中不需要截断文本，只检查结尾是否需要添加省略号
  const lastChar = desc[desc.length - 1];
  if (lastChar === '。' || lastChar === '？' || lastChar === '！' || 
      lastChar === '.' || lastChar === '?' || lastChar === '!' ||
      lastChar === '…' || lastChar === ';' || lastChar === '；') {
    // 如果已经以标点符号结尾，直接返回
    return desc;
  } else {
    // 如果不是以标点符号结尾，添加省略号
    return desc + '...';
  }
};

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

/* 添加分页样式 */
.pagination-container {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

:deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background-color: #b71c1c;
}

:deep(.el-pagination.is-background .el-pager li:not(.is-disabled):hover) {
  color: #b71c1c;
}

/* 添加详情弹窗样式 */
.detail-dialog {
  :deep(.el-dialog__header) {
    background-color: #b71c1c;
    padding: 20px;
    margin-right: 0;
  }
  
  :deep(.el-dialog__title) {
    color: white;
    font-weight: bold;
  }
  
  :deep(.el-dialog__headerbtn .el-dialog__close) {
    color: white;
  }
  
  :deep(.el-dialog__body) {
    padding: 20px;
  }
}

.article-detail {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.detail-image {
  text-align: center;
  margin-bottom: 20px;
  
  img {
    max-width: 100%;
    max-height: 300px;
    object-fit: contain;
    border-radius: 8px;
  }
}

.detail-title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
  color: #303133;
}

.detail-tag {
  align-self: flex-start;
}

.detail-time {
  color: #909399;
  font-size: 14px;
  margin: 0;
}

.detail-description {
  margin-top: 20px;
  
  h4 {
    margin-top: 0;
    margin-bottom: 10px;
    font-size: 18px;
    color: #303133;
  }
  
  .scrollable-content {
    max-height: 200px;
    overflow-y: auto;
    border: 1px solid #ebeef5;
    border-radius: 4px;
    padding: 10px;
    background-color: #f9f9f9;
    
    /* 自定义滚动条样式 */
    &::-webkit-scrollbar {
      width: 6px;
    }
    
    &::-webkit-scrollbar-track {
      background: #f1f1f1;
      border-radius: 3px;
    }
    
    &::-webkit-scrollbar-thumb {
      background: #b71c1c;
      border-radius: 3px;
    }
    
    &::-webkit-scrollbar-thumb:hover {
      background: #951616;
    }
    
    p {
      line-height: 1.6;
      color: #606266;
      margin: 0;
    }
  }
}

/* 修改分页样式 */
:deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background-color: #b71c1c;
}

:deep(.el-pagination.is-background .el-pager li:not(.is-disabled):hover) {
  color: #b71c1c;
}

:deep(.el-pagination .btn-prev:hover, .el-pagination .btn-next:hover) {
  color: #b71c1c;
}

:deep(.el-timeline-item__node--primary) {
  background-color: #b71c1c;
}

:deep(.el-timeline-item__node--success) {
  background-color: #51a73d;
}

.batch-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-bottom: 15px;
  padding: 10px;
  background-color: #f8f9fa;
  border-radius: 4px;
}

.batch-checkbox {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1;
}

.batch-checkbox :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: #b71c1c;
  border-color: #b71c1c;
}

.batch-checkbox :deep(.el-checkbox__input.is-focus .el-checkbox__inner) {
  border-color: #b71c1c;
}
</style>
