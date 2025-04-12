<template>
    <div class="tab-inner">
      <!-- 图片和弹幕区域 -->
      <div class="image-danmu-container">
        <!-- 左边图片区域 -->
        <div 
          class="city-image-container"
          v-loading="isImageLoading"
          :element-loading-text="t('common.loading')"
        >
          <el-skeleton v-if="isImageLoading" :rows="3" animated />
          <img
            v-else
            :src="currentImageUrl"
            :alt="t('detail.image.alt')"
            class="city-image"
          />
        </div>
  
        <!-- 词云图区域 -->
        <div 
          class="wordcloud-container"
          v-loading="isWordCloudLoading"
          :element-loading-text="t('common.loading')"
        >
          <el-skeleton v-if="isWordCloudLoading" :rows="3" animated />
          <img
            v-else
            :src="cloudUrl"
            :alt="t('detail.wordcloud.alt')"
            class="wordcloud"
          />
        </div>
  
        <!-- 弹幕区域 -->
        <div class="danmu-container">
          <el-skeleton v-if="isDanmuLoading" :rows="3" animated />
          <div v-else class="danmu">
            <danmaku
              ref="danmakuRef"
              v-model:danmus="danmus"
              :speeds="50"
              useSlot
              loop
              :channels="7"
              style="height: 300px;"
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
  
      <!-- 饼图和评论排行区域 -->
      <div class="charts-container">
        <!-- 饼图区域 -->
        <div class="pie-chart-container">
          <el-skeleton v-if="isPieChartLoading" :rows="3" animated />
          <PieChart
            v-else
            :chartData="data1"
            style="width: 100%; height: 100%;"
          />
        </div>
  
        <!-- 评论排行区域 -->
        <div class="comments-ranking">
          <h3>{{ t('detail.comments.positiveRanking') }}</h3>
          <div class="comments-list">
            <el-scrollbar>
              <div v-for="(comment, index) in positiveComments" :key="index" class="comment-item">
                <div class="comment-header">
                  <span class="user-name">{{ comment.name }}</span>
                  <span class="sentiment-score">{{ comment.sentiment_confidence }}%</span>
                </div>
                <div class="comment-text">{{ comment.text }}</div>
                <div class="comment-platform">{{ t('detail.comments.source') }}: {{ comment.platform }}</div>
              </div>
            </el-scrollbar>
          </div>
        </div>
      </div>
    </div>
  </template>
  


<script lang="ts" setup>
  import PieChart from "@/components/DetailPage/subcomponent/PieChart.vue";
  import CloudAPI from "@/api/cloud";
  import danmaku from 'vue3-danmaku';
  import SpotsAPI from "@/api/spot";
  import FoodAPI from "@/api/food";
  import FolkAPI from "@/api/folk"
  import CommentAPI from "@/api/comment";
  import SentimentAPI from "@/api/sentiment";
  import { ElMessage } from 'element-plus';
  import FilmLiterature from "@/api/filmLiterature";
  import {ref, onMounted, watch, Ref, UnwrapRef} from 'vue';
  import { useRoute } from 'vue-router';
  import { computed, withDefaults } from 'vue';
  import { useI18n } from 'vue-i18n';

  const { t } = useI18n();

  // Props 定义
  interface Props {
    name: string
    pageType: string | number
    themeType?: string | number // 使用可选参数，因为不是所有情况都需要
  }

  const props = withDefaults(defineProps<Props>(), {
    name: '',
    pageType: '1',
    themeType: '1'
  })

  // 确保 nowName 正确初始化
  const nowName = ref(props.name || '');

  // 修改 computed 属性的定义
  const pageTypeNum = computed(() => {
    const num = Number(props.pageType);
    return isNaN(num) ? 1 : num;
  });

  const pageTheme = computed(() => {
    const num = Number(props.themeType);
    return isNaN(num) ? 1 : num;
  });

  const interestData = ref<any>(null);
  const bookData = ref<any>(null);
  const foodData = ref<any>(null);
  const folkData = ref<any>(null);

  const attractions = ref<any>({}); // 初始化为一个空对象
  const books = ref<any>({});
  const food = ref<any>({});
  const folk = ref<any>({});
  
  const cloudUrl = ref('');
  const processedTimeData = ref<any>([]);
  const sentiment = ref<any>([]); // LDA 数据绑定到 SentimentStats
  const topic = ref<any>([]);
  const currentImageUrl = ref<string>(''); // 用于存储当前需要展示的图片 URL
  
  const isImageLoading = ref(true);
  const isWordCloudLoading = ref(true);
  const isDanmuLoading = ref(true);
  const isPieChartLoading = ref(true);
  
  const data1 = ref([  // 将 data1 用 ref 包装成响应式数据
    { name: '正面', value: 58.84 },
    { name: '中立', value: 7.28 },
    { name: '负面', value: 33.73 }
  ]);
  
  const fetchAttractionName = () => {
    if (props.name) {
      nowName.value = props.name;
      console.log("设置景点名称:", nowName.value);
    } else {
      console.warn("未收到有效的景点名称");
    }
  };
  
  // 添加重试机制
  const fetchWithRetry = async (fetchFn: () => Promise<any>, retries = 3) => {
    for (let i = 0; i < retries; i++) {
      try {
        return await fetchFn();
      } catch (error) {
        if (i === retries - 1) throw error;
        await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1))); // 延迟重试
      }
    }
  };
  
  // 修改 isPieResponse 的类型定义和判断逻辑
  interface PieData {
    data: Array<{
      year: number;
      month: number;
      sentiment: string;
      comment_count: number;
      sentiment_score: number;
      percentage: number;
    }>;
  }

  const isPieResponse = (response: unknown): response is PieData => {
    return response !== null &&
           typeof response === 'object' &&
           'data' in response &&
           Array.isArray((response as any).data);
  };
  
  // 修改数据处理函数
  const processSpotData = (data) => {
    console.log('处理前的景点数据:', data);
    try {
      if (typeof data === 'string') {
        // 使用正则表达式匹配每个完整的对象
        const regex = /{[^}]+}/g;
        const matches = data.match(regex);
        
        if (!matches) {
          console.error('未找到有效的对象');
          return [];
        }

        // 处理每个对象
        const spots = matches.map(objStr => {
          try {
            // 清理字符串
            const cleanStr = objStr
              .replace(/'/g, '"')  // 替换单引号为双引号
              .replace(/Decimal\("([\d.]+)"\)/g, '$1')  // 处理 Decimal("x.xx")
              .replace(/Decimal\('([\d.]+)'\)/g, '$1')  // 处理 Decimal('x.xx')
              .replace(/None/g, 'null')  // 处理 Python 的 None
              .replace(/True/g, 'true')  // 处理 Python 的 True
              .replace(/False/g, 'false');  // 处理 Python 的 False

            // 解析 JSON
            const obj = JSON.parse(cleanStr);
            return {
              spot_id: Number(obj.spot_id),
              spot_name: String(obj.spot_name),
              description: String(obj.description || ''),
              image_url: String(obj.image_url || ''),
              rating: Number(obj.rating || 0),
              city_id: Number(obj.city_id),
              text: String(obj.text || '')
            };
          } catch (e) {
            console.error('处理单个对象时出错:', e);
            console.error('问题对象:', objStr);
            return null;
          }
        }).filter(Boolean); // 过滤掉 null 值

        console.log('成功解析的数据:', spots);
        return spots;
      }
      
      // 如果已经是数组则直接返回
      if (Array.isArray(data)) {
        return data;
      }
      
      // 如果是单个对象，转换为数组
      if (typeof data === 'object' && data !== null) {
        return [data];
      }

      return [];
    } catch (e) {
      console.error('数据解析失败:', e);
      return [];
    }
  };

  // 加载所有数据
  const loadAllData = async () => {
    // 先设置名称
    fetchAttractionName();
    
    // 检查必要参数
    if (!nowName.value) {
      console.warn('缺少景点名称:', { name: nowName.value });
      ElMessage.warning('缺少景点名称');
      return;
    }

    // 确保 pageType 有效
    if (!pageTypeNum.value || ![1, 2, 3, 4].includes(pageTypeNum.value)) {
      console.warn('页面类型无效:', { pageType: pageTypeNum.value });
      ElMessage.warning('页面类型无效');
      return;
    }

    console.log('开始加载数据:', {
      name: nowName.value,
      pageType: pageTypeNum.value,
      themeType: pageTheme.value
    });
  
    console.log("这里pageType", pageTypeNum.value);
  
    if(pageTypeNum.value === 1){ // 景点
      try {
        const spotsResponse = await SpotsAPI.getSpotsAPI();
        console.log("获取到的原始景点数据:", spotsResponse);
        
        if (typeof spotsResponse === "string") {
          const processedData = processSpotData(spotsResponse);
          if (processedData && processedData.length > 0) {
            interestData.value = processedData;
            console.log("处理后的景点数据:", interestData.value);
            await loadAttractions(nowName);
          } else {
            console.warn("处理后的景点数据为空");
            isImageLoading.value = false;
          }
        } else {
          console.error("景点数据格式错误，期望为字符串形式");
          isImageLoading.value = false;
        }
      } catch (error) {
        console.error("加载景点数据时出错:", error);
        isImageLoading.value = false;
      }
    }else   if(pageTypeNum.value===2){ // 文学
      console.log("我叫喂！")
      try {
        console.log("我不叫喂！")
        // 根据 themeType 设置 type_id
        let type_id = '';
        if (pageTheme.value === 1) {
          type_id = '文学';
        } else if (pageTheme.value === 2) {
          type_id = '表演艺术';
        } else if (pageTheme.value === 3) {
          type_id = '新媒体艺术';
        } else if (pageTheme.value === 4) {
          type_id = '古诗词';
        }
        console.log("ThemeType",pageTheme.value)
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
    }else   if(pageTypeNum.value === 3){ // 美食
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
    }else   if(pageTypeNum.value === 4){ // 民俗
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
  

    // 加载词云数据
    try {
      const cloudResponse = await CloudAPI.getCloudAPI(nowName.value,pageTypeNum.value);
      console.log("词云地址:", cloudResponse);
  
      if (cloudResponse && typeof cloudResponse === 'object' && 'wordcloud_url' in cloudResponse) {
        isWordCloudLoading.value=false;
        cloudUrl.value="http://127.0.0.1:8080"+cloudResponse.wordcloud_url;
      } else {
        console.warn("词云数据格式不正确:", cloudResponse);
      }
    } catch (error) {
      console.error("加载词云数据时出错:", error);
      isWordCloudLoading.value = false;
      // 设置一个默认的词云图片或显示错误提示
      cloudUrl.value = ''; // 或设置为默认图片
      ElMessage.error('词云数据加载失败，请稍后重试');
    }
  
    // 加载饼图数据
    try {
      const pieResponse = await SentimentAPI.getSentimentPieAPI(nowName.value, pageTypeNum.value);
  
      if (isPieResponse(pieResponse)) {
        // 计算各情感类别的总数量和百分比
        const sentimentTotals = {
          positive: { count: 0, percentage: 0 },
          neutral: { count: 0, percentage: 0 },
          negative: { count: 0, percentage: 0 }
        };
  
        // 累加每个情感类别的数量和百分比
        pieResponse.data.forEach(item => {
          if (item.sentiment === 'positive') {
            sentimentTotals.positive.count += Math.round(item.comment_count);
            sentimentTotals.positive.percentage += item.percentage;
          } else if (item.sentiment === 'neutral') {
            sentimentTotals.neutral.count += Math.round(item.comment_count);
            sentimentTotals.neutral.percentage += item.percentage;
          } else if (item.sentiment === 'negative') {
            sentimentTotals.negative.count += Math.round(item.comment_count);
            sentimentTotals.negative.percentage += item.percentage;
          }
        });
  
        // 更新饼图数据
        data1.value = [
          { 
            name: '正面', 
            value: Number(sentimentTotals.positive.percentage.toFixed(2)) || 0,
            count: Math.round(sentimentTotals.positive.count)
          },
          { 
            name: '中立', 
            value: Number(sentimentTotals.neutral.percentage.toFixed(2)) || 0,
            count: Math.round(sentimentTotals.neutral.count)
          },
          { 
            name: '负面', 
            value: Number(sentimentTotals.negative.percentage.toFixed(2)) || 0,
            count: Math.round(sentimentTotals.negative.count)
          }
        ];
        isPieChartLoading.value = false;
        console.log("饼图数据（处理后）:", data1.value);
      } else {
        console.warn("饼图数据格式不正确:", pieResponse);
        // 设置默认数据
        data1.value = [
          { name: '正面', value: 33, count: 0 },
          { name: '中立', value: 33, count: 0 },
          { name: '负面', value: 34, count: 0 }
        ];
        isPieChartLoading.value = false;
      }
    } catch (error) {
      console.error("加载饼图数据时出错:", error);
      // 设置默认数据
      data1.value = [
        { name: '正面', value: 33, count: 0 },
        { name: '中立', value: 33, count: 0 },
        { name: '负面', value: 34, count: 0 }
      ];
      isPieChartLoading.value = false;
    }
        // 使用重试机制
        try {
      const commentResponse = await fetchWithRetry(() => 
        CommentAPI.getPostiveComment(nowName.value)
      );
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
      console.error("评论数据加载失败（已重试）:", error);
      // 设置默认空数组，避免界面报错
      danmus.value = [];
      isDanmuLoading.value = false;
      // 可以显示一个友好的错误提示
      ElMessage.error('评论数据加载失败，请稍后重试');
    }
  
  
  
  }
  
  // 加载景点数据
  const loadAttractions = async (spotName: Ref<UnwrapRef<string>, UnwrapRef<string> | string>) => {
    if (!interestData.value || !Array.isArray(interestData.value)) {
      console.warn("景点数据未加载或格式错误");
      return;
    }
  
    console.log("正在查找景点:", spotName.value);
    // 查找匹配的单个景点
    const spot = interestData.value.find((spot: any) => spot.spot_name === spotName.value);
    if (spot) {
      attractions.value = {
        name: spot.spot_name,
        image: spot.image_url,
        description: spot.description,
      };
  
      // 直接使用完整的图片URL
      currentImageUrl.value = spot.image_url;
      console.log("找到景点:", spot.spot_name);
      console.log("图片URL:", currentImageUrl.value);
      isImageLoading.value = false;
    } else {
      console.warn(`未找到名称为 "${spotName.value}" 的景点`);
      attractions.value = null;
      isImageLoading.value = false;
    }
  };
  
  // 加载书籍数据
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

  // 加载美食数据
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
  
  // 加载民俗数据
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
  
  // 生成随机颜色的函数
  const danmus = ref([]);
  const colorList = ref(['rgb(204,255,255)', 'white', 'rgb(204,255,204)', 'white', 'rgb(0,255,255)', 'white', 'rgb(255,204,255)', 'pink']);

  // watch 修改
  watch(
    () => [props.name, props.pageType, props.themeType],
    async (newValues, oldValues) => {
      // 确保新值有效
      if (!newValues[0]) {
        console.warn('新的景点名称无效');
        return;
      }

      if (newValues.some((val, idx) => val !== oldValues?.[idx])) {
        console.log('属性变化:', {
          name: newValues[0],
          pageType: newValues[1],
          themeType: newValues[2]
        });

        // 重置状态
        isWordCloudLoading.value = true;
        isDanmuLoading.value = true;
        isPieChartLoading.value = true;
        isImageLoading.value = true;

        // 清空数据
        danmus.value = [];
        cloudUrl.value = '';
        data1.value = [];
        currentImageUrl.value = '';

        // 重新加载
        await loadAllData();
      }
    },
    {
      immediate: true,
      deep: true
    }
  );

  // 生成随机颜色的函数
  function getRandomColor() {
    const color = colorList.value[Math.floor(Math.random() * 8)];
    return color;
  }
  
  // 添加正面评论计算属性
  const positiveComments = computed(() => {
    return danmus.value
      .filter(comment => comment.sentiment === 'positive')
      .sort((a, b) => (Number(b.sentiment_confidence) || 0) - (Number(a.sentiment_confidence) || 0))
      .slice(0, 10); // 只显示前10条
  });
  
  onMounted(async () => {
    console.log('Component mounted with props:', { 
      name: props.name, 
      pageType: props.pageType, 
      themeType: props.themeType 
    });
    await loadAllData();
  });
  
</script>

<style scoped>
  .tab-inner {
    height: 100%;
    width: 100%;
    display: flex;
    flex-direction: column;
    padding: 10px;
    overflow: hidden; /* 改为 hidden，防止滚动 */
  }
  
  .image-danmu-container {
    display: flex;
    justify-content: space-between;
    align-items: stretch;
    gap: 20px;
    min-height: 280px;
    width: 97%;
  }
  
  .city-image-container,
  .wordcloud-container {
    flex: 0 0 auto;
    width: 300px;
    height: 300px;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
  }
  
  .city-image,
  .wordcloud {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .danmu-container {
    flex: 1;
    height: 93.5%;
    min-width: 250px;
    padding-top: 10px;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 8px;
    overflow: hidden;
    position: relative;
  }
  
  .danmu {
    width: 100%;
    height: 100%;
    position: relative;
  }
  
  .charts-container {
    display: flex;
    gap: 20px;
    height: 265px;
    width: 100%;
    margin-top: 10px;
    justify-content: flex-start;
  }
  
  .pie-chart-container {
    flex: 0 0 420px;
    padding: 10px;
    padding-left: 30px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
    height: 100%;
  }
  
  .comments-ranking {
    flex: 1;
    min-width: 0;
    max-width: 835px;
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
    display: flex;
    flex-direction: column;
    height: 92.5%;
  }
  
  .comments-ranking h3 {
    margin: 0 0 12px 0;
    font-size: 16px;
  }
  
  .comments-list {
    flex: 1;
    overflow: hidden;
    position: relative;
  }
  
  :deep(.el-scrollbar) {
    height: 100%;
  }
  
  :deep(.el-scrollbar__wrap) {
    overflow-x: hidden;
  }
  
  .comment-item {
    padding: 8px;
    font-size: 13px;
    border-bottom: 1px solid #ebeef5;
    transition: background-color 0.3s;
  }
  
  .comment-item:hover {
    background-color: #f5f7fa;
  }
  
  .comment-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
  }
  
  .user-name {
    font-weight: 600;
    color: #b71c1c;
  }
  
  .sentiment-score {
    color: #67c23a;
    font-size: 14px;
  }
  
  .comment-text {
    color: #606266;
    line-height: 1.5;
    margin-bottom: 8px;
    word-break: break-all;
    white-space: normal;
  }
  
  .comment-platform {
    color: #909399;
    font-size: 12px;
    text-align: right;
  }

  /* 添加弹幕相关样式 */
  .danmu-item {
    white-space: nowrap;
    color: #FFFFFF;
    font-size: 16px;
    background-color: rgba(0, 0, 0, 0.3);
    padding: 4px 10px;
    border-radius: 15px;
    margin-bottom: 8px;
    cursor: pointer;
    transition: transform 0.2s;
  }

  .danmu-item:hover {
    transform: scale(1.05);
    background-color: rgba(0, 0, 0, 0.5);
  }

  .bullet-item {
    display: inline-block;
    text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
  }

  .danmu-container {
    flex: 1;
    min-width: 300px;
    background-color: rgba(0, 0, 0, 0.5);
    border-radius: 8px;
    overflow: hidden;
    position: relative;
  }

  .danmu {
    width: 100%;
    height: 100%;
    position: relative;
  }

  :deep(.vue3-danmaku) {
    background: transparent !important;
  }

  :deep(.vue3-danmaku__item) {
    pointer-events: auto !important;
  }

  :deep(.vue3-danmaku__item:hover) {
    cursor: pointer;
    transform: scale(1.1);
  }
</style>