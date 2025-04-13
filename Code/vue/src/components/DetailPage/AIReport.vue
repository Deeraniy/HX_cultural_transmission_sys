<template>
  <div class="ai-report-container" :class="{ 'styled-font': fontStore.isStyled }">
    <div class="report-header">
      <h2>{{ t('detail.tabs.report') }}</h2>
    </div>

    <div class="report-content-wrapper">
      <!-- 左侧报告内容 -->
      <div class="report-scroll-container" @scroll="handleScroll" ref="reportContainer" id="reportContainer">
        <div v-if="loading" class="loading-container">
          <el-skeleton :rows="10" animated />
          <div class="loading-text">
            <el-icon class="is-loading"><Loading /></el-icon>
            {{ t('common.loading') }}
          </div>
        </div>

        <div v-else-if="!report" class="empty-state">
          <el-empty :description="t('detail.report.clickToGenerate')">
            <el-button 
              type="primary"
              :icon="Document"
              @click="generateReport"
              class="generate-report-btn"
            >
              {{ t('detail.report.generate') }}
            </el-button>
          </el-empty>
        </div>

        <div v-else class="report-container markdown-body" v-html="markdownContent"></div>
      </div>

      <!-- 右侧时间轴 -->
      <div class="timeline-container" ref="timelineContainer">
        <div class="timeline-center-line"></div>
        <div class="timeline" :style="{ transform: `translateY(${-scrollTop}px)` }">
          <div v-for="(item, index) in timelineItems" :key="index" class="timeline-item">
            <div class="timeline-dot" :class="item.sentiment"></div>
            <div class="timeline-content">
              <div class="timeline-date">{{ item.date }}</div>
              <div class="timeline-sentiment" :class="item.sentiment" :style="getTimelineItemStyle(item.score)">
                {{ getSentimentText(item.sentiment) }}
                <div class="timeline-count">{{ t('detail.report.commentCount', { count: item.count }) }}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, Loading } from '@element-plus/icons-vue'
import { marked } from 'marked'
import { useI18n } from 'vue-i18n'
import SentimentAPI from "@/api/sentiment"
import { useFontStore } from '@/stores/font'

const { t, locale } = useI18n()

const props = defineProps({
  name: {
    type: String,
    required: true
  },
  pageType: {
    type: String,
    required: true
  },
  themeType: {
    type: String,
    required: true
  }
})

const report = ref<string>('')
const loading = ref(false)
const reportContainer = ref<HTMLElement | null>(null)
const timelineContainer = ref<HTMLElement | null>(null)
const timelineItems = ref<Array<{
  date: string;
  sentiment: string;
  score: number;
  count: number;
}>>([])

const activeTimelineItem = ref('')
const observer = ref<IntersectionObserver | null>(null)
const scrollTop = ref(0)

const fontStore = useFontStore()

// 使用 marked 处理 Markdown
const markdownContent = computed(() => {
  if (!report.value) return ''
  const cleanedMarkdown = report.value.replace(/^\s+/, '')
  return marked(cleanedMarkdown)
})

// 添加响应类型定义
interface ReportResponse {
  status: string;
  report: string;
  timeline: Array<{
    date: string;
    sentiment: string;
    count: number;
    score: number;
  }>;
}

const generateReport = async () => {
  loading.value = true;
  try {
    console.log('Generating report for:', props.name, 'type:', Number(props.pageType));
    const response = await SentimentAPI.getSentimentReportAPI(props.name, Number(props.pageType));
    console.log('API Response:', response);

    if ((response as ReportResponse).status === 'success') {
  const reportField = locale.value === 'en' ? 'report_en' : 'report';
  report.value = (response as ReportResponse)[reportField]; // 动态选择字段
  timelineItems.value = (response as ReportResponse).timeline;
  ElMessage.success(t('detail.report.generateSuccess'));
}
 else {
      throw new Error((response as any).message || t('detail.report.generateError'));
    }
  } catch (error) {
    console.error('生成报告失败:', error.response || error);
    ElMessage.error(t('detail.report.generateError'));
  } finally {
    loading.value = false;
  }
};

// 添加复制功能
const handleCopyReport = () => {
  if (markdownContent.value) {
    const tempElement = document.createElement('div')
    tempElement.innerHTML = markdownContent.value
    const textContent = tempElement.textContent || ''

    navigator.clipboard.writeText(textContent)
      .then(() => {
        ElMessage.success(t('detail.report.copySuccess'))
      })
      .catch(() => {
        ElMessage.error(t('detail.report.copyError'))
      })
  }
}

onMounted(() => {
  // 创建 Intersection Observer
  observer.value = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const date = entry.target.id.replace('marker-', '')
        activeTimelineItem.value = date
      }
    })
  }, {
    root: document.getElementById('reportContainer'),
    threshold: 0.5
  })

  // 监视标记元素
  const markers = document.querySelectorAll('.timeline-marker')
  markers.forEach(marker => {
    observer.value?.observe(marker)
  })
})

// 监听时间轴数据变化，重新设置观察者
watch(timelineItems, () => {
  if (observer.value) {
    observer.value.disconnect()
    nextTick(() => {
      const markers = document.querySelectorAll('.timeline-marker')
      markers.forEach(marker => {
        observer.value?.observe(marker)
      })
    })
  }
})

const handleScroll = () => {
  if (!reportContainer.value || !timelineContainer.value) return
  
  const reportElement = reportContainer.value
  const timelineElement = timelineContainer.value.querySelector('.timeline')
  if (!timelineElement) return

  const reportScrollableHeight = reportElement.scrollHeight - reportElement.clientHeight
  const timelineScrollableHeight = timelineElement.scrollHeight - timelineContainer.value.clientHeight

  const lastTimelineItem = timelineElement.lastElementChild
  const lastItemOffset = lastTimelineItem ? lastTimelineItem.offsetTop : 0
  
  const timelineVisibleHeight = timelineContainer.value.clientHeight
  
  const maxTimelineScroll = Math.max(0, lastItemOffset - timelineVisibleHeight * 0.4)

  const scrollRatio = reportElement.scrollTop / reportScrollableHeight
  scrollTop.value = Math.min(maxTimelineScroll * scrollRatio, maxTimelineScroll)
}

const getSentimentText = (sentiment: string) => {
  return t(`detail.report.sentiment.${sentiment}`)
}

// 修改时间轴项的显示
const getTimelineItemStyle = (score: number) => {
  return {
    backgroundColor: score > 0.6 ? '#f0f9eb' : 
                    score > 0.4 ? '#f4f4f5' : '#fef0f0'
  }
}
</script>

<style scoped>
.ai-report-container {
  height: calc(88vh - 92px); /* 减去顶部导航栏和底栏的高度 */
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  
  margin-bottom: 10px;
  margin-top: 10px;
  margin-left: 15px;
  margin-right: 15px;
}

.report-header {
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
  align-items: center;
}

.report-header h2 {
  margin: 0;
  color: #303133;
  font-size: 18px;
}

.report-content-wrapper {
  flex: 1;
  display: flex;
  overflow: hidden;
  height: calc(88vh - 92px);  /* 只减去报告头部的高度 */
}

.report-scroll-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px 30px;
  border-right: 1px solid #ebeef5;
  position: relative;
}

.report-text {
  font-size: 14px;
  line-height: 1.8;
  color: #606266;
  white-space: pre-wrap;
}

.empty-state {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px;
}

.emoji {
  font-size: 1.2em;
  vertical-align: middle;
  margin: 0 2px;
}

/* 滚动条样式 */
.report-scroll-container::-webkit-scrollbar {
  width: 6px;
}

.report-scroll-container::-webkit-scrollbar-thumb {
  background-color: #C0C4CC;
  border-radius: 3px;
}

.report-scroll-container::-webkit-scrollbar-track {
  background-color: #F4F4F5;
}

.generate-report-btn {
  font-size: 16px;
  border: 2px solid #f1ce5b;
  padding: 12px 24px;
  border-radius: 25px;
  background: #fff8f0;
  color: black;
  font-family: 'HelveticaNeue', serif;
  transition: all 0.3s;
}

.generate-report-btn:hover {
  background: #FFC107;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
  border-radius: 25px;
}

.loading-container {
  padding: 20px;
  text-align: center;
}

.loading-text {
  margin-top: 20px;
  color: #909399;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.markdown-body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.6;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3 {
  margin-top: 16px;
  margin-bottom: 8px;
  line-height: 1.4;
}

.markdown-body p {
  margin: 8px 0;
  line-height: 1.6;
}

.markdown-body ul,
.markdown-body ol {
  padding-left: 24px;
  margin: 8px 0;
}

.timeline-container {
  width: 250px;
  padding: 20px;
  overflow: hidden;
  position: relative;
  background-color: #f8f9fa;
  height: calc(88vh - 92px);
  display: flex;
  flex-direction: column;
}

.timeline-center-line {
  position: absolute;
  left: 31px;
  top: 20px;
  height: calc(100% - 20px); /* 延长中线 */
  width: 2px;
  background-color: #E4E7ED;
  z-index: 0;
}

.timeline {
  position: relative;
  transition: transform 0.1s linear;
  padding: 20px 0 200px 0;
  min-height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  gap: 40px;
}

.timeline-item {
  display: flex;
  align-items: flex-start;
  position: relative;
  padding-left: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 80px;
}

.timeline-item:last-child {
  margin-bottom: 0;
}

.timeline-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-right: 15px;
  margin-top: 5px;
  position: absolute;
  left: 0;
  z-index: 1;
  border: 2px solid #fff;
  box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.8); /* 改为白色阴影 */
  transition: transform 0.3s ease;
  top: 50%;
  transform: translateY(-50%);
}

.timeline-dot.positive {
  background-color: #67c23a;
  box-shadow-color: rgba(103, 194, 58, 0.3);
}

.timeline-dot.neutral {
  background-color: #909399;
  box-shadow-color: rgba(144, 147, 153, 0.3);
}

.timeline-dot.negative {
  background-color: #f56c6c;
  box-shadow-color: rgba(245, 108, 108, 0.3);
}

.timeline-item.active .timeline-dot {
  transform: scale(1.2);
}

.timeline-content {
  flex: 1;
  padding-left: 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.timeline-date {
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 4px;
}

.timeline-item.active .timeline-date {
  color: #b71c1c;
  font-weight: bold;
}

.timeline-sentiment {
  font-size: 12px;
  padding: 8px 15px; /* 增加内边距使长条更长 */
  border-radius: 6px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  min-width: 160px; /* 设置最小宽度确保长条足够长 */
}

.timeline-sentiment:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.timeline-count {
  font-size: 11px;
  margin-top: 4px;
  opacity: 0.8;
}

.timeline-sentiment.positive {
  background-color: #f0f9eb;
  color: #67c23a;
  border-left: 3px solid #67c23a;
}

.timeline-sentiment.neutral {
  background-color: #f4f4f5;
  color: #909399;
  border-left: 3px solid #909399;
}

.timeline-sentiment.negative {
  background-color: #fef0f0;
  color: #f56c6c;
  border-left: 3px solid #f56c6c;
}

.timeline-markers {
  position: absolute;
  top: 0;
  right: 0;
  height: 100%;
  pointer-events: none;
}

.timeline-marker {
  height: 100px;  /* 根据实际内容调整高度 */
  margin-bottom: 20px;
}

.styled-font {
  font-family: 'HelveticaNeue', serif;
}

/* 非风格字体时的样式 */
.ai-report-container:not(.styled-font) {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: calc(1em - 2px);
}
</style>