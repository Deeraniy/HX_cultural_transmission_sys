<template>
  <div class="fullpage-container" @wheel="handleWheel">
    <!-- 添加用户信息和偏好检查 -->
    <div v-if="!userStore.isLoggedIn || !userStore.userId" class="loading-overlay">
      <div class="loading-spinner">
        <el-button type="primary" @click="$router.push('/login')">
          {{ t('common.pleaseLogin') }}
        </el-button>
      </div>
    </div>
    <!-- 数据加载中显示 -->
    <div v-else-if="loading || !hasCheckedPreferences" class="loading-overlay">
      <div class="loading-content">
        <!-- 修改进度条样式 -->
        <el-progress 
          :percentage="loadingProgress"
          :stroke-width="10"
          :show-text="true"
          class="custom-progress"
        />
        <div class="loading-steps">
          <div v-for="(step, index) in loadingSteps" 
               :key="index" 
               :class="['step-item', { 'done': step.done }]">
            <!-- 修改加载图标 -->
            <i v-if="!step.done" class="el-icon-loading loading-icon"></i>
            <i v-else class="el-icon-check"></i>
            <span class="step-text">{{ t(step.textKey) }}</span>
          </div>
        </div>
        <div class="loading-tip">{{ t('recommend.loadingTip') }}</div>
      </div>
    </div>
    <!-- 内容显示 -->
    <template v-else>
      <!-- 侧边标签栏 -->
      <div class="sidebar-tabs">
        <div v-for="(tab, index) in tabs"
             :key="index"
             :class="['tab-item', { active: currentIndex === index }]"
             @click="handleTabClick(index)">
          {{ t(`recommend.tabs.${tab}`) }}
        </div>
      </div>

      <!-- 滑动容器 -->
      <div class="slides-container" :style="slideStyle">
        <div v-for="(slide, index) in slides"
             :key="index"
             class="slide"
             :class="{
               'empty-slide': !slide.favoriteCards || slide.favoriteCards.length === 0,
               'slide-1': index === 0,
               'slide-2': index === 1,
               'slide-3': index === 2,
               'slide-4': index === 3,
               'slide-5': index === 4,
               'slide-6': index === 5,
               active: currentIndex === index
             }">
          <!-- 跳转按钮 -->
          <div v-if="hasPreferences(slide)" class="navigate-button top-right" @click="navigateToPage(index)">
            {{ t('recommend.viewMore') }} <i class="el-icon-arrow-right"></i>
          </div>

          <div class="slide-content">
            <!-- 无偏好时显示中央提示 -->
            <div v-if="!hasPreferences(slide)" class="empty-content">
              <h2>{{ t(`recommend.slides.${slide.titleKey}`) }}</h2>
              <p>{{ t(`recommend.slides.${slide.descriptionKey}`) }}</p>
              <button class="navigate-button center" @click="navigateToPage(index)">
                {{ t('recommend.goToPage', { page: t(`recommend.slides.${slide.titleKey}`) }) }}
              </button>
            </div>

            <!-- 有偏好时显示正常内容 -->
            <template v-else>
              <!-- 第一行：改为卡片轮播 + 描述 -->
              <div class="main-content">
                <!-- 卡片轮播部分 -->
                <div class="swiper">
                  <div class="swiper-wrapper">
                    <div v-for="(card, cardIndex) in slide.favoriteCards"
                         :key="cardIndex"
                         class="swiper-slide"
                         @click="selectCard(card)"
                         :class="{ 'empty-card': card.rating === '-' }">
                      <img
                        :src="getImageUrl(card.image)"
                        :alt="card.title"
                        class="card-image"
                        @error="(e) => {
                          console.error(t('common.imageLoadError'), e.target.src);
                          e.target.src = defaultEmptyImg;
                        }"
                      >
                      <div class="overlay">
                        <span :class="{ 'user-preference': card.userPreference }">
                          {{ card.rating }}
                        </span>
                        <h2>{{ card.title }}</h2>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 描述部分 -->
                <div class="main-description">
                  <h1>{{ selectedCard ? selectedCard.title : t(`recommend.slides.${slide.titleKey}`) }}</h1>
                  <div class="card-details" v-if="selectedCard">
                    <div class="rating-badge">{{ t('recommend.rating') }}: {{ selectedCard.rating || t('common.noRating') }}</div>
                    <p class="card-description">{{ formatDescription(selectedCard.description) || t('common.noDescription') }}</p>
                  </div>
                  <p v-else>{{ t(`recommend.slides.${slide.descriptionKey}`) }}</p>
                </div>
              </div>

              <!-- 第二行：小卡片列表 -->
              <div class="sub-content">
                <div class="cards-row" v-if="slide.subCards.length > 0">
                  <!-- 用户偏好部分 -->
                  <div class="row user-preferences">
                    <div class="row-header">
                      <h3>
                        <span>{{ t('recommend.yourPreferences') }}</span>
                      </h3>
                    </div>
                    <div class="cards-container">
                      <div v-for="(card, cardIndex) in userPreferenceCards.slice(0, 5)"
                           :key="'pref-' + cardIndex"
                           class="sub-card"
                           @click="navigateToSentiment(card)">
                        <img :src="getImageUrl(card.image_url)"
                             :alt="card.folk_name || card.tag_name"
                             @error="(e) => e.target.src = defaultEmptyImg">
                        <div class="card-overlay">
                          <p class="title">{{ card.folk_name || card.tag_name }}</p>
                        </div>
                        <div class="hover-mask">
                          <span class="mask-text">{{ t('recommend.clickForSentiment') }}</span>
                        </div>
                      </div>
                    </div>
                    <div v-if="userPreferenceCards.length > 5"
                         class="more-button"
                         @click="showMorePreferences">
                      {{ t('recommend.more') }} ({{ userPreferenceCards.length - 5 }})
                    </div>
                  </div>

                  <!-- 相似用户偏好部分 -->
                  <div class="row similar-users">
                    <div class="row-header">
                      <h3>
                        <span>{{ t('recommend.recommendedPreferences') }}</span>
                      </h3>
                    </div>
                    <div class="cards-container">
                      <div v-for="(card, cardIndex) in similarUserCards.slice(0, 5)"
                           :key="'similar-' + cardIndex"
                           class="sub-card"
                           @click="navigateToSentiment(card)">
                        <img :src="getImageUrl(card.image_url)"
                             :alt="card.folk_name || card.tag_name"
                             @error="(e) => e.target.src = defaultEmptyImg">
                        <div class="card-overlay">
                          <p class="title">{{ card.folk_name || card.tag_name }}</p>
                        </div>
                        <div class="hover-mask">
                          <span class="mask-text">{{ t('recommend.clickForSentiment') }}</span>
                        </div>
                      </div>
                    </div>
                    <div v-if="similarUserCards.length > 5"
                         class="more-button"
                         @click="showMoreSimilarPreferences">
                      {{ t('recommend.more') }} ({{ similarUserCards.length - 5 }})
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>

      <!-- <div v-if="currentIndex === 4" class="map-container">
        <div class="map-wrapper">
          <world-map-chart />
        </div>
      </div> -->
    </template>

    <!-- 更多偏好弹窗 -->
    <el-dialog
      v-model="showAllPreferencesDialog"
      :title="dialogTitle"
      width="80%"
      class="preferences-dialog"
    >
      <div class="all-preferences-container">
        <div v-for="(card, index) in currentDialogCards"
             :key="index"
             class="preference-card"
             @click="navigateToSentiment(card)">
          <img :src="getImageUrl(card.image_url || card.image)" :alt="card.folk_name || card.tag_name">
          <div class="card-overlay">
            <p class="title">{{ card.folk_name || card.tag_name }}</p>
          </div>
          <div class="hover-mask">
            <span class="mask-text">{{ t('recommend.clickForSentiment') }}</span>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import Swiper from 'swiper'
import { EffectCards } from 'swiper/modules'
import RecommendAPI from "@/api/recommend"
import TagsAPI from "@/api/tags"
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'
import WorldMapChart from './WorldMapChart.vue'
import cultureElements from '@/json/culture_elements_translated.json'

const { t, locale } = useI18n()

// 导入默认图片以备用
import defaultEmptyImg from '@/assets/BookB.jpg'

const currentIndex = ref(0)
const isAnimating = ref(false)
const loading = ref(true)
const userStore = useUserStore()
const router = useRouter()
const selectedCard = ref(null) // 当前选中的卡片
const hasCheckedPreferences = ref(false);  // 是否已检查用户偏好

// 添加进度相关的状态
const loadingProgress = ref(0)
const loadingSteps = ref([
  { textKey: 'recommend.steps.checkLogin', done: false },
  { textKey: 'recommend.steps.getUserPreferences', done: false },
  { textKey: 'recommend.steps.getTags', done: false },
  { textKey: 'recommend.steps.processPlaces', done: false },
  { textKey: 'recommend.steps.processFood', done: false },
  { textKey: 'recommend.steps.processLiterature', done: false },
  { textKey: 'recommend.steps.processFolk', done: false }
])

// 定义所有标签页
const tabs = ref([
  'places',
  'food',
  'literature',
  'folk'
])

// 初始化slides数据结构
const slides = ref([
  {
    titleKey: 'places.title',
    descriptionKey: 'places.description',
    favoriteCards: [],
    subCards: []
  },
  {
    titleKey: 'food.title',
    descriptionKey: 'food.description',
    favoriteCards: [],
    subCards: []
  },
  {
    titleKey: 'literature.title',
    descriptionKey: 'literature.description',
    favoriteCards: [],
    subCards: []
  },
  {
    titleKey: 'folk.title',
    descriptionKey: 'folk.description',
    favoriteCards: [],
    subCards: []
  }
])

// 添加地图相关的状态
const mapData = ref({
  china: {
    hunan: 200,
    guangdong: 150,
    beijing: 120,
    shanghai: 180,
    // ... 其他省份数据
  }
})

// 计算属性：用户偏好卡片
const userPreferenceCards = computed(() =>
  slides.value[currentIndex.value]?.subCards.filter(card => card.userPreference) || []
);

// 计算属性：相似用户卡片
const similarUserCards = computed(() => {
  const currentSlide = slides.value[currentIndex.value];
  if (!currentSlide) return [];
  
  // 获取当前用户的偏好
  const userPreferences = new Set(
    currentSlide.subCards
      .filter(card => card.userPreference)
      .map(card => card.folk_name || card.tag_name)
  );
  
  // 过滤掉与用户偏好重复的推荐
  return currentSlide.subCards.filter(card => {
    const cardName = card.folk_name || card.tag_name;
    return !card.userPreference && !userPreferences.has(cardName);
  });
});

// 弹窗控制
const showAllPreferencesDialog = ref(false);
const dialogTitle = ref('');
const currentDialogCards = ref([]);

// 显示更多用户偏好
const showMorePreferences = () => {
  dialogTitle.value = '全部用户偏好';
  currentDialogCards.value = userPreferenceCards.value.slice(6); // 从第六个元素开始切割数组
  showAllPreferencesDialog.value = true;
  document.body.style.overflow = 'hidden'; // 禁用body滚动
};


// 显示更多相似用户推荐
const showMoreSimilarPreferences = () => {
  dialogTitle.value = '相似用户推荐';
  currentDialogCards.value = similarUserCards.value;
  showAllPreferencesDialog.value = true;
  document.body.style.overflow = 'hidden'; // 禁用body滚动
};

// 监听弹窗关闭
watch(showAllPreferencesDialog, (newVal) => {
  if (!newVal) {
    document.body.style.overflow = ''; // 恢复body滚动
  }
});

// 修改 getImageUrl 函数
const getImageUrl = (url) => {
  if (!url) return defaultEmptyImg;
  // 直接返回完整的 URL
  return url;
};

// 修改 getItemTitle 函数来支持国际化
const getItemTitle = (item) => {
  const name = item.folk_name || item.tag_name || item.title || '';
  
  // 从翻译文件中查找对应的元素
  const element = cultureElements.find(el => el.title === name);
  
  if (element) {
    // 根据当前语言返回对应的标题
    return locale.value === 'en' ? element['title-en'] : element.title;
  }
  
  return name;
};

// 修改 formatDescription 函数来支持国际化
const formatDescription = (description) => {
  if (!description) return t('common.noDescription');
  
  // 如果描述是URL，返回默认文本
  if (description.startsWith('http')) {
    return t('common.clickToView');
  }
  
  // 尝试从翻译文件中查找对应的描述
  const element = cultureElements.find(el => el.description === description);
  
  if (element) {
    // 根据当前语言返回对应的描述
    return locale.value === 'en' ? element['description-en'] : element.description;
  }
  
  return description;
};

// 修改处理标签数据的部分
const processTagData = (tag, tagDetail, isUserPreference, preference) => {
  const tagId = tag.tag_id || tag.id;
  const name = tagDetail.folk_name || tag.tag_name || tag.name || t('common.unknownTag');
  
  // 从翻译文件中查找对应的元素
  const element = cultureElements.find(el => el.title === name);
  
  const translatedName = element ? 
    (locale.value === 'en' ? element['title-en'] : element.title) : 
    name;
  
  const translatedDescription = element ? 
    (locale.value === 'en' ? element['description-en'] : element.description) : 
    (tagDetail.description || tag.description || t('common.noDescription'));

  return {
    ...tag,
    userPreference: isUserPreference,
    userScore: isUserPreference ? preference?.score || 0.7 : 0,
    title: translatedName,
    image_url: tagDetail.image_url || defaultEmptyImg,
    folk_name: translatedName,
    tag_name: translatedName,
    description: translatedDescription
  };
};

// 修改 fetchData 函数
const fetchData = async () => {
  loading.value = true;
  hasCheckedPreferences.value = false;
  loadingProgress.value = 0;
  
  try {
    // 更新第一步状态
    loadingSteps.value[0].done = true;
    loadingProgress.value = 10;

    console.log("开始获取数据");
    const userId = userStore.userId;
    console.log("当前用户ID:", userId);

    if (!userId || !userStore.isLoggedIn) {
      console.log("用户未登录，跳转到登录页面");
      router.push('/login');
      return;
    }

    // 获取用户偏好数据
    const preferenceResponse = await RecommendAPI.getPerferenceAPI(userId);
    loadingSteps.value[1].done = true;
    loadingProgress.value = 25;
    console.log('用户偏好数据:', preferenceResponse.data);

    // 检查用户是否有任何偏好
    const hasPreferences = preferenceResponse?.data?.detailed_preferences &&
      Object.values(preferenceResponse.data.detailed_preferences).some(
        prefs => Array.isArray(prefs) && prefs.length > 0
      );

    if (!hasPreferences) {
      console.log("用户没有偏好数据");
      hasCheckedPreferences.value = true;
      loading.value = false;
      return;
    }

    // 获取所有标签数据
    const tagsResponse = await TagsAPI.getAllTagsAPI();
    loadingSteps.value[2].done = true;
    loadingProgress.value = 40;
    console.log('所有标签数据:', tagsResponse.data);

    if (preferenceResponse?.data && tagsResponse?.data) {
      const userPreferences = preferenceResponse.data;
      const allTags = tagsResponse.data;

      // 主题映射
      const themeIndexMap = {
        'spot': 0,    // 名胜古迹
        'food': 1,    // 美食文化
        'literature': 2, // 影视文学
        'folk': 3,    // 非遗民俗
      };

      // 按主题分类标签
      const tagsByTheme = {
        spot: [],
        food: [],
        literature: [],
        folk: []
      };

      // 将标签分类到对应主题
      allTags.forEach(tag => {
        const theme = tag.theme_name?.toLowerCase();
        if (tagsByTheme.hasOwnProperty(theme)) {
          tagsByTheme[theme].push(tag);
        }
      });

      // 初始化所有主题的数据结构
      slides.value = slides.value.map(slide => ({
        ...slide,
        favoriteCards: [],
        subCards: []
      }));

      // 处理每个主题
      for (const [theme, tags] of Object.entries(tagsByTheme)) {
        const slideIndex = themeIndexMap[theme];
        if (slideIndex === undefined || !Array.isArray(tags)) continue;

        // 获取该主题的用户偏好
        const themePreferences = userPreferences.detailed_preferences[theme] || [];
        console.log(`处理${theme}主题数据:`, {
          偏好数量: themePreferences.length,
          标签数量: tags.length
        });

        // 获取用户偏好的标签ID
        const userPreferredTagIds = new Set(
          themePreferences
            .filter(pref => pref.score > 0)
            .map(pref => pref.tag_id)
        );

        // 获取所有需要查询的标签ID
        const tagIds = tags.map(tag => tag.tag_id || tag.id).filter(id => id);
        
        if (tagIds.length === 0) continue;

        try {
          // 获取标签详细信息
          const tagDetailsResponse = await RecommendAPI.getTagDetailAPI(tagIds);
          console.log(`${theme}主题标签详情:`, tagDetailsResponse);

          if (!tagDetailsResponse?.tag_details) continue;

          // 创建标签详情映射
          const tagDetailsMap = new Map(
            tagDetailsResponse.tag_details.map(detail => [detail.tag_id, detail])
          );

          // 处理标签数据
          const processedTags = tags.map(tag => {
            const tagId = tag.tag_id || tag.id;
            const isUserPreference = userPreferredTagIds.has(tagId);
            const preference = themePreferences.find(p => p.tag_id === tagId);
            const tagDetail = tagDetailsMap.get(tagId) || {};
            
            return processTagData(tag, tagDetail, isUserPreference, preference);
          });

          // 更新 slides
          if (processedTags.length > 0) {
            const preferredTags = processedTags.filter(tag => tag.userPreference);
            const similarTags = processedTags.filter(tag => !tag.userPreference);

            slides.value[slideIndex].favoriteCards = preferredTags.slice(0, 5).map(tag => ({
              title: tag.title,
              image: tag.image_url,
              rating: (tag.userScore * 10).toFixed(1),
              userPreference: true,
              description: tag.description,
              folk_name: tag.folk_name,
              tag_name: tag.tag_name
            }));

            slides.value[slideIndex].subCards = [
              ...preferredTags,  // 用户偏好
              ...similarTags.slice(0, 10)  // 相似推荐
            ];
          }

          // 更新对应主题的进度
          loadingSteps.value[3 + slideIndex].done = true;
          loadingProgress.value = 40 + ((slideIndex + 1) * 15);
        } catch (error) {
          console.error(`处理${theme}主题数据时出错:`, error);
        }
      }
    }
  } catch (error) {
    console.error("获取数据失败:", error);
  } finally {
    // 完成所有加载
    loadingProgress.value = 100;
    hasCheckedPreferences.value = true;
    loading.value = false;
    nextTick(() => {
      initSwiper();
      if (slides.value[currentIndex.value]?.favoriteCards?.length > 0) {
        selectedCard.value = slides.value[currentIndex.value].favoriteCards[0];
      }
    });
  }
};

// 计算滑动样式
const slideStyle = computed(() => ({
  transform: `translateY(-${currentIndex.value * 100}vh)`
}))

// 处理标签点击
const handleTabClick = (index) => {
  currentIndex.value = index;
};

// 处理滚轮事件
const handleWheel = (e) => {
  if (showAllPreferencesDialog.value) return;
  if (isAnimating.value) return;

  isAnimating.value = true;
  setTimeout(() => {
    isAnimating.value = false;
  }, 1000);

  if (e.deltaY > 0 && currentIndex.value < slides.value.length - 1) {
    currentIndex.value++;
  } else if (e.deltaY < 0 && currentIndex.value > 0) {
    currentIndex.value--;
  }
};

// 处理地图点击事件
const handleMapClick = (region) => {
  if (region === 'china') {
    // 实现地图放大逻辑
  }
}

// 处理返回世界地图
const handleBackToWorld = () => {
  // 实现返回世界地图逻辑
}

// 初始化 Swiper
const initSwiper = () => {
  console.log("初始化 Swiper");
  const swiperElements = document.querySelectorAll('.swiper');
  if (swiperElements.length > 0) {
    swiperElements.forEach((element, index) => {
      console.log(`初始化第 ${index} 个 Swiper`);
      new Swiper(element, {
        modules: [EffectCards],
        effect: 'cards',
        grabCursor: true,
        loop: true,  // 启用循环模式
        cardsEffect: {
          slideShadows: false,  // 禁用阴影以提高性能
          perSlideRotate: 4,    // 减少旋转角度
          perSlideOffset: 8,    // 减少偏移量，使卡片更紧凑
        },
        autoplay: {
          delay: 3000,          // 3秒切换一次
          disableOnInteraction: false, // 用户交互后不停止自动播放
        },
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
        },
        on: {
          click: function(swiper, event) {
            // 获取点击位置
            const clickX = event.clientX - this.el.getBoundingClientRect().left;
            const halfWidth = this.el.offsetWidth / 2;

            // 点击左侧向前，右侧向后
            if (clickX < halfWidth) {
              this.slidePrev();
            } else {
              this.slideNext();
            }
          }
        }
      });
    });
  } else {
    console.warn("未找到 Swiper 元素");
  }
};

// 监听 currentIndex 变化，重新初始化 Swiper
watch(currentIndex, () => {
  console.log("currentIndex 变化:", currentIndex.value);
  nextTick(() => {
    initSwiper();
  });
});

// 选择卡片
const selectCard = (card) => {
  console.log('选中卡片:', card);
  selectedCard.value = card;

  // 找到当前卡片在轮播中的索引
  const currentSlide = slides.value[currentIndex.value];
  const cardIndex = currentSlide.favoriteCards.findIndex(c => c.title === card.title);

  // 如果找到了卡片，并且不是最后一个，则自动切换到下一个卡片
  if (cardIndex !== -1 && cardIndex < currentSlide.favoriteCards.length - 1) {
    // 使用setTimeout模拟点击后的延迟切换效果
    setTimeout(() => {
      selectedCard.value = currentSlide.favoriteCards[cardIndex + 1];
      console.log('自动切换到下一个卡片:', selectedCard.value);

      // 如果有Swiper实例，也更新轮播位置
      if (swiperInstances[currentIndex.value]) {
        swiperInstances[currentIndex.value].slideTo(cardIndex + 1);
      }
    }, 300);
  }
};

// 检查主题是否有偏好
const hasPreferences = (slide) => {
  return slide.favoriteCards && slide.favoriteCards.length > 0;
};

// 修改跳转到情感分析页面的方法
const navigateToSentiment = (card) => {
  const name = card.folk_name || card.tag_name;
  // 获取当前路由的 query 参数
  const query = {
    name: name,
    value: '1',
    theme: '1'
  };
  
  // 根据卡片类型设置不同的 theme 和 value 值
  if (currentIndex.value === 0) {
    query.theme = '1';
    query.value = '1';
  } else if (currentIndex.value === 1) {
    query.theme = '1';
    query.value = '3';
  } else if (currentIndex.value === 2) {
    // 这里需要根据文学子类型设置不同的 theme
    const literatureType = getLiteratureType(card);
    query.theme = literatureType;
    query.value = '2';
  } else if (currentIndex.value === 3) {
    query.theme = '1';
    query.value = '4';
  }

  router.push({
    path: '/detail',
    query,
  });
};

// 添加判断文学子类型的函数
const getLiteratureType = (card) => {
  // 这里需要根据卡片的具体信息来判断属于哪个子类型
  // 假设卡片中有一个 type 字段表示子类型
  if (card.type === '表演艺术') {
    return '2';
  } else if (card.type === '新媒体艺术') {
    return '3';
  } else if (card.type === '古诗词') {
    return '4';
  } else {
    return '1'; // 默认为文学类型
  }
};

// 修改页面跳转方法
const navigateToPage = (index) => {
  let route = '/';

  switch (index) {
    case 0:
      route = '/placeOfInterest';
      break;
    case 1:
      route = '/food';
      break;
    case 2:
      route = '/filmLiterature';
      break;
    case 3:
      route = '/folkCustom';
      break;
    case 4:
      route = '/recommendMap';
      break;
    default: route = '/';
  }

  router.push({
    path: route
  });
};

// 当切换标签页时，选择当前页的第一个卡片
watch(currentIndex, (newIndex) => {
  if (slides.value[newIndex]?.favoriteCards?.length > 0) {
    selectedCard.value = slides.value[newIndex].favoriteCards[0];
    console.log('切换标签后选中卡片:', selectedCard.value);
  } else {
    selectedCard.value = null;
  }
});

watch(slides, (newSlides) => {
  // 检查所有主题是否都已正确加载
  const allThemesLoaded = newSlides.every(slide => 
    Array.isArray(slide.favoriteCards) && Array.isArray(slide.subCards)
  );
  
  if (allThemesLoaded) {
    loading.value = false;
  }
}, { deep: true });

onMounted(async () => {
  loading.value = true;
  hasCheckedPreferences.value = false;
  
  try {
    // 简单检查用户登录状态
    if (!userStore.isLoggedIn || !userStore.userId) {
      console.log("用户未登录，重定向到登录页面");
      router.push('/login');
      return;
    }

    console.log("当前登录用户:", {
      userId: userStore.userId,
      username: userStore.username
    });

    // 加载数据
    await fetchData();
  } catch (error) {
    console.error("初始化失败:", error);
  }
});
</script>

<style lang="scss">
/* 移除灰点 */
.fullpage-container::before,
.fullpage-container::after {
  display: none !important;
}

/* 移除所有可能的灰点 */
.slide::before,
.slide::after,
.slides-container::before,
.slides-container::after {
  display: none !important;
}

.fullpage-container {
  height: 695px;
  overflow: hidden;
  position: relative;
  font-family: 'HelveticaNeue', serif;
}

.slides-container {
  height: 90%;
  width: 100%;
  position: absolute;
  top: 0;
  left: 0;
  transition: transform 1s ease;
}

.slide {
  height: 100vh;
  width: 100%;
  position: relative;
  background-color: transparent;
}

/* 只有空白幻灯片才显示蒙版 */
.empty-slide.slide-1 { background-color: rgba(52, 152, 219, 0.2); }  /* 半透明蓝色 */
.empty-slide.slide-2 { background-color: rgba(241, 196, 15, 0.2); }  /* 半透明黄色 */
.empty-slide.slide-3 { background-color: rgba(231, 76, 60, 0.2); }   /* 半透明红色 */
.empty-slide.slide-4 { background-color: rgba(241, 196, 15, 0.2); }  /* 半透明黄色 */
.empty-slide.slide-5 { background-color: transparent; }   /* 发现更多模块不需要蒙版 */
.empty-slide.slide-6 { background-color: rgba(52, 152, 219, 0.2); }  /* 半透明蓝色 */

.slide-content {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;  /* 调整内容宽度 */

}

/* 活动页面的特效 */
.slide.active {
  animation: fadeIn 1s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 新增样式 */
.sidebar-tabs {
  position: fixed;
  left: 0;
  top: 54%;
  transform: translateY(-50%);
  z-index: 100;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20px 10px;
  border-radius: 0 10px 10px 0;
}

.tab-item {
  writing-mode: vertical-lr;
  padding: 15px 5px;
  cursor: pointer;
  transition: all 0.3s;

  font-family: 'HelveticaNeue', serif;
}

.tab-item.active {
  color: #b71c1c;
  font-weight: bold;
}

.main-content {
  display: flex;
  gap: 30px;
  align-items: center;
  padding: 0 5%;
  margin-left: -10px; /* 添加左边距使其与"您的偏好"标签对齐 */
  margin-bottom: 30px;
}

.main-description {
  flex: 1;
  margin-left: 100px;
  max-width: 700px;

  .card-details {
    margin-top: 20px;
  }

  .rating-badge {
    display: inline-block;
    background-color: #b71c1c;
    color: white;
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 0.9em;
    margin-bottom: 15px;
    font-family: 'HelveticaNeue', serif;
  }

  .card-description {
    line-height: 1.6;
    font-size: 1.1em;
    color: #333;
    max-height: 180px;
    overflow-y: auto;
    padding-right: 10px;
    font-family: 'HelveticaNeue', serif;
  }

  .card-description::-webkit-scrollbar {
    width: 4px;
  }

  .card-description::-webkit-scrollbar-track {
    background: #f1f1f1;
  }

  .card-description::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 2px;
  }
}

.sub-content {
  width: 90%;
  margin: 0 auto;
  padding-top: 20px;
  padding-left: 10px; /* 添加左边距使内容对齐 */
  max-width: 1300px; /* 限制最大宽度 */
  height: 300px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 15px;
  padding: 20px 20px 5px 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  margin-bottom: 40px;
  margin-left: 80px;
  margin-top: -10px;
  padding-bottom: -10px;
}

.cards-row {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-left: 30px; /* 增加左边距 */
}

.row {
  display: flex;
  width: 100%;
  gap: 15px;
  flex-wrap: nowrap; /* 确保不换行 */
  margin-bottom: 20px;
  position: relative; /* 为绝对定位的按钮提供参考点 */
  align-items: flex-start; /* 顶部对齐 */
}

/* 更多按钮样式 */
.more-button {
  writing-mode: vertical-lr; /* 竖排文字 */
  padding: 15px 7px;
  background-color: #b71c1c;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
  white-space: nowrap;
  font-size: 1.2em;
  height: 101px; /* 与卡片高度一致 */
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0; /* 防止收缩 */
  font-family: 'HelveticaNeue', serif;
}

.more-button:hover {
  background-color: #7f0c07;
}

/* 用户偏好和相似用户的行样式 */
.user-preferences, .similar-users {
  display: flex;
  flex-direction: row; /* 水平排列 */
  align-items: flex-start; /* 顶部对齐 */
  width: 100%;
  margin-bottom: 20px;
}

.row-header {
  display: flex;
  height: 101px;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* 添加垂直居中 */
  padding: 15px 5px;
  background-color: #b71c1c; /* 改为红色背景 */
  border-radius: 8px;
  margin-right: 5px;
  flex-shrink: 0;
  width: 30px; /* 固定宽度 */
}

.row-header h3 {
  margin: 0;
  font-size: 1.2em;
  color: white; /* 改为白色文字 */
  display: flex;
  flex-direction: column;
  line-height: 1.8;
  justify-content: center; /* 添加垂直居中 */
  height: 100%; /* 使其占满整个高度 */
  font-family: 'HelveticaNeue', serif;
}

.row-header h3 span {
  display: block;
  text-align: center;
  writing-mode: vertical-lr;
  letter-spacing: 2px;
}


.similar-users .sub-card {
  border: 1px solid #ddd;
}

.sub-card {
  flex: 0 0 180px;
  height: 130px;
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
  cursor: pointer;
  
  /* 添加悬停效果 */
  &:hover {
    transform: translateY(-5px);
    
    .hover-mask {
      opacity: 1;
    }
  }
}

.sub-card img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.card-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 8px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
}

.card-overlay .title {
  margin: 0;
  color: white;
  font-size: 1.1em;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  font-family: 'HelveticaNeue', serif;
}

/* 卡片容器样式 */
.cards-container {
  display: flex;
  gap: 15px;
  position: relative;
  flex-wrap: nowrap;
  overflow-x: auto;
  scrollbar-width: none; /* Firefox */
  flex: 1; /* 让容器占据剩余空间 */
  min-width: 0; /* 防止flex项目溢出 */

  &::-webkit-scrollbar {
    display: none; /* Chrome, Safari, Edge */
  }
}

.map-container {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 40px;
}

.map-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
}

.china-map {
  width: 100%;
  height: 100%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

.province-region {
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover {
    filter: brightness(1.1);
    
    .region-tooltip {
      opacity: 1;
    }
  }
}

.region-tooltip {
  position: absolute;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 14px;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
}

/* 添加 Swiper 相关样式 */
.swiper {
  width: 300px;
  height: 300px;
  margin-top: -30px;
  margin-left: 30px; /* 增加左边距 */
}

.swiper-slide {
  position: relative;
  width: 100%;
  height: 100%;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  background: #fff; /* 添加背景色以便于查看图片加载状态 */
}

.swiper-slide:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
}

.swiper-slide img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
}

.overlay {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(to top, #0f2027, transparent, transparent);
  border-radius: 10px;
}

.overlay span {
  position: absolute;
  top: 0;
  right: 0;
  color: #fff;
  padding: 7px 18px;
  margin: 10px;
  border-radius: 20px;
  letter-spacing: 2px;
  font-size: 0.8rem;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.095);
  box-shadow: inset 2px -2px 20px rgba(214, 214, 214, 0.2),
    inset -3px 3px 3px rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(74px);
  font-family: 'HelveticaNeue', serif;
}

.overlay h2 {
  position: absolute;
  bottom: 0;
  left: 0;
  color: #fff;
  font-weight: 400;
  font-size: 1.5rem;
  line-height: 1.4;
  margin: 0 0 20px 20px;
  font-family: 'HelveticaNeue', serif;
}

.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.95);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 30px;
  width: 80%;
  max-width: 600px;
}

.loading-steps {
  margin-top: 20px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 15px;
}

.step-item {
  display: flex;
  align-items: center;
  color: #666;
  transition: all 0.3s;
  font-size: 14px;
  
  &.done {
    color: #b71c1c;
  }
}

.loading-icon {
  color: #b71c1c;
  margin-right: 10px;
  font-size: 16px;
  animation: rotating 1s linear infinite;
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.el-icon-check {
  color: #b71c1c;
  margin-right: 10px;
  font-size: 16px;
}

.step-text {
  font-size: 14px;
  margin-left: 8px;
}

.loading-tip {
  margin-top: 10px;
  color: #909399;
  font-size: 12px;
  text-align: center;
}

.empty-card {
  opacity: 0.5;
  cursor: default !important;
}

.empty-card:hover {
  transform: none !important;
}

.user-preference {
  background: rgba(52, 152, 219, 0.2) !important;
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 10px;
  display: block;
}

.empty-card .card-image {
  opacity: 0.5;
}

.preferences-dialog {
  .all-preferences-container {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
    padding: 20px;
    max-height: 70vh;
    overflow-y: auto;
    overscroll-behavior: contain;
  }

  .all-preferences-container::-webkit-scrollbar {
    width: 8px;
  }

  .all-preferences-container::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
  }

  .all-preferences-container::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 4px;
  }

  .all-preferences-container::-webkit-scrollbar-thumb:hover {
    background: #555;
  }

  .preference-card {
    position: relative;
    height: 130px;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.3s;

    &:hover {
      transform: translateY(-5px);
    }

    img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .card-overlay {
      position: absolute;
      bottom: 0;
      left: 0;
      right: 0;
      padding: 8px;
      background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
    }

    .title {
      margin: 0;
      color: white;
      font-size: 0.95em;
      text-align: center;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  }
}

.swiper-button-next,
.swiper-button-prev {
  color: white;
  background: rgba(0, 0, 0, 0.3);
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.swiper-button-next:after,
.swiper-button-prev:after {
  font-size: 14px;
}

.swiper-button-next {
  right: 10px;
}

.swiper-button-prev {
  left: 10px;
}

.swiper-slide {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  }
}

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  padding: 0 20%;

  h2 {
    font-size: 2.5rem;
    margin-bottom: 1rem;
    color: #333;
    font-family: 'HelveticaNeue', serif;
  }

  p {
    font-size: 1.2rem;
    margin-bottom: 2rem;
    color: #666;
    line-height: 1.6;
    font-family: 'HelveticaNeue', serif;
  }
}

.navigate-button {
  padding: 10px 20px;
  background-color: #b71c1c;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s, transform 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;

  &:hover {
    background-color: #7f0c07;
    transform: translateY(-2px);
  }

  &.center {
    font-size: 1.2rem;
    padding: 12px 24px;
  }

  &.top-right {
    position: absolute;
    top: 10px;
    right: 10px;
    z-index: 1;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }
}

.fullpage-container {
  font-family: 'HelveticaNeue', serif;
}

.tab-item,
.main-description h2,
.main-description p,
.card-description,
.row-header h3,
.card-overlay .title,
.more-button,
.empty-content h2,
.empty-content p,
.navigate-button,
.rating-badge,
.overlay h2,
.overlay span,
.region-tooltip,
.loading-spinner {
  font-family: 'HelveticaNeue', serif;
}

.hover-mask {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.mask-text {
  color: white;
  font-size: 14px;
  font-weight: 500;
  text-align: center;
  padding: 8px 12px;
  border: 1px solid white;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.2);
}

/* 自定义进度条样式 */
.custom-progress {
  width: 100%;
  
  :deep(.el-progress-bar__outer) {
    background-color: #f5f5f5;
    height: 10px;
    border-radius: 5px;
  }
  
  :deep(.el-progress-bar__inner) {
    background-color: #b71c1c;
    border-radius: 5px;
  }
  
  :deep(.el-progress__text) {
    color: #b71c1c;
    font-size: 14px;
    font-weight: bold;
  }
}

/* 加载图标动画 */
.loading-icon {
  color: #b71c1c;
  margin-right: 10px;
  font-size: 16px;
  animation: rotating 1s linear infinite;
}

@keyframes rotating {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>

