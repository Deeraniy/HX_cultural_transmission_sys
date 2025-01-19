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
    xiaohongshuSentimentScore: number;
    douyinSentimentScore: number;
    weiboSentimentScore: number;
    bilibiliSentimentScore: number;
  }>;
};

// 接收父组件传递的时间情感数据
const props = defineProps<Props>();

const lineRaceChart = ref(null);
let chartInstance = null;

// 初始化图表并设置选项
function initChart(data) {
  if (!lineRaceChart.value) {
    console.error("图表容器未挂载");
    return;
  }
  console.log("11111子组件接收到的 timeData:", data)
  chartInstance = echarts.init(lineRaceChart.value);
  const option = setChartOption(data);
  chartInstance.setOption(option);
}

// 设置图表选项
function setChartOption(data) {
  console.log("22222子组件接收到的 timeData:", data)
  const chartData = data.map(item => ({
    date: item.date,
    xiaohongshuSentimentScore: item.xiaohongshuSentimentScore * 100,
    douyinSentimentScore: item.douyinSentimentScore * 100,
    weiboSentimentScore: item.weiboSentimentScore * 100,
    bilibiliSentimentScore: item.bilibiliSentimentScore * 100,
  }));
  console.log("33333子组件接收到的 timeData:", chartData)
  return {
    title: {
      text: '情感变化趋势',
      left: 'center',
    },
    tooltip: {
      trigger: 'axis',
      formatter: function (params) {
        const point = params[0].data;
        return `
          日期: ${point.date || '未知'}<br/>
          小红书情感分数: ${point.xiaohongshuSentimentScore || '未知'}<br/>
          抖音情感分数: ${point.douyinSentimentScore || '未知'}<br/>
          微博情感分数: ${point.weiboSentimentScore || '未知'}<br/>
          哔哩哔哩情感分数: ${point.bilibiliSentimentScore || '未知'}
        `;
      },
    },
    xAxis: {
      type: 'category',
      name: '日期',
      nameLocation: 'middle',
      nameGap: 55,
      data: chartData.map(item => item.date),
      axisLabel: {
        interval: 1,
        rotate: 45,
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
        name: '小红书',
        data: chartData.map(item => ({
          value: item.xiaohongshuSentimentScore,
          date: item.date,
          xiaohongshuSentimentScore: item.xiaohongshuSentimentScore,
        })),
        showSymbol: true,
        symbolSize: 8,
        lineStyle: {
          width: 2,
        },
      },
      {
        type: 'line',
        name: '抖音',
        data: chartData.map(item => ({
          value: item.douyinSentimentScore,
          date: item.date,
          douyinSentimentScore: item.douyinSentimentScore,
        })),
        showSymbol: true,
        symbolSize: 8,
        lineStyle: {
          width: 2,
        },
      },
      {
        type: 'line',
        name: '微博',
        data: chartData.map(item => ({
          value: item.weiboSentimentScore,
          date: item.date,
          weiboSentimentScore: item.weiboSentimentScore,
        })),
        showSymbol: true,
        symbolSize: 8,
        lineStyle: {
          width: 2,
        },
      },
      {
        type: 'line',
        name: '哔哩哔哩',
        data: chartData.map(item => ({
          value: item.bilibiliSentimentScore,
          date: item.date,
          bilibiliSentimentScore: item.bilibiliSentimentScore,
        })),
        showSymbol: true,
        symbolSize: 8,
        lineStyle: {
          width: 2,
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

// 添加 onMounted 钩子
onMounted(() => {
  if (props.timeData && props.timeData.length) {
    console.log("子组件接收到的 timeData:", props.timeData);
    initChart(props.timeData); // 初始化图表
  } else {
    console.warn("props.timeData 数据为空或未传递");
  }
});
</script>

<style scoped>
#lineRaceChart {
  width: 100%;
  height: 600px;
}
</style>
