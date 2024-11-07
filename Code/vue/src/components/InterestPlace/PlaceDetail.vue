<template>
  <div class="common-layout">
    <el-container style="height: 100vh; overflow: auto;">
      <el-header class="header" style="height:90px;width: 100%">
        <Header :title="attractionName"/>
<!--       {{attractionName}}-->
      </el-header>
      <el-main class="main">
        <div class="content">
          <!-- 图片和弹幕区域 -->
          <div class="image-danmu-container">
            <img src="https://newbbs-fd.zol-img.com.cn/t_s1200x5000/g7/M00/06/0D/ChMkLGMemR2Ib0M8AAeC6JO1m20AAHa6gLY1ukAB4MA189.jpg" alt="城市图片" class="city-image" />
            <img src="@/assets/CS.png" alt="城市词云图" class="wordcloud" />
            <div class="danmu">
              <danmaku ref="danmakuRef" v-model:danmus="danmus" :speeds="50" useSlot loop :channels="7" style="height:100%; width:100%;">
                <template v-slot:dm="{ danmu }">
                  <div class="danmu-item">
                    <span class="bullet-item" :style="{ color: getRandomColor() }">
                      {{ danmu.name }}：{{ danmu.text }}
                    </span>
                  </div>
                </template>
              </danmaku>
            </div>
          </div>

          <!-- BarChart和SentimentStats在同一行 -->
          <div class="charts-row">
            <BarChart :chartData="sentiment" style="width: 70%; height: 400px;" />
            <PieChart :chartData="data1" style="width: 30%; height: 400px;" />
          </div>

          <!-- PieChart和WordCloud上下并列，与TopicCluster同一行 -->
          <div class="mixed-charts-row">
            <SentimentStats :tableData="sentiment" style="width: 50%; height: 500px; border: 15px" />
            <TopicCluster :tableData="topic" style="width: 50%; height: 500px; justify-self: right;" />
          </div>
        </div>
        <LineRace  style="width: 100%; height: 500px;" />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import Header from "@/components/InterestPlace/subcomponent/Header.vue";
import BarChart from "@/components/InterestPlace/subcomponent/BarChart.vue";
import PieChart from "@/components/InterestPlace/subcomponent/PieChart.vue";
import TopicCluster from "@/components/InterestPlace/subcomponent/TopicCluster.vue";
import LineChart from "@/components/InterestPlace/subcomponent/LineChart.vue";
import WordCloud from "@/components/InterestPlace/subcomponent/WordCloud.vue";
import SentimentStats from "@/components/InterestPlace/subcomponent/SentimentStats.vue";
import data1 from "@/json/data1.json";
import data2 from "@/json/data2.json";
import sentiment from "@/json/sentiment.json";
import topic from '@/json/topic.json';
import wordcloud from '@/json/wordCloud.json';
import danmaku from 'vue3-danmaku';
import danmuData from '@/json/danmuData.json';
import LineRace from "@/components/InterestPlace/subcomponent/LineRace.vue";

const danmus = ref(danmuData);
const colorList = ref(['rgb(204,255,255)', 'white', 'rgb(204,255,204)', 'white', 'rgb(0,255,255)', 'white', 'rgb(255,204,255)', 'pink']);
// 生成随机颜色的函数
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
const route = useRoute();
const attractionName = ref('');

onMounted(() => {
  fetchAttractionName();
});

const fetchAttractionName = () => {
  attractionName.value = route.query.name;
  console.log("name",route.query.name);
};
watch(() => route.query.name, (newAttractionName) => {
  attractionName.value = newAttractionName;
}, { immediate: true });

function getRandomColor() {
  const color = colorList.value[Math.floor(Math.random() * 8)];
  return color;
}
</script>

<style scoped>
.common-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-image: url('@/assets/img2.png');
  background-color: #fff8f0;
  width: 100%;
}

.image-danmu-container {
  display: flex;
  align-items: center;
  gap: 25px;
}
.wordcloud {
  object-fit: contain; /* 确保图片不裁剪 */
  width: 300px;
}
.el-header{
  padding: 0;
}
.city-image{
  width: 400px; /* 设置图片和词云图的宽度一致 */
  height: 305px; /* 设置图片和词云图的高度一致 */
  object-fit: cover;
  border-radius: 8px;
}

.danmu {
  flex: 1;
  height: 285px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: rgba(0, 0, 0, 0.5);
  position: relative;
  padding: 10px;
}

.danmu-item {
  white-space: nowrap;
  color: #FFFFFF;
  font-size: 16px;
  background-color: rgba(0, 0, 0, 0.3);
  padding: 4px 10px;
  border-radius: 15px;
  margin-bottom: 8px;
}

.charts-row {
  display: flex;
  width: 100%;
  margin-top: 20px;
  gap: 10px;
}

/* 新增的混合布局，包含PieChart和WordCloud的容器，并与TopicCluster同一行 */
.mixed-charts-row {
  display: flex;
  width: 100%;
  margin-top: 20px;
  gap: 20px;
}

.pie-wordcloud-container {
  display: flex;
  flex-direction: column;
  width: 49%; /* 调整宽度使得与TopicCluster并列 */
  gap: 10px;
}


.main {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
