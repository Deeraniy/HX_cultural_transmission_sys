<template>
  <div class="common-layout">
    <el-container style="height: 100vh; overflow: auto;">
      <el-header class="header" style="height:90px;width: 100%">
        <Header />
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

<script lang="ts" setup>
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
import CloudAPI from "@/api/cloud";
import danmaku from 'vue3-danmaku';
import danmuData from '@/json/danmuData.json';
import {onMounted, ref} from 'vue';
import LineRace from "@/components/InterestPlace/subcomponent/LineRace.vue";
import SpotsAPI from "@/api/spot";
import SentimentAPI from "@/api/sentiment";
const interestData = ref<any>(null);
const attractions = ref<any | null>(null); // 初始化为 null

const loadAttractions = (spotName: string) => {
  if (!interestData.value || !Array.isArray(interestData.value)) {
    console.warn("景点数据未加载或格式错误");
    return;
  }

  // 查找匹配的单个景点
  const spot = interestData.value.find((spot: any) => spot.spot_name === spotName);
  if (spot) {
    attractions.value = {
      name: spot.spot_name,
      image: spot.image_url,
      description: spot.description,
    };
  } else {
    console.warn(`未找到名称为 "${spotName}" 的景点`);
    attractions.value = null;
  }

  console.log("当前选中的景点:", attractions.value);
};
const danmus = ref(danmuData);
const colorList = ref(['rgb(204,255,255)', 'white', 'rgb(204,255,204)', 'white', 'rgb(0,255,255)', 'white', 'rgb(255,204,255)', 'pink']);
// 生成随机颜色的函数
function getRandomColor() {
  const color = colorList.value[Math.floor(Math.random() * 8)];
  return color;
}

onMounted(async () => {
  try {
    const spotsResponse = await SpotsAPI.getSpotsAPI();

    if (typeof spotsResponse === "string") {
      // 替换 "Decimal('4.40')" 为合法的数字 4.40
      const fixedResponse = spotsResponse.replace(/Decimal\('([\d.]+)'\)/g, '$1');

      // 替换单引号为双引号，解析 JSON 对象
      const spotsArray = fixedResponse
          .replace(/'/g, '"')
          .match(/{[^}]+}/g)
          .map((spot) => JSON.parse(spot));

      interestData.value = spotsArray;

      console.log("景点数据（处理后）:", interestData.value);
    } else {
      console.error("景点数据格式错误，期望为字符串形式");
    }
  } catch (error) {
    console.error("加载景点数据时出错:", error);
  }

});
CloudAPI.getCloudAPI("橘子洲").then((res) => {
  console.log("词云数据:", res);

});
SentimentAPI.getSentimentReportAPI("橘子洲").then((res)=>{
  console.log("ai报告",res)
})

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
