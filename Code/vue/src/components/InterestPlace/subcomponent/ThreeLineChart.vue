<script setup>
import { ref, onMounted, watch, defineProps } from 'vue';
import * as echarts from 'echarts/core';
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  VisualMapComponent,
  MarkAreaComponent,
  DatasetComponent,
  TransformComponent,
  LegendComponent
} from 'echarts/components';
import { LineChart } from 'echarts/charts';
import { LabelLayout, UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  VisualMapComponent,
  MarkAreaComponent,
  DatasetComponent,
  TransformComponent,
  LegendComponent,
  LineChart,
  LabelLayout,
  UniversalTransition,
  CanvasRenderer
]);

const props = defineProps({
  timeData: {
    type: Array,
    default: () => []
  }
});

const showReport = ref(false);
const chartRef = ref(null);
let chart = null;

const initChart = () => {
  if (!chartRef.value) return;
  
  if (chart) {
    chart.dispose();
  }
  
  chart = echarts.init(chartRef.value);
  
  chart.on('click', (params) => {
    if (params.componentType === 'markLine') {
      showReport.value = true;
    }
  });
  
  chart.showLoading();
};

const updateChart = () => {
  if (!chart || !props.timeData || props.timeData.length === 0) {
    return;
  }
  
  chart.hideLoading();
  
  const data = props.timeData;
  
  const option = {
    title: {
      text: '综合经济与情感分析',
      subtext: '实际数据 vs 预测分析'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' }
    },
    legend: {
      data: ['CPI', '投资', '销售率', '实际情感', '预测情感', '置信区间']
    },
    toolbox: {
      show: true,
      feature: { saveAsImage: {} }
    },
    xAxis: {
      type: 'category',
      data: data.map(item => item.date || ''),
      axisLabel: { rotate: 45 }
    },
    yAxis: [
      {
        type: 'value',
        name: 'CPI/销售率',
        position: 'left',
        scale: true
      },
      {
        type: 'value',
        name: '投资/情感',
        position: 'right',
        axisLabel: {
          formatter: '{value}%'
        },
        offset: 0
      }
    ],
    series: [
      {
        name: 'CPI',
        type: 'line',
        yAxisIndex: 1,
        data: data.map(item => item.cpi),
        smooth: true,
        itemStyle: { color: '#5470C6' }
      },
      {
        name: '投资',
        type: 'line',
        yAxisIndex: 1,
        data: data.map(item => item.investment),
        smooth: true,
        itemStyle: { color: '#91CC75' }
      },
      {
        name: '销售率',
        type: 'line',
        yAxisIndex: 1,
        data: data.map(item => item.sales_rate),
        smooth: true,
        itemStyle: { color: '#FAC858' }
      },
      {
        name: '实际情感',
        type: 'line',
        data: data.map(item => item.sentiment_score * 100),
        smooth: true,
        itemStyle: { color: '#FF6B6B' },
        markLine: {
          triggerEvent: true,
          data: [{ xAxis: data.findIndex(d => d.sentiment_score === 1) }],
          symbol: 'circle',
          lineStyle: { color: '#FF6B6B', type: 'dashed' },
          label: {
            position: 'end',
            formatter: '突变点\n{@score}',
            backgroundColor: 'rgba(255,107,107,0.3)'
          }
        }
      },
      {
        name: '预测情感',
        type: 'line',
        data: data.map(item => item.predict_sentiment * 100),
        smooth: true,
        itemStyle: { color: '#A685E2' }
      },
      {
        name: '置信区间',
        type: 'line',
        data: data.map(item => item.ci_upper * 100),
        itemStyle: { color: 'transparent' },
        areaStyle: {
          color: 'rgba(166,133,226,0.2)',
          origin: 'start'
        },
        lineStyle: { opacity: 0 },
        stack: 'confidence',
        symbol: 'none'
      },
      {
        name: '置信区间',
        type: 'line',
        data: data.map(item => item.ci_lower * 100),
        itemStyle: { color: 'transparent' },
        areaStyle: { color: 'rgba(166,133,226,0.2)' },
        lineStyle: { opacity: 0 },
        stack: 'confidence',
        symbol: 'none'
      }
    ],
    dataZoom: [{
      type: 'inside',
      start: 50,
      end: 100
    }]
  };
  
  chart.setOption(option);
};

watch(() => props.timeData, (newData) => {
  if (newData && newData.length > 0) {
    updateChart();
  }
}, { deep: true });

const handleResize = () => {
  if (chart) {
    chart.resize();
  }
};

onMounted(() => {
  initChart();
  updateChart();
  window.addEventListener('resize', handleResize);
});

const onUnmounted = () => {
  window.removeEventListener('resize', handleResize);
  if (chart) {
    chart.dispose();
    chart = null;
  }
};
</script>

<template>
  <div ref="chartRef" style="width: 100%; height: 400px;"></div>
  <!-- 因果推理报告 Drawer -->
  <el-drawer
      v-model="showReport"
      title="因果推理报告"
      direction="rtl"
      size="40%"
      :before-close="handleClose"
  >
    <template #default>
      <pre style="white-space: pre-wrap; padding: 20px">{{ timeData.casual_impact_analysis.impact_report }}</pre>
    </template>
    <template #footer>
      <div style="flex: auto">
        <el-button @click="showReport = false">关闭报告</el-button>
      </div>
    </template>
  </el-drawer>
</template>

<style scoped>
:deep(.el-drawer__body) {
  overflow: auto;
  padding: 0 20px;
}

pre {
  font-family: 'Microsoft YaHei', sans-serif;
  line-height: 1.6;
  background: #f8f9fa;
  border-radius: 4px;
  padding: 15px !important;
}

:deep(.el-drawer__header) {
  margin-bottom: 10px;
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
}
</style>
