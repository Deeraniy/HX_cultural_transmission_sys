<template>
  <div class="report-generation">
    <el-card class="form-card">
      <div class="card-header">
        <p class="subtitle">
          {{ locale === 'en' ? 'Select appropriate tags and platform to generate specialized propaganda content' : '选择合适的标签和平台生成专业的宣传内容' }}
        </p>
      </div>

      <el-form :model="report" ref="form" label-width="120px" class="form">

        <!-- 活动信息分组 -->
        <div class="form-group">
          <h3 class="group-title">
            {{ locale === 'en' ? 'Activity Information (Required)' : '活动信息（必填）' }}
          </h3>
          <el-form-item
            :label="locale === 'en' ? 'Event Name' : '活动名称'"
            prop="eventName"
            :rules="[{ required: true, message: locale === 'en' ? 'Please enter the event name' : '请输入活动名称', trigger: 'blur' }]"
          >
            <el-input
              v-model="report.eventName"
              placeholder=""
            />
          </el-form-item>
          <el-form-item
            :label="locale === 'en' ? 'Event Type' : '活动属性'"
            prop="eventType"
            :rules="[{ required: true, message: locale === 'en' ? 'Please enter the event type' : '请输入活动属性', trigger: 'blur' }]"
          >
            <el-input
              v-model="report.eventType"
              :placeholder="locale === 'en' ? 'e.g. Cultural Exhibition/Intangible Cultural Heritage Inheritance/Folk Activities' : '例如：文化展览/非遗传承/民俗活动'"
            />
          </el-form-item>
        </div>

        <!-- 宣传信息分组 -->
        <div class="form-group">
          <h3 class="group-title">
            {{ locale === 'en' ? 'Promotion Strategy' : '宣传策略' }}
          </h3>
          <el-form-item :label="locale === 'en' ? 'Promotion Tendency' : '宣传倾向'" prop="promotionTendency">
            <el-input
              v-model="report.promotionTendency"
              :placeholder="locale === 'en' ? 'e.g. Highlighting cultural heritage value / Increasing youth participation' : '例如：突出文化传承价值/提升青年参与感'"
            />
          </el-form-item>
          <el-form-item :label="locale === 'en' ? 'Promotion Method' : '宣传方式'" prop="promotionMethod">
            <el-input
              v-model="report.promotionMethod"
              :placeholder="locale === 'en' ? 'e.g. Combination of images and text / Short videos / Live broadcasting' : '例如：图文结合/短视频/现场直播'"
            />
          </el-form-item>
        </div>

        <!-- 平台选择 -->
        <el-form-item :label="locale === 'en' ? 'Promotion Platform' : '宣传平台'" prop="platform" :rules="[{ required: true, message: locale === 'en' ? 'Please select a promotion platform' : '请选择宣传平台', trigger: 'change' }]">
          <el-select v-model="report.platform" :placeholder="locale === 'en' ? 'Please select a promotion platform' : '请选择宣传平台'" class="platform-select">
            <el-option-group :label="locale === 'en' ? 'Social Media Platforms' : '社交种草平台'">
              <el-option :label="locale === 'en' ? 'Xiaohongshu' : '小红书'" value="小红书" />
              <el-option :label="locale === 'en' ? 'Weibo' : '微博'" value="微博" />
            </el-option-group>
            <el-option-group :label="locale === 'en' ? 'Short Video Platforms' : '短视频平台'">
              <el-option :label="locale === 'en' ? 'Douyin' : '抖音'" value="抖音" />
              <el-option :label="locale === 'en' ? 'Bilibili' : 'B站'" value="B站" />
            </el-option-group>
            <el-option-group :label="locale === 'en' ? 'Government Release Platforms' : '政务发布平台'">
              <el-option :label="locale === 'en' ? 'Government Platform' : '政府平台'" value="政府平台" />
              <el-option :label="locale === 'en' ? 'Party Building Platform' : '党建平台'" value="党建平台" />
            </el-option-group>
            <el-option-group :label="locale === 'en' ? 'News Media' : '新闻媒体'">
              <el-option :label="locale === 'en' ? 'News Media' : '新闻媒体'" value="新闻媒体" />
            </el-option-group>
            <el-option-group :label="locale === 'en' ? 'Other Platforms' : '其他平台'">
              <el-option :label="locale === 'en' ? 'Overseas Propagation' : '海外传播'" value="海外传播" />
              <el-option :label="locale === 'en' ? 'Offline Materials' : '线下物料'" value="线下物料" />
              <el-option :label="locale === 'en' ? 'Research Activities' : '研学活动'" value="研学活动" />
              <el-option :label="locale === 'en' ? 'Commercial Cooperation' : '商业合作'" value="商业合作" />
              <el-option :label="locale === 'en' ? 'Academic Research' : '学术研究'" value="学术研究" />
            </el-option-group>
          </el-select>
        </el-form-item>

        <!-- 可选标签展示 -->
        <el-form-item :label="locale === 'en' ? 'Select Tags' : '选择标签'" prop="tags">
          <div class="tag-section">
            <div class="tag-header">
              <span class="tag-title">{{ locale === 'en' ? 'Recommended Tags' : '推荐标签' }}</span>
              <span class="tag-count">{{ $t('yi-xuan-ze-selectedtagslength-ge-biao-qian', [selectedTags.length]) }}</span>
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
                    >
  {{ getName(tag) }} <!-- 这里使用getName来获取标签的翻译 -->
      </el-tag>
                    <el-button
                      class="more-tags-btn"
                      type="text"
                      @click="showAllTags"
                    >
                      {{ $t('geng-duo-0') }} </el-button>
                  </div>
                </div>
                <div v-else class="no-preferences">
                  <span>{{ $t('nin-huan-mei-you-pian-hao-biao-qian-0') }}</span>
                  <el-button type="text" @click="showAllTags">{{ $t('cha-kan-suo-you-biao-qian-0') }}</el-button>
                </div>
              </div>

              <!-- 右侧已选标签 -->
              <div class="selected-tags">
                <h4>{{ locale === 'en' ? 'Selected Tags' : '已选标签' }}</h4>
                <div class="selected-tags-container">
                  <el-tag
                    v-for="tag in selectedTags"
                    :key="tag"
                    closable
                    effect="dark"
                    @close="removeTag(tag)"
                  >
                  >
  {{ getName(tag) }} <!-- 这里使用getName来获取标签的翻译 -->

                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </el-form-item>

        <!-- 标题输入 -->
        <el-form-item :label="locale === 'en' ? 'Title' : '标题'" prop="title">
          <el-input
            v-model="report.title"
            :placeholder="locale === 'en' ? 'For example: Explore thousand-year-old Yao culture, feel the charm of intangible cultural heritage (optional, if provided, we will focus on analyzing your title)' : '例如：探寻千年瑶族文化，感受非遗魅力（选填，如果填写我们会着重分析您的标题）'"
            maxlength="50"
            show-word-limit
          />
        </el-form-item>

        <!-- 内容输入 -->
        <el-form-item :label="locale === 'en' ? 'Content' : '内容'" prop="content">
          <el-input
            type="textarea"
            v-model="report.content"
            :placeholder="locale === 'en' ? 'For example: This event will showcase the traditional costume-making process of the Yao ethnic group, and invite intangible cultural heritage inheritors to demonstrate on-site...' : '例如：本次活动将展示瑶族传统服饰制作工艺，并邀请非遗传承人现场展示...（选填，如果填写我们会着重分析您的内容）'"
            rows="6"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <!-- 操作按钮 -->
        <el-form-item class="form-actions">
          <el-button type="primary" @click="generateReport" :loading="generating">
            {{ generating ? locale === 'en' ? 'Generating...' : '生成报道' : locale === 'en' ? 'Generate Report' : '生成报道' }}
          </el-button>
          <el-button @click="resetForm">{{ $t('zhong-zhi-biao-dan') }}</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 修改报告卡片部分 -->
    <el-card class="report-card" v-if="generating || generatedReport">
      <div class="report-header">
        <h3>{{ locale === 'en' ? 'Propagation Report' : '宣传报告' }}</h3>
        <el-button type="primary" @click="copyReport" v-if="generatedReport">
          {{ locale === 'en' ? 'Copy Content' : '复制内容' }}
        </el-button>
      </div>

      <!-- 加载状态 -->
      <div v-if="generating" class="loading-state">
        <el-skeleton :rows="10" animated />
        <div class="loading-text">
          <el-icon class="is-loading"><Loading /></el-icon>
          {{ locale === 'en' ? 'Generating report, please wait...' : '正在生成报告，请稍等...' }}
        </div>
      </div>

      <!-- 报告内容 -->
      <div v-else-if="generatedReport" class="report-content">
        <div class="report-section">
          <div class="platform-info">
  <el-tag size="large" effect="dark" type="success">{{ getPlatformName(report.platform) }}</el-tag>
</div>

          <div class="tags-info">
            <el-tag
              v-for="tag in selectedTags"
              :key="tag"
              size="small"
              effect="plain"
              class="report-tag"
            >
              {{ getName(tag) }} <!-- 这里使用getName来获取标签的翻译 -->
            </el-tag>
          </div>
          <div class="content-text markdown-body" v-html="renderedMarkdown"></div>
        </div>
      </div>
    </el-card>

    <!-- 修改图片生成卡片 -->
    <el-card class="image-card" v-if="report.eventName && report.eventType">
      <div class="card-header">
        <h3>{{ locale === 'en' ? 'Generate Propaganda Image' : '生成宣传图片' }}</h3>
        <el-button
          type="primary"
          @click="generateImage"
          :loading="generatingImage"
          :icon="Picture"
        >
          {{ locale === 'en' ? 'Generate Propaganda Image' : '生成宣传图片' }}
        </el-button>
      </div>

      <div class="image-section" v-if="generatedImages.length">
        <div class="image-gallery">
          <div v-for="(image, index) in generatedImages" :key="index" class="image-item">
            <div class="image-wrapper">
              <el-image
                :src="image"
                :preview-src-list="generatedImages"
                :initial-index="index"
                fit="contain"
                class="gallery-image"
              >
                <template #placeholder>
                  <div class="image-loading">
                    <el-icon class="is-loading"><Loading /></el-icon>
                    <span>{{ locale === 'en' ? 'Loading...(This may take 2-3 minutes)' : '加载中...（这可能需要2-3分钟时间）' }}</span>
                  </div>
                </template>
                <template #error>
                  <div class="image-error">
                    <el-icon><Picture /></el-icon>
                    <span>{{ locale === 'en' ? 'Loading failed' : '加载失败' }}</span>
                  </div>
                </template>
              </el-image>
            </div>
            <div class="image-actions">
              <el-button
                type="primary"
                @click="handleDownload(image)"
                class="download-btn"
              >
                <el-icon><Download /></el-icon>
                {{ locale === 'en' ? 'Download Image' : '下载图片' }}
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </el-card>

    <!-- 添加标签选择弹窗 -->
    <el-dialog
      v-model="tagDialogVisible"
      :title="locale === 'en' ? 'Select Tags' : '选择标签'"
      width="50%"
      class="tag-dialog"
    >
      <div class="tag-search">
        <el-input
          v-model="tagSearchQuery"
          :placeholder="locale === 'en' ? 'Search tags' : '搜索标签'"
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
              {{ getName(tag.name) }} <!-- 这里使用getName来获取标签的翻译 -->
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
    color: #b71c1c;
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
  background-color: #b71c1c;
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
  white-space: pre-wrap;
  line-height: 1.6;
  color: #303133;
  padding: 16px;
  font-size: 15px;
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
  color: #b71c1c;
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
    background-color: #b71c1c;
    color: white;
    border-color: #b71c1c;
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
  background-color: #b71c1c;
  color: white;
  border-color: #b71c1c;
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
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.report-header h3 {
  margin: 0;
  font-size: 20px;
  color: #303133;
}

.report-content {
  padding: 20px;
}

.platform-info {
  margin-bottom: 20px;
}

.tags-info {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.report-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.image-card {
  margin-top: 30px;
  background: #fff;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.card-header h3 {
  margin: 0;
  font-size: 20px;
  color: #303133;
}

.image-section {
  padding: 20px;
  display: flex;
  justify-content: center;
}

.image-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  max-width: 1200px;
  width: 100%;
  padding: 20px;
}

.image-item {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  aspect-ratio: 1;
  background: #f5f7fa;
  display: flex;
  flex-direction: column;
}

.image-wrapper {
  flex: 1;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.gallery-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.image-loading {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
}

.image-loading .el-icon {
  font-size: 24px;
  margin-bottom: 8px;
}

.image-error {
  height: 280px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  background: #f5f7fa;
}

.image-error .el-icon {
  font-size: 48px;
  margin-bottom: 10px;
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

.image-actions {
  padding: 12px;
  background: #fff;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: center;
}

.download-btn {
  display: flex;
  align-items: center;
  gap: 5px;
}

.download-btn .el-icon {
  margin-right: 4px;
}

/* 修改 markdown 样式，确保标题和内容对齐 */
.markdown-body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}

.markdown-body :deep(h1),
.markdown-body :deep(h2),
.markdown-body :deep(h3) {
  position: relative;
  display: flex;
  align-items: baseline;
  margin: 8px 0 4px 0;
  line-height: 1.4;
}

.markdown-body :deep(h1) {
  font-size: 1.4em;
  padding-bottom: 4px;
  border-bottom: 1px solid #eaecef;
}

.markdown-body :deep(h2) {
  font-size: 1.2em;
  padding-bottom: 4px;
  border-bottom: 1px solid #eaecef;
}

.markdown-body :deep(h3) {
  font-size: 1.1em;
}

/* 调整列表样式 */
.markdown-body :deep(ul),
.markdown-body :deep(ol) {
  padding-left: 24px;
  margin: 4px 0;
}

.markdown-body :deep(li) {
  margin: 2px 0;
  line-height: 1.6;
  position: relative;
}

/* 调整段落样式 */
.markdown-body :deep(p) {
  margin: 4px 0;
  line-height: 1.6;
}

/* 确保内容对齐 */
.content-text {
  white-space: pre-wrap;
  line-height: 1.6;
  color: #303133;
  padding: 16px;
  font-size: 15px;
}

/* 调整标题和内容的间距 */
.markdown-body :deep(h1) + p,
.markdown-body :deep(h2) + p,
.markdown-body :deep(h3) + p {
  margin-top: 4px;
}

/* 修改标签样式 */
:deep(.el-tag) {
  &.el-tag--dark {
    background-color: #b71c1c !important;
    border-color: #b71c1c !important;
  }
  
  &.el-tag--plain {
    color: #b71c1c !important;
    border-color: #b71c1c !important;
    
    &:hover {
      background-color: #b71c1c !important;
      color: white !important;
    }
  }
}

/* 修改按钮样式 */
:deep(.el-button--primary) {
  background-color: #b71c1c !important;
  border-color: #b71c1c !important;
  
  &:hover, &:focus {
    background-color: #d32f2f !important;
    border-color: #d32f2f !important;
  }
  
  &:active {
    background-color: #7f0c07 !important;
    border-color: #7f0c07 !important;
  }
}

/* 修改文字按钮样式 */
:deep(.el-button--text) {
  color: #b71c1c !important;
  
  &:hover, &:focus {
    color: #d32f2f !important;
  }
  
  &:active {
    color: #7f0c07 !important;
  }
}

/* 修改选中标签的背景色 */
.tag-item.selected {
  background-color: #b71c1c !important;
  border-color: #b71c1c !important;
  color: white !important;
}

/* 修改导航按钮样式 */
.navigate-button {
  background-color: #b71c1c !important;
  
  &:hover {
    background-color: #d32f2f !important;
  }
  
  &:active {
    background-color: #7f0c07 !important;
  }
}

/* 修改更多按钮样式 */
.more-button {
  color: #b71c1c !important;
  
  &:hover {
    color: #d32f2f !important;
  }
}

/* 修改输入框选中时的边框颜色 */
:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #b71c1c !important;
}

/* 修改文本域选中时的边框颜色 */
:deep(.el-textarea__inner:focus) {
  box-shadow: 0 0 0 1px #b71c1c !important;
}

/* 修改普通按钮（包括重置表单按钮）的样式 */
:deep(.el-button) {
  &:not(.el-button--primary):not(.el-button--text) {
    &:hover, &:focus {
      color: #b71c1c !important;
      border-color: #b71c1c !important;
      background-color: #fff !important;
    }
    
    &:active {
      color: #7f0c07 !important;
      border-color: #7f0c07 !important;
      background-color: #fff !important;
    }
  }
}

/* 修改下拉选择框选中时的边框颜色 */
:deep(.el-select .el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px #b71c1c !important;
}

/* 修改下拉选项选中和悬停的颜色 */
:deep(.el-select-dropdown__item.selected) {
  color: #b71c1c !important;
  background-color: #fde9e9 !important;
}

:deep(.el-select-dropdown__item.hover) {
  background-color: #fde9e9 !important;
}
</style>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import MarkdownIt from 'markdown-it';
import RecommendAPI from '@/api/recommend';
import TagsAPI from '@/api/tags';
import ReportAPI from '@/api/report';
import { Loading, Document, Picture, Download } from '@element-plus/icons-vue'
import cultureElements from '@/json/culture_elements_translated.json'; // 假设包含菜名的翻译数据
// 获取名称的翻译
const getName = (name) => {
  const element = cultureElements.find(item => item.title === name);
  return locale.value === 'en' && element?.['title-en'] ? 
    element['title-en'] : 
    name;
};
import { useI18n } from 'vue-i18n';
const {t,locale} = useI18n();
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
      const warningMessage = locale.value === 'en' ? 'You can only select up to 5 tags' : '最多只能选择5个标签';
      ElMessage.warning(warningMessage);
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
    // 判断当前语言，选择不同的 API 调用
    const apiMethod = locale.value === 'en' ? ReportAPI.generatePublicityENReportAPI : ReportAPI.generatePublicityReportAPI;

    // 调用相应的 API
    const response = await apiMethod({
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
      const successMessage = locale.value === 'en' ? 'Report generated successfully!' : '报告生成成功！';
      ElMessage.success(successMessage);
    }
    console.log("省钱");
  } catch (error) {
    console.error('生成报告失败:', error);
    const errorMessage = locale.value === 'en' ? 'Failed to generate report, please try again.' : '生成报告失败，请重试';
    ElMessage.error(errorMessage);
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
        const successMessage = locale.value === 'en' ? 'Content copied to clipboard' : '内容已复制到剪贴板';
        ElMessage.success(successMessage);
      })
      .catch(() => {
        const errorMessage = locale.value === 'en' ? 'Failed to copy' : '复制失败，请手动复制';
        ElMessage.error(errorMessage);
      });
  }
};

// 获取用户偏好标签
const fetchUserPreferences = async () => {
  try {
    const userId = localStorage.getItem('userId');
    if (!userId) {
      const warningMessage = locale.value === 'en' ? 'Please log in first' : '请先登录';
      ElMessage.warning(warningMessage);
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
    const errorMessage = locale.value === 'en' ? 'Failed to get user preference tags' : '获取用户偏好标签失败';
    ElMessage.error(errorMessage);
  }
};

// 计算可见的偏好标签
const visiblePreferences = computed(() => {
  return userPreferences.value.slice(0, maxVisibleTags);
});



// 获取主题显示名称的翻译
const getThemeDisplayName = (theme) => {
  const themeNames = {
    folk: { cn: '民俗文化', en: 'Folk Culture' },
    food: { cn: '饮食文化', en: 'Food Culture' },
    spot: { cn: '名胜古迹', en: 'Cultural Heritage Sites' },
    literature: { cn: '文学艺术', en: 'Literature and Arts' },
    other: { cn: '其他', en: 'Other' }
  };
  
  return locale.value === 'en' ? themeNames[theme]?.en : themeNames[theme]?.cn || theme;
};

// 按主题分组的标签
const groupedTags = ref({});
const getPlatformName = (platform) => {
  const platformNames = {
    '小红书': locale.value === 'en' ? 'Xiaohongshu' : '小红书',
    '微博': locale.value === 'en' ? 'Weibo' : '微博',
    '抖音': locale.value === 'en' ? 'Douyin' : '抖音',
    'B站': locale.value === 'en' ? 'Bilibili' : 'B站',
    '政府平台': locale.value === 'en' ? 'Government Platform' : '政府平台',
    '党建平台': locale.value === 'en' ? 'Party Building Platform' : '党建平台',
    '新闻媒体': locale.value === 'en' ? 'News Media' : '新闻媒体',
    '海外传播': locale.value === 'en' ? 'Overseas Spread' : '海外传播',
    '线下物料': locale.value === 'en' ? 'Offline Materials' : '线下物料',
    '研学活动': locale.value === 'en' ? 'Research and Study Activities' : '研学活动',
    '商业合作': locale.value === 'en' ? 'Business Cooperation' : '商业合作',
    '学术研究': locale.value === 'en' ? 'Academic Research' : '学术研究'
  };
  return platformNames[platform] || platform;
};

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
    const warningMessage = locale.value === 'en' ? 'Please fill in the event name and type first' : '请先填写活动名称和类型';
    ElMessage.warning(warningMessage);
    return;
  }

  generatingImage.value = true;
  try {
    const apiMethod = locale.value === 'en' ? ReportAPI.generatePublicityImageENAPI : ReportAPI.generatePublicityImageAPI;
    const response = await apiMethod({
      eventName: report.value.eventName,
      eventType: report.value.eventType,
      tags: selectedTags.value,
      title: report.value.title,
      content: report.value.content
    });

    if (response.code === 200) {
      generatedImages.value = response.data.images;
// 根据语言环境显示不同的提示信息
const successMessage = locale.value === 'en' ? 'Image generated successfully!' : '图片生成成功！';
    ElMessage.success(successMessage);
    }
  } catch (error) {
    console.error('生成图片失败:', error);
    const errorMessage = locale.value === 'en' ? 'Failed to generate image, please try again.' : '生成图片失败，请重试';
    ElMessage.error(errorMessage);
  } finally {
    generatingImage.value = false;
  }
};

// 修改下载方法
const handleDownload = (imageUrl) => {
  try {
    // 直接使用 a 标签下载
    const a = document.createElement('a');
    a.href = imageUrl;
    a.download = `宣传图片_${Date.now()}.png`;
    a.target = '_blank';  // 在新标签页打开
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    const downloadMessage = locale.value === 'en' ? 'Download started' : '开始下载';
    ElMessage.success(downloadMessage);
  } catch (error) {
    console.error('下载失败:', error);
    const downloadErrorMessage = locale.value === 'en' ? 'Failed to download' : '下载失败';
    ElMessage.error(downloadErrorMessage);
  }
};

// 初始化 markdown-it
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  breaks: true
});

// 修改 markdown 渲染计算属性
const renderedMarkdown = computed(() => {
  if (!generatedReport.value) return '';

  // 处理文本，避免话题标签被识别为标题
  const formattedText = generatedReport.value
    // 转义话题标签中的 #，但保留真正的标题标记
    .replace(/(^|\n)#(?!#|\s)/g, '$1\\#')  // 行首的单个#，但不是标题的情况
    .replace(/\s#(?!#|\s)/g, ' \\#')       // 空格后的#，但不是标题的情况
    // 确保真正的标题格式正确
    .replace(/^###(?!#)/gm, '### ')  // 确保 ### 后有空格
    .replace(/^##(?!#)/gm, '## ')    // 确保 ## 后有空格
    .replace(/^#(?!#)/gm, '# ');     // 确保 # 后有空格

  return md.render(formattedText);
});
</script>
