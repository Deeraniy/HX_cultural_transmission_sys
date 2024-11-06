<template>
  <div ref="pieChart"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import { onMounted, ref, watch } from 'vue'
import { defineProps } from 'vue'

const pieChart = ref(null)
const props = defineProps({
  chartData: {
    type: Array,
    required: true
  }
})

const chartColors = ['#57A773', '#FF6B6B', '#4ECDC4']
const labelOptions = {
  show: true,
  //position: 'inside',
  formatter: '{b}: {d}%'
}

const updateChart = (chart, data) => {
  const option = {
    series: [
      {
        type: 'pie',
        data: data,
        color: chartColors,
        label: labelOptions
      }
    ]
  }
  chart.setOption(option)
}

let chartInstance

onMounted(() => {
  chartInstance = echarts.init(pieChart.value)
  updateChart(chartInstance, props.chartData)
})

watch(() => props.chartData, (newChartData) => {
  if (newChartData) {
    updateChart(chartInstance, newChartData)
  }
})
</script>
