<template>
  <div ref="pieChart" style="width: 100%; height: 100%;"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import { onMounted, ref, watch, onUnmounted } from 'vue'
import { defineProps } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// 添加情感类型映射
const sentimentTypeMap = {
  '正面': 'positive',
  '中立': 'neutral',
  '负面': 'negative'
}

// 获取情感类型的英文映射
const getSentimentType = (chineseName) => {
  return sentimentTypeMap[chineseName] || chineseName.toLowerCase()
}

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
const chartColors = ['#57A773', '#FFD166', '#FF6B6B'] // 绿、黄、红对应正面、中性、负面
const labelOptions = {
  show: true,
  position: 'inside',
  formatter: (params) => {
    const sentimentType = getSentimentType(params.name)
    return `${t(`detail.report.sentiment.${sentimentType}`)}\n${t('detail.sentiment.count')}: ${params.value}\n${t('detail.sentiment.ratio')}: ${params.percent}%`
  },
  backgroundColor: 'rgba(0,0,0,0.5)', // 半透明背景
  borderRadius: 5,
  padding: [5, 10], // 内边距使标签不贴边
  color: '#FFF', // 字体颜色
  fontFamily: 'HelveticaNeue, serif',
  fontSize: 14,
}

// 初始化和更新图表的函数
const updateChart = (chart, data) => {
  // 处理数据，将中文情感类型映射为英文
  const processedData = data.map(item => ({
    ...item,
    name: getSentimentType(item.name)
  }))

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        const sentimentType = getSentimentType(params.name)
        return `${t('detail.sentiment.analysis')} <br/>${t(`detail.report.sentiment.${sentimentType}`)}: ${params.value} (${params.percent}%)`
      },
      textStyle: {
        fontFamily: 'HelveticaNeue, serif',
        fontSize: 16
      }
    },
    legend: {
      orient: 'vertical',  // 垂直方向
      right: '5%',         // 放置在右侧
      top: 'middle',       // 垂直居中
      data: processedData.map(item => t(`detail.report.sentiment.${item.name}`)),
      textStyle: {
        color: '#333', // 图例文本颜色
        fontSize: 14,
        fontFamily: 'HelveticaNeue, serif'
      },
      formatter: (name) => {
        const sentimentType = getSentimentType(name)
        return t(`detail.report.sentiment.${sentimentType}`)
      },
      itemWidth: 15,      // 图例标记的宽度
      itemHeight: 15,     // 图例标记的高度
      itemGap: 15         // 图例项之间的间距
    },
    series: [
      {
        name: t('detail.sentiment.analysis'),
        type: 'pie',
        radius: ['45%', '93%'], // 调整环形饼图的内外半径
        center: ['35%', '50%'], // 将饼图更靠左，为右侧图例腾出更多空间
        avoidLabelOverlap: false,
        data: processedData.map(item => ({
          ...item,
          name: item.name,
          value: item.value
        })),
        color: chartColors,
        label: labelOptions,
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontFamily: 'HelveticaNeue, serif',
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

// 添加一个重置图表大小的函数
const resizeChart = () => {
  if (chartInstance) {
    chartInstance.resize();
  }
}

onMounted(() => {
  console.log('子组件接收到的 chartData:', props.chartData)
  // 初始化图表实例
  chartInstance = echarts.init(pieChart.value)

  // 首次渲染图表
  updateChart(chartInstance, props.chartData)
  
  // 使用防抖函数处理 resize 事件
  const handleResize = () => {
    if (chartInstance) {
      chartInstance.resize()
    }
  }
  
  // 添加 ResizeObserver 监听容器大小变化
  const resizeObserver = new ResizeObserver(() => {
    handleResize();
  });
  
  if (pieChart.value) {
    resizeObserver.observe(pieChart.value);
  }
  
  // 添加窗口大小变化的监听器
  window.addEventListener('resize', handleResize)
  
  // 在组件卸载时清理
  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
    resizeObserver.disconnect();
    if (chartInstance) {
      chartInstance.dispose()
    }
  })
})

// 监听数据变化并更新图表
watch(() => props.chartData, (newChartData) => {
  if (newChartData && chartInstance) {
    updateChart(chartInstance, newChartData)
  }
})

// 导出 resizeChart 方法供父组件调用
defineExpose({
  resizeChart
})
</script>

<style scoped>
/* 让饼图容器可以自适应父元素的宽高 */
div[ref="pieChart"] {
  width: 100%;
  height: 100%;
  min-height: 300px; /* 添加最小高度 */
}
</style>
