<template>
  <div ref="lineChart"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import { defineProps, onMounted, ref, watch } from 'vue'

const lineChart = ref(null)
const props = defineProps({
  chartData: {
    type: Array,
    required: true
  }
})

const xAxisOptions = {
  type: 'category',
  name: '年份'
}

const yAxisOptions = {
  type: 'value',
  name: '参观数量'
}

const updateChart = (chart, data) => {
  const option = {
    xAxis: { ...xAxisOptions, data: data.xAxis },
    yAxis: yAxisOptions,
    series: [
      {
        data: data.yAxis,
        type: 'line',
        label: {
          show: true,
          position: 'inside'
        }
      }
    ]
  }
  chart.setOption(option)
}

let chartInstance

onMounted(() => {
  chartInstance = echarts.init(lineChart.value)
  updateChart(chartInstance, props.chartData)
})

watch(() => props.chartData, (newChartData) => {
  if (newChartData) {
    updateChart(chartInstance, newChartData)
  }
})
</script>
