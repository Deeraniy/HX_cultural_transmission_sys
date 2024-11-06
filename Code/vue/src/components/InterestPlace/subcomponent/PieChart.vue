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
  position: 'inside',
  formatter: (params) => {
    return `${params.name}\n数量: ${params.value}\n比例: ${params.percent}%`
  },
  backgroundColor: 'rgba(0,0,0,0.5)',  // 半透明背景
  borderRadius: 5,
  padding: [5, 10],  // 内边距使标签不贴边
  color: '#FFF',     // 字体颜色
  fontWeight: 'bold' // 加粗字体
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
