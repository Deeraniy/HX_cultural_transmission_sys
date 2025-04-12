<template>
  <div ref="lineChart" style="width: 100%; height: 400px;"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import { defineProps, onMounted, ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// 接收从父组件传递的 chartData
const props = defineProps({
  chartData: {
    type: Object,
    required: true,
    default: () => ({
      xAxis: [],     // X轴数据
      yAxis: []      // 原有Y轴折线图数据
    })
  }
})

const lineChart = ref(null)
let chartInstance

// 随机生成喜好程度数据
const generateRandomData = (length) => {
  return Array.from({ length }, () => Math.floor(Math.random() * 200) + 50)
}

const updateChart = (chart, data) => {
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross',
        crossStyle: {
          color: '#999'
        }
      }
    },
    toolbox: {
      feature: {
        dataView: { show: true, readOnly: false },
        magicType: { show: true, type: ['line', 'bar'] },
        restore: { show: true },
        saveAsImage: { show: true }
      }
    },
    legend: {
      data: [t('detail.place.preference'), t('detail.place.visitCount')] // 图例名称
    },
    xAxis: {
      type: 'category',
      data: data.xAxis,
      axisPointer: {
        type: 'shadow'
      }
    },
    yAxis: [
      {
        type: 'value',
        name: t('detail.place.preference'),
        min: 0,
        max: 250,
        interval: 50,
        axisLabel: {
          formatter: '{value}'
        }
      },
      {
        type: 'value',
        name: t('detail.place.visitCount'),
        min: 0,
        max: 300,
        interval: 50,
        axisLabel: {
          formatter: '{value}'
        }
      }
    ],
    series: [
      {
        name: t('detail.place.preference'),
        type: 'bar',
        data: generateRandomData(data.xAxis.length),
        tooltip: {
          valueFormatter: function (value) {
            return value + t('detail.place.preferenceUnit');
          }
        }
      },
      {
        name: t('detail.place.visitCount'),
        type: 'line',
        yAxisIndex: 1,
        data: data.yAxis,
        tooltip: {
          valueFormatter: function (value) {
            return value + t('detail.place.visitUnit');
          }
        }
      }
    ]
  }
  chart.setOption(option)
}

onMounted(() => {
  chartInstance = echarts.init(lineChart.value)
  updateChart(chartInstance, props.chartData)
})

// 监听数据变化，更新图表
watch(() => props.chartData, (newChartData) => {
  if (newChartData) {
    updateChart(chartInstance, newChartData)
  }
})
</script>

<style scoped>
/* 可根据需要设置宽高 */
</style>
