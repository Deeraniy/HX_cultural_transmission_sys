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

      <!-- 滑动容器 -->
      <div class="slides-container" :style="slideStyle">
        <div v-for="(slide, index) in slides"
             :key="index"
             class="slide"
             :class="{ active: currentIndex === index }">
          <div class="slide-content">
            <!-- 第一行：改为卡片轮播 + 描述 -->
            <div class="main-content">
              <!-- 卡片轮播部分 -->
              <div class="swiper">
                <div class="swiper-wrapper">
                  <div v-for="(card, cardIndex) in slide.favoriteCards"
                       :key="cardIndex"
                       class="swiper-slide"
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
                <h2>{{ slide.title }}</h2>
                <p>{{ slide.description }}</p>
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
                    <div v-for="(card, cardIndex) in userPreferenceCards.slice(0, 4)"
                         :key="'pref-' + cardIndex"
                         class="sub-card">
                      <img :src="card.image_url" :alt="card.folk_name || card.tag_name">
                      <div class="card-info">
                        <p class="title">{{ card.folk_name || card.tag_name }}</p>
                      </div>
                    </div>
                  </div>
                  <div v-if="userPreferenceCards.length > 4"
                       class="more-button"
                       @click="showMorePreferences">
                    更多 ({{ userPreferenceCards.length - 4 }})
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
                    <div v-for="(card, cardIndex) in similarUserCards.slice(0, 4)"
                         :key="'similar-' + cardIndex"
                         class="sub-card">
                      <img :src="card.image_url" :alt="card.folk_name || card.tag_name">
                      <div class="card-info">
                        <p class="title">{{ card.folk_name || card.tag_name }}</p>
                      </div>
                    </div>
                  </div>
                  <div v-if="similarUserCards.length > 4"
                       class="more-button"
                       @click="showMoreSimilarPreferences">
                    更多 ({{ similarUserCards.length - 4 }})
                  </div>
                </div>
              </div>
            </div>
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
          <img :src="card.image" :alt="card.title">
          <div class="card-info">
            <p class="title">{{ card.title }}</p>
            <p class="description">{{ card.description }}</p>
            <p v-if="!card.userPreference" class="similarity">
              相似度: {{ (card.similarityScore * 100).toFixed(0) }}%
            </p>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from 'vue'
import Swiper from 'swiper'
import { EffectCards } from 'swiper/modules'
import RecommendAPI from "@/api/user"
import TagsAPI from "@/api/tags"
import 'swiper/css'
import 'swiper/css/effect-cards'

// 导入默认图片以备用
import defaultEmptyImg from '@/assets/BookB.jpg'

const currentIndex = ref(0)
const isAnimating = ref(false)
const loading = ref(true)

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
};

// 显示更多相似用户推荐
const showMoreSimilarPreferences = () => {
  dialogTitle.value = '相似用户推荐';
  currentDialogCards.value = similarUserCards.value;
  showAllPreferencesDialog.value = true;
};

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
    const userId = 1;
    const preferenceResponse = await RecommendAPI.getPerferenceAPI(userId);
    const tagsResponse = await TagsAPI.getAllTagsAPI();

    console.log('所有标签数据:', tagsResponse.data);
    console.log('用户偏好数据:', preferenceResponse.data);

    if (preferenceResponse?.data && tagsResponse?.data) {
      const userPreferences = preferenceResponse.data;
      const tagData = tagsResponse.data;

      Object.entries(tagData).forEach(([theme, tags]) => {
        console.log(`\n处理主题: ${theme}`);

        let slideIndex = -1;
        switch(theme.toLowerCase()) {
          case 'spot': slideIndex = 0; break;
          case 'food': slideIndex = 1; break;
          case 'literature': slideIndex = 2; break;
          case 'folk': slideIndex = 3; break;
          case 'history': slideIndex = 4; break;
        }

        if (slideIndex !== -1) {
          const themePreferences = userPreferences.detailed_preferences[theme.toLowerCase()] || [];
          const similarUsers = userPreferences.similar_users || [];

          // 处理用户偏好
          const preferredTags = tags.filter(tag =>
            themePreferences.some(p => p.tag_id === tag.tag_id)
          ).map(tag => {
            const preference = themePreferences.find(p => p.tag_id === tag.tag_id);
            return {
              ...tag,
              userScore: preference.score,
              name: tag.folk_name || tag.tag_name,
              image: tag.image_url,
              userPreference: true,
              description: '您的偏好'
            }
          }).sort((a, b) => b.userScore - a.userScore);

          // 处理相似用户的偏好
          const similarUserTags = [];
          similarUsers.forEach(simUser => {
            const userPrefs = simUser.preferences || {};
            Object.entries(userPrefs).forEach(([tagId, prefData]) => {
              if (prefData.theme_name.toLowerCase() === theme.toLowerCase()) {
                const tag = tags.find(t => t.tag_id === parseInt(tagId));
                if (tag) {
                  similarUserTags.push({
                    ...tag,
                    name: tag.folk_name || tag.tag_name,
                    image: tag.image_url,
                    userPreference: false,
                    similarityScore: simUser.similarity_score,
                    description: `来自相似用户的推荐`
                  });
                }
              }
            });
          });

          // 更新 slides
          if (preferredTags.length > 0) {
            slides.value[slideIndex].favoriteCards = preferredTags.slice(0, 5).map(tag => ({
              title: tag.name,
              image: tag.image,
              rating: (tag.userScore * 10).toFixed(1),
              userPreference: true
            }));
          } else {
            slides.value[slideIndex].favoriteCards = [{
              title: '暂无推荐',
              image: defaultEmptyImg,
              rating: '-',
              userPreference: false
            }];
          }

          // 合并用户偏好和相似用户推荐
          slides.value[slideIndex].subCards = [
            ...preferredTags,
            ...similarUserTags
          ];
        }
      });
    }
  } catch (error) {
    console.error('获取数据失败:', error);
  } finally {
    loading.value = false;
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
  if (isAnimating.value) return

  isAnimating.value = true
  setTimeout(() => {
    isAnimating.value = false
  }, 1000)

  if (e.deltaY > 0 && currentIndex.value < slides.value.length - 1) {
    currentIndex.value++
  } else if (e.deltaY < 0 && currentIndex.value > 0) {
    currentIndex.value--
  }
}

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
  const swipers = document.querySelectorAll('.swiper')
  swipers.forEach(swiperEl => {
    new Swiper(swiperEl, {
      effect: 'cards',
      grabCursor: true,
      initialSlide: 0,
      speed: 800,
      loop: true,
      modules: [EffectCards],
      on: {
        click: function() {
          this.slideNext()
        }
      }
    })
  })
}

onMounted(() => {
  fetchData().then(() => {
    nextTick(() => {
      initSwiper()
    })
  })
})
</script>

<style scoped>
.fullpage-container {
  height: 100vh;
  overflow: hidden;
  position: relative;
}

.slides-container {
  height: 100%;
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
}

/* 可以为每个页面添加不同的背景色 */
.slide:nth-child(1) { background-color: #f1c40f; }
.slide:nth-child(2) { background-color: #e74c3c; }
.slide:nth-child(3) { background-color: #3498db; }

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
}

.tab-item.active {
  color: #3498db;
  font-weight: bold;
}

.main-content {
  display: flex;
  gap: 30px;
  align-items: center;
  padding: 0 5%;
}

.main-description {
  flex: 1;
}

.sub-content {
  width: 90%;
  margin: 0 auto;
  padding-top: 40px;
}

.cards-row {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.row {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 30px;
}

.user-preferences .sub-card {
  border: 2px solid #3498db;
}

.similar-users .sub-card {
  border: 1px solid #ddd;
}

.sub-card {
  flex: 0 0 200px;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
  border: 2px solid #3498db;
  height: 130px;
}

.sub-card img {
  width: 100%;
  height: 120px;
  object-fit: cover;
}

.more-button {
  position: absolute;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  font-size: 0.85em;
  padding: 4px 8px;
  background-color: #3498db;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  white-space: nowrap;
}

.more-button:hover {
  background-color: #2980b9;
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
  background: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background 0.3s;
}

.back-button:hover {
  background: #2980b9;
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
  font-size: 12px;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.3s;
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
  height: 350px;
  margin-top: 30px;
}

.swiper-slide {
  position: relative;
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  user-select: none;
  cursor: pointer;
  transition: transform 0.3s ease;
  background: #fff; /* 添加背景色以便于查看图片加载状态 */
}

.swiper-slide:hover {
  transform: scale(1.02);
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
}

.overlay h2 {
  position: absolute;
  bottom: 0;
  left: 0;
  color: #fff;
  font-weight: 400;
  font-size: 1.1rem;
  line-height: 1.4;
  margin: 0 0 20px 20px;
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
    gap: 20px;
    padding: 20px;
  }

  .preference-card {
    border: 1px solid #ddd;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.3s;

    &:hover {
      transform: translateY(-5px);
    }

    img {
      width: 100%;
      height: 150px;
      object-fit: cover;
    }

    .card-info {
      padding: 8px;
    }
  }
}

.row-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 15px 10px;
  background-color: #f8f9fa;
  border-radius: 8px;
  margin-right: 20px;
}

.row-header h3 {
  margin: 0;
  font-size: 1.2em;
  color: #333;
  display: flex;
  flex-direction: column;
  line-height: 2;
}

.row-header h3 span {
  display: block;
  text-align: center;
  writing-mode: vertical-lr;
  letter-spacing: 2px;
}

.cards-container {
  display: flex;
  gap: 15px;
  position: relative;
  padding-right: 80px;
}

.card-info {
  padding: 8px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card-info .title {
  margin: 0;
  font-size: 0.95em;
  font-weight: 500;
  color: #333;
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  width: 100%;
}

.user-preferences .sub-card,
.similar-users .sub-card {
  border: 2px solid #3498db;
}

.more-button {
  padding: 4px 12px;
  background-color: #3498db;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  white-space: nowrap;
  font-size: 0.85em;
  height: fit-content;
  align-self: center; /* 确保按钮垂直居中 */
}
</style>

