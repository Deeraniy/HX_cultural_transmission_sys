<template>
  <div ref="lineRaceChart" style="width: 100%; height: 600px;"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import { onMounted, ref } from 'vue'

const lineRaceChart = ref(null)
let chartInstance = null

// 随机生成数据
function generateRandomData() {
  const data = [];
  const countries = [
    'Finland', 'France', 'Germany', 'Iceland', 'Norway', 'Poland', 'Russia', 'United Kingdom'
  ];

  countries.forEach(country => {
    for (let year = 1950; year <= 2020; year++) {
      data.push({
        Year: year,
        Country: country,
        Income: Math.floor(Math.random() * 50000) + 10000  // 随机生成收入数据
      });
    }
  });

  return data;
}

// 设置图表选项
function setChartOption(data) {
  const countries = [
    'Finland', 'France', 'Germany', 'Iceland', 'Norway', 'Poland', 'Russia', 'United Kingdom'
  ];
  const datasetWithFilters = [];
  const seriesList = [];

  echarts.util.each(countries, function (country) {
    var datasetId = 'dataset_' + country;
    datasetWithFilters.push({
      id: datasetId,
      fromDatasetId: 'dataset_raw',
      transform: {
        type: 'filter',
        config: {
          and: [
            { dimension: 'Year', gte: 1950 },
            { dimension: 'Country', '=': country }
          ]
        }
      }
    });
    seriesList.push({
      type: 'line',
      datasetId: datasetId,
      showSymbol: false,
      name: country,
      endLabel: {
        show: true,
        formatter: function (params) {
          return params.value[3] + ': ' + params.value[0];
        }
      },
      labelLayout: {
        moveOverlap: 'shiftY'
      },
      emphasis: {
        focus: 'series'
      },
      encode: {
        x: 'Year',
        y: 'Income',
        label: ['Country', 'Income'],
        itemName: 'Year',
        tooltip: ['Income']
      }
    });
  });

  return {
    animationDuration: 10000,
    dataset: [
      {
        id: 'dataset_raw',
        source: data
      },
      ...datasetWithFilters
    ],
    title: {
      text: 'Income of Selected European Countries since 1950',
      bottom: 0,  // 将标题放置在图表底部
      left: 'center'  // 水平居中
    },
    tooltip: {
      order: 'valueDesc',
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      nameLocation: 'middle'
    },
    yAxis: {
      name: 'Income'
    },
    grid: {
      right: 140
    },
    series: seriesList
  };
}

// 初始化图表并设置选项
function initChart() {
  if (lineRaceChart.value) {
    chartInstance = echarts.init(lineRaceChart.value)
    const data = generateRandomData();
    const option = setChartOption(data);
    chartInstance.setOption(option);
  }
}

onMounted(() => {
  initChart();
});
</script>

<style scoped>
#lineRaceChart {
  width: 100%;
  height: 600px;
}
</style>
