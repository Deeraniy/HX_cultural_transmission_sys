<template>
  <div ref="barChart" style="width: 100%; height: 100%;"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import { onMounted, ref, watch, onUnmounted } from 'vue'

// 引入 props
const props = defineProps({
  chartData: {
    type: Array,
    required: true
  },
  chartType: {
    type: String,
    default: 'sentiment'
  }
})

// 图表容器的 ref
const barChart = ref(null)

// 图表实例
let chartInstance = null

// 初始化和更新图表的函数
const updateChart = (chart, data, type) => {
  // 检查数据是否有效
  if (!data || data.length === 0) {
    console.warn('No valid data provided for chart');
    return;
  }
  
  console.log('Updating chart with data:', data, 'type:', type);
  
  // 根据类型处理数据
  let categories = [], positiveData = [], neutralData = [], negativeData = [];
  
  if (type === 'sentiment') {
    // 情感分析数据处理 - 使用 word 字段
    data.forEach(item => {
      if (item.word) {
        categories.push(item.word);
        
        if (item.sentiment === 'positive') {
          positiveData.push(item.frequency);
          neutralData.push(0);
          negativeData.push(0);
        } else if (item.sentiment === 'neutral') {
          positiveData.push(0);
          neutralData.push(item.frequency);
          negativeData.push(0);
        } else if (item.sentiment === 'negative') {
          positiveData.push(0);
          neutralData.push(0);
          negativeData.push(item.frequency);
        }
      }
    });
  } else {
    // 主题聚类数据处理 - 使用 topic 字段
    data.forEach(item => {
      if (item.topic) {
        categories.push(item.topic);
        
        if (item.sentiment === 'positive') {
          positiveData.push(item.frequency);
          neutralData.push(0);
          negativeData.push(0);
        } else if (item.sentiment === 'neutral') {
          positiveData.push(0);
          neutralData.push(item.frequency);
          negativeData.push(0);
        } else if (item.sentiment === 'negative') {
          positiveData.push(0);
          neutralData.push(0);
          negativeData.push(item.frequency);
        }
      }
    });
  }
  
  console.log('Processed data:', {
    categories,
    positiveData,
    neutralData,
    negativeData
  });

  // 设置图表选项
  const option = {
    title: {
      text: type === 'sentiment' ? '词语情感分析' : '主题情感分析',
      left: '45%',
      top: 30,
      textStyle: {
        fontSize: 18,
        fontWeight: 'bold',
        fontFamily: 'HelveticaNeue, serif'
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['正面', '中性', '负面'],
      top: 70,
      left: '40%',
      textStyle: {
        fontSize: 14,
        fontFamily: 'HelveticaNeue, serif'
      }
    },
    grid: {
      left: '5%',
      right: '5%',
      bottom: '10%',
      top: '35%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLabel: {
        interval: 0,
        rotate: 30,
        fontSize: 12,
        margin: 15,
        fontFamily: 'HelveticaNeue, serif'
      }
    },
    yAxis: {
      type: 'value',
      name: '频率',
      nameTextStyle: {
        fontSize: 14,
        fontFamily: 'HelveticaNeue, serif'
      },
      axisLabel: {
        fontSize: 12,
        fontFamily: 'HelveticaNeue, serif'
      }
    },
    series: [
      {
        name: '正面',
        type: 'bar',
        stack: 'total',
        barWidth: '50%',
        itemStyle: {
          color: '#57A773' // 绿色
        },
        emphasis: {
          focus: 'series'
        },
        data: positiveData
      },
      {
        name: '中性',
        type: 'bar',
        stack: 'total',
        barWidth: '50%',
        itemStyle: {
          color: '#FFD166' // 黄色
        },
        emphasis: {
          focus: 'series'
        },
        data: neutralData
      },
      {
        name: '负面',
        type: 'bar',
        stack: 'total',
        barWidth: '50%',
        itemStyle: {
          color: '#FF6B6B' // 红色
        },
        emphasis: {
          focus: 'series'
        },
        data: negativeData
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
  console.log('BarChart mounted with data:', props.chartData, 'type:', props.chartType)
  
  // 初始化图表实例
  chartInstance = echarts.init(barChart.value)
  
  // 首次渲染图表
  if (props.chartData && props.chartData.length > 0) {
    updateChart(chartInstance, props.chartData, props.chartType)
  }
  
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
  
  if (barChart.value) {
    resizeObserver.observe(barChart.value);
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

// 监听数据和类型变化并更新图表
watch(
  () => [props.chartData, props.chartType], 
  ([newChartData, newChartType]) => {
    if (newChartData && newChartData.length > 0 && chartInstance) {
      updateChart(chartInstance, newChartData, newChartType);
      // 添加延时重绘
      setTimeout(() => {
        resizeChart();
      }, 0);
    }
  },
  { deep: true }
)

// 导出 resizeChart 方法供父组件调用
defineExpose({
  resizeChart
})
</script>

<style scoped>
/* 让图表容器可以自适应父元素的宽高 */
div[ref="barChart"] {
  width: 100%;
  height: 100%;
  min-height: 300px; /* 添加最小高度 */
}
</style>
