<template>
  <div class="fullpage-container" @wheel="handleWheel">
    <!-- 添加加载状态 -->
    <div v-if="loading" class="loading-overlay">
      <div class="loading-spinner">加载中...</div>
    </div>

    <template v-else>
      <!-- 侧边标签栏 -->
      <div class="sidebar-tabs">
        <div v-for="(tab, index) in tabs"
             :key="index"
             :class="['tab-item', { active: currentIndex === index }]"
             @click="handleTabClick(index)">
          {{ tab }}
        </div>
      </div>

      <!-- 滑动容器 - 移除灰点 -->
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
          <!-- 跳转按钮 - 有偏好时显示在右上角 -->
          <div v-if="hasPreferences(slide)" class="navigate-button top-right" @click="navigateToPage(index)">
            查看更多 <i class="el-icon-arrow-right"></i>
          </div>

          <div class="slide-content">
            <!-- 无偏好时显示中央提示 -->
            <div v-if="!hasPreferences(slide)" class="empty-content">
              <h2>{{ slide.title }}</h2>
              <p>{{ slide.description }}</p>
              <button class="navigate-button center" @click="navigateToPage(index)">
                前往{{ slide.title }}页面
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
                        :src="card.image"
                        :alt="card.title"
                        class="card-image"
                        @error="(e) => {
                          console.error('图片加载失败:', e.target.src);
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
                  <h1>{{ selectedCard ? selectedCard.title : slide.title }}</h1>
                  <div class="card-details" v-if="selectedCard">
                    <div class="rating-badge">评分: {{ selectedCard.rating || '暂无评分' }}</div>
                    <p class="card-description">{{ formatDescription(selectedCard.description) || '暂无描述' }}</p>
                  </div>
                  <p v-else>{{ slide.description }}</p>
                </div>
              </div>

              <!-- 第二行：小卡片列表 -->
              <div class="sub-content">
                <div class="cards-row" v-if="slide.subCards.length > 0">
                  <!-- 用户偏好部分 -->
                  <div class="row user-preferences">
                    <div class="row-header">
                      <h3>
                        <span>您</span>
                        <span>的</span>
                        <span>喜</span>
                        <span>好</span>
                      </h3>
                    </div>
                    <div class="cards-container">
                      <div v-for="(card, cardIndex) in userPreferenceCards.slice(0, 5)"
                           :key="'pref-' + cardIndex"
                           class="sub-card">
                        <img :src="getImageUrl(card.image)"
                             :alt="card.folk_name || card.tag_name"
                             @error="(e) => e.target.src = defaultEmptyImg">
                        <div class="card-overlay">
                          <p class="title">{{ card.folk_name || card.tag_name }}</p>
                        </div>
                      </div>
                    </div>
                    <div v-if="userPreferenceCards.length > 5"
                         class="more-button"
                         @click="showMorePreferences">
                      更多 ({{ userPreferenceCards.length - 5 }})
                    </div>
                  </div>

                  <!-- 相似用户偏好部分 -->
                  <div class="row similar-users">
                    <div class="row-header">
                      <h3>
                        <span>推</span>
                        <span>荐</span>
                        <span>偏</span>
                        <span>好</span>
                      </h3>
                    </div>
                    <div class="cards-container">
                      <div v-for="(card, cardIndex) in similarUserCards.slice(0, 5)"
                           :key="'similar-' + cardIndex"
                           class="sub-card">
                        <img :src="getImageUrl(card.image)"
                             :alt="card.folk_name || card.tag_name"
                             @error="(e) => e.target.src = defaultEmptyImg">
                        <div class="card-overlay">
                          <p class="title">{{ card.folk_name || card.tag_name }}</p>
                        </div>
                      </div>
                    </div>
                    <div v-if="similarUserCards.length > 5"
                         class="more-button"
                         @click="showMoreSimilarPreferences">
                      更多 ({{ similarUserCards.length - 5 }})
                    </div>
                  </div>
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>

      <div v-if="currentIndex === 5" class="map-container">
        <div class="map-controls">
          <button v-if="isMapZoomed"
                  @click="handleBackToWorld"
                  class="back-button">
            返回世界地图
          </button>
        </div>

        <div class="map-wrapper" :class="{ 'zoomed': isMapZoomed }">
          <div v-if="!isMapZoomed" class="world-map">
            <!-- 世界地图 SVG 或图片 -->
            <div class="map-region china"
                 @click="handleMapClick('china')">
              <div class="region-tooltip">
                中国地区: {{ mapData.global.asia }}位相似用户
              </div>
            </div>
            <!-- 其他地区类似 -->
          </div>

          <div v-else class="china-map">
            <!-- 中国地图 SVG 或图片 -->
            <div v-for="(count, province) in mapData.china"
                 :key="province"
                 class="province-region"
                 :class="province">
              <div class="region-tooltip">
                {{ province }}: {{ count }}位相似用户
              </div>
            </div>
          </div>
        </div>
      </div>
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
             class="preference-card">
          <img :src="getImageUrl(card.image)" :alt="card.title">
          <div class="card-overlay">
            <p class="title">{{ card.folk_name || card.tag_name }}</p>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import Swiper from 'swiper'
import { EffectCards } from 'swiper/modules'
import RecommendAPI from "@/api/recommend"
import TagsAPI from "@/api/tags"
import 'swiper/css'
import 'swiper/css/effect-cards'
import { useUserStore } from '@/stores/user' // 导入用户存储
import { useRouter } from 'vue-router' // 导入路由

// 导入默认图片以备用
import defaultEmptyImg from '@/assets/BookB.jpg'

const currentIndex = ref(0)
const isAnimating = ref(false)
const loading = ref(true)
const userStore = useUserStore() // 使用用户存储
const selectedCard = ref(null) // 当前选中的卡片
const router = useRouter() // 使用路由

// 定义所有标签页
const tabs = ['名胜古迹', '美食文化', '影视文学', '非遗民俗', '红色人物', '发现更多']

// 初始化slides数据结构
const slides = ref([
  {
    title: '名胜古迹',
    description: '探索湖南历史文化遗产',
    favoriteCards: [],
    subCards: []
  },
  {
    title: '美食文化',
    description: '品味湖南特色美食',
    favoriteCards: [],
    subCards: []
  },
  {
    title: '影视文学',
    description: '感受湖南文化艺术',
    favoriteCards: [],
    subCards: []
  },
  {
    title: '非遗民俗',
    description: '传承湖南非物质文化遗产',
    favoriteCards: [],
    subCards: []
  },
  {
    title: '红色人物',
    description: '追忆湖南革命历史',
    favoriteCards: [],
    subCards: []
  },
  {
    title: '发现更多',
    description: '探索更多湖南文化',
    favoriteCards: [],
    subCards: []
  }
])

// 添加地图相关的状态
const isMapZoomed = ref(false)
const selectedRegion = ref(null)
const mapData = ref({
  global: {
    // 示例数据：各地区用户数量
    asia: 1200,
    europe: 850,
    america: 650,
    africa: 320,
  },
  china: {
    // 示例数据：中国各省份用户数量
    beijing: 150,
    shanghai: 180,
    guangdong: 200,
    // ... 其他省份
  }
})

// 计算属性：用户偏好卡片
const userPreferenceCards = computed(() =>
  slides.value[currentIndex.value]?.subCards.filter(card => card.userPreference) || []
);

// 计算属性：相似用户卡片
const similarUserCards = computed(() =>
  slides.value[currentIndex.value]?.subCards.filter(card => !card.userPreference) || []
);

// 弹窗控制
const showAllPreferencesDialog = ref(false);
const dialogTitle = ref('');
const currentDialogCards = ref([]);

// 显示更多用户偏好
const showMorePreferences = () => {
  dialogTitle.value = '全部用户偏好';
  currentDialogCards.value = userPreferenceCards.value;
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

// 简化图片处理函数
const getImageUrl = (url) => {
  if (!url) return defaultEmptyImg;
  // 直接返回完整的 URL
  return url;
};

// 获取用户推荐数据和标签信息
const fetchData = async () => {
  try {
    loading.value = true;
    console.log("fetchData 开始执行");

    // 获取当前登录用户的ID
    const userId = userStore.user?.id || 1; // 如果没有登录用户，则使用默认ID 1
    console.log("当前用户ID:", userId);

    const preferenceResponse = await RecommendAPI.getPerferenceAPI(userId);
    const tagsResponse = await TagsAPI.getAllTagsAPI();

    console.log('所有标签数据:', tagsResponse.data);
    console.log('用户偏好数据:', preferenceResponse.data);

    // 检查数据结构并创建默认结构
    if (!preferenceResponse?.data?.detailed_preferences) {
      console.warn('用户偏好数据结构不完整，创建默认结构');
      preferenceResponse.data = {
        detailed_preferences: {},
        similar_users: [],
        theme_preferences: {}
      };
    }

    if (preferenceResponse?.data && tagsResponse?.data) {
      const userPreferences = preferenceResponse.data;
      const tagData = tagsResponse.data;

      // 如果 tagData 不是预期的格式，进行转换
      let processedTagData = tagData;
      if (!Array.isArray(tagData.folk) && !Array.isArray(tagData.food)) {
        console.log('标签数据不是预期格式，进行转换');
        processedTagData = {
          'folk': [],
          'food': [],
          'literature': [],
          'spot': [],
          'history': []
        };

        // 将所有标签按主题分类
        if (Array.isArray(tagData)) {
          tagData.forEach(tag => {
            const theme = (tag.theme_name || 'other').toLowerCase();
            if (processedTagData[theme]) {
              processedTagData[theme].push(tag);
            }
          });
        }
      }

      // 打印每个主题的标签数量
      for (const [theme, tags] of Object.entries(processedTagData)) {
        console.log(`主题 ${theme} 的标签数量:`, Array.isArray(tags) ? tags.length : '不是数组');
      }

      for (const [theme, tags] of Object.entries(processedTagData)) {
        let slideIndex = -1;
        switch(theme.toLowerCase()) {
          case 'spot': slideIndex = 0; break;
          case 'food': slideIndex = 1; break;
          case 'literature': slideIndex = 2; break;
          case 'folk': slideIndex = 3; break;
          case 'history': slideIndex = 4; break;
        }

        if (slideIndex !== -1 && Array.isArray(tags)) {  // 确保 tags 是数组
          console.log(`处理主题 ${theme} 的标签数据，共 ${tags.length} 个标签`);

          // 如果没有该主题的偏好数据，创建空数组
          if (!userPreferences.detailed_preferences[theme.toLowerCase()]) {
            userPreferences.detailed_preferences[theme.toLowerCase()] = [];
          }

          const themePreferences = userPreferences.detailed_preferences[theme.toLowerCase()] || [];
          console.log(`用户对主题 ${theme} 的偏好数量:`, themePreferences.length);

          const similarUsers = userPreferences.similar_users || [];
          console.log(`相似用户数量:`, similarUsers.length);

          // **提取用户偏好的 tag_id**
          const userPreferredTagIds = themePreferences.map(p => p.tag_id).filter(id => typeof id === "number");
          console.log(`用户偏好的标签ID:`, userPreferredTagIds);

          // **提取相似用户推荐的 tag_id**
          const recommendedTagIds = similarUsers.flatMap(simUser =>
              Object.entries(simUser.preferences || {})
                  .filter(([_, prefData]) => prefData.theme_name.toLowerCase() === theme.toLowerCase())
                  .map(([tagId]) => parseInt(tagId))
          ).filter(id => typeof id === "number");
          console.log(`相似用户推荐的标签ID:`, recommendedTagIds);

          // **合并所有 tag_id**
          const tagIds = [...new Set([...userPreferredTagIds, ...recommendedTagIds])];

          console.log(`主题 ${theme} 需要查询的 tagIds:`, tagIds);

          // 如果没有用户偏好和推荐，创建一些示例数据
          if (userPreferredTagIds.length === 0 && tags.length > 0) {
            console.log(`为主题 ${theme} 创建示例用户偏好数据`);
            // 随机选择最多5个标签作为用户偏好
            const sampleTags = tags.slice(0, Math.min(5, tags.length));
            sampleTags.forEach(tag => {
              userPreferredTagIds.push(tag.tag_id || tag.id);
            });
          }

          if (tagIds.length > 0) {
            console.log(`即将调用 getTagDetailAPI 获取 ${theme} 的详细信息...`);
            const tagDetailsResponse = await RecommendAPI.getTagDetailAPI(tagIds);
            console.log(`getTagDetailAPI 返回数据:`, tagDetailsResponse);

            const tagDetailsArray = Array.isArray(tagDetailsResponse?.tag_details)
                ? tagDetailsResponse.tag_details
                : [];
            console.log(`标签详情数组长度:`, tagDetailsArray.length);

            const tagDetailsMap = new Map(
                tagDetailsArray
                    .filter(tag => typeof tag.tag_id === "number")
                    .map(tag => [tag.tag_id, tag])
            );

            console.log("tagDetailsMap 赋值后:", tagDetailsMap);
            console.log(`getTagDetailAPI 返回 ${theme} 数据:`, tagDetailsResponse.tag_details);

            // 处理用户偏好
            const preferredTags = tags.filter(tag => userPreferredTagIds.includes(tag.tag_id || tag.id))
                .map(tag => {
                  const preference = themePreferences.find(p => p.tag_id === (tag.tag_id || tag.id));
                  const tagDetail = tagDetailsMap.get(tag.tag_id || tag.id) || {};

                  console.log(`处理用户偏好标签 ${tag.tag_id || tag.id}:`, {
                    preference,
                    tagDetail,
                    image: tagDetail.image_url || tag.image_url || defaultEmptyImg
                  });

                  return {
                    ...tag,
                    userScore: preference?.score || 0.7,  // 默认分数0.7
                    name: tagDetail.folk_name || tag.folk_name || tag.tag_name || '未知标签',
                    image: tagDetail.image_url || tag.image_url || defaultEmptyImg,
                    userPreference: true,
                    description: tagDetail.details?.description || '您的偏好'
                  };
                }).sort((a, b) => b.userScore - a.userScore);
            console.log(`处理后的用户偏好标签数量:`, preferredTags.length);

            // 处理相似用户的偏好
            const similarUserTags = tags.filter(tag => recommendedTagIds.includes(tag.tag_id || tag.id))
                .map(tag => {
                  const tagDetail = tagDetailsMap.get(tag.tag_id || tag.id) || {};

                  console.log(`处理相似用户偏好标签 ${tag.tag_id || tag.id}:`, {
                    tagDetail,
                    image: tagDetail.image_url || defaultEmptyImg
                  });

                  return {
                    ...tag,
                    name: tagDetail.folk_name || tag.tag_name || '未知标签',
                    image: tagDetail.image_url || defaultEmptyImg,
                    userPreference: false,
                    similarityScore: 0, // 你可以在 `similarUsers` 里找到对应的 `similarity_score`
                    description: `来自相似用户的推荐`
                  };
                });
            console.log(`处理后的相似用户偏好标签数量:`, similarUserTags.length);

            // 如果没有用户偏好标签，使用一些标签作为示例
            if (preferredTags.length === 0) {
              console.log(`为主题 ${theme} 创建示例用户偏好标签`);
              const sampleTags = tags.slice(0, Math.min(5, tags.length)).map(tag => ({
                ...tag,
                userScore: 0.7,  // 默认分数
                name: tag.tag_name || tag.name || '未知标签',
                image: tag.image_url || defaultEmptyImg,
                userPreference: true,
                description: '示例偏好'
              }));
              preferredTags.push(...sampleTags);
            }

            // 更新 slides，确保从 tagDetailsMap 获取详细信息
            slides.value[slideIndex].favoriteCards = preferredTags.slice(0, 5).map(tag => {
              const tagDetail = tagDetailsMap.get(tag.tag_id || tag.id) || {}; // 获取 tag 详情
              return {
                title: tagDetail.title || tagDetail.folk_name || tag.name || '未知标签',
                image: tagDetail.details?.image_url || tagDetail.image_url || tag.image || defaultEmptyImg,
                rating: tag.userScore ? (tag.userScore * 10).toFixed(1) : '7.0', // 评分
                userPreference: true
              };
            });
            console.log(`更新 slides[${slideIndex}].favoriteCards:`, slides.value[slideIndex].favoriteCards);

            slides.value[slideIndex].subCards = [...preferredTags, ...similarUserTags].map(tag => {
              const tagDetail = tagDetailsMap.get(tag.tag_id || tag.id) || {}; // 获取 tag 详情
              return {
                ...tag,
                title: tagDetail.title || tagDetail.folk_name || tag.name || '未知标签',
                image: tagDetail.details?.image_url || tagDetail.image_url || tag.image || defaultEmptyImg,
                description: tagDetail.details?.description || tag.description || "暂无描述",
                userPreference: tag.userPreference || false
              };
            });
            console.log(`更新 slides[${slideIndex}].subCards:`, slides.value[slideIndex].subCards);
          }
        }
      }
    }
  } catch (error) {
    console.error("获取数据失败:", error);
    // 创建一些示例数据以确保界面不为空
    for (let i = 0; i < slides.value.length; i++) {
      if (slides.value[i].favoriteCards.length === 0) {
        slides.value[i].favoriteCards = Array(5).fill(0).map((_, idx) => ({
          title: `示例标签 ${idx + 1}`,
          image: defaultEmptyImg,
          rating: '7.0',
          userPreference: true
        }));
      }

      if (slides.value[i].subCards.length === 0) {
        slides.value[i].subCards = Array(8).fill(0).map((_, idx) => ({
          title: `示例标签 ${idx + 1}`,
          image: defaultEmptyImg,
          description: '示例描述',
          userPreference: idx < 5
        }));
      }
    }
  } finally {
    loading.value = false;
    console.log("fetchData 执行完成");
  }
};


// 计算滑动样式
const slideStyle = computed(() => ({
  transform: `translateY(-${currentIndex.value * 100}vh)`
}))

// 处理标签点击
const handleTabClick = (index) => {
  currentIndex.value = index
}

// 处理滚轮事件
const handleWheel = (e) => {
  // 如果弹窗打开，不处理滚轮事件
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
    isMapZoomed.value = true
    selectedRegion.value = region
  }
}

// 处理返回世界地图
const handleBackToWorld = () => {
  isMapZoomed.value = false
  selectedRegion.value = null
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

// 格式化描述文本
const formatDescription = (description) => {
  if (!description) return '暂无描述';
  // 如果描述是URL，则提取有用信息或返回默认文本
  if (description.startsWith('http')) {
    return '点击查看详细介绍';
  }
  return description;
};

// 检查主题是否有偏好
const hasPreferences = (slide) => {
  return slide.favoriteCards.length > 0 || slide.subCards.length > 0;
};

// 导航到相应页面
const navigateToPage = (index) => {
  // 根据索引确定要跳转的路由
  let route = '';
  switch (index) {
    case 0: route = '/placeOfInterest'; break;
    case 1: route = '/food'; break;
    case 2: route = '/filmLiterature'; break;
    case 3: route = '/folkCustom'; break;
    case 4: route = '/red'; break;
    case 5: route = '/discover'; break;
    default: route = '/';
  }

  // 在跳转前清理状态
  selectedCard.value = null;

  // 使用 nextTick 确保状态更新后再跳转
  nextTick(() => {
    // 使用 push 而不是 replace，保留历史记录
    router.push(route);
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

onMounted(async () => {
  // 确保用户数据已加载
  if (!userStore.isLoggedIn) {
    console.log("用户未登录，使用默认用户数据");
  } else {
    console.log("当前登录用户:", userStore.user);
  }

  await fetchData();

  // 初始化轮播
  nextTick(() => {
    initSwiper();
    // 立即设置第一个卡片为选中状态
    if (slides.value[currentIndex.value]?.favoriteCards?.length > 0) {
      selectedCard.value = slides.value[currentIndex.value].favoriteCards[0];
      console.log('初始选中卡片:', selectedCard.value);
    }
  });
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
.empty-slide.slide-5 { background-color: rgba(231, 76, 60, 0.2); }   /* 半透明红色 */
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
  top: 50%;
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
  margin-left: 20px; /* 添加左边距使其与"您的偏好"标签对齐 */
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
    max-height: 200px;
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
  padding-top: 40px;
  padding-left: 20px; /* 添加左边距使内容对齐 */
  max-width: 1300px; /* 限制最大宽度 */
}

.cards-row {
  display: flex;
  flex-direction: column;
  gap: 20px;
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
  padding: 15px 8px;
  background-color: #b71c1c;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
  white-space: nowrap;
  font-size: 1.2em;
  height: 105px; /* 与卡片高度一致 */
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
  height: 105px;
  flex-direction: column;
  align-items: center;
  justify-content: center; /* 添加垂直居中 */
  padding: 15px 10px;
  background-color: #b71c1c; /* 改为红色背景 */
  border-radius: 8px;
  margin-right: 5px;
  flex-shrink: 0;
  width: 30px; /* 固定宽度 */
}

.row-header h3 {
  margin: 0;
  font-size: 1.5em;
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

.user-preferences .sub-card {
  border: 2px solid #b71c1c;
}

.similar-users .sub-card {
  border: 1px solid #ddd;
}

.sub-card {
  flex: 0 0 180px; /* 减小卡片宽度 */
  height: 130px;
  position: relative;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
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
  background: #f5f5f5;
}

.map-controls {
  position: absolute;
  top: 20px;
  left: 20px;
  z-index: 10;
}

.back-button {
  padding: 10px 20px;
  background: #b71c1c;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
}

.back-button:hover {
  background: #7f0c07;
}

.map-wrapper {
  position: relative;
  width: 100%;
  height: 100%;
  transition: all 0.5s ease;
}

.world-map, .china-map {
  width: 100%;
  height: 100%;
  position: relative;
}

.map-region {
  cursor: pointer;
  transition: all 0.3s;
}

.map-region:hover {
  filter: brightness(1.1);
}

.region-tooltip {
  position: absolute;
  background: rgba(0, 0, 0, 0.8);
  color: white;
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 16px;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
  font-family: 'HelveticaNeue', serif;
}

.map-region:hover .region-tooltip {
  opacity: 1;
}

.province-region {
  cursor: pointer;
  transition: all 0.3s;
}

.province-region:hover {
  filter: brightness(1.1);
}

.zoomed {
  transform: scale(1.5);
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
  background: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-spinner {
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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
  display: block; /* 确保图片正确显示 */
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
    max-height: 70vh; /* 限制最大高度 */
    overflow-y: auto; /* 允许内容滚动 */
    overscroll-behavior: contain; /* 防止滚动传播 */
  }

  /* 自定义滚动条样式 */
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

/* 导航按钮样式 */
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

/* 增强卡片点击区域 */
.swiper-slide {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;

  &:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
  }
}

/* 空内容样式 */
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

/* 导航按钮样式 */
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
    z-index: 10;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }
}

/* 添加全局字体样式 */
.fullpage-container {
  font-family: 'HelveticaNeue', serif;
}

/* 确保所有文本元素都使用相同字体 */
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
</style>

