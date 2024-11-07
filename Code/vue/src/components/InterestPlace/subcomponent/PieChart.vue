<template>
  <div ref="pieChart" style="width: 100%; height: 100%;"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import { onMounted, ref, watch } from 'vue'
import { defineProps } from 'vue'

// 引入 props
const props = defineProps({
  chartData: {
    type: Array,
    required: true
  }
})

// 饼图容器的 ref
const pieChart = ref(null)

// 图表实例
let chartInstance = null

// 自定义颜色和标签样式
const chartColors = ['#57A773', '#FF6B6B', '#4ECDC4'] // 颜色数组
const labelOptions = {
  show: true,
  position: 'inside',
  formatter: (params) => {
    return `${params.name}\n数量: ${params.value}\n比例: ${params.percent}%`
  },
  backgroundColor: 'rgba(0,0,0,0.5)', // 半透明背景
  borderRadius: 5,
  padding: [5, 10], // 内边距使标签不贴边
  color: '#FFF', // 字体颜色
  fontWeight: 'bold' // 加粗字体
}

// 初始化和更新图表的函数
const updateChart = (chart, data) => {
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{a} <br/>{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'horizontal',
      bottom: '10%',
      data: data.map(item => item.name), // 根据数据动态生成图例
      textStyle: {
        color: '#333', // 图例文本颜色
        fontSize: 14
      }
    },
    series: [
      {
        name: '情感分析',
        type: 'pie',
        radius: ['40%', '70%'], // 设置环形饼图的内外半径
        avoidLabelOverlap: false,
        data: data,
        color: chartColors,
        label: labelOptions,
        emphasis: {
          label: {
            show: true,
            fontSize: '16',
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: true,
          length: 10,
          length2: 10
        }
      }
    ]
  }
  chart.setOption(option)
}

onMounted(() => {
  // 初始化图表实例
  chartInstance = echarts.init(pieChart.value)

  // 首次渲染图表
  updateChart(chartInstance, props.chartData)
})

// 监听数据变化并更新图表
watch(() => props.chartData, (newChartData) => {
  if (newChartData) {
    updateChart(chartInstance, newChartData)
  }
})
</script>

<style scoped>
/* 让饼图容器可以自适应父元素的宽高 */
div[ref="pieChart"] {
  width: 100%;
  height: 100%;
}
</style>
