<template>
  <div class="common-layout">
    <el-container style="height: 100vh;">
      <!-- Header 和主内容区域 -->
      <el-header class="header" style="height:90px;width: 100%">
        <Header
          :title="title"
          @update:type="handleTypeChange"
          @update:search="handleSearchChange"
        />
      </el-header>

      <el-main v-if="hasRequiredParams" class="main">
        <!-- 内容展示区域 -->
        <div class="content-area">
          <!-- 基本信息页面 -->
          <div v-show="currentTab === 'basic'" class="tab-content">
            <BasicInfo
              :name="currentName"
              :page-type="pageType"
              :theme-type="themeType"
              style="height: 100%"
            />
          </div>

          <!-- 评论分析页面 -->
          <div v-show="currentTab === 'comments'" class="tab-content">
            <CommentAnalysis
              :name="name"
              :pageType="value"
              :themeType="theme"
            />
          </div>

          <!-- 情感分析页面 -->
          <div v-show="currentTab === 'sentiment'" class="tab-content">
            <SentimentAnalysis
              :name="name"
              :pageType="value"
              :themeType="theme"
            />
          </div>

          <!-- AI 报告页面 -->
          <div v-show="currentTab === 'report'" class="tab-content">
            <AIReport
              :name="name"
              :pageType="value"
              :themeType="theme"
            />
          </div>
        </div>

        <!-- 底部导航栏 -->
        <div class="nav-tabs">
          <el-menu
            :default-active="currentTab"
            mode="horizontal"
            @select="handleTabChange"
            class="tab-menu"
          >
            <el-menu-item index="basic">
              <el-icon><InfoFilled /></el-icon>
              <span>基本信息</span>
            </el-menu-item>
            <el-menu-item index="comments">
              <el-icon><ChatDotRound /></el-icon>
              <span>评论分析</span>
            </el-menu-item>
            <el-menu-item index="sentiment">
              <el-icon><TrendCharts /></el-icon>
              <span>情感分析</span>
            </el-menu-item>
            <el-menu-item index="report">
              <el-icon><Document /></el-icon>
              <span>AI 报告</span>
            </el-menu-item>
          </el-menu>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { InfoFilled, ChatDotRound, TrendCharts, Document } from '@element-plus/icons-vue'
import Header from "@/components/DetailPage/subcomponent/Header.vue"
import { ElMessage } from 'element-plus'
import BasicInfo from "@/components/DetailPage/BasicInfo.vue"
import CommentAnalysis from "@/components/DetailPage/CommentAnalysis.vue"
import SentimentAnalysis from "@/components/DetailPage/SentimentAnalysis.vue"
import AIReport from "@/components/DetailPage/AIReport.vue"
import ThreeLineChart from "@/components/DetailPage/subcomponent/ThreeLineChart.vue";

const router = useRouter()
const route = useRoute()
const currentTab = ref('basic')
const name = ref('')
const value = ref('')
const theme = ref('')
const title = ref('')

// 保存上一次的路由参数用于比较
const previousQuery = ref({
  name: '',
  value: '',
  theme: ''
});

// 检查是否有必要的路由参数
const hasRequiredParams = computed(() => {
  return route.query.name && route.query.value && route.query.theme;
});

// 修改路由参数监听
watch(
  () => route.query,
  async (newQuery) => {
    // 如果没有必要的参数，不进行刷新
    if (!hasRequiredParams.value) {
      return;
    }

    // 检查参数是否真的发生变化
    const hasChanged = 
      newQuery.name !== previousQuery.value.name ||
      newQuery.value !== previousQuery.value.value ||
      newQuery.theme !== previousQuery.value.theme;

    if (hasChanged) {
      // 更新上一次的参数
      previousQuery.value = {
        name: newQuery.name as string,
        value: newQuery.value as string,
        theme: newQuery.theme as string
      };

      name.value = newQuery.name as string
      value.value = newQuery.value as string
      theme.value = newQuery.theme as string
      
      // 更新当前显示的名称和类型
      currentName.value = newQuery.name as string
      pageType.value = newQuery.value as string
      themeType.value = newQuery.theme as string

      // 只在参数变化时刷新页面
      window.location.reload()
    }
  },
  { immediate: true, deep: true }
)

// 处理标签页切换
const handleTabChange = (tab: string) => {
  currentTab.value = tab
}

// 处理类型变化
const handleTypeChange = (typeId: string) => {
  console.log('Type changed:', typeId)
}

// 处理搜索
const handleSearchChange = (searchText: string) => {
  console.log('Search text:', searchText)
}

// 修改组件挂载逻辑
onMounted(() => {
  try {
    // 获取路由参数
    const routeName = route.query.name as string
    const routeValue = route.query.value as string
    const routeTheme = route.query.theme as string

    // 只有在有必要参数时才进行初始化
    if (hasRequiredParams.value) {
      // 更新响应式变量
      name.value = routeName
      value.value = routeValue
      theme.value = routeTheme
      
      // 更新当前显示的名称和类型
      currentName.value = routeName
      pageType.value = routeValue
      themeType.value = routeTheme

      // 初始化上一次的参数
      previousQuery.value = {
        name: routeName,
        value: routeValue,
        theme: routeTheme
      };
    }
  } catch (error) {
    console.error('数据加载失败:', error)
    ElMessage.error('数据加载失败，请重试')
  }
})

const currentName = ref('')
const currentPageType = ref('1')
const currentThemeType = ref('1')

// 在这里设置这些值
// 可能是从路由参数获取
currentName.value = route.query.name as string || ''
currentPageType.value = route.query.value as string || '1'
currentThemeType.value = route.query.theme as string || '1'

const pageType = ref(currentPageType.value)
const themeType = ref(currentThemeType.value)

</script>

<style scoped>
.common-layout {
  height: 97.8vh;
  display: flex;
  flex-direction: column;
  background-image: url('@/assets/img2.png');
  background-color: #fff8f0;
  width: 100%;
  overflow: hidden;
}

.header {
  padding: 0;
  margin: 0;
}

.main {
  flex: 1;
  display: flex;
  flex-direction: column;
  padding: 0;
  margin-top: -20px;
  padding-left: 10px;
  padding-right: 10px;
  overflow: hidden;
}

.content-area {
  flex: 1;
  position: relative;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.tab-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  border-radius: 8px;
  overflow: hidden;
}

.tab-inner {
  height: 100%;
  margin-top: -10px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.tab-inner h2 {
  margin: 0 0 20px 0;
  color: #fff8f0;
}

.nav-tabs {
  height: 58px;
  background-image: url('@/assets/img/a333.jpg');
  background-blend-mode: overlay;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  border-radius: 8px;
  position: relative;
  overflow: hidden;
}

.nav-tabs::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.4);
  z-index: 0;
}

.tab-menu {
  display: flex;
  justify-content: space-around;
  height: 100%;
  background: transparent;
  position: relative;
  z-index: 1;
}

:deep(.el-menu--horizontal) {
  border-bottom: none;
  height: 100%;
  background: transparent;
}

:deep(.el-menu--horizontal > .el-menu-item) {
  background-color: transparent !important;
}

:deep(.el-menu-item) {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100%;
  line-height: 1.2;
  padding: 8px 20px;
  color: #000000;
  font-weight: bold;
  background-color: transparent !important;
}

:deep(.el-menu-item:hover) {
  background-color: rgba(255, 255, 255, 0.2) !important;
}

:deep(.el-menu-item.is-active) {
  color: #b71c1c;
  border-bottom: 2px solid #b71c1c;
  background-color: transparent !important;
}

:deep(.el-menu-item .el-icon) {
  margin-right: 0;
  margin-bottom: 4px;
  font-size: 20px;
  color: #ffffff;
}

:deep(.el-menu-item span) {
  font-size: 14px;
  color: #ffffff;
  letter-spacing: 0.5px;
}

.image-danmu-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  position: relative;
  margin-bottom: 20px;
}

.wordcloud-container,
.city-image-container,
.danmu-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.loader {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 10;
  pointer-events: none;
}

.city-image,
.wordcloud {
  object-fit: contain;
  width: 100%;
  height: 100%;
  border-radius: 10px;
}

.danmu {
  flex: 1;
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: rgba(0, 0, 0, 0.5);
  position: relative;
}

.danmu-item {
  white-space: nowrap;
  color: #FFFFFF;
  font-size: 16px;
  background-color: rgba(0, 0, 0, 0.3);
  padding: 4px 10px;
  border-radius: 15px;
  margin-bottom: 8px;
}

.chart-container {
  position: relative;
  margin-top: 20px;
}

.charts-row {
  display: flex;
  justify-content: space-between;
}

.mixed-charts-row {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}
</style>
