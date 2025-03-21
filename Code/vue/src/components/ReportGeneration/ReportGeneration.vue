<template>
  <div class="report-generation">
    <el-card class="form-card">
      <div class="card-header">


<p class="subtitle">选择合适的标签和平台，生成专业的宣传内容</p>

</div>

      <el-form :model="report" ref="form" label-width="120px" class="form">

        <!-- 活动信息分组 -->
        <div class="form-group">
          <h3 class="group-title">活动信息（必填）</h3>
          <el-form-item
            label="活动名称"
            prop="eventName"
            :rules="[{ required: true, message: '请输入活动名称', trigger: 'blur' }]"
          >
            <el-input
              v-model="report.eventName"
              placeholder="例如：2024湖南非物质文化遗产展示周"
            />
          </el-form-item>
          <el-form-item
            label="活动属性"
            prop="eventType"
            :rules="[{ required: true, message: '请输入活动属性', trigger: 'blur' }]"
          >
            <el-input
              v-model="report.eventType"
              placeholder="例如：文化展览/非遗传承/民俗活动"
            />
          </el-form-item>
        </div>

        <!-- 宣传信息分组 -->
        <div class="form-group">
          <h3 class="group-title">宣传策略</h3>
          <el-form-item label="宣传倾向" prop="promotionTendency">
            <el-input
              v-model="report.promotionTendency"
              placeholder="例如：突出文化传承价值/提升青年参与感"
            />
          </el-form-item>
          <el-form-item label="宣传方式" prop="promotionMethod">
            <el-input
              v-model="report.promotionMethod"
              placeholder="例如：图文结合/短视频/现场直播"
            />
          </el-form-item>
        </div>
        <!-- 平台选择 -->
        <el-form-item label="宣传平台" prop="platform" :rules="[{ required: true, message: '请选择宣传平台', trigger: 'change' }]">
          <el-select v-model="report.platform" placeholder="请选择宣传平台" class="platform-select">
            <el-option-group label="社交种草平台">
              <el-option label="小红书" value="小红书" />
              <el-option label="微博" value="微博" />
            </el-option-group>
            <el-option-group label="短视频平台">
              <el-option label="抖音" value="抖音" />
              <el-option label="B站" value="B站" />
            </el-option-group>
            <el-option-group label="政务发布平台">
              <el-option label="政府平台" value="政府平台" />
              <el-option label="党建平台" value="党建平台" />
            </el-option-group>
            <el-option-group label="新闻媒体">
              <el-option label="新闻媒体" value="新闻媒体" />
            </el-option-group>
            <el-option-group label="其他平台">
              <el-option label="海外传播" value="海外传播" />
              <el-option label="线下物料" value="线下物料" />
              <el-option label="研学活动" value="研学活动" />
              <el-option label="商业合作" value="商业合作" />
              <el-option label="学术研究" value="学术研究" />
            </el-option-group>
          </el-select>
        </el-form-item>

        <!-- 可选标签展示 -->
        <el-form-item label="选择标签" prop="tags">
          <div class="tag-section">
            <div class="tag-header">
              <span class="tag-title">推荐标签</span>
              <span class="tag-count">已选择 {{ selectedTags.length }} 个标签</span>
            </div>

            <!-- 左侧推荐标签 -->
            <div class="tags-container">
              <div class="left-tags">
                <div v-if="userPreferences.length" class="preference-tags">
                  <div class="tags-row">
                    <el-tag
                      v-for="tag in visiblePreferences"
                      :key="tag"
                      :effect="isTagSelected(tag) ? 'dark' : 'plain'"
                      :class="['tag-item', { 'selected': isTagSelected(tag) }]"
                      @click="toggleTagSelection(tag)"
                    >
                      {{ tag }}
                    </el-tag>
                    <el-button
                      class="more-tags-btn"
                      type="text"
                      @click="showAllTags"
                    >
                      更多...
                    </el-button>
                  </div>
                </div>
                <div v-else class="no-preferences">
                  <span>您还没有偏好标签</span>
                  <el-button type="text" @click="showAllTags">查看所有标签</el-button>
                </div>
              </div>

              <!-- 右侧已选标签 -->
              <div class="selected-tags">
                <h4>已选标签</h4>
                <div class="selected-tags-container">
                  <el-tag
                    v-for="tag in selectedTags"
                    :key="tag"
                    closable
                    effect="dark"
                    @close="removeTag(tag)"
                  >
                    {{ tag }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </el-form-item>

        <!-- 标题输入 -->
        <el-form-item label="标题" prop="title">
          <el-input
            v-model="report.title"
            placeholder="例如：探寻千年瑶族文化，感受非遗魅力（选填，如果填写我们会着重分析您的标题）"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>

        <!-- 内容输入 -->
        <el-form-item label="内容" prop="content">
          <el-input
            type="textarea"
            v-model="report.content"
            placeholder="例如：本次活动将展示瑶族传统服饰制作工艺，并邀请非遗传承人现场展示...（选填，如果填写我们会着重分析您的内容）"
            rows="6"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
        <!-- 操作按钮 -->
        <el-form-item class="form-actions">
          <el-button type="primary" @click="generateReport" :loading="generating">
            {{ generating ? '生成中...' : '生成报道' }}
          </el-button>
          <el-button @click="resetForm">重置表单</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 新增：报告展示部分 -->
    <el-card class="report-card" v-if="generating || generatedReport">
      <div class="report-header">
        <h3>生成的报告</h3>
        <el-button type="primary" @click="copyReport" v-if="generatedReport">
          复制内容
        </el-button>
      </div>

      <!-- 加载状态 -->
      <div v-if="generating" class="loading-state">
        <el-skeleton :rows="10" animated />
        <div class="loading-text">
          <el-icon class="is-loading"><Loading /></el-icon>
          正在生成报告，请稍候...
        </div>
      </div>

      <!-- 报告内容 -->
      <div v-else-if="generatedReport" class="report-content">
        <div class="report-section">
          <div class="platform-info">
            <el-tag size="small" type="success">{{ report.platform }}</el-tag>
          </div>
          <div class="tags-info">
            <el-tag
              v-for="tag in selectedTags"
              :key="tag"
              size="small"
              effect="plain"
              class="report-tag"
            >
              {{ tag }}
            </el-tag>
          </div>
          <div class="content-text">
            {{ generatedReport }}
          </div>
        </div>
      </div>
    </el-card>

    <!-- 新增：独立的图片生成卡片 -->
    <el-card class="image-card" v-if="report.eventName && report.eventType">
      <div class="card-header">
        <h3>宣传图片生成</h3>
      </div>
      
      <div class="image-section">
        <el-button
          type="primary"
          @click="generateImage"
          :loading="generatingImage"
        >
          生成宣传图片
        </el-button>

        <div v-if="generatedImages.length" class="image-gallery">
          <div v-for="(image, index) in generatedImages" :key="index" class="image-item">
            <el-image
              :src="image"
              :preview-src-list="[image]"
              fit="contain"
              :initial-index="0"
            >
              <template #error>
                <div class="image-error">
                  <el-icon><i class="el-icon-picture-outline" /></el-icon>
                  <span>加载失败</span>
                </div>
              </template>
            </el-image>
            <div class="image-actions">
              <el-button type="text" @click="handleDownload(image)">
                下载图片
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 添加标签选择弹窗 -->
    <el-dialog
      v-model="tagDialogVisible"
      title="选择标签"
      width="50%"
      class="tag-dialog"
    >
      <div class="tag-search">
        <el-input
          v-model="tagSearchQuery"
          placeholder="搜索标签"
          prefix-icon="el-icon-search"
          clearable
        />
      </div>
      <div class="tag-groups">
        <!-- 按主题分组显示标签 -->
        <div v-for="(tags, theme) in groupedTags" :key="theme" class="tag-group">
          <h4 class="theme-title">{{ getThemeDisplayName(theme) }}</h4>
          <div class="theme-tags">
            <el-tag
              v-for="tag in filterTagsBySearch(tags)"
              :key="tag.id"
              :closable="isTagSelected(tag.name)"
              @close="removeTag(tag.name)"
              :effect="isTagSelected(tag.name) ? 'dark' : 'plain'"
              :class="['tag-item', { 'selected': isTagSelected(tag.name) }]"
              @click="toggleTagSelection(tag.name)"
            >
              {{ tag.name }}
            </el-tag>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<style scoped>
.report-generation {
  max-width: 900px;
  margin: 30px auto;
  padding: 0 40px;
}

.form-card {
  background: #fff;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.card-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px 0;
  border-bottom: 1px solid #f0f0f0;
  background-color: #fff;
}

.card-header h2 {
  color: #333;
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.subtitle {
  color: #666;
  margin-top: 8px;
  font-size: 14px;
}

.platform-select {
  width: 100%;
  :deep(.el-input__wrapper) {
    background-color: #fff !important;
  }
  :deep(.el-input__inner) {
    background-color: #fff !important;
  }
}

:deep(.el-select-dropdown__item-group__title) {
  background-color: #f5f7fa !important;
  padding: 10px 20px;
  font-size: 14px;
  font-weight: bold;
  color: #606266;
}

:deep(.el-select-dropdown__wrap) {
  background-color: #fff !important;
}

:deep(.el-select-dropdown) {
  background-color: #fff !important;
  border: 1px solid #e4e7ed;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

:deep(.el-select-dropdown__list) {
  background-color: #fff !important;
}

:deep(.el-select-dropdown__item) {
  background-color: #fff !important;
  &:hover {
    background-color: #f5f7fa !important;
  }
  &.selected {
    background-color: #f0f2f5 !important;
    color: #409eff;
  }
}

.tag-section {
  background: #f9f9f9;
  padding: 15px;
  border-radius: 8px;
}

.tag-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.tag-title {
  font-weight: bold;
  color: #333;
}

.tag-count {
  color: #666;
  font-size: 13px;
}

.available-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  cursor: pointer;
  transition: all 0.3s ease;
}

.tag-item:hover {
  transform: translateY(-2px);
}

.tag-item.selected {
  background-color: #409EFF;
  color: white;
}

.form-group {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.group-title {
  font-size: 16px;
  color: #333;
  margin-top: -10px;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
}

.form-actions {
  margin-top: 30px;
  text-align: center;
}

.preview-dialog :deep(.el-dialog) {
  border-radius: 15px;
}

.preview-content {
  padding: 20px;
}

.preview-header {
  margin-bottom: 20px;
}

.preview-header h3 {
  margin: 0 0 15px;
  color: #333;
}

.preview-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.preview-body {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
}

.preview-item {
  margin-bottom: 20px;
}

.preview-item h4 {
  color: #333;
  margin: 0 0 10px;
}

.content-text {
  line-height: 1.8;
  color: #444;
  white-space: pre-wrap;
}

.preview-meta {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 15px;
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.meta-item {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.meta-item .label {
  color: #666;
  font-size: 13px;
}

.dialog-footer {
  text-align: right;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .report-generation {
    margin: 15px auto;
    padding: 0 10px;
  }

  .preview-meta {
    grid-template-columns: 1fr;
  }
}

:deep(.el-input__inner) {
  background-color: #fff !important;
}

:deep(.el-textarea__inner) {
  background-color: #fff !important;
}

:deep(.el-input__inner::placeholder) {
  color: #909399;
  font-size: 14px;
}

:deep(.el-textarea__inner::placeholder) {
  color: #909399;
  font-size: 14px;
}

:deep(.el-form-item) {
  background-color: #fff;
}

:deep(.el-card__body) {
  background-color: #fff;
}

.preference-tags {
  margin-bottom: 16px;
}

.tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.more-tags-btn {
  font-size: 14px;
  color: #409EFF;
  padding: 0 12px;
}

.no-preferences {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #909399;
  margin-bottom: 16px;
}

.tag-dialog {
  .tag-search {
    margin-bottom: 20px;
  }

  .tag-groups {
    max-height: 60vh;
    overflow-y: auto;
    padding: 0 10px;
  }
}

.tag-item {
  cursor: pointer;
  transition: all 0.3s;

  &:hover {
    transform: translateY(-2px);
  }

  &.selected {
    background-color: #409EFF;
    color: white;
    border-color: #409EFF;
  }
}

.tag-groups {
  max-height: 60vh;
  overflow-y: auto;
  padding: 0 10px;
}

.tag-group {
  margin-bottom: 20px;
}

.theme-title {
  margin: 10px 0;
  padding-bottom: 8px;
  border-bottom: 1px solid #eee;
  color: #606266;
  font-size: 16px;
}

.theme-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}

.tags-container {
  display: flex;
  gap: 20px;
  margin-top: 10px;
}

.left-tags {
  flex: 2;
}

.selected-tags {
  flex: 1;
  border-left: 1px solid #eee;
  padding-left: 20px;
}

.selected-tags h4 {
  margin: 0 0 10px 0;
  color: #606266;
}

.selected-tags-container {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.selected-tags .el-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.preference-tags {
  margin-bottom: 10px;
}

.tags-row {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  align-items: center;
}

.tag-item {
  cursor: pointer;
  transition: all 0.3s;
}

.tag-item:hover {
  transform: translateY(-2px);
}

.tag-item.selected {
  background-color: #409EFF;
  color: white;
  border-color: #409EFF;
}

.report-card {
  margin-top: 30px;
  background: #fff;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.report-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 20px;
}

.loading-state {
  padding: 20px;
}

.loading-text {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
  color: #909399;
}

.report-content {
  padding: 20px;
}

.report-section {
  margin-bottom: 30px;
}

.platform-info {
  margin-bottom: 15px;
}

.tags-info {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 20px;
}

.content-text {
  white-space: pre-wrap;
  line-height: 1.8;
  color: #303133;
  font-size: 16px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.report-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.image-section {
  margin-top: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.image-gallery {
  margin-top: 20px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.image-item {
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.image-actions {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 10px;
  background: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
}

.el-image {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.image-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #909399;
}

.image-error .el-icon {
  font-size: 24px;
  margin-bottom: 8px;
}
</style>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import RecommendAPI from '@/api/recommend';
import TagsAPI from '@/api/tags';
import ReportAPI from '@/api/report';
import { Loading } from '@element-plus/icons-vue'

const availableTags = [
  "文化", "科技", "教育", "公益", "环境", "健康", "经济", "体育", "艺术", "创新",
  "社会", "旅游", "历史", "政治", "法律", "军事", "生态", "企业", "金融", "城市"
];

const report = ref({
  platform: '',
  title: '',
  content: '',
  tags: [],
  eventName: '',
  eventType: '',
  promotionTendency: '',
  promotionMethod: '',
});

const selectedTags = ref([]);
const generatedReport = ref(null);
const dialogVisible = ref(false);
const generating = ref(false);

// 用户偏好相关
const userPreferences = ref([]);
const tagDialogVisible = ref(false);
const tagSearchQuery = ref('');
const maxVisibleTags = 8;

const isTagSelected = (tag) => selectedTags.value.includes(tag);

const toggleTagSelection = (tag) => {
  if (isTagSelected(tag)) {
    removeTag(tag);
  } else {
    if (selectedTags.value.length < 5) {
      selectedTags.value.push(tag);
    } else {
      ElMessage.warning('最多只能选择5个标签');
    }
  }
};

const removeTag = (tag) => {
  const index = selectedTags.value.indexOf(tag);
  if (index !== -1) {
    selectedTags.value.splice(index, 1);
  }
};

const generateReport = async () => {
  generating.value = true;
  try {
    const response = await ReportAPI.generatePublicityReportAPI({
      platform: report.value.platform,
      title: report.value.title,
      content: report.value.content,
      tags: selectedTags.value,
      eventName: report.value.eventName,
      eventType: report.value.eventType,
      promotionTendency: report.value.promotionTendency,
      promotionMethod: report.value.promotionMethod
    });
    console.log('生成报告响应:', response);
    if (response.code === 200) {
      generatedReport.value = response.data.report;
      ElMessage.success('报告生成成功！');
    }
    console.log("省钱");
  } catch (error) {
    console.error('生成报告失败:', error);
    ElMessage.error('生成报告失败，请重试');
  } finally {
    generating.value = false;
  }
};

const resetForm = () => {
  Object.keys(report.value).forEach(key => report.value[key] = '');
  selectedTags.value = [];
  ElMessage.success('表单已重置');
};

const copyReport = () => {
  if (generatedReport.value) {
    navigator.clipboard.writeText(generatedReport.value)
      .then(() => {
        ElMessage.success('内容已复制到剪贴板');
      })
      .catch(() => {
        ElMessage.error('复制失败，请手动复制');
      });
  }
};

// 获取用户偏好标签
const fetchUserPreferences = async () => {
  try {
    const userId = localStorage.getItem('userId');
    if (!userId) {
      ElMessage.warning('请先登录');
      return;
    }

    // 使用 RecommendAPI 获取用户偏好
    const preferenceResponse = await RecommendAPI.getPerferenceAPI(userId);
    console.log('偏好数据响应:', preferenceResponse);

    if (preferenceResponse.status === "ok" && preferenceResponse.data) {
      const detailedPreferences = preferenceResponse.data.detailed_preferences || {};

      // 收集所有主题的标签ID
      const allTags = [];
      const tagIds = [];

      // 处理每个主题下的标签
      Object.entries(detailedPreferences).forEach(([theme, tags]) => {
        if (Array.isArray(tags)) {
          tags.forEach(tagInfo => {
            allTags.push({
              theme,
              tag_id: tagInfo.tag_id,
              score: tagInfo.score || 0
            });
            tagIds.push(tagInfo.tag_id);
          });
        }
      });

      console.log('收集到的所有标签:', allTags);

      // 获取标签详细信息
      const tagDetailsResponse = await RecommendAPI.getTagDetailAPI(tagIds);
      console.log('标签详细信息响应:', tagDetailsResponse);
      if (tagDetailsResponse.status === 'success' && tagDetailsResponse.tag_details) {
        // 创建标签ID到名称的映射
        const tagMap = new Map(
          tagDetailsResponse.tag_details.map(tag => [tag.tag_id, tag.tag_name])
        );

        // 按分数排序并过滤掉分数过低的标签
        const sortedTags = allTags
          .filter(tag => tag.score > 0.05)
          .sort((a, b) => b.score - a.score)
          .map(tag => ({
            ...tag,
            name: tagMap.get(tag.tag_id)
          }))
          .filter(tag => tag.name); // 过滤掉没有找到名称的标签

        console.log('排序后的标签:', sortedTags);

        // 使用标签名
        userPreferences.value = sortedTags.map(tag => tag.name);
        console.log('最终的偏好标签列表:', userPreferences.value);
      }
    }
  } catch (error) {
    console.error('获取用户偏好标签失败:', error);
    ElMessage.error('获取用户偏好标签失败');
  }
};

// 计算可见的偏好标签
const visiblePreferences = computed(() => {
  return userPreferences.value.slice(0, maxVisibleTags);
});

// 主题名称映射
const themeDisplayNames = {
  folk: '民俗文化',
  food: '饮食文化',
  spot: '文化景点',
  literature: '文学艺术',
  other: '其他'
};

// 获取主题显示名称
const getThemeDisplayName = (theme) => {
  return themeDisplayNames[theme] || theme;
};

// 按主题分组的标签
const groupedTags = ref({});

// 获取所有标签
const fetchAllTags = async () => {
  try {
    const response = await TagsAPI.getAllTagsAPI();
    if (response.code === 200 && Array.isArray(response.data)) {
      // 按主题分组标签
      const grouped = response.data.reduce((acc, tag) => {
        const theme = tag.theme_name || 'other'; // 使用 theme_name 而不是 theme
        if (!acc[theme]) {
          acc[theme] = [];
        }
        acc[theme].push({
          id: tag.id,
          name: tag.tag_name, // 使用 tag_name 而不是 name
          theme: theme,
          total_likes: tag.total_likes,
          total_clicks: tag.total_clicks
        });
        return acc;
      }, {});

      // 按照主题名称排序
      const orderedGroups = {};
      const themeOrder = ['folk', 'food', 'spot', 'literature'];

      // 先添加有序的主题
      themeOrder.forEach(theme => {
        if (grouped[theme]) {
          orderedGroups[theme] = grouped[theme];
        }
      });

      // 添加其他主题
      Object.keys(grouped)
        .filter(theme => !themeOrder.includes(theme))
        .forEach(theme => {
          orderedGroups[theme] = grouped[theme];
        });

      groupedTags.value = orderedGroups;
      console.log('分组后的标签:', groupedTags.value);
    }
  } catch (error) {
    console.error('获取所有标签失败:', error);
  }
};

// 根据搜索过滤标签
const filterTagsBySearch = (tags) => {
  if (!tagSearchQuery.value) return tags;
  return tags.filter(tag =>
    tag.name.toLowerCase().includes(tagSearchQuery.value.toLowerCase())
  );
};

// 显示所有标签
const showAllTags = () => {
  tagDialogVisible.value = true;
};

// 在组件挂载时获取所有标签
onMounted(() => {
  fetchUserPreferences();
  fetchAllTags(); // 添加获取所有标签的调用
});

// 在 setup 中添加
const generatingImage = ref(false);
const generatedImages = ref([]);

// 生成图片方法
const generateImage = async () => {
  if (!report.value.eventName || !report.value.eventType) {
    ElMessage.warning('请先填写活动名称和类型');
    return;
  }

  generatingImage.value = true;
  try {
    const response = await ReportAPI.generatePublicityImageAPI({
      eventName: report.value.eventName,
      eventType: report.value.eventType,
      tags: selectedTags.value,
      title: report.value.title,
      content: report.value.content
    });

    if (response.code === 200) {
      generatedImages.value = response.data.images;
      ElMessage.success('图片生成成功！');
    }
  } catch (error) {
    console.error('生成图片失败:', error);
    ElMessage.error('生成图片失败，请重试');
  } finally {
    generatingImage.value = false;
  }
};

// 简化的下载方法
const handleDownload = (imageUrl) => {
  try {
    // 创建一个隐藏的 a 标签
    const a = document.createElement('a');
    a.href = imageUrl;  // 直接使用图片 URL
    a.target = '_blank'; // 在新标签页打开
    a.rel = 'noopener noreferrer';
    
    // 设置文件名
    const fileName = imageUrl.split('/').pop() || 'image.png';
    a.download = fileName;
    
    // 触发点击
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  } catch (error) {
    console.error('下载失败:', error);
    ElMessage.error('下载失败，请重试');
  }
};
</script>
