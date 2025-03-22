<template>
  <div class="tab-inner">
    <div class="analysis-container">
      <!-- 左侧表格区域 -->
      <div class="table-section">
        <!-- 切换按钮 -->
        <div class="switch-buttons">
          <el-radio-group v-model="currentTable" size="large">
            <el-radio-button label="sentiment">情感分析</el-radio-button>
            <el-radio-button label="topic">主题聚类</el-radio-button>
          </el-radio-group>
        </div>
        
        <!-- 表格区域 -->
        <div class="table-container">
          <el-skeleton v-if="isSentimentStatsLoading" :rows="10" animated />
          <SentimentStats
            v-else-if="currentTable === 'sentiment'"
            :tableData="topic"
            style="width: 100%; height: 100%;"
          />
          <TopicCluster
            v-else
            :tableData="sentiment"
            style="width: 100%; height: 100%;"
          />
        </div>
      </div>

      <!-- 右侧图表区域 -->
      <div class="chart-section">
        <el-skeleton v-if="isBarChartLoading" :rows="3" animated />
        <BarChart
          v-else
          :chartData="sentiment"
          style="width: 100%; height: 100%;"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import BarChart from "@/components/DetailPage/subcomponent/BarChart.vue";
import TopicCluster from "@/components/DetailPage/subcomponent/TopicCluster.vue";
import SentimentStats from "@/components/DetailPage/subcomponent/SentimentStats.vue";
import LdaAPI from "@/api/lda";
import SentimentAPI from "@/api/sentiment";
import { ElMessage } from 'element-plus';

// Props 定义
interface Props {
  name: string;
  pageType: string | number;
  themeType?: string | number;
}

const props = withDefaults(defineProps<Props>(), {
  name: '',
  pageType: '1',
  themeType: '1'
});

// 数据状态
const sentiment = ref<any>([]);
const topic = ref<any>([]);
const isBarChartLoading = ref(true);
const isSentimentStatsLoading = ref(true);
const currentTable = ref('sentiment'); // 当前显示的表格类型

// 加载数据
const loadData = async () => {
  try {
    console.log('Loading data for:', props.name, props.pageType);
    
    // 加载主题聚类数据
    const ldaResponse = await LdaAPI.LdaAPI(props.name, String(props.pageType));
    if (Array.isArray(ldaResponse)) {
      sentiment.value = ldaResponse.map(item => ({
        topic: item.topic,
        frequency: item.frequency,
        sentiment: item.sentiment,
      }));
      isBarChartLoading.value = false;
      console.log('LDA data loaded:', sentiment.value);
    } else {
      console.warn('Invalid LDA response:', ldaResponse);
    }

    // 加载词频统计数据
    const wordResponse = await SentimentAPI.getSentimentWordAPI(props.name, String(props.pageType));
    if (wordResponse?.data && Array.isArray(wordResponse.data)) {
      topic.value = wordResponse.data.map(item => ({
        word: item.word,
        frequency: item.frequency,
        sentiment: item.sentiment,
      }));
      isSentimentStatsLoading.value = false;
      console.log('Word data loaded:', topic.value);
    } else {
      console.warn('Invalid word response:', wordResponse);
    }
  } catch (error) {
    console.error('Failed to load data:', error);
    ElMessage.error('数据加载失败，请重试');
    // 重置加载状态
    isBarChartLoading.value = false;
    isSentimentStatsLoading.value = false;
  }
};

// 监听属性变化
watch(
  () => [props.name, props.pageType, props.themeType],
  async (newValues) => {
    if (!newValues[0]) {
      console.warn('Invalid name provided');
      return;
    }

    // 重置状态
    isBarChartLoading.value = true;
    isSentimentStatsLoading.value = true;
    sentiment.value = [];
    topic.value = [];

    // 重新加载数据
    await loadData();
  },
  { immediate: true, deep: true }
);

onMounted(async () => {
  console.log('CommentAnalysis mounted with props:', props);
  await loadData();
});
</script>

<style scoped>
.tab-inner {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  padding: 20px;
  overflow: auto;
}

.analysis-container {
  display: flex;
  gap: 20px;
  height: calc(100vh - 200px); /* 调整高度以适应页面 */
  width: 100%;
}

.table-section {
  flex: 0 0 33.333%; /* 固定宽度为1/3 */
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.switch-buttons {
  display: flex;
  justify-content: center;
  padding: 16px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.table-container {
  flex: 1;
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  overflow: auto;
}

.chart-section {
  flex: 1; /* 占据剩余空间 */
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
}

/* 确保图表容器占满可用空间 */
.chart-section > div {
  flex: 1;
  width: 100%;
  height: 100%;
}

/* Radio按钮组样式 */
:deep(.el-radio-group) {
  display: flex;
  width: 100%;
}

:deep(.el-radio-button) {
  flex: 1;
}

:deep(.el-radio-button__inner) {
  width: 100%;
}
</style>