<template>
  <div ref="wordCloud" style="width: 400px; height: 305px;"></div>
</template>

<script setup>
import * as echarts from 'echarts'
import 'echarts-wordcloud'
import { onMounted, ref } from 'vue'

const props = defineProps({
  wordCloudData: {
    type: Array,
    required: true
  }
});

const wordCloud = ref(null);

onMounted(() => {
  const chart = echarts.init(wordCloud.value);
  const option = {
    series: [
      {
        type: 'wordCloud',
        data: props.wordCloudData,
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
  };
  chart.setOption(option);
});
</script>

<style scoped>
.word-cloud-container {
  width: 400px; /* 确保和图片宽度一致 */
  height: 305px; /* 确保和图片高度一致 */
  margin: 0 auto;
}
</style>
