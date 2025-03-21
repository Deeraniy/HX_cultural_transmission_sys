<template>
  <div class="sentiment-analysis">
    <div class="sentiment-analysis-header">
      <div class="sentiment-analysis-header-title">
        <div class="sentiment-analysis-header-title-text">
          情感分析
        </div>
      </div>
      <!-- 添加切换按钮 -->
      <div class="chart-switch">
        <el-radio-group v-model="currentChart" size="large">
          <el-radio-button label="time">时间趋势</el-radio-button>
          <el-radio-button label="threeLine">情感分布</el-radio-button>
        </el-radio-group>
      </div>
    </div>
    <div class="sentiment-analysis-content">
      <div class="chart-container">
        <!-- 折线图 -->
        <template v-if="currentChart === 'time'">
          <el-skeleton v-if="isTimeChartLoading" :rows="3" animated />
          <LineRace
            v-else
            :timeData="timeData"
            :height="'100%'"
            :width="'100%'"
          />
        </template>
        
        <!-- 三线图 -->
        <template v-else>
          <el-skeleton v-if="isThreeLineLoading" :rows="3" animated />
          <ThreeLineChart
            v-else
            :timeData="threeLineData"
            :height="'100%'"
            :width="'100%'"
          />
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue';
import LineRace from "@/components/DetailPage/subcomponent/LineRace.vue";
import ThreeLineChart from "@/components/DetailPage/subcomponent/ThreeLineChart.vue";
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
const timeData = ref<any>([]);
const threeLineData = ref<any>([]);
const isTimeChartLoading = ref(true);
const isThreeLineLoading = ref(true);
const currentChart = ref('time'); // 当前显示的图表类型

// 修改数据处理函数
const processTimeData = (data: any) => {
  // 检查数据格式
  if (!Array.isArray(data)) {
    console.warn('Invalid time data format:', data);
    return [];
  }

  // 按月份统计情感分数
  const monthlyStats = data.reduce((acc: any, item: any) => {
    if (!item.comment || !item.sentiment) return acc;
    
    // 提取时间信息（假设评论中包含时间信息）
    const date = new Date();
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const key = `${year}-${month.toString().padStart(2, '0')}`;
    
    if (!acc[key]) {
      acc[key] = {
        count: 0,
        totalScore: 0,
        sentiment: {
          positive: 0,
          neutral: 0,
          negative: 0
        }
      };
    }
    
    acc[key].count++;
    // 根据情感类型计数
    acc[key].sentiment[item.sentiment.toLowerCase()]++;
    
    return acc;
  }, {});

  // 转换为图表所需格式
  return Object.entries(monthlyStats).map(([date, stats]: [string, any]) => ({
    date,
    value: stats.count,
    type: Object.entries(stats.sentiment).reduce((a, [k, v]) => v > stats.sentiment[a] ? k : a, 'neutral')
  }));
};

const processThreeLineData = (data: any) => {
  // 检查数据格式
  if (!Array.isArray(data)) {
    console.warn('Invalid data format:', data);
    return [];
  }

  // 按月份统计不同情感类型的数量
  const monthlyStats = data.reduce((acc: any, item: any) => {
    if (!item.comment || !item.sentiment) return acc;
    
    // 提取时间信息
    const date = new Date();
    const year = date.getFullYear();
    const month = date.getMonth() + 1;
    const key = `${year}-${month.toString().padStart(2, '0')}`;
    
    if (!acc[key]) {
      acc[key] = {
        positive: 0,
        neutral: 0,
        negative: 0
      };
    }
    
    // 统计各种情感类型的数量
    acc[key][item.sentiment.toLowerCase()]++;
    
    return acc;
  }, {});

  // 转换为图表所需格式
  return Object.entries(monthlyStats).map(([date, counts]: [string, any]) => ({
    date,
    positive: counts.positive,
    neutral: counts.neutral,
    negative: counts.negative
  }));
};

// 修改 loadData 函数
const loadData = async () => {
  try {
    console.log('Loading sentiment analysis data for:', props.name, props.pageType);
    
    // 加载时间序列数据
    try {
      const timeResponse = await SentimentAPI.getSentimentAnalyzeAPI(props.name, Number(props.pageType));
      console.log('Time response:', timeResponse);
      
      // 直接处理响应数据
      timeData.value = processTimeData(timeResponse);
      console.log('Processed time data:', timeData.value);
      isTimeChartLoading.value = false;
    } catch (error) {
      console.error('Error loading time data:', error);
      isTimeChartLoading.value = false;
    }

    // 加载三线图数据
    try {
      const threeLineResponse = await SentimentAPI.getSentimentResultAPI(props.name, Number(props.pageType));
      console.log('Three line response:', threeLineResponse);
      
      // 直接处理整个响应
      threeLineData.value = processThreeLineData(threeLineResponse);
      console.log('Processed three line data:', threeLineData.value);
      isThreeLineLoading.value = false;
    } catch (error) {
      console.error('Error loading three line data:', error);
      isThreeLineLoading.value = false;
    }
  } catch (error) {
    console.error('Failed to load sentiment analysis data:', error);
    ElMessage.error('数据加载失败，请重试');
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
    isTimeChartLoading.value = true;
    isThreeLineLoading.value = true;
    timeData.value = [];
    threeLineData.value = [];

    // 重新加载数据
    await loadData();
  },
  { immediate: true, deep: true }
);

onMounted(async () => {
  console.log('SentimentAnalysis mounted with props:', props);
  await loadData();
});
</script>

<style scoped>
.sentiment-analysis {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
}

.sentiment-analysis-header {
  padding: 16px 20px;
  background-color: white;
  border-radius: 8px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sentiment-analysis-header-title-text {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.chart-switch {
  margin-left: 20px;
}

.sentiment-analysis-content {
  flex: 1;
  overflow: hidden;
  padding: 20px;
}

.chart-container {
  height: calc(100vh - 200px);
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
}

/* Radio按钮组样式 */
:deep(.el-radio-group) {
  display: flex;
}

:deep(.el-radio-button) {
  flex: 1;
}

:deep(.el-radio-button__inner) {
  width: 100%;
}

/* 确保图表容器占满可用空间 */
.chart-container :deep(.echarts) {
  width: 100% !important;
  height: 100% !important;
}

/* 加载状态样式 */
:deep(.el-skeleton) {
  width: 100%;
  height: 100%;
}
</style>