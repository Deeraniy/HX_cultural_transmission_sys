<template>
  <div class="tab-inner">
    <div class="analysis-container">
      <!-- 左侧表格区域 -->
      <div class="table-section">
        <!-- 切换按钮 -->
        <div class="switch-buttons">
          <el-radio-group v-model="currentTable" size="large" @change="handleTableChange">
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
          ref="barChartRef"
          v-else
          :chartData="currentChartData"
          :chartType="currentTable"
          style="width: 100%; height: 100%;"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, computed, nextTick, onActivated } from 'vue';
import BarChart from "@/components/DetailPage/subcomponent/BarChart.vue";
import TopicCluster from "@/components/DetailPage/subcomponent/TopicCluster.vue";
import SentimentStats from "@/components/DetailPage/subcomponent/SentimentStats.vue";
import LdaAPI from "@/api/lda";
import SentimentAPI from "@/api/sentiment";
import { ElMessage } from 'element-plus';
import { useRoute } from 'vue-router';

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

// 计算属性：根据当前选择的表格类型返回对应的数据
const currentChartData = computed(() => {
  return currentTable.value === 'sentiment' ? topic.value : sentiment.value;
});

// 处理表格类型变化
const handleTableChange = (value) => {
  console.log('Table type changed to:', value);
  // 不需要额外操作，计算属性会自动更新图表数据
};

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

const barChartRef = ref(null);

// 添加 activated 钩子
onActivated(() => {
  // 在组件激活时重置图表大小
  nextTick(() => {
    if (barChartRef.value) {
      barChartRef.value.resizeChart();
    }
  });
});

// 监听路由变化
const route = useRoute();
watch(
  () => route.path,
  () => {
    nextTick(() => {
      if (barChartRef.value) {
        barChartRef.value.resizeChart();
      }
    });
  }
);
</script>

<style scoped>
.tab-inner {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;

  overflow: hidden; /* 防止滚动 */
}

.analysis-container {
  display: flex;
  gap: 20px;
  height: calc(100vh - 180px);
  width: 100%; /* 减小宽度，防止溢出 */
  margin: 0 auto; /* 居中显示 */
}

.table-section {
  flex: 0 0 28%; /* 进一步减小表格区域的宽度 */
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
  flex: 0 0 64%; /* 固定宽度，防止溢出 */
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden; /* 防止内容溢出 */
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

/* 自定义radio按钮颜色 - 更全面的颜色覆盖 */
:deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background-color: #b71c1c !important;
  border-color: #b71c1c !important;
  box-shadow: -1px 0 0 0 #b71c1c !important;
  color: white !important;
}

/* 未选中状态下的按钮文字颜色 */
:deep(.el-radio-button__inner) {
  color: #b71c1c;
  border-color: #b71c1c;
}

/* 第一个按钮的左边框 */
:deep(.el-radio-button:first-child .el-radio-button__inner) {
  border-left-color: #b71c1c;
}

/* 悬停状态 */
:deep(.el-radio-button__inner:hover) {
  color: #b71c1c;
}

/* 选中状态下相邻按钮的边框 */
:deep(.el-radio-button__original-radio:checked + .el-radio-button__inner + .el-radio-button__inner) {
  border-left-color: #b71c1c;
}

/* 焦点状态 */
:deep(.el-radio-button:focus:not(.is-focus):not(:active):not(.is-disabled)) {
  box-shadow: 0 0 2px 2px rgba(183, 28, 28, 0.25);
}

/* 禁用状态下但选中的按钮 */
:deep(.el-radio-button.is-disabled.is-checked .el-radio-button__inner) {
  background-color: rgba(183, 28, 28, 0.6) !important;
  border-color: rgba(183, 28, 28, 0.6) !important;
  box-shadow: -1px 0 0 0 rgba(183, 28, 28, 0.6) !important;
}
</style>