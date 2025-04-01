<template>
    <div class="common-layout">
      <el-container style="height: 100vh; overflow: auto;">
        <!-- Header 和主内容区域 -->
        <el-header class="header" style="height:90px;width: 100%">
          <Header
              :title="nowName"
              @update:type="handleTypeChange"
              @update:search="handleSearchChange"
          />
        </el-header>
        <el-main class="main">
          <div class="content">
            <!-- 图片和弹幕区域 -->
            <div class="image-danmu-container">
              <!-- 左边加载图 -->
              <div class="city-image-container" style="position: relative; width: 400px; height: 305px;">
                <Loader v-if="isImageLoading" class="loader" />
                <img
                    v-if="!isImageLoading"
                    :src="currentImageUrl"
                    alt="当前展示的图片"
                    :style="{
      height: '300px',
      width: '100%',
      objectFit:  'cover'
    }"
                    class="city-image"
                />
  
  
              </div>
  
              <!-- 词云图和加载动画的区域 -->
              <div class="wordcloud-container" style="position: relative; width: 300px; height: 300px;">
                <Loader v-if="isWordCloudLoading" class="loader" />
                <img
                    v-if="!isWordCloudLoading"
                    :src="cloudUrl"
                    alt="词云图"
                    class="wordcloud"
                />
              </div>
  
              <!-- 弹幕加载动画 -->
              <div class="danmu-container" style="position: relative; width: 600px; height: 305px;">
                <Loader v-if="isDanmuLoading" class="loader" />
                <div v-if="!isDanmuLoading" class="danmu">
                  <danmaku
                      ref="danmakuRef"
                      v-model:danmus="danmus"
                      :speeds="50"
                      useSlot
                      loop
                      :channels="7"
                      style="height: 100%; width: 100%;"
                      :is-suspend="true"
                  >
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
            </div>
  
            <!-- BarChart 和 SentimentStats -->
            <div class="charts-row">
              <div class="chart-container" style="position: relative; width: 70%; height: 400px;">
                <Loader v-if="isBarChartLoading" class="loader" />
                <BarChart
                    v-if="!isBarChartLoading"
                    :chartData="sentiment"
                    style="width: 100%; height: 100%;"
                />
              </div>
              <div class="chart-container" style="position: relative; width: 30%; height: 400px;">
                <Loader v-if="isPieChartLoading" class="loader" />
                <PieChart
                    v-if="!isPieChartLoading && data1 && data1.length > 0"
                    :chartData="data1"
                    style="width: 100%; height: 100%;"
                />
              </div>
            </div>
  
            <!-- PieChart 和 WordCloud -->
            <div class="mixed-charts-row">
              <div class="chart-container" style="position: relative; width: 50%; height: 500px;">
                <Loader v-if="isSentimentStatsLoading" class="loader" />
                <SentimentStats
                    v-if="!isSentimentStatsLoading && topic && topic.length > 0"
                    :tableData="topic"
                    style="width: 100%; height: 100%;"
                />
              </div>
              <div class="chart-container" style="position: relative; width: 50%; height: 500px;">
                <Loader v-if="isTopicClusterLoading" class="loader" />
                <TopicCluster
                    v-if="!isTopicClusterLoading && sentiment && sentiment.length > 0"
                    :tableData="sentiment"
                    style="width: 100%; height: 100%;"
                />
              </div>
            </div>
          </div>
          <LineRace
              v-if="processedTimeData && processedTimeData.length > 0"
              :timeData="processedTimeData"
              style="margin-top: 30px"
          />
          <ThreeLineChart
              v-if="threeLineData && threeLineData.length > 0"
              :timeData="threeLineData"
          />
        </el-main>
      </el-container>
  
    </div>
  </template>
  
  
  <script lang="ts" setup>
  import ThreeLineChart from "@/components/InterestPlace/subcomponent/ThreeLineChart.vue"
  import Header from "@/components/InterestPlace/subcomponent/Header.vue";
  import BarChart from "@/components/InterestPlace/subcomponent/BarChart.vue";
  import PieChart from "@/components/InterestPlace/subcomponent/PieChart.vue";
  import TopicCluster from "@/components/InterestPlace/subcomponent/TopicCluster.vue";
  import LineChart from "@/components/InterestPlace/subcomponent/LineChart.vue";
  import WordCloud from "@/components/InterestPlace/subcomponent/WordCloud.vue";
  import SentimentStats from "@/components/InterestPlace/subcomponent/SentimentStats.vue";
  import Loader from '@/components/Loader.vue';  // 导入 Loader 组件
  //import data1 from "@/json/data1.json";
  //import data2 from "@/json/data2.json";
  //import time from "@/json/time.json"
  //import sentiment from "@/json/sentiment.json";
  //import topic from '@/json/topic.json';
  //import wordcloud from '@/json/wordCloud.json';
  import CloudAPI from "@/api/cloud";
  import danmaku from 'vue3-danmaku';
  import LdaAPI from "@/api/lda";
  //import danmuData from '@/json/danmuData.json';
  import LineRace from "@/components/InterestPlace/subcomponent/LineRace.vue";
  import SpotsAPI from "@/api/spot";
  import FoodAPI from "@/api/food";
  import FolkAPI from "@/api/folk"
  import CommentAPI from "@/api/comment";
  import SentimentAPI from "@/api/sentiment";
  import { ElMessage } from 'element-plus';
  import FilmLiterature from "@/api/filmLiterature";
  
  import * as echarts from 'echarts/core';
  
  
  
  const threeLineData = ref<any>([]);
  const interestData = ref<any>(null);
  const bookData = ref<any>(null);
  const foodData = ref<any>(null);
  const folkData = ref<any>(null);
  
  import router from "@/router.js";
  var option;
  const attractions = ref<any>({}); // 初始化为一个空对象
  const books = ref<any>({});
  const food = ref<any>({});
  const folk = ref<any>({});
  
  const searchQuery = ref(''); // 新增：存储搜索内容
  const cloudUrl = ref('');
  const processedTimeData = ref<any>([]);
  const sentiment = ref<any>([]); // LDA 数据绑定到 SentimentStats
  const topic = ref<any>([]);
  const currentImageUrl = ref<string>(''); // 用于存储当前需要展示的图片 URL
  
  const isLoading = ref(true);  // 控制加载状态
  const isImageLoading = ref(true);
  const isWordCloudLoading = ref(true);
  const isDanmuLoading = ref(true);
  const isBarChartLoading = ref(true);
  const isPieChartLoading = ref(true);
  const isSentimentStatsLoading = ref(true);
  const isTopicClusterLoading = ref(true);
  const isLineRaceLoading = ref(true);
  
  const data1 = ref([  // 将 data1 用 ref 包装成响应式数据
    { name: '正面', value: 58.84 },
    { name: '中立', value: 7.28 },
    { name: '负面', value: 33.73 }
  ]);
  
  const fetchAttractionName = () => {
    nowName.value = <string>route.query.name;
    console.log("hhhhhname",route.query.name);
  };
  
  const loadAllData = async () => {
    fetchAttractionName();
    const pageTypeNum = Number(pageType.value);
    console.log("这里pageType", pageTypeNum);
  
    if(pageTypeNum === 1){
      try {
        const spotsResponse = await SpotsAPI.getSpotsAPI();
        console.log("我不叫喂！")
        if (typeof spotsResponse === "string") {
          const fixedResponse = spotsResponse.replace(/Decimal\('([\d.]+)'\)/g, '$1');
          const spotsArray = fixedResponse
              .replace(/'/g, '"')
              .match(/{[^}]+}/g)
              .map((spot) => JSON.parse(spot));
  
          interestData.value = spotsArray;
  
          console.log("景点数据（处理后）:", interestData.value);
  
          if (interestData.value.length > 0) {
            loadAttractions(nowName);
          } else {
            console.warn("景点数据为空");
          }
        } else {
          console.error("景点数据格式错误，期望为字符串形式");
        }
      } catch (error) {
        console.error("加载景点数据时出错:",error);
      }
    }else if(pageTypeNum===2){
      console.log("我叫喂！")
      try {
        console.log("我不叫喂！")
        // 根据 themeType 设置 type_id
        let type_id = '';
        const pageTheme = Number(themeType.value);
        if (pageTheme === 1) {
          type_id = '文学';
        } else if (pageTheme === 2) {
          type_id = '表演艺术';
        } else if (pageTheme === 3) {
          type_id = '新媒体艺术';
        } else if (pageTheme === 4) {
          type_id = '古诗词';
        }
        console.log("ThemeType",pageTheme)
        console.log("Type_id", type_id)
   // 调用 getBook 并传递 type_id
   const booksResponse = await FilmLiterature.getBook(type_id);
        console.log("书籍数据（未处理）:", type_id);
  
        if (booksResponse && typeof booksResponse === 'object' && 'data' in booksResponse) {
          if (Array.isArray(booksResponse.data)) {
            const booksArray = booksResponse.data.map((book) => {
              // 假设数据中 Decimal 字符串类型的字段需要处理，可以对其做处理
              if (typeof book.someDecimalField === "string") {
                book.someDecimalField = book.someDecimalField.replace(/Decimal\('([\d.]+)'\)/g, '$1');
              }
              return book;
            });
  
            bookData.value = booksArray;
  
            console.log("书籍数据（处理后）:", bookData.value);
  
            if (bookData.value.length > 0) {
              loadBooks(nowName);
            } else {
              console.warn("书籍数据为空");
            }
          } else {
            console.log("bookResponse", booksResponse.data)
            console.error("书籍数据格式错误，期望为字符串形式");
          }
        } else {
          console.error("书籍数据格式不正确:", booksResponse);
        }
      } catch (error) {
        console.error("加载书籍数据时出错:", error);
      }
    }else   if(pageTypeNum === 3){
      try {
        const foodResponse = await FoodAPI.getFoodAPI();
        console.log("我不叫喂！",foodResponse)
        if (foodResponse && typeof foodResponse === 'object' && 'data' in foodResponse) {
          if (Array.isArray(foodResponse.data)) {
            const foodArray = foodResponse.data.map((food) => {
              // 假设数据中 Decimal 字符串类型的字段需要处理，可以对其做处理
              if (typeof food.someDecimalField === "string") {
                food.someDecimalField = food.someDecimalField.replace(/Decimal\('([\d.]+)'\)/g, '$1');
              }
              return food;
            });
  
            foodData.value = foodArray;
  
            console.log("美食数据（处理后）:", foodData.value);
  
            if (foodData.value.length > 0) {
              loadFood(nowName);
            } else {
              console.warn("美食数据为空");
            }
          } else {
            console.log("foodResponse", foodResponse.data)
            console.error("美食数据格式错误，期望为字符串形式");
          }
        } else {
          console.error("美食数据格式不正确:", foodResponse);
        }
      } catch (error) {
        console.error("加载美食数据时出错:",error);
      }
    }else   if(pageTypeNum === 4){
      try {
        const folkResponse = await FolkAPI.getFolkCustomAPI();
        console.log("我不叫喂！",folkResponse)
        if (folkResponse && typeof folkResponse === 'object' && 'data' in folkResponse) {
          if (Array.isArray(folkResponse.data)) {
            const folkArray = folkResponse.data.map((folk) => {
              // 假设数据中 Decimal 字符串类型的字段需要处理，可以对其做处理
              if (typeof folk.someDecimalField === "string") {
                folk.someDecimalField = folk.someDecimalField.replace(/Decimal\('([\d.]+)'\)/g, '$1');
              }
              return folk;
            });
  
            folkData.value = folkArray;
  
            console.log("民俗数据（处理后）:", folkData.value);
  
            if (folkData.value.length > 0) {
              loadFolk(nowName);
            } else {
              console.warn("民俗数据为空");
            }
          } else {
            console.log("folkResponse", folkResponse.data)
            console.error("民俗数据格式错误，期望为字符串形式");
          }
        } else {
          console.error("民俗数据格式不正确:", folkResponse);
        }
      } catch (error) {
        console.error("加载民俗数据时出错:",error);
      }
    }

  // 评论
    try {
      const commentResponse = await CommentAPI.getCommentList(nowName.value, pageType.value);
      // 评论改了格式，要记得修改
      console.log("原始评论数据:", commentResponse);
  
      // 确保返回的数据包含 comments 数组
      if (commentResponse && typeof commentResponse === 'object' && 'comments' in commentResponse && Array.isArray(commentResponse.comments)) {
        const commentsArray = commentResponse.comments;
  
        // 映射到弹幕数据
        danmus.value = commentsArray.map(comment => ({
          name: comment.user_id || '匿名用户',
          text: comment.comment_text || '',  // 使用新的字段 comment_text
          sentiment: comment.sentiment || '',  // 如果需要，可以把情感分析加入
          sentiment_confidence: comment.sentiment_confidence || '',  // 情感分析置信度
          platform: comment.platform || ''  // 评论平台
        }));
        isDanmuLoading.value=false;
        console.log("成功解析的评论数组:", commentsArray);
      } else {
        throw new Error("返回的数据格式不正确，未找到有效的评论数组。");
      }
    } catch (error) {
      console.error("加载评论数据时出错:", error);
    }
  
  
  // 词云
    try {
      const cloudResponse = await CloudAPI.getCloudAPI(nowName.value,pageType.value);
      console.log("词云地址:", cloudResponse);
  
      if (cloudResponse && typeof cloudResponse === 'object' && 'wordcloud_url' in cloudResponse) {
        isWordCloudLoading.value=false;
        cloudUrl.value="http://127.0.0.1:8080"+cloudResponse.wordcloud_url;
      } else {
        console.warn("词云数据格式不正确:", cloudResponse);
      }
    } catch (error) {
      console.error("加载词云数据时出错:", error);
    }
  
  // 饼图
    try {
      const pieResponse = await SentimentAPI.getSentimentPieAPI(nowName.value, pageType.value);
  
      if (pieResponse && typeof pieResponse === 'object' && 'data' in pieResponse &&
          'positive_percentage' in pieResponse.data &&
          'neutral_percentage' in pieResponse.data &&
          'negative_percentage' in pieResponse.data) {
  
        // 格式化为 PieChart 需要的数据结构
        data1.value = [
          { name: '正面', value: parseFloat(pieResponse.data.positive_percentage) || 0 },
          { name: '中立', value: parseFloat(pieResponse.data.neutral_percentage) || 0 },
          { name: '负面', value: parseFloat(pieResponse.data.negative_percentage) || 0 }
        ];
        isPieChartLoading.value = false;
        console.log("饼图数据（处理后）:", data1.value);
      } else {
        console.warn("饼图数据格式不正确:", pieResponse);
        // 设置默认数据，避免渲染错误
        data1.value = [
          { name: '正面', value: 33 },
          { name: '中立', value: 33 },
          { name: '负面', value: 34 }
        ];
        isPieChartLoading.value = false;
      }
    } catch (error) {
      console.error("加载饼图数据时出错:", error);
      // 设置默认数据，避免渲染错误
      data1.value = [
        { name: '正面', value: 33 },
        { name: '中立', value: 33 },
        { name: '负面', value: 34 }
      ];
      isPieChartLoading.value = false;
    }
  
    // 主题聚类
    try {
      // 获取 LdaResponse 数据
      const ldaResponse = await LdaAPI.LdaAPI(nowName.value,pageType.value);
  
      // 检查数据有效性，并格式化为表格需要的格式
      if (Array.isArray(ldaResponse)) {
        sentiment.value = ldaResponse.map(item => ({
          topic: item.topic, // 主题
          frequency: item.frequency, // 出现频率
          sentiment: item.sentiment, // 情感
        }));
        console.log("LDA 数据加载成功:", sentiment.value);
        isTopicClusterLoading.value=false;
        isBarChartLoading.value=false;
      } else {
        console.warn("LDA 数据格式不正确:", ldaResponse);
      }
    } catch (error) {
      console.error("加载 LDA 数据时出错:", error);
    }

  // 词频统计
    try {
      // 获取 WordResponse 数据
      const wordResponse = await SentimentAPI.getSentimentWordAPI(nowName.value,pageType.value);
  
      // 检查数据有效性，并格式化为表格需要的格式
      if (wordResponse && typeof wordResponse === 'object' && 'data' in wordResponse) {
        if (Array.isArray(wordResponse.data)) {
          topic.value = wordResponse.data.map(item => ({
            word: item.word, // 关键词
            frequency: item.frequency, // 出现频率
            sentiment: item.sentiment, // 情感
          }));
          // console.log("Word 数据加载成功:", topic.value);
          isSentimentStatsLoading.value=false;
        } else {
          console.warn("Word 数据格式不正确:", wordResponse);
        }
      } else {
        console.error("Word 数据格式不正确:", wordResponse);
      }
    } catch (error) {
      console.error("加载 Word 数据时出错:", error);
    }
  
  // 在加载时间情感数据后，赋值给 processedTimeData
    try {
      const timeResponse = await SentimentAPI.getSentimentResultAPI(nowName.value,pageType.value);
      if (timeResponse && typeof timeResponse === "object" && 'data' in timeResponse && Array.isArray(timeResponse.data)) {
        processedTimeData.value = timeResponse.data.map(item => {
          const paddedMonth = item.month < 10 ? '0' + item.month : item.month;
          //console.log("你好！！！" + parseFloat(item.sentiment_score));
          return {
            date: `${item.year}-${paddedMonth}`,
            sentimentScore: parseFloat(item.sentiment_score) || 0,
            sentiment: item.sentiment,
            commentCount: item.comment_count,
          };
        });
        isLineRaceLoading.value=false;
        // console.log("时间情感数据（处理后）:", processedTimeData.value);
      } else {
        console.warn("时间情感数据格式不正确:", timeResponse);
      }
    } catch (error) {
      console.error("加载时间情感数据时出错:", error);
    }
  
    // 三线图
    try {
      const threeLineResponse = await SentimentAPI.getCasualImpactAPI(nowName.value);
      console.log("三线图原始数据:", threeLineResponse);
  
      // 检查数据结构是否符合预期
      if (threeLineResponse &&
          typeof threeLineResponse === 'object' &&
          'economic_data' in threeLineResponse &&
          'sentiment_data' in threeLineResponse &&
          'casual_impact_analysis' in threeLineResponse) {
  
        threeLineData.value = threeLineResponse;
        console.log("三线图数据处理成功");
      } else {
        console.warn("三线图数据格式不符合预期:", threeLineResponse);
        threeLineData.value = []; // 设置为空数组避免渲染错误
      }
    } catch (error) {
      console.error("加载三线图数据时出错:", error);
      threeLineData.value = []; // 出错时也设置为空数组
    }
   
    // try {
    //   const sentimentResponse = await SentimentAPI.getSentimentReportAPI(nowName.value);
    //   if (sentimentResponse && typeof sentimentResponse === "object" && sentimentResponse.data) {
    //     // 将 Markdown 转换为 HTML
    //     let markdownContent;
    //     markdownContent.value = marked(sentimentResponse.data);
    //     console.log("AI 报告解析后的 HTML:", markdownContent.value);
    //
    //     // 如果需要，也可以在这里进行进一步的数据处理
    //     // 例如，提取 sentiment 或其他相关信息
    //
    //   } else {
    //     console.error("AI 报告数据格式不符合预期:", sentimentResponse);
    //   }
    // } catch (error) {
    //   console.error("加载 AI 报告时出错:", error);
    // }
  
  }
  
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
  
      // 更新图片 URL
      currentImageUrl.value = spot.image_url;
      console.log("currentImgUrl:", currentImageUrl.value)
      console.log("当前选中的景点:", attractions.value.name);
      isImageLoading.value=false;
    } else {
      console.warn(`未找到名称为 "${spotName}" 的景点`);
      attractions.value = null;
    }
  
    console.log("当前选中的景点:", attractions);
  };
  const loadBooks = (bookName: Ref<UnwrapRef<string>, UnwrapRef<string> | string>) => {
    if (!bookData.value || !Array.isArray(bookData.value)) {
      console.warn("书籍数据未加载或格式错误");
      return;
    }
  
    console.log("书籍数据（未处理）1111:", bookName.value);
    // 查找匹配的单个书籍
    const book = bookData.value.find((book: any) => book.liter_name === bookName.value);
    if (book) {
      books.value = {
        name: book.liter_name,
        image: book.image_url,
        description: book.text,
      };
      // 更新图片 URL
      currentImageUrl.value = book.image_url;
      console.log("currentImgUrl:", currentImageUrl.value)
      console.log("当前选中的书籍:", books.value.name);
      isImageLoading.value=false;
    } else {
      console.warn(`未找到名称为 "${bookName.value}" 的书`);
      books.value = null;
    }
  
    console.log("当前选中的书籍:", book);
  };
  const loadFood = (foodName: Ref<UnwrapRef<string>, UnwrapRef<string> | string>) => {
    if (!foodData.value || !Array.isArray(foodData.value)) {
      console.warn("美食数据未加载或格式错误");
      return;
    }
  
    console.log("美食数据（未处理）:", foodName.value);
    // 查找匹配的单个景点
    const foods = foodData.value.find((foods: any) => foods.food_name === foodName.value);
    if (foods) {
      food.value = {
        name: foods.food_name,
        image: foods.image_url,
        description: foods.description,
      };
  
      // 更新图片 URL
      currentImageUrl.value = foods.image_url;
      console.log("currentImgUrl:", currentImageUrl.value)
      console.log("当前选中的美食:", food.value?.name);
      isImageLoading.value=false;
    } else {
      console.warn(`未找到名称为 "${foodName}" 的美食`);
      food.value = null;
    }
  
    console.log("当前选中的美食:", food);
  };
  const loadFolk = (folkName: Ref<UnwrapRef<string>, UnwrapRef<string> | string>) => {
    if (!folkData.value || !Array.isArray(folkData.value)) {
      console.warn("民俗数据未加载或格式错误");
      return;
    }
  
    console.log("民俗数据（未处理）:", folkName.value);
    // 查找匹配的单个景点
    const folks = folkData.value.find((folks: any) => folks.folk_name === folkName.value);
    if (folks) {
      folk.value = {
        name: folks.folk_name,
        image: folks.image_url,
        description: folks.description,
      };
  
      // 更新图片 URL
      currentImageUrl.value = folks.image_url;
      console.log("currentImgUrl:", currentImageUrl.value)
      console.log("当前选中的民俗:", folk.value?.name);
      isImageLoading.value=false;
  
    } else {
      console.warn(`未找到名称为 "${folkName}" 的民俗`);
      folk.value = null;
    }
  
    console.log("当前选中的民俗:", folk);
  };
  
  const danmus = ref([]);
  const colorList = ref(['rgb(204,255,255)', 'white', 'rgb(204,255,204)', 'white', 'rgb(0,255,255)', 'white', 'rgb(255,204,255)', 'pink']);
  // 生成随机颜色的函数
  import {ref, onMounted, watch, Ref, UnwrapRef} from 'vue';
  import { useRoute } from 'vue-router';
  const route = useRoute();
  const nowName = ref<string>('');
  const themeType = ref(null);
  const pageType = ref(null);
  
  // 只保留一个统一的 watch
  watch(
      () => route.query, // 直接监听整个 query 对象
      async (newQuery, oldQuery) => {
        console.log("路由参数变化检测：", newQuery, oldQuery);
        // 重置加载状态
        isWordCloudLoading.value = true;
        isDanmuLoading.value = true;
        isBarChartLoading.value = true;
        isPieChartLoading.value = true;
        isSentimentStatsLoading.value = true;
        isTopicClusterLoading.value = true;
        isImageLoading.value = true;
        // 更新各个响应式变量
        if (typeof newQuery.name === 'string') {
          nowName.value = newQuery.name;
        }
  
        if (newQuery.value) {
          pageType.value = newQuery.value;
        }
  
        if (newQuery.theme) {
          themeType.value = newQuery.theme;
        }
  
        // 如果任何相关参数发生变化，则重新加载数据
        if (newQuery.name !== oldQuery?.name ||
            newQuery.value !== oldQuery?.value ||
            newQuery.theme !== oldQuery?.theme) {
          console.log("参数发生变化，准备重新加载数据");
  
          // 清空之前的数据
          sentiment.value = [];
          topic.value = [];
          processedTimeData.value = [];
          danmus.value = [];
          cloudUrl.value = '';
          data1.value = [];
  
          // 重新加载数据
          await loadAllData();
        }
      },
      {
        immediate: true,
        deep: true
      }
  );
  
  // 在父组件中添加以下方法
  const handleTypeChange = async (typeId) => {
    pageType.value = parseInt(typeId);
  
    // 检查搜索内容是否存在于对应数据中
    if (searchQuery.value) {
      checkContentAvailability();
    }
  };
  
  const handleSearchChange = (searchText) => {
    searchQuery.value = searchText;
    if (pageType.value) {
      checkContentAvailability();
    }
  };
  
  const checkContentAvailability = async () => {
    try {
      // 根据类型加载对应数据
      if (pageType.value === 1) {
        // 如果景点数据还未加载，先加载数据
        if (!interestData.value) {
          const spotsResponse = await SpotsAPI.getSpotsAPI();
          if (typeof spotsResponse === "string") {
            const fixedResponse = spotsResponse.replace(/Decimal\('([\d.]+)'\)/g, '$1');
            const spotsArray = fixedResponse
                .replace(/'/g, '"')
                .match(/{[^}]+}/g)
                .map((spot) => JSON.parse(spot));
  
            interestData.value = spotsArray;
            console.log("景点数据加载成功:", interestData.value);
          }
        }
  
        // 检查名胜古迹
        const spot = interestData.value?.find(
            (item) => item.spot_name === searchQuery.value
        );
        if (spot) {
          nowName.value = searchQuery.value;
          loadAttractions(nowName);
  
          // 更新 URL
          router.push({
            path: '/detail',
            query: {
              name: searchQuery.value,
              value: '1', // 名胜古迹的 pageType 是 1
              theme: '1'  // 名胜古迹的 theme 是 1
            }
          });
  
          ElMessage.success('已找到相关景点信息');
          await loadAllData();
        } else {
          ElMessage.warning('未找到相关名胜古迹信息');
        }
  
      } else if (pageType.value === 2) {
        try {
  // 创建一个临时数组存储所有类型的书籍
          let allBooks = [];
          console.log("我在找书中……")
  // 加载所有类型的书籍数据
          const typeIds = ['文学', '表演艺术', '新媒体艺术', '古诗词'];
  
          try {
            // 循环处理每一个类型的书籍数据
            for (const type_id of typeIds) {
              const booksResponse = await FilmLiterature.getBook(type_id);
              console.log(`获取类型 ${type_id} 的书籍数据:`, booksResponse);
  
  // 确保返回的是字符串格式
            if (booksResponse && typeof booksResponse === 'object' && 'status' in booksResponse && 'data' in booksResponse) {
                if (booksResponse.status === 'success' && Array.isArray(booksResponse.data)) {
                  // 从响应中提取 data 字段
                  const booksArray = booksResponse.data;
                  // 将当前类型的书籍加入到总的 allBooks 数组中
                  allBooks.push(...booksArray);
                }
              } else {
                console.error(`获取类型 ${type_id} 的数据格式不正确`, booksResponse);
              }
            }
  
            // 所有类型的书籍加载完成后，更新到响应式数据
            bookData.value = allBooks;
            console.log("所有类型书籍数据加载成功:", bookData.value);
  
          } catch (error) {
            console.error("加载书籍数据时发生错误:", error);
          }
          // 检查影视文学
          const book = bookData.value?.find(
              (item) => item.liter_name === searchQuery.value
          );
          if (book) {
            nowName.value = searchQuery.value;
            loadBooks(nowName);
  
            // 更新 URL
            router.push({
              path: '/detail',
              query: {
                name: searchQuery.value,
                value: '2', // 页面类型 2 为书籍相关
                theme: book.type_id  // 书籍类型 theme 可以根据实际情况修改
              }
            });
  
            ElMessage.success('已找到相关文学作品信息');
            await loadAllData();
          } else {
            ElMessage.warning('未找到相关影视文学信息');
          }
        } catch (error) {
          console.error("数据加载或检查过程中出错:", error);
          ElMessage.error('数据加载失败，请稍后重试');
        }
      }else if (pageType.value === 3) {
        // 如果景点数据还未加载，先加载数据
        if (!foodData.value) {
          const foodResponse = await FoodAPI.getFoodAPI();
          console.log("我在找美食中……");
  
          // 确保 foodResponse 是一个对象，并且包含有效的 status 和 data
          if (foodResponse && typeof foodResponse === 'object' && 'status' in foodResponse && 'data' in foodResponse) {
            if (foodResponse.status === "ok" && Array.isArray(foodResponse.data)) {
              const foodArray = foodResponse.data;
              foodData.value = foodArray;
              console.log("美食数据加载成功:", foodData.value);
            }
          } else {
            console.error("美食数据加载失败，响应格式不正确:", foodResponse);
          }
        }
  
  
        // 检查名胜古迹
        const foods = foodData.value?.find(
            (item) => item.food_name === searchQuery.value
        );
        if (foods) {
          nowName.value = searchQuery.value;
          console.log("现在是美食的天下！",nowName)
          loadFood(nowName);
  
          // 更新 URL
          router.push({
            path: '/detail',
            query: {
              name: searchQuery.value,
              value: '3', // 名胜古迹的 pageType 是 1
              theme: '1'  // 名胜古迹的 theme 是 1
            }
          });
  
          ElMessage.success('已找到相关美食信息');
          await loadAllData();
        } else {
          ElMessage.warning('未找到相关美食信息');
        }
  
      }else if (pageType.value === 4) {
        // 如果民俗数据还未加载，先加载数据
        if (!folkData.value) {
          const folkResponse = await FolkAPI.getFolkCustomAPI();
          if (typeof folkResponse === "string") {
            const fixedResponse = folkResponse.replace(/Decimal\('([\d.]+)'\)/g, '$1');
            const folkArray = fixedResponse
                .replace(/'/g, '"')
                .match(/{[^}]+}/g)
                .map((folk) => JSON.parse(folk));
  
            folkData.value = folkArray;
            console.log("民俗数据加载成功:", folkData.value);
          }
        }
  
        // 检查名胜古迹
        const folks = folkData.value?.find(
            (item) => item.folk_name === searchQuery.value
        );
        if (folks) {
          nowName.value = searchQuery.value;
          loadFolk(nowName);
  
          // 更新 URL
          router.push({
            path: '/detail',
            query: {
              name: searchQuery.value,
              value: '4', // 名胜古迹的 pageType 是 1
              theme: '1'  // 名胜古迹的 theme 是 1
            }
          });
  
          ElMessage.success('已找到相关民俗信息');
          await loadAllData();
        } else {
          ElMessage.warning('未找到相关民俗信息');
        }
  
      }
    } catch (error) {
      console.error("数据加载或检查过程中出错:", error);
      ElMessage.error('数据加载失败，请稍后重试');
    }
  };
  
  function getRandomColor() {
    const color = colorList.value[Math.floor(Math.random() * 8)];
    return color;
  }
  
  onMounted(async () => {
    await loadAllData();
  
  });
  
  
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
    justify-content: center;
    align-items: center;
    gap: 20px;
    position: relative;
  }
  
  .wordcloud-container,
  .city-image-container,
  .danmu-container {
    position: relative;
    width: 100%;
    height: 100%;
  }
  
  .loader {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 10;
    pointer-events: none;
  }
  
  .city-image,
  .wordcloud {
    object-fit: contain;
    width: 100%;
    height: 100%;
    border-radius: 10px;
  }
  
  .danmu {
    flex: 1;
    height: 100%;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: rgba(0, 0, 0, 0.5);
    position: relative;
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
  
  .mixed-charts-row {
    display: flex;
    width: 100%;
    margin-top: 20px;
    gap: 20px;
  }
  </style>
  