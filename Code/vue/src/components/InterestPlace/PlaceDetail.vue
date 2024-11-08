<template>
  <div class="common-layout">
    <el-container style="height: 100vh; overflow: auto;">
      <el-header class="header" style="height:90px;width: 100%">
        <Header :title="attractionName"/>
<!--               {{attractionName}}-->
      </el-header>
      <el-main class="main">
        <div class="content">
          <!-- 图片和弹幕区域 -->
          <div class="image-danmu-container">
            <img :src="attractions.image" alt="城市图片" class="city-image" />
            <img :src="cloudUrl" alt="城市词云图" class="wordcloud" />
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
            <SentimentStats :tableData="topic" style="width: 50%; height: 500px; border: 15px" />
            <TopicCluster :tableData="sentiment" style="width: 50%; height: 500px; justify-self: right;" />
          </div>
        </div>
        <LineRace v-if="processedTimeData.length > 0" :timeData="processedTimeData"  style="margin-top: 30px"/>
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
//import data1 from "@/json/data1.json";
import data2 from "@/json/data2.json";
import time from "@/json/time.json"
//import sentiment from "@/json/sentiment.json";
//import topic from '@/json/topic.json';
import wordcloud from '@/json/wordCloud.json';
import CloudAPI from "@/api/cloud";
import danmaku from 'vue3-danmaku';
import LdaAPI from "@/api/lda";
import danmuData from '@/json/danmuData.json';
import LineRace from "@/components/InterestPlace/subcomponent/LineRace.vue";
import SpotsAPI from "@/api/spot";
import CommentAPI from "@/api/comment";
import SentimentAPI from "@/api/sentiment";
const interestData = ref<any>(null);
const attractions = ref<any>({}); // 初始化为一个空对象
const cloudUrl = ref('');
const processedTimeData = ref<any>([]);
const sentiment = ref<any>([]); // LDA 数据绑定到 SentimentStats
const topic = ref<any>([]);
const data1 = [
  { name: '正面', value: 58.84 },
  { name: '中立', value: 7.28 },
  { name: '负面', value: 33.73 }
]
const loadAttractions = (spotName: Ref<UnwrapRef<string>, UnwrapRef<string> | string>) => {
  if (!interestData.value || !Array.isArray(interestData.value)) {
    console.warn("景点数据未加载或格式错误");
    return;
  }

console.log("景点数据（未处理）:", spotName.value);
  // 查找匹配的单个景点
  const spot = interestData.value.find((spot: any) => spot.spot_name === spotName.value);
  if (spot) {
    attractions.value = {
      name: spot.spot_name,
      image: spot.image_url,
      description: spot.description,
    };
    console.log("当前选中的景点:", attractions.name);
  } else {
    console.warn(`未找到名称为 "${spotName}" 的景点`);
    attractions.value = null;
  }

  console.log("当前选中的景点:", attractions);
};
const danmus = ref([]);
const colorList = ref(['rgb(204,255,255)', 'white', 'rgb(204,255,204)', 'white', 'rgb(0,255,255)', 'white', 'rgb(255,204,255)', 'pink']);
// 生成随机颜色的函数
import {ref, onMounted, watch, Ref, UnwrapRef} from 'vue';
import { useRoute } from 'vue-router';
import {marked} from "marked";
const route = useRoute();
const attractionName = ref<string>('');

watch(() => route.query.name, (newAttractionName) => {
  if (typeof newAttractionName === 'string') {
    attractionName.value = newAttractionName;
    console.log("name2", attractionName.value)
  } else {
    console.warn('路由参数 "name" 不是字符串:', newAttractionName);
    attractionName.value = '';
  }
}, { immediate: true });


onMounted(() => {
  fetchAttractionName();
});

const fetchAttractionName = () => {
  attractionName.value = <string>route.query.name;
  console.log("name",route.query.name);
};


function getRandomColor() {
  const color = colorList.value[Math.floor(Math.random() * 8)];
  return color;
}

onMounted(async () => {
  try {
    const spotsResponse = await SpotsAPI.getSpotsAPI();

    if (typeof spotsResponse === "string") {
      const fixedResponse = spotsResponse.replace(/Decimal\('([\d.]+)'\)/g, '$1');
      const spotsArray = fixedResponse
          .replace(/'/g, '"')
          .match(/{[^}]+}/g)
          .map((spot) => JSON.parse(spot));

      interestData.value = spotsArray;

      console.log("景点数据（处理后）:", interestData.value);
      if (interestData.value.length > 0) {
        loadAttractions(attractionName);
      } else {
        console.warn("景点数据为空");
      }
    } else {
      console.error("景点数据格式错误，期望为字符串形式");
    }
  } catch (error) {
    console.error("加载景点数据时出错:", error);
  }


  try {
    const commentResponse = await CommentAPI.getCommentList(attractionName.value);

    console.log("原始评论数据:", commentResponse);

    if (typeof commentResponse === "string") {
      // 1. 修复常见的 JSON 格式问题
      const fixedResponse = commentResponse
          .replace(/None/g, 'null')
          .replace(/Decimal\('([\d.]+)'\)/g, '$1')
          .replace(/'/g, '"')
          .replace(/\\(?!["\\/bfnrtu])/g, '');

      console.log("修复后的评论数据:", fixedResponse);

      // 2. 提取每个 JSON 对象
      const matches = fixedResponse.match(/{[^}]+}/g); // 匹配每个 JSON 对象

      if (matches) {
        const commentsArray = [];

        for (const match of matches) {
          try {
            const comment = JSON.parse(match); // 逐个解析 JSON 对象
            commentsArray.push(comment);
          } catch (jsonError) {
            console.warn("跳过无法解析的 JSON 对象:", match, jsonError); // 输出无法解析的对象
          }
        }

        console.log("成功解析的评论数组:", commentsArray);

        // 映射到弹幕数据
        danmus.value = commentsArray.map(comment => ({
          name: comment.user_id || '匿名用户',
          text: comment.content || '',
        }));
      } else {
        console.warn("未找到有效的 JSON 对象。");
      }
    } else if (Array.isArray(commentResponse)) {
      // 直接处理对象数组
      danmus.value = commentResponse.map(comment => ({
        name: comment.user_id || '匿名用户',
        text: comment.content || '',
      }));
    } else {
      throw new Error("评论数据格式不正确");
    }
  } catch (error) {
    console.error("加载评论数据时出错:", error);
  }


  try {
    const cloudResponse = await CloudAPI.getCloudAPI(attractionName.value);
    console.log("词云地址:", cloudResponse.wordcloud_url);
    cloudUrl.value="http://127.0.0.1:8080"+cloudResponse.wordcloud_url;
  } catch (error) {
    console.error("加载评论数据时出错:", error);
  }
  try {
    const pieResponse = await SentimentAPI.getSentimentPieAPI(attractionName.value);

    if (pieResponse && pieResponse.data) {
      // 格式化为 PieChart 需要的数据结构
      data1.value = [
        { name: '正面', value: parseFloat(pieResponse.data.positive_percentage) },
        { name: '中立', value: parseFloat(pieResponse.data.neutral_percentage) },
        { name: '负面', value: parseFloat(pieResponse.data.negative_percentage) }
      ];

      console.log("饼图数据（处理后）:", data1.value);
    } else {
      console.warn("饼图数据格式不正确:", pieResponse);
    }
  } catch (error) {
    console.error("加载饼图数据时出错:", error);
  }


  try {
    // 获取 LdaResponse 数据
    const ldaResponse = await LdaAPI.LdaAPI(attractionName.value);

    // 检查数据有效性，并格式化为表格需要的格式
    if (Array.isArray(ldaResponse)) {
      sentiment.value = ldaResponse.map(item => ({
        topic: item.topic, // 主题
        frequency: item.frequency, // 出现频率
        sentiment: item.sentiment, // 情感
      }));
      console.log("LDA 数据加载成功:", sentiment.value);
    } else {
      console.warn("LDA 数据格式不正确:", ldaResponse);
    }
  } catch (error) {
    console.error("加载 LDA 数据时出错:", error);
  }

  try {
    // 获取 WordResponse 数据
    const wordResponse = await SentimentAPI.getSentimentWordAPI(attractionName.value);

    // 检查数据有效性，并格式化为表格需要的格式
    if (wordResponse && Array.isArray(wordResponse.data)) {
      topic.value = wordResponse.data.map(item => ({
        word: item.word, // 关键词
        frequency: item.frequency, // 出现频率
        sentiment: item.sentiment, // 情感
      }));
      console.log("Word 数据加载成功:", topic.value);
    } else {
      console.warn("Word 数据格式不正确:", wordResponse);
    }
  } catch (error) {
    console.error("加载 Word 数据时出错:", error);
  }



// 在加载时间情感数据后，赋值给 processedTimeData
  try {
    const timeResponse = await SentimentAPI.getSentimentResultAPI(attractionName.value);
    if (timeResponse && typeof timeResponse === "object" && Array.isArray(timeResponse.data)) {
      processedTimeData.value = timeResponse.data.map(item => {
        const paddedMonth = item.month < 10 ? '0' + item.month : item.month;
        console.log("你好！！！" + parseFloat(item.sentiment_score));
        return {
          date: `${item.year}-${paddedMonth}`,
          sentimentScore: parseFloat(item.sentiment_score) || 0,
          sentiment: item.sentiment,
          commentCount: item.comment_count,
        };
      });

      console.log("时间情感数据（处理后）:", processedTimeData.value);
    }
  } catch (error) {
    console.error("加载时间情感数据时出错:", error);
  }


});

// SentimentAPI.getSentimentReportAPI(attractionName.value).then((res) => {
//   console.log("AI 报告原始 Markdown:", res);
//   markdownContent.value = marked(res); // 将 Markdown 转换为 HTML
//   console.log("AI 报告解析后的 HTML:", markdownContent.value);
// }).catch((error) => {
//   console.error("加载 AI 报告时出错:", error);
// });

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
