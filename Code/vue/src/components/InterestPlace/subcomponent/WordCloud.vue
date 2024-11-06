<!--<template>
  <div ref="wordCloud" style="width: 100%; height: 300px;"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import 'echarts-wordcloud'
import { onMounted, ref } from 'vue'

const wordCloud = ref(null)

onMounted(() => {
  const chart = echarts.init(wordCloud.value)
  const option = {
    series: [
      {
        type: 'wordCloud',
        data: [
          { name: 'Amazing', value: 50 },
          { name: 'Beautiful', value: 40 },
          { name: 'Convenient', value: 30 },
          { name: '美不胜收', value: 50 },
          { name: '风景如画', value: 45 },
          { name: '山清水秀', value: 40 },
          { name: '鸟语花香', value: 35 },
          { name: '心旷神怡', value: 30 },
          { name: '诗情画意', value: 48 },
          { name: '流连忘返', value: 42 },
          { name: '神奇', value: 50 },
          { name: '美丽', value: 40 },
          { name: '方便', value: 30 },
          { name: '壮观', value: 45 },
          { name: '宁静', value: 35 },
          { name: '舒适', value: 32 },
          { name: '迷人', value: 48 },
          { name: '独特', value: 38 },
          { name: '宜人', value: 33 },
          { name: '幽静', value: 31 },
          // 其他词汇
        ],
        gridSize: 20,
        sizeRange: [12, 60],
        rotationRange: [-90, 90],
        shape: 'circle',
        textStyle: {
          normal: {
            color: function () {
              return 'rgb(' + [
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160),
                Math.round(Math.random() * 160)
              ].join(',') + ')';
            }
          }
        }
      }
    ]
  }
  chart.setOption(option)
})
</script>

<style scoped>
.word-cloud-container {
  width: 100%;
  height: 300px;
}
</style>-->
<template>
  <div ref="wordCloud" style="width: 100%; height: 300px;"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import 'echarts-wordcloud'
import { onMounted, ref } from 'vue'
const props=defineProps({
  wordCloudData: {
    type: Array,
    required: true
}})
const wordCloud = ref(null)

onMounted(() => {
  const chart = echarts.init(wordCloud.value)
  const option = {
    series: [
      {
        type: 'wordCloud',
        data:props.wordCloudData,
        /*[
          { name: 'Amazing', value: 50 },
          { name: 'Beautiful', value: 40 },
          { name: 'Convenient', value: 30 },
          { name: '美不胜收', value: 50 },
          { name: '风景如画', value: 45 },
          { name: '山清水秀', value: 40 },
          { name: '鸟语花香', value: 35 },
          { name: '心旷神怡', value: 30 },
          { name: '诗情画意', value: 48 },
          { name: '流连忘返', value: 42 },
          { name: '神奇', value: 50 },
          { name: '美丽', value: 40 },
          { name: '方便', value: 30 },
          { name: '壮观', value: 45 },
          { name: '宁静', value: 35 },
          { name: '舒适', value: 32 },
          { name: '迷人', value: 48 },
          { name: '独特', value: 38 },
          { name: '宜人', value: 33 },
          { name: '幽静', value: 31 },
          // 其他词汇
        ]*/
        gridSize: 20,
        sizeRange: [12, 60],
        rotationRange: [-90, 90],
        shape: 'circle',
        textStyle: {
          normal: {
            color: function () {
              const colors = [
                '#FF6F61', '#6B5B95', '#88B04B', '#F7CAC9', '#92A8D1',
                '#955251', '#B565A7', '#FFD393', '#E6E6FA', '#FFB6C1',
                '#ADD8E6', '#9ACD32', '#FFA07A', '#DAA520', '#90EE90',
                '#FFDEAD', '#FF69B4', '#8A2BE2', '#FF4500', '#7CFC00'
              ];
              return colors[Math.floor(Math.random() * colors.length)];
            },
            fontFamily: 'Arial, sans-serif',
            fontWeight: 'bold',
            fontSize: 12
          },
          emphasis: {
            shadowBlur: 10,
            shadowColor: '#333'
          }
        }
      }
    ]
  }
  chart.setOption(option)
})
</script>

<style scoped>
.word-cloud-container {
  width: 100%;
  height: 300px;
}
</style>
