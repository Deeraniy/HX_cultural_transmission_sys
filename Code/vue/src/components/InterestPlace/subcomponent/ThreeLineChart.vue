<script setup>
import {onMounted, ref} from 'vue';
import * as echarts from 'echarts/core';
import {
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  VisualMapComponent,
  MarkAreaComponent
} from 'echarts/components';
import { LineChart } from 'echarts/charts';
import { UniversalTransition } from 'echarts/features';
import { CanvasRenderer } from 'echarts/renderers';

echarts.use([
  TitleComponent,
  ToolboxComponent,
  TooltipComponent,
  GridComponent,
  VisualMapComponent,
  MarkAreaComponent,
  LineChart,
  CanvasRenderer,
  UniversalTransition
]);

const props = defineProps({
  timeData: {
    type: Object,
    required: true,
  }
})

const showReport = ref(false);
onMounted(() => {
  const economicData = [...props.timeData.economic_data]
      .sort((a, b) => a.year - b.year || a.month - b.month); // 按时间排序
  const sentimentData = [...props.timeData.sentiment_data]
      .sort((a, b) => a.year - b.year || a.month - b.month); // 按时间排序

  // 生成x轴标签（年-月）
  const xData = economicData.map(item =>
      `${item.year}-${item.month.toString().padStart(2, '0')}`
  );
  const allDates = Array.from(new Set([
    ...economicData.map(d => `${d.year}-${d.month.toString().padStart(2, '0')}`),
    ...sentimentData.map(d => `${d.year}-${d.month.toString().padStart(2, '0')}`),
    ...timeData.casual_impact_analysis.counterfactual_predictions.dates
        .map(d => `${d.year}-${d.month.toString().padStart(2, '0')}`)
  ])).sort();

  // 数据对齐
  const alignData = (source, key, scale = 1) => {
    return allDates.map(date => {
      const item = source.find(d =>
          `${d.year}-${d.month.toString().padStart(2, '0')}` === date
      );
      return item ? (item[key] !== null ? item[key] * scale : null) : null;
    });
  };

  // 突变点信息
  const changePoint = timeData.casual_impact_analysis.change_point_info.date;
  const changePointIndex = allDates.findIndex(d =>
      d === `${changePoint.year}-${changePoint.month.toString().padStart(2, '0')}`
  );
  var chartDom = document.getElementById('main');
  var myChart = echarts.init(chartDom);
  myChart.on('click', (params) => {
    if (params.componentType === 'markLine') {
      showReport.value = true;
    }
  });

  var option;
  const seriesData = [
    {
      name: 'CPI',
      data: economicData.map(item => item.cpi),
      color: '#5470C6' // 蓝色
    },
    {
      name: 'Investment',
      data: economicData.map(item => item.investment),
      color: '#91CC75' // 绿色
    },
    {
      name: 'Sales Rate',
      data: economicData.map(item => item.sales_rate),
      color: '#FAC858' // 黄色
    },
    {
      name: 'sentiment',
      data: sentimentData.map(item => item.sentiment_score * 100),
      color: '#FFB7C5' // 粉色
    }
  ];
  option =  {
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
      data: allDates,
      axisLabel: { rotate: 45 }
    },
    yAxis: [ // 双Y轴配置
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
        yAxisIndex: 1, // 指定左轴
        data: alignData(economicData, 'cpi'),
        smooth: true,
        itemStyle: { color: '#5470C6' }
      },
      {
        name: '投资',
        type: 'line',
        yAxisIndex: 1, // 指定右轴
        data: alignData(economicData, 'investment'),
        smooth: true,
        itemStyle: { color: '#91CC75' }
      },
      {
        name: '销售率',
        type: 'line',
        yAxisIndex: 1,
        data: alignData(economicData, 'sales_rate'),
        smooth: true,
        itemStyle: { color: '#FAC858' }
      },
      {
        name: '实际情感',
        type: 'line',
        data: alignData(sentimentData, 'sentiment_score', 100),
        smooth: true,
        itemStyle: { color: '#FF6B6B' },
        markLine: {
          triggerEvent: true,
          data: [{ xAxis: changePointIndex }],
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
        data: alignData(
            timeData.casual_impact_analysis.counterfactual_predictions.dates
                .map((d, i) => ({
                  year: d.year,
                  month: d.month,
                  sentiment_score: timeData.casual_impact_analysis
                      .counterfactual_predictions.predicted_sentiment[i]
                })),
            'sentiment_score',
            100
        ),
        smooth: true,
        itemStyle: { color: '#A685E2' }
      },
      {
        name: '置信区间',
        type: 'line',
        data: alignData(
            timeData.casual_impact_analysis.counterfactual_predictions.dates
                .map((d, i) => ({
                  year: d.year,
                  month: d.month,
                  value: timeData.casual_impact_analysis
                      .counterfactual_predictions.ci_upper[i] * 100
                })),
            'value'
        ),
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
        data: alignData(
            timeData.casual_impact_analysis.counterfactual_predictions.dates
                .map((d, i) => ({
                  year: d.year,
                  month: d.month,
                  value: timeData.casual_impact_analysis
                      .counterfactual_predictions.ci_lower[i] * 100
                })),
            'value'
        ),
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

  option && myChart.setOption(option);
});
</script>

<template>

  <div id="main" style="width: 100%; height: 400px;"></div>
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
