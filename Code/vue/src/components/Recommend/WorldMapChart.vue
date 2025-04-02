<template>
  <div class="world-map-container">
    <div ref="chartContainer" class="chart-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import * as echarts from 'echarts';
import worldJson from '@/json/world.json';

const chartContainer = ref(null);
let chart = null;

// 生成随机饼图数据
const generatePieData = (region) => {
  const themes = ['名胜古迹', '美食文化', '影视文学', '非遗民俗'];
  return themes.map(theme => ({
    value: Math.round(Math.random() * 100),
    name: theme
  }));
};

// 创建饼图系列
const createPieSeries = (center, radius, regionName) => {
  return {
    type: 'pie',
    coordinateSystem: 'geo',
    tooltip: {
      formatter: (params) => {
        return `${regionName}<br/>${params.name}: ${params.value} (${params.percent}%)`
      }
    },
    label: {
      show: false
    },
    labelLine: {
      show: false
    },
    animationDuration: 0,
    radius,
    center,
    data: generatePieData(regionName)
  };
};

const initChart = async () => {
  if (!chartContainer.value) return;

  // 创建 ECharts 实例
  chart = echarts.init(chartContainer.value);
  chart.showLoading();

  try {
    // 注册世界地图
    echarts.registerMap('world', worldJson);

    // 配置项
    const option = {
      backgroundColor: '#f5f5f5',
      geo: {
        map: 'world',
        roam: true,
        zoom: 1.2,
        center: [10, 30],
        itemStyle: {
          areaColor: '#e7e8ea',
          borderColor: '#ccc'
        },
        emphasis: {
          itemStyle: {
            areaColor: '#b71c1c',
            borderColor: '#fff'
          }
        }
      },
      tooltip: {
        trigger: 'item'
      },
      legend: {
        data: ['名胜古迹', '美食文化', '影视文学', '非遗民俗'],
        orient: 'vertical',
        right: 10,
        top: 'center',
        textStyle: {
          color: '#333'
        }
      },
      series: [
        // 主要地区的饼图
        createPieSeries([116.4, 39.9], 20, '中国'),
        createPieSeries([-95, 39.8], 15, '美国'),
        createPieSeries([37, 55], 15, '俄罗斯'),
        createPieSeries([139, 35], 15, '日本'),
        createPieSeries([10, 51], 15, '欧洲')
      ]
    };

    chart.hideLoading();
    chart.setOption(option);
  } catch (error) {
    console.error('加载世界地图数据失败:', error);
    chart.hideLoading();
  }
};

onMounted(() => {
  initChart();
  
  // 添加窗口大小变化的监听
  window.addEventListener('resize', () => {
    chart?.resize();
  });
});

onUnmounted(() => {
  // 清理
  chart?.dispose();
  window.removeEventListener('resize', () => {
    chart?.resize();
  });
});
</script>

<style scoped>
.world-map-container {
  width: 100%;
  height: 100%;
  background: #f5f5f5;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.chart-container {
  width: 100%;
  height: 100%;
  min-height: 500px;
  padding: 20px;
  box-sizing: border-box;
}
</style> 