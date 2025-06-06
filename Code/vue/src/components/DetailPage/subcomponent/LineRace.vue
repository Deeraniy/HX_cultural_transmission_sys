<template>
  <div class="line-race-container">
    <div ref="chartRef" class="chart"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import { useI18n } from 'vue-i18n';

const { t } = useI18n();

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

const resizeChart = () => {
  if (chart) {
    chart.resize();
  }
};

const updateChart = () => {
  if (!chart || !props.timeData.length) return;

  const option = {
    grid: {
      top: '10%',
      left: '3%',
      right: '4%',
      bottom: '15%',
      containLabel: true
    },
    tooltip: {
      trigger: 'axis',
      formatter: function(params: any) {
        const data = params[0];
        return `${data.name}<br/>
                ${t('detail.sentiment.score')}: ${data.value}<br/>
                ${t('detail.report.commentCount', { count: data.data.count })}<br/>
                ${t('detail.sentiment.type')}: ${t(`detail.report.sentiment.${data.data.type}`)}`;
      }
    },
    xAxis: {
      type: 'category',
      data: props.timeData.map(item => item.date),
      axisLabel: {
        interval: 'auto',
        rotate: 45,
        margin: 14,
        fontFamily: 'HelveticaNeue, serif', // ✅ 确保 x 轴字体正确
        fontSize: 14
      }
    },
    yAxis: {
      type: 'value',
      name: t('detail.sentiment.score'),
      min: 0,
      max: 1,
      scale: true,
      splitNumber: 3,
      splitLine: {
        show: true,
        lineStyle: {
          type: 'dashed'
        }
      },
      nameTextStyle: { // ✅ 这里确保 y 轴 "情感得分" 文字的字体正确
        fontFamily: 'HelveticaNeue, serif',
        fontSize: 14,
        color: '#333' // 可调整颜色
      },
      axisLabel: { // ✅ 这里确保 y 轴刻度的字体正确
        fontFamily: 'HelveticaNeue, serif',
        fontSize: 14,
        color: '#666' // 可调整颜色
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
      symbolSize: 6,
      lineStyle: {
        width: 2
      }
    }]
  };

  chart.setOption(option);
};

const initChart = () => {
  if (!chartRef.value) return;
  chart = echarts.init(chartRef.value);
  updateChart();
};

onMounted(() => {
  chart = echarts.init(chartRef.value);
  updateChart();
  
  const handleResize = () => {
    if (chart) {
      chart.resize();
    }
  };
  
  const resizeObserver = new ResizeObserver(() => {
    handleResize();
  });
  
  if (chartRef.value) {
    resizeObserver.observe(chartRef.value);
  }
  
  window.addEventListener('resize', handleResize);
  
  onUnmounted(() => {
    window.removeEventListener('resize', handleResize);
    resizeObserver.disconnect();
    if (chart) {
      chart.dispose();
    }
  });
});

watch(() => props.timeData, (newData) => {
  if (newData && chart) {
    updateChart();
  }
}, { deep: true });

defineExpose({
  resizeChart
});
</script>

<style scoped>
.line-race-container {
  width: 100%;
  height: 90%;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
}

.chart {
  width: 100%;
  height: 100%;
  min-height: 250px;
}
</style>
