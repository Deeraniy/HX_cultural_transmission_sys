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
              <span class="tag-title">可选标签</span>
              <span class="tag-count">已选择 {{ selectedTags.length }} 个标签</span>
            </div>
            <div class="available-tags">
              <el-tag
                  v-for="(tag, index) in availableTags"
                  :key="index"
                  :closable="isTagSelected(tag)"
                  @close="removeTag(tag)"
                  :effect="isTagSelected(tag) ? 'dark' : 'plain'"
                  :class="['tag-item', { 'selected': isTagSelected(tag) }]"
                  @click="toggleTagSelection(tag)"
              >
                {{ tag }}
              </el-tag>
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

    <!-- 生成的报道预览弹窗 -->
    <el-dialog
        v-model="dialogVisible"
        title="生成的报道预览"
        width="60%"
        class="preview-dialog"
    >
      <div v-if="generatedReport" class="preview-content">
        <div class="preview-header">
          <h3>{{ generatedReport.title }}</h3>
          <div class="preview-tags">
            <el-tag v-for="tag in generatedReport.tags" :key="tag" size="small" effect="plain">
              {{ tag }}
            </el-tag>
          </div>
        </div>
        <div class="preview-body">
          <div class="preview-item">
            <h4>内容预览</h4>
            <p class="content-text">{{ generatedReport.content }}</p>
          </div>
          <div class="preview-meta">
            <div class="meta-item">
              <span class="label">活动名称：</span>
              <span>{{ generatedReport.eventName }}</span>
            </div>
            <div class="meta-item">
              <span class="label">活动属性：</span>
              <span>{{ generatedReport.eventType }}</span>
            </div>
            <div class="meta-item">
              <span class="label">宣传倾向：</span>
              <span>{{ generatedReport.promotionTendency }}</span>
            </div>
            <div class="meta-item">
              <span class="label">宣传方式：</span>
              <span>{{ generatedReport.promotionMethod }}</span>
            </div>
          </div>
        </div>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">关闭</el-button>
          <el-button type="primary" @click="copyReport">复制内容</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.report-generation {
  max-width: 900px;
  margin: 30px auto;
  padding: 0 140px;
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
</style>

<script>
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';

export default {
  setup() {
    const availableTags = [
      "文化", "科技", "教育", "公益", "环境", "健康", "经济", "体育", "艺术", "创新",
      "社会", "旅游", "历史", "政治", "法律", "军事", "生态", "企业", "金融", "城市"
    ];

    const report = reactive({
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
        // 这里添加生成报告的API调用
        await new Promise(resolve => setTimeout(resolve, 1500)); // 模拟API调用
        generatedReport.value = { ...report, tags: selectedTags.value };
        dialogVisible.value = true;
        ElMessage.success('报告生成成功！');
      } catch (error) {
        ElMessage.error('生成报告失败，请重试');
      } finally {
        generating.value = false;
      }
    };

    const resetForm = () => {
      Object.keys(report).forEach(key => report[key] = '');
      selectedTags.value = [];
      ElMessage.success('表单已重置');
    };

    const copyReport = () => {
      // 实现复制功能
      ElMessage.success('内容已复制到剪贴板');
    };

    return {
      availableTags,
      report,
      selectedTags,
      generatedReport,
      dialogVisible,
      generating,
      isTagSelected,
      toggleTagSelection,
      removeTag,
      generateReport,
      resetForm,
      copyReport
    };
  }
};
</script>
