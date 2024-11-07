<template>
  <div ref="lineRaceChart" style="width: 100%; height: 600px;"></div>
</template>

<script setup lang="ts">
import * as echarts from 'echarts';
import { onMounted, ref, watch } from 'vue';

// 定义 props 类型
type Props = {
  timeData: Array<{
    date: string;
    sentimentScore: number;
    sentiment: string;
    commentCount: number;
  }>;
};

// 接收父组件传递的时间情感数据
const props = defineProps<Props>();

const lineRaceChart = ref(null);
let chartInstance = null;

// 初始化图表并设置选项
function initChart(data) {
  if (lineRaceChart.value) {
    chartInstance = echarts.init(lineRaceChart.value);
    const option = setChartOption(data);
    chartInstance.setOption(option);
  }
}

// 设置图表选项
function setChartOption(data) {
  // 数据转换为 echarts 能识别的格式
  const chartData = data.map(item => ({
    date: item.date, // 横轴日期
    sentimentScore: item.sentimentScore * 100, // 纵轴情感分数（扩大比例）
  }));

  return {
    title: {
      text: '情感变化趋势',
      left: 'center',
    },
    tooltip: {
      trigger: 'axis',
      formatter: function (params) {
        const point = params[0];
        return `
          日期: ${point.data.date}<br/>
          情感分数: ${(point.data.sentimentScore / 100).toFixed(2)}
        `;
      },
    },
    xAxis: {
      type: 'category',
      name: '日期',
      nameLocation: 'middle',
      nameGap: 30,
      data: chartData.map(item => item.date), // 横轴为日期
      axisLabel: {
        interval: 1, // 每个点显示一个标签
        rotate: 45, // 旋转标签避免拥挤
      },
    },
    yAxis: {
      type: 'value',
      name: '情感分数',
    },
    grid: {
      left: '10%',
      right: '10%',
      bottom: '15%',
    },
    series: [
      {
        type: 'line',
        name: '情感变化',
        data: chartData.map(item => ({
          value: item.sentimentScore, // 数据点的值
          date: item.date, // 数据点的日期
        })),
        showSymbol: true, // 显示数据点
        symbolSize: 8, // 数据点大小
        lineStyle: {
          width: 2, // 线条宽度
        },
      },
    ],
  };
}

// 监听 props 数据的变化
watch(
    () => props.timeData,
    newData => {
      if (newData && newData.length) {
        initChart(newData);
      }
    },
    { immediate: true }
);
</script>

<style scoped>
#lineRaceChart {
  width: 100%;
  height: 600px;
}
</style>
