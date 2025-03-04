<script setup>
import { onMounted } from 'vue';
import { Clock, DataAnalysis } from "@element-plus/icons-vue";
import * as echarts from 'echarts';

onMounted(() => {
  var chartDom = document.getElementById('main');
  var myChart = echarts.init(chartDom);
  var option = {
    title: {
      text: 'Basic Radar Chart'
    },
    legend: {
      data: ['Allocated Budget', 'Actual Spending']
    },
    radar: {
      // shape: 'circle',
      indicator: [
        { name: 'Sales', max: 6500 },
        { name: 'Administration', max: 16000 },
        { name: 'Information Technology', max: 30000 },
        { name: 'Customer Support', max: 38000 },
        { name: 'Development', max: 52000 },
        { name: 'Marketing', max: 25000 }
      ]
    },
    series: [
      {
        name: 'Budget vs spending',
        type: 'radar',
        data: [
          {
            value: [4200, 3000, 20000, 35000, 50000, 18000],
            name: 'Allocated Budget'
          },
          {
            value: [5000, 14000, 28000, 26000, 42000, 21000],
            name: 'Actual Spending'
          }
        ]
      }
    ]
  };
  option && myChart.setOption(option);
});
</script>

<template>
  <div>
    <div>
      <el-icon style="font-size: 20px;"><DataAnalysis /></el-icon>
      <el-text class="mainTitle">用户画像</el-text>
    </div>
    <div>
      <!-- Insert the radar chart container here -->
      <div id="main" style="height: 400px;margin-top: 20px"></div>
    </div>
  </div>
</template>

<style scoped>
.mainTitle {
  margin-left: 30px;
  font-size: 18px;
  color: #000;
  font-weight: bolder;
}
</style>
