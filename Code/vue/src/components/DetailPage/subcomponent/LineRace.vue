<template>
  <div class="line-race-container">
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue';
import * as echarts from 'echarts';

const props = defineProps({
  timeData: {
    type: Array,
    required: true
  },
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '100%'
  }
});

const chartRef = ref(null);
let chart: echarts.ECharts | null = null;

const initChart = () => {
  if (!chartRef.value) return;
  
  chart = echarts.init(chartRef.value);
  updateChart();
};

const updateChart = () => {
  if (!chart || !props.timeData.length) return;

  const option = {
    grid: {
      top: '5%',
      left: '3%',
      right: '4%',
      bottom: '8%',
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params: any) {
        const data = params[0];
        return `${data.name}<br/>
                情感得分: ${data.value}<br/>
                评论数量: ${data.data.count}<br/>
                情感类型: ${data.data.type}`;
      }
    },
    xAxis: {
      type: 'category',
      data: props.timeData.map(item => item.date),
      axisLabel: {
        interval: 'auto',
        rotate: 45
      }
    },
    yAxis: {
      type: 'value',
      name: '情感得分',
      min: 0,
      max: 1,
      splitLine: {
        show: true,
        lineStyle: {
          type: 'dashed'
        }
      }
    },
    series: [{
      data: props.timeData.map(item => ({
        value: item.value,
        itemStyle: {
          color: item.type === 'positive' ? '#67C23A' :
                item.type === 'negative' ? '#F56C6C' : '#E6A23C'
        },
        count: item.count,
        type: item.type
      })),
      type: 'line',
      smooth: true,
      symbolSize: 8,
      lineStyle: {
        width: 2
      }
    }]
  };

  chart.setOption(option);
};

// 监听数据变化
watch(() => props.timeData, () => {
  if (chart) {
    updateChart();
  }
}, { deep: true });

// 监听容器大小变化
const handleResize = () => {
  if (chart) {
    chart.resize();
  }
};

onMounted(() => {
  initChart();
  window.addEventListener('resize', handleResize);
});

onUnmounted(() => {
  if (chart) {
    chart.dispose();
  }
  window.removeEventListener('resize', handleResize);
});
</script>

<style scoped>
.line-race-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.chart {
  width: 100%;
  height: 100%;
  min-height: 400px;
}
</style>
