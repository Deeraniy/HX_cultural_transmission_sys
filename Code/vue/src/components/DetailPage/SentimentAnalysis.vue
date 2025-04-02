<template>
  <div class="sentiment-analysis">
    <div class="sentiment-analysis-content">
      <div class="chart-container">
        <!-- 标题和切换按钮放在一起 -->
        <div class="chart-header">
          <div class="chart-title">情感分析</div>
          <div class="chart-switch">
            <el-radio-group v-model="currentChart" size="large">
              <el-radio-button label="time">时间趋势</el-radio-button>
              <el-radio-button label="threeLine">情感分布</el-radio-button>
            </el-radio-group>
          </div>
        </div>

        <!-- 图表区域 -->
        <div class="chart-area">
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
            <el-skeleton v-if="isThreeLineLoading" :rows="3" animated />
            <ThreeLineChart
              v-else
              v-show="threeLineData && Object.keys(threeLineData).length > 0"
              :timeData="threeLineData"
              class="three-line-chart"
            />
          </template>
        </div>
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
import { initChart } from '@/utils/echartConfig';

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

  const chartDom = document.getElementById('myChart');
  if (chartDom) {
    const chart = initChart(chartDom);
    chart.setOption(option);
  }
});

const initChartOption = () => {
  // 获取当前字体样式
  const fontStyle = document.documentElement.getAttribute('data-font-style');
  const fontFamily = fontStyle === 'normal' ? 
    'system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif' : 
    'HelveticaNeue, serif';
  const fontSize = fontStyle === 'normal' ? 14 : 16;

  return {
    // 全局字体设置
    textStyle: {
      fontFamily: 'HelveticaNeue, serif',
      fontSize: 16
    },
    title: {
      text: '情感分析',
      textStyle: {
        fontFamily: 'HelveticaNeue, serif',
        fontSize: 20  // 标题字体稍大
      }
    },
    tooltip: {
      trigger: 'axis',
      textStyle: {
        fontFamily: 'HelveticaNeue, serif',
        fontSize: 16
      }
    },
    xAxis: {
      type: 'category',
      data: [],
      axisLabel: {
        fontFamily: 'HelveticaNeue, serif',
        fontSize: 16
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        fontFamily: 'HelveticaNeue, serif',
        fontSize: 16
      }
    },
    legend: {
      textStyle: {
        fontFamily: 'HelveticaNeue, serif',
        fontSize: 16
      }
    },
    // ... 其他配置
  };
};

// 监听字体样式变化
watch(
  () => document.documentElement.getAttribute('data-font-style'),
  () => {
    if (chart.value) {
      const option = initChartOption();
      // 更新已有数据
      option.xAxis.data = chart.value.getOption().xAxis[0].data;
      option.series = chart.value.getOption().series;
      chart.value.setOption(option);
    }
  }
);
</script>

<style scoped>
.sentiment-analysis {
  margin-top: 10px;
  width: 97%;
  margin-left: 1.5%;
  height: 95%;
  min-height: 300px;
}

.sentiment-analysis-content {
  height: 100%;
}

.chart-container {
  height: 100%;
  min-height: 300px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.chart-header {
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #ebeef5;
}

.chart-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.chart-area {
  height: calc(100% - 60px); /* 减去header的高度 */
  padding: 20px;
}

/* Radio按钮组样式 */
:deep(.el-radio-group) {
  display: flex;
}

:deep(.el-radio-button) {
  margin-left: 10px;
}

:deep(.el-radio-button__inner) {
  border-radius: 4px !important;
}

:deep(.el-radio-button:first-child .el-radio-button__inner) {
  border-radius: 4px !important;
}

:deep(.el-radio-button:last-child .el-radio-button__inner) {
  border-radius: 4px !important;
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

.three-line-chart {
  height: 100%;
  min-height: 250px;
}
</style>
