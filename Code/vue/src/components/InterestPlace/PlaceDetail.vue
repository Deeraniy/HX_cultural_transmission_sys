<template>
  <div class="common-layout">
    <el-container style="height: 100vh; overflow: auto;">
      <el-header class="header" >
        <Header/>
      </el-header>
      <el-main class="main"><<div class="content" >
        <div class="charts" >
          <PieChart :chartData="data1" style="width: 50%;height:300px;"/>
          <LineChart :chartData="data2" style="width: 50%;height: 300px"/>
        </div>
        <div style="display: flex;margin-bottom: 30px">
          <!--词云图-->
             <WordCloud :wordCloudData="wordcloud" style="width: 50%;height:400px"/>
<!--         情感统计表 -->
            <SentimentStats :tableData="sentiment" style="width: 50%;height:400px"/>
        </div>
<!--              主题聚类表 -->
        <div class="topic-cluster" >
          <TopicCluster :tableData="topic" style="width: 70%;height: 500px;justify-self: center"/>
        </div>
      </div></el-main>
      <el-footer class="footer"><Footer/></el-footer>
    </el-container>
  </div>
</template>

<style scoped>
.common-layout {
  height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100%;
}

el-container {
  flex: 1;
  display: flex;
  flex-direction: column;

}

.header, .main, .footer {
  text-align: center;
  color: white;
}

.header {
  background-color: #d32f2f; /* 红色 */
  height: 120px;
  line-height: 20px;
}

.main {
  background-color: #fff8f0; /* 较浅的红色 */
  flex: 1;
  padding: 20px;
  overflow-y: auto; /* 支持上下滑动 */
}

.footer {
  background-color: #d32f2f; /* 红色 */
  height: 60px;
  line-height: 60px;
}
.charts {
  display: flex;
}
</style>

<script setup>

import Header from "@/components/InterestPlace/subcomponent/Header.vue";
import Footer from "@/components/InterestPlace/subcomponent/Footer.vue";
import PieChart from "@/components/InterestPlace/subcomponent/PieChart.vue";
import TopicCluster from "@/components/InterestPlace/subcomponent/TopicCluster.vue";
import LineChart from "@/components/InterestPlace/subcomponent/LineChart.vue";
import WordCloud from "@/components/InterestPlace/subcomponent/WordCloud.vue";
import SentimentStats from "@/components/InterestPlace/subcomponent/SentimentStats.vue";
import data1 from "@/json/data1.json"
import data2 from "@/json/data2.json"
import sentiment from "@/json/sentiment.json"
import topic from '@/json/topic.json'
import wordcloud from '@/json/wordCloud.json'
</script>
