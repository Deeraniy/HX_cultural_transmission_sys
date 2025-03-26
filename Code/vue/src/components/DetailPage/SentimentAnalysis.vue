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
            v-else-if="timeData && timeData.length > 0"
            :timeData="timeData"
            :height="'100%'"
            :width="'100%'"
          />
          <div v-else class="no-data">暂无数据</div>
        </template>

        <!-- 三线图 -->
        <template v-else>

          <el-skeleton v-show="isThreeLineLoading" :rows="3" animated />
          <ThreeLineChart
              v-show="threeLineData && threeLineData.length > 0"
              :timeData="threeLineData"
              style="height: 1000px;width: 1000px"
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
const processTimeData = (timeResponse: any) => {
  if (!timeResponse?.data || !Array.isArray(timeResponse.data)) {
    console.warn('Invalid time data format:', timeResponse);
    return [];
  }

  // 按时间排序
  const sortedData = [...timeResponse.data].sort((a, b) => {
    const dateA = new Date(`${a.year}-${a.month}`);
    const dateB = new Date(`${b.year}-${b.month}`);
    return dateA.getTime() - dateB.getTime();
  });

  // 转换数据格式
  return sortedData.map(item => ({
    date: `${item.year}-${item.month.toString().padStart(2, '0')}`,
    value: parseFloat(item.sentiment_score.toFixed(3)), // 保留三位小数
    type: item.sentiment || 'neutral',
    count: item.comment_count || 0
  }));
};

// 修改 processThreeLineData 函数
const processThreeLineData = (data: any) => {
  // 检查数据格式
  if (!data || !data.data || !Array.isArray(data.data)) {
    console.warn('Invalid data format:', data);
    return [];
  }

  // 直接使用原始数据，按月份分组统计
  const monthlyStats = new Map();

  data.data.forEach(item => {
    const key = `${item.year}-${item.month.toString().padStart(2, '0')}`;

    if (!monthlyStats.has(key)) {
      monthlyStats.set(key, {
        date: key,
        positive: 0,
        neutral: 0,
        negative: 0
      });
    }

    const stats = monthlyStats.get(key);
    // 根据情感类型累加评论数量
    if (item.sentiment === 'positive') {
      stats.positive += item.comment_count;
    } else if (item.sentiment === 'negative') {
      stats.negative += item.comment_count;
    } else {
      stats.neutral += item.comment_count;
    }
  });

  // 转换为数组并排序
  const result = Array.from(monthlyStats.values())
    .sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

  console.log('Processed three line data:', result);
  return result;
};

// 修改 loadData 函数
const loadData = async () => {
  try {
    console.log('Loading sentiment analysis data for:', props.name, props.pageType);

    // 加载时间序列数据
    try {
      isTimeChartLoading.value = true;

      const timeResponse = await SentimentAPI.getSentimentResultAPI(props.name, Number(props.pageType));
      console.log('Raw time response:', timeResponse);

      if (timeResponse?.status === 'success') {
        const processedData = processTimeData(timeResponse);
        if (processedData.length > 0) {
          timeData.value = processedData;
          console.log('Processed time data:', processedData);
        } else {
          console.warn('No data after processing');
          timeData.value = [];
        }
      } else {
        console.warn('Invalid API response:', timeResponse);
        timeData.value = [];
      }
    } catch (error) {
      console.error('Error loading time data:', error);
      timeData.value = [];
      ElMessage.error('加载时间数据失败，请稍后重试');
    } finally {
      isTimeChartLoading.value = false;
    }

    // 加载三线图数据
    try {
      const threeLineResponse = await SentimentAPI.getCasualImpactAPI(props.name);
      console.log("三线图原始数据为:", threeLineResponse);

      // 检查数据结构是否符合预期
      if (threeLineResponse &&
          typeof threeLineResponse === 'object' &&
          'economic_data' in threeLineResponse &&
          'sentiment_data' in threeLineResponse &&
          'casual_impact_analysis' in threeLineResponse) {

        threeLineData.value = threeLineResponse;
        console.log("三线图数据处理成功");
      } else {
        console.warn("三线图数据格式不符合预期:", threeLineResponse);
        threeLineData.value = []; // 设置为空数组避免渲染错误
      }
    } catch (error) {
      console.error("加载三线图数据时出错:", error);
      threeLineData.value = []; // 出错时也设置为空数组
    }finally {
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

// 添加数据监听，用于调试
watch(timeData, (newValue) => {
  console.log('timeData changed:', newValue);
}, { deep: true });

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
  height: 100%;
  min-height: 400px;
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

.no-data {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  color: #909399;
  font-size: 14px;
}
</style>
