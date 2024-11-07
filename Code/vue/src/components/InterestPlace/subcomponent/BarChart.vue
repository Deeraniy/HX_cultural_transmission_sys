<template>
  <div ref="barChart" style="width: 100%; height: 100%;"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import { onMounted, watch, ref } from 'vue'
import { defineProps } from 'vue'

const props = defineProps({
  chartData: {
    type: Array,
    required: true,
  }
})

const barChart = ref(null)
let chartInstance

const initializeChart = () => {
  chartInstance = echarts.init(barChart.value)

  const option = {
    title: {
      text: '喜好程度与参观数量分析',
      left: 'center',
      bottom: '0%',
      textStyle: {
        color: '#333',
        fontSize: 18,
      },
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['喜好程度', '参观数量'],
      top: '10%',
    },
    xAxis: {
      type: 'category',
      data: props.chartData.map(item => item.topic), // X轴数据为词汇
    },
    yAxis: [
      {
        type: 'value',
        name: '喜好程度',
        min: 0,
        max: 250,
        position: 'left',
        axisLabel: {
          formatter: '{value} 点'
        }
      },
      {
        type: 'value',
        name: '参观数量',
        min: 0,
        max: 5000,
        position: 'right',
        axisLabel: {
          formatter: '{value} 次'
        }
      }
    ],
    series: [
      {
        name: '喜好程度',
        type: 'bar',
        data: props.chartData.map(item => item.frequency), // 以频率表示喜好程度
        yAxisIndex: 0,
        itemStyle: {
          color: '#5470c6'
        }
      },
      {
        name: '参观数量',
        type: 'bar',
        data: props.chartData.map(item => Math.floor(Math.random() * 5000)), // 随机生成参观数量
        yAxisIndex: 1,
        itemStyle: {
          color: '#91cc75'
        }
      }
    ]
  }

  chartInstance.setOption(option)
}

onMounted(() => {
  initializeChart()
})

watch(() => props.chartData, (newData) => {
  if (chartInstance && newData) {
    initializeChart()
  }
})
</script>

<style scoped>

</style>
