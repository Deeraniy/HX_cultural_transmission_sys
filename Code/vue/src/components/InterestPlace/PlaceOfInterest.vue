<template>
  <el-main>
    <div class="hunan-tourist-attractions">
      <div class="map-info-container">
        <!-- 气泡动画区域 -->
        <div class="map-box">
          <div class="bubble-container"
               :data-city-name="selectedCity ? getCityDisplayName(selectedCity) : ''"
               @mousemove="handleMouseMove"
               @mouseup="handleMouseUp"
               @mouseleave="handleMouseUp">
            <div v-for="city in cityList" 
                 :key="city"
                 class="city-bubble"
                 :class="{ 
                   'selected': selectedCity === city,
                   'dragging': draggedBubble === city
                 }"
                 :style="{
                   width: bubbleStates[city]?.size + 'px',
                   height: bubbleStates[city]?.size + 'px',
                   left: bubbleStates[city]?.x + 'px',
                   top: bubbleStates[city]?.y + 'px',
                   transform: draggedBubble === city ? 'scale(1.2)' : 'scale(1)'
                 }"
                 @mousedown="handleMouseDown(city, $event)"
                 @click="onCitySelect(city)">
              <span class="bubble-text">{{ getCityDisplayName(city) }}</span>
            </div>
          </div>
        </div>

        <!-- 地理位置名称显示框 -->
        <div class="location-box">
          <!-- 城市选择下拉框 -->
          <el-select v-model="selectedCity" :placeholder="t('detail.selectTheme')" @change="onCitySelect" class="city-select">
            <el-option
                v-for="city in cityList"
                :key="city"
                :label="getCityDisplayName(city)"
                :value="city">
            </el-option>
          </el-select>
          <div>
            <h3 class="location-title">{{ t('detail.tabs.basic') }}</h3>
            <div v-if="selectedCityInfoLocal" class="city-info">
              <div class="image-container">
                <img :src="selectedCityInfoLocal.image" :alt="getCityDisplayName(selectedCity)" class="city-image" />
                <img :src="getImageUrl(selectedCityInfoLocal.wordCloudImage)" :alt="getCityDisplayName(selectedCity)" class="wordcloud-image" />
              </div>
              <div class="description-box">
                <p>{{ getCityDescription(selectedCity) }}</p>
              </div>
            </div>
            <div v-else class="city-name-display" style="display: flex; justify-content: center; align-items: center; height: 100%;">
              <el-text style="color: darkgray;">{{ t('detail.defaultTitle') }}</el-text>
            </div>
          </div>
        </div>
      </div>
      <div class="attraction-card-box">
        <!-- 动态展示当前选中的城市景点 -->
        <div class="attractions-container">
          <div class="attraction-card" @click="showDetail(attraction)" v-for="attraction in filteredAttractions" :key="attraction.name">
            <img :src="attraction.image" :alt="getAttractionDisplayName(attraction.name)" class="attraction-image" />
            <div class="attraction-details">
              <h3>
                {{ getAttractionDisplayName(attraction.name) }}
                <span class="fancy-name">({{ attraction.name }})</span>
              </h3>
              <p>{{ getAttractionDescription(attraction.name) }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 搜索功能 -->
      <div class="search-container">
        <input v-model="searchQuery" type="text"  />
        <button @click="searchAttractions">{{ $t('sou-suo') }}</button>
      </div>
    </div>

    <!-- 详情弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      width="80%"
      class="detail-dialog"
      :show-close="false"
      :modal-class="'custom-modal'"
    >
      <!-- 添加右上角关闭按钮 -->
      <div class="dialog-close-button" @click="dialogVisible = false">
        <el-icon class="close-icon"><Close /></el-icon>
      </div>

      <div class="dialog-content">
        <!-- 左侧固定图片区域 -->
        <div class="left-section">
          <div class="image-wrapper">
            <img :src="selectedPlace?.image" class="detail-image">
          </div>
        </div>

        <!-- 右侧可滚动内容区域 -->
        <div class="right-section">
          <!-- 固定顶栏 -->
          <div class="right-header">
            <div class="title-wrapper">
              <h2>{{ getAttractionDisplayName(selectedPlace?.name) }}</h2>
            </div>
          </div>

          <!-- 可滚动的内容区域 -->
          <div class="right-content">
            <div class="info-content">
              <div class="info-item">
                <div class="info-title">
                  <h3>{{ t('detail.place.location') }}</h3>
                </div>
                <p>{{ selectedPlace?.location }}</p>
              </div>
              <div class="info-item">
                <h3>{{ t('detail.place.history') }}</h3>
                <p>{{ selectedPlace?.history }}</p>
              </div>
              <div class="info-item">
                <h3>{{ t('detail.place.culture') }}</h3>
                <p>{{ selectedPlace?.culture }}</p>
              </div>
              <div class="info-item">
                <h3>{{ t('detail.place.description') }}</h3>
                <p>{{ getAttractionDescription(selectedPlace?.name) }}</p>
              </div>
            </div>
          </div>

          <!-- 固定底栏 -->
          <div class="right-footer">
            <el-button
              type="primary"
              class="analysis-btn"
              @click="goToAnalysis(selectedPlace)"
            >
              {{ t('detail.place.sentimentAnalysis') }}
            </el-button>
            <div class="dialog-interaction-icons">
              <div class="icon-wrapper" @click="toggleLike(selectedPlace)">
                <img
                  :src="tagStatus.is_liked ? likeActiveIcon : likeIcon"
                  :class="['icon', { 'active': tagStatus.is_liked }]"
                  :alt="t('detail.place.like')"
                />
                <span>{{ tagStatus.total_likes || 0 }}</span>
              </div>
              <div class="icon-wrapper" @click="toggleFavorite(selectedPlace)">
                <img
                  :src="tagStatus.is_favorite ? favoriteActiveIcon : favoriteIcon"
                  :class="['icon', { 'active': tagStatus.is_favorite }]"
                  :alt="t('detail.place.favorite')"
                />
                <span>{{ t('detail.place.favorite') }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </el-dialog>

  </el-main>
</template>

<script lang="ts" setup>
import {computed, onMounted, ref, watch} from 'vue';
import cityInfoDataLocal from '@/assets/cityInfo.json';
import cultureElements from '@/json/culture_elements_translated.json';
import SpotsAPI  from "@/api/spot";
import CityAPI from "@/api/city";
import CloudAPI from "@/api/cloud";
import SentimentAPI from "@/api/sentiment";
import {error} from "echarts/types/src/util/log";
import Sentiment from "@/api/sentiment";
import { useRouter } from 'vue-router'
import TagsAPI from '@/api/tags';
import { useUserStore } from '@/stores/user';
import { Close } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import UserAPI from "@/api/user";
import {hColgroup} from "element-plus/es/components/table/src/h-helper";
import props = hColgroup.props;
import { useI18n } from 'vue-i18n';

// 使用import导入图标
import likeIcon from '@/assets/setting/赞.png';
import likeActiveIcon from '@/assets/setting/赞 (1).png';
import favoriteIcon from '@/assets/setting/收藏.png';
import favoriteActiveIcon from '@/assets/setting/收藏(1).png';

const router = useRouter()
const searchQuery = ref<string>('');
const selectedCity = ref('');
const selectedCityInfo = ref(null);
const selectedCityInfoLocal = ref(null);
const selectedCityWordCloudImage = ref(null);
const cityList = ref([
  '长沙市', '株洲市', '湘潭市', '衡阳市', '邵阳市', '岳阳市', '常德市',
  '张家界市', '益阳市', '郴州市', '永州市', '怀化市', '娄底市', '湘西土家族苗族自治州'
]);
const interestData = ref(null);
const cityInfoData = ref(null);

const attractions = ref([]); // 保存当前选中的城市的所有景点

const dialogVisible = ref(false)
const selectedPlace = ref<Place | null>(null)

interface Place {
  id: number;
  name: string;
  image: string;
  description: string;
  location: string;
  history: string;
  culture: string;
}

// 添加新的接口和状态
interface TagStatus {
  is_liked: boolean;
  is_favorite: boolean;
  total_likes: number;
  click_count: number;
}

const tagStatus = ref<TagStatus>({
  is_liked: false,
  is_favorite: false,
  total_likes: 0,
  click_count: 0
});

// 获取用户存储
const userStore = useUserStore();

// 修改 getUserId 函数，参考 UserHomeMain.vue 的实现
const getUserId = () => {
  // 首先从 userStore 中获取
  if (userStore.userId) {
    return userStore.userId;
  }

  // 如果 userStore 中没有，尝试从 localStorage 获取
  const userId = localStorage.getItem('userId');
  if (userId) {
    return userId;
  }

  // 如果都没有，返回 null 并提示用户登录
  ElMessage.warning('请先登录以使用此功能');
  return null;
};

// 从 interest.json 中加载数据并更新 attractions
const loadAttractions = (cityName: string) => {

  // 确保 cityInfoData 和 interestData 已加载且是数组
  if (!cityInfoData.value || !Array.isArray(cityInfoData.value)) {
    console.warn("城市数据未加载或格式错误");
    return;
  }
  if (!interestData.value || !Array.isArray(interestData.value)) {
    console.warn("景点数据未加载或格式错误");
    return;
  }

  console.log(cityInfoData.value);
  console.log("当前城市的名称:", cityName);

  // 找到当前城市的 city_id
  const city = cityInfoData.value.find((c: any) => c.city_name === cityName);
  console.log("当前城市的城市ID:", city);

  if (city) {
    const cityId = city.city_id;

    // 根据 city_id 筛选景点数据
    attractions.value = interestData.value
        .filter((spot: any) => spot.city_id === cityId)
        .map((spot: any) => ({
          id: spot.spot_id,
          name: spot.spot_name,
          image: spot.image_url,
          description: spot.description,
          location: spot.location || '',
          history: spot.history || '',
          culture: spot.culture || ''
        }));
    console.log("筛选后的景点:", attractions.value);
  } else {
    console.warn("未找到匹配的城市");
    attractions.value = [];
  }
};

// 修改词云图初始化和更新逻辑
const initWordCloud = () => {
  // 确保容器存在
  const wordCloudContainer = document.getElementById('wordCloudChart');
  if (!wordCloudContainer) {
    console.error('词云图容器不存在');
    return;
  }

  // 初始化echarts实例
  const chart = echarts.init(wordCloudContainer);

  // 基础配置
  const option = {
    tooltip: {},
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      left: 'center',
      top: 'center',
      width: '100%',
      height: '100%',
      right: null,
      bottom: null,
      sizeRange: [12, 60],
      rotationRange: [-90, 90],
      rotationStep: 45,
      gridSize: 8,
      drawOutOfBound: false,
      textStyle: {
        fontFamily: 'sans-serif',
        fontWeight: 'bold',
        color: function () {
          return 'rgb(' + [
            Math.round(Math.random() * 160),
            Math.round(Math.random() * 160),
            Math.round(Math.random() * 160)
          ].join(',') + ')';
        }
      },
      emphasis: {
        textStyle: {
          shadowBlur: 10,
          shadowColor: '#333'
        }
      },
      data: []
    }]
  };

  // 设置配置项
  chart.setOption(option);

  // 保存实例以便后续更新
  wordCloudChart.value = chart;

  // 监听窗口大小变化
  window.addEventListener('resize', () => {
    chart.resize();
  });
};

// 更新词云数据
const updateWordCloud = (tags) => {
  if (!wordCloudChart.value) {
    console.error('词云图实例不存在');
    return;
  }

  // 转换标签数据为词云所需格式
  const data = tags.map(tag => ({
    name: tag.name,
    value: tag.weight || Math.random() * 100, // 如果没有权重则随机生成
    textStyle: {
      color: `rgb(${Math.random() * 160}, ${Math.random() * 160}, ${Math.random() * 160})`
    }
  }));

  // 更新配置
  wordCloudChart.value.setOption({
    series: [{
      data: data
    }]
  });
};

// 添加 tags 的定义
const tags = ref([]);
const wordCloudChart = ref(null);

// 添加获取标签数据的函数
const fetchTags = async (placeId) => {
  try {
    // 调用后端 API 获取标签数据
    const response = await CloudAPI.getWordCloudAPI(placeId);
    if (response && response.code === 200) {
      tags.value = response.data.map(tag => ({
        name: tag.word,
        weight: tag.weight
      }));
      console.log('获取到的标签数据:', tags.value);
    }
  } catch (error) {
    console.error('获取标签数据失败:', error);
  }
};

// 在选择景点时获取标签数据
const showPlaceDetails = async (place) => {
  selectedPlace.value = place;
  dialogVisible.value = true;

  // 获取该景点的标签数据
  await fetchTags(place.id);
};

// 添加气泡位置和速度状态
const bubbleStates = ref({});
const draggedBubble = ref(null);
const isDragging = ref(false);

// 初始化气泡状态
const initBubbleStates = () => {
  cityList.value.forEach(city => {
    bubbleStates.value[city] = {
      x: Math.random() * 400, // 初始x位置
      y: Math.random() * 500, // 初始y位置
      vx: (Math.random() - 0.5) * 2, // x方向速度
      vy: (Math.random() - 0.5) * 2, // y方向速度
      size: 60 + Math.random() * 40, // 随机大小
      mass: 1 // 质量，用于碰撞计算
    };
  });
};

// 计算两个气泡之间的距离
const getDistance = (bubble1, bubble2) => {
  const dx = bubble1.x - bubble2.x;
  const dy = bubble1.y - bubble2.y;
  return Math.sqrt(dx * dx + dy * dy);
};

// 处理气泡碰撞
const handleCollision = (bubble1, bubble2) => {
  const distance = getDistance(bubble1, bubble2);
  const minDistance = (bubble1.size + bubble2.size) / 2;
  
  if (distance < minDistance) {
    // 计算碰撞后的速度
    const dx = bubble2.x - bubble1.x;
    const dy = bubble2.y - bubble1.y;
    const angle = Math.atan2(dy, dx);
    
    // 计算碰撞后的速度
    const speed1 = Math.sqrt(bubble1.vx * bubble1.vx + bubble1.vy * bubble1.vy);
    const speed2 = Math.sqrt(bubble2.vx * bubble2.vx + bubble2.vy * bubble2.vy);
    
    // 更新速度
    bubble1.vx = -speed1 * Math.cos(angle);
    bubble1.vy = -speed1 * Math.sin(angle);
    bubble2.vx = speed2 * Math.cos(angle);
    bubble2.vy = speed2 * Math.sin(angle);
    
    // 防止重叠
    const overlap = minDistance - distance;
    const moveX = (overlap * Math.cos(angle)) / 2;
    const moveY = (overlap * Math.sin(angle)) / 2;
    
    bubble1.x -= moveX;
    bubble1.y -= moveY;
    bubble2.x += moveX;
    bubble2.y += moveY;
  }
};

// 更新气泡位置
const updateBubblePositions = () => {
  cityList.value.forEach(city => {
    const state = bubbleStates.value[city];
    
    // 如果是正在拖动的气泡，跳过位置更新
    if (isDragging.value && city === draggedBubble.value) {
      return;
    }
    
    // 更新位置
    state.x += state.vx;
    state.y += state.vy;
    
    // 边界检测和反弹
    if (state.x <= 0 || state.x >= 400) {
      state.vx *= -1;
      state.x = Math.max(0, Math.min(400, state.x));
    }
    if (state.y <= 0 || state.y >= 500) {
      state.vy *= -1;
      state.y = Math.max(0, Math.min(500, state.y));
    }
    
    // 检查与其他气泡的碰撞
    cityList.value.forEach(otherCity => {
      if (city !== otherCity) {
        // 如果两个气泡中有一个正在被拖动，跳过碰撞检测
        if (isDragging.value && (city === draggedBubble.value || otherCity === draggedBubble.value)) {
          return;
        }
        handleCollision(state, bubbleStates.value[otherCity]);
      }
    });
  });
};

// 鼠标事件处理
const handleMouseDown = (city, event) => {
  isDragging.value = true;
  draggedBubble.value = city;
  const state = bubbleStates.value[city];
  state.vx = 0;
  state.vy = 0;
};

const handleMouseMove = (event) => {
  if (!isDragging.value || !draggedBubble.value) return;
  
  const state = bubbleStates.value[draggedBubble.value];
  const container = event.currentTarget;
  const rect = container.getBoundingClientRect();
  
  state.x = Math.max(0, Math.min(400, event.clientX - rect.left - state.size / 2));
  state.y = Math.max(0, Math.min(500, event.clientY - rect.top - state.size / 2));
};

const handleMouseUp = () => {
  if (!isDragging.value || !draggedBubble.value) return;
  
  const state = bubbleStates.value[draggedBubble.value];
  // 给被拖动的气泡一个初始速度
  state.vx = (Math.random() - 0.5) * 4;
  state.vy = (Math.random() - 0.5) * 4;
  
  isDragging.value = false;
  draggedBubble.value = null;
};

// 启动动画
onMounted(() => {
  initBubbleStates();
  setInterval(updateBubblePositions, 50);
});

onMounted(async () => {
  try {
    const spotsResponse = await SpotsAPI.getSpotsAPI();

    if (typeof spotsResponse === "string") {
      const jsonObjects = spotsResponse.match(/{[^}]+}/g) || [];
      
      const parsedSpots = jsonObjects.map(jsonStr => {
        try {
          const cleanJson = jsonStr
            .replace(/Decimal\('([\d.]+)'\)/g, '$1')
            .replace(/'/g, '"')
            .replace(/([{,]\s*)([a-zA-Z_][a-zA-Z0-9_]*)\s*:/g, '$1"$2":');
          
          return JSON.parse(cleanJson);
        } catch (parseError) {
          console.error('解析单个景点数据失败:', jsonStr);
          console.error('错误详情:', parseError);
          return null;
        }
      }).filter(spot => spot !== null);

      interestData.value = parsedSpots;
      console.log("解析后的景点数据:", interestData.value);
    } else {
      console.error("景点数据格式错误，期望为字符串形式");
    }
  } catch (error) {
    console.error("加载景点数据时出错:", error);
  }

  try {
    const cityResponse = await CityAPI.getCityAPI();

    if (typeof cityResponse === "string") {
      const fixedString = cityResponse.replace(/'/g, '"');
      const cityArray = fixedString
          .match(/{[^}]+}/g)
          .map((city) => JSON.parse(city));

      cityInfoData.value = cityArray;
      console.log("城市数据（处理后）:", cityInfoData.value);
    } else {
      console.error("城市数据格式错误，期望为字符串形式");
    }
  } catch (error) {
    console.error("加载城市数据时出错:", error);
  }
});

// 当从下拉框选择城市时的处理函数
const onCitySelect = (city) => {
  selectedCity.value = city;
  updateCityInfo();
  loadAttractions(city);
};
//const attractionName=ref('')//保存当前点击的景点的名字，并进行跳转，将景点名传给详情页
const addHistory = async (attraction: Place) => {
  try {
    const userId = getUserId();
    if (!userId) {
      ElMessage.warning('请先登录以记录浏览历史');
      return;
    }
    const historyData = {
      uid: Number(userId), // 确保是数字类型
      type: "placeOfInterest", // 记录类型
      name: attraction.name, // 景点名称
      img_url: attraction.image, // 景点图片
      describe: attraction.description.substring(0, 50) || "景点描述", // 景点描述
    };

    const response = await UserAPI.AddUserHistory(historyData);
    console.log("response ",response);
    if (response  === "添加成功") {
      console.log('浏览记录添加成功:', response);
    } else {
      console.error('浏览记录添加失败:', response);
    }
  } catch (error) {
    console.error('添加浏览记录失败:', error);
  }
};
const showDetail = async (attraction) => {
  selectedPlace.value = attraction;
  dialogVisible.value = true;

  try {
    // 获取标签ID
    const response = await TagsAPI.getTagByThemeAndOriginAPI('spot', attraction.id);
    if (response.code === 200) {
      const tagId = response.data.id;
      console.log(`获取到的标签ID: ${tagId}`);

      // 获取用户ID
      const userId = getUserId();
      addHistory(attraction);
      if (userId) {
        // 记录浏览
        await TagsAPI.viewTagAPI(userId, tagId);

        console.log(`记录浏览: 用户ID=${userId}, 标签ID=${tagId}`);

        // 获取标签状态
        const statusResponse = await TagsAPI.getTagStatusAPI(userId, tagId);
        if (statusResponse.code === 200) {
          tagStatus.value = statusResponse.data;
          console.log('标签状态:', tagStatus.value);
        }
      } else {
        // 未登录用户设置默认状态
        tagStatus.value = {
          is_liked: false,
          is_favorite: false,
          total_likes: 0,
          click_count: 0
        };
        console.log('用户未登录，使用默认标签状态');
      }
    } else {
      console.error('获取标签ID失败:', response.message);
    }
  } catch (error) {
    console.error('获取标签状态失败:', error);
  }
};

// 更新城市信息
const updateCityInfo = () => {
  console.log('Selected City:', selectedCity.value);
  selectedCityInfo.value = cityInfoData[selectedCity.value] || null;
  selectedCityInfoLocal.value = cityInfoDataLocal[selectedCity.value];
  console.log(selectedCityInfo);
};

const getImageUrl = (imagePath) => {
  try {
    if (imagePath.startsWith('http')) {
      return imagePath;
    }

    if (imagePath.includes('setting/')) {
      return new URL(`../../assets/${imagePath}`, import.meta.url).href;
    }

    const cleanPath = imagePath.replace('@/assets/', '');
    console.log('清理后的路径:', cleanPath);

    return new URL(`../../assets/${cleanPath}`, import.meta.url).href;
  } catch (e) {
    console.error('图片加载失败', e);
    return '';
  }
};
// 判断是否为 URL 的函数
const isUrl = (text: string): boolean => {
  const urlPattern = new RegExp('^(https?:\\/\\/)?'+ // protocol
      '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.?)+[a-z]{2,}|'+ // domain name
      '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
      '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
      '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
      '(\\#[-a-z\\d_]*)?$','i'); // fragment locator
  return !!urlPattern.test(text);
};

// 计算属性用于动态更新过滤后的景点
const filteredAttractions = computed(() => {
  if (!searchQuery.value) return attractions.value;

  return attractions.value.filter(attraction =>
      attraction.name.includes(searchQuery.value) ||
      (attraction.description && attraction.description.includes(searchQuery.value))
  );
});

const searchAttractions = () => {
  console.log("搜索结果：", filteredAttractions.value);
  // 您可以在这里添加额外的逻辑，比如记录搜索日志等
};

const goToAnalysis = (place: Place) => {
  if (!place) return;
  router.push({
    path: '/detail',
    query: {
      name: place.name,
      value: '1',  // 这个值代表什么？
      theme: '1'   // 这个值代表景点类型
    }
  })
}

// 修改 getTagStatus 函数，使用新的 getUserId 函数
const getTagStatus = async (attraction) => {
  try {
    // 获取用户ID
    const userId = getUserId();
    if (!userId) {
      console.log('用户未登录，无法获取标签状态');
      return;
    }

    // 获取标签ID
    const response = await TagsAPI.getTagByThemeAndOriginAPI('spot', attraction.id);
    if (response && typeof response === 'object' && 'code' in response && response.code === 200) {
      const tagId = response.data.id;
      console.log(`获取到的标签ID: ${tagId}`);

      // 记录浏览
      await TagsAPI.viewTagAPI(Number(userId), tagId);
      console.log(`记录浏览: 用户ID=${userId}, 标签ID=${tagId}`);

      // 获取标签状态
      const statusResponse = await TagsAPI.getTagStatusAPI(Number(userId), tagId);
      if (statusResponse && typeof statusResponse === 'object' && 'code' in statusResponse && statusResponse.code === 200) {
        tagStatus.value = statusResponse.data;
        console.log('标签状态:', tagStatus.value);
      }
    } else {
      console.error('获取标签ID失败:', response);
    }
  } catch (error) {
    console.error('获取标签状态失败:', error);
  }
};

// 修改 toggleLike 函数，使用新的 getUserId 函数
const toggleLike = async (place) => {
  try {
    // 获取用户ID
    const userId = getUserId();
    if (!userId) {
      ElMessage.warning('请先登录后再点赞');
      return;
    }

    // 获取标签ID
    const response = await TagsAPI.getTagByThemeAndOriginAPI('spot', place.id);
    if (response && typeof response === 'object' && 'code' in response && response.code === 200) {
      const tagId = response.data.id;
      console.log(`获取到的标签ID: ${tagId}`);

      console.log(`用户ID: ${userId}, 标签ID: ${tagId}`);

      const likeResponse = await TagsAPI.toggleLikeAPI(Number(userId), tagId);
      console.log('点赞响应:', likeResponse);

      if (likeResponse && typeof likeResponse === 'object' && 'code' in likeResponse && likeResponse.code === 200) {
        // 更新点赞状态
        console.log('点赞前状态:', { ...tagStatus.value });
        // 确保深拷贝对象，避免引用问题
        tagStatus.value = {
          ...tagStatus.value,
          is_liked: likeResponse.data.is_liked,
          total_likes: typeof likeResponse.data.total_likes === 'number' ? likeResponse.data.total_likes : 0
        };
        console.log('点赞后状态:', { ...tagStatus.value });
        console.log('响应中的点赞数:', likeResponse.data.total_likes);
      }
    }
  } catch (error) {
    console.error('点赞操作失败:', error);
    ElMessage.error('点赞失败，请稍后重试');
  }
};

// 修改 toggleFavorite 函数，使用新的 getUserId 函数
const toggleFavorite = async (place) => {
  try {
    // 获取用户ID
    const userId = getUserId();
    if (!userId) {
      ElMessage.warning('请先登录后再收藏');
      return;
    }

    // 获取标签ID
    const response = await TagsAPI.getTagByThemeAndOriginAPI('spot', place.id);
    if (response && typeof response === 'object' && 'code' in response && response.code === 200) {
      const tagId = response.data.id;

      const favoriteResponse = await TagsAPI.toggleFavoriteAPI(Number(userId), tagId);
      if (favoriteResponse && typeof favoriteResponse === 'object' && 'code' in favoriteResponse && favoriteResponse.code === 200) {
        // 更新收藏状态
        tagStatus.value.is_favorite = favoriteResponse.data.is_favorite;
        ElMessage.success(favoriteResponse.data.is_favorite ? '收藏成功' : '已取消收藏');
      }
    }
  } catch (error) {
    console.error('收藏操作失败:', error);
    ElMessage.error('收藏失败，请稍后重试');
  }
};

// 监听标签数据变化
watch(tags, (newTags) => {
  if (newTags && newTags.length > 0) {
    updateWordCloud(newTags);
  }
}, { deep: true });

const { t, locale } = useI18n();

// 获取城市显示名称
const getCityDisplayName = (city) => {
  // 直接返回城市名称，如果是英文模式则返回英文名称
  if (locale.value === 'en') {
    // 这里可以添加城市名称的英文翻译映射
    const cityTranslations = {
      '长沙市': 'Changsha',
      '株洲市': 'Zhuzhou',
      '湘潭市': 'Xiangtan',
      '衡阳市': 'Hengyang',
      '邵阳市': 'Shaoyang',
      '岳阳市': 'Yueyang',
      '常德市': 'Changde',
      '张家界市': 'Zhangjiajie',
      '益阳市': 'Yiyang',
      '郴州市': 'Chenzhou',
      '永州市': 'Yongzhou',
      '怀化市': 'Huaihua',
      '娄底市': 'Loudi',
      '湘西土家族苗族自治州': 'Xiangxi Tujia and Miao Autonomous Prefecture'
    };
    return cityTranslations[city] || city;
  }
  return city;
};

// 获取城市描述
const getCityDescription = (cityName: string) => {
  const cityInfo = cityInfoDataLocal[cityName];
  return locale.value === 'en' && cityInfo?.['description-en'] ? cityInfo['description-en'] : cityInfo?.description;
};

// 获取景点显示名称
const getAttractionDisplayName = (attractionName: string) => {
  const element = cultureElements.find(item => item.title === attractionName);
  return locale.value === 'en' && element?.['title-en'] ? element['title-en'] : attractionName;
};

// 获取景点描述
const getAttractionDescription = (attractionName: string) => {
  const element = cultureElements.find(item => item.title === attractionName);
  return locale.value === 'en' && element?.['description-en'] ? element['description-en'] : element?.description || '';
};

</script>

<style scoped lang="scss">
@import '@/assets/font/font.css';
#app {
  height: 100vh;
  margin: 0;
}

.el-main {
  --el-main-padding:0;

}
.hunan-tourist-attractions {

  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}


.hunan-tourist-attractions {
  display: flex;
  flex-direction: column;
  align-items: center;

  min-height: 100vh;
  padding: 10px;

}

.map-info-container {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.map-box {
  width: 500px;
  height: 600px;
  padding: 10px;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  position: relative;
}

.bubble-container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  padding: 10px;
  
  // 添加城市名背景
  &::before {
    
    content: attr(data-city-name);
    position: absolute;
    top: 50%;
    left: 60%;
    transform: translate(-50%, -50%);
    font-size: 120px;
    font-weight: bold;
    color: rgba(183, 28, 28, 0.2);

    text-orientation: upright;  // 保持每个字符正立
    letter-spacing: 20px;
    font-family: 'ZhuanTi', serif;
    pointer-events: none;
    z-index: 0;
    line-height: 1.2;
  }
  
  // 添加渐变蒙版
  &::after {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(
      to right,
      rgba(255, 255, 255, 0.8) 0%,
      rgba(255, 255, 255, 0.4) 50%,
      rgba(255, 255, 255, 0.8) 100%
    );
    pointer-events: none;
    z-index: 1;
  }
}

.city-bubble {
  position: absolute;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 8px 32px rgba(183, 28, 28, 0.15), inset 0 0 32px rgba(183, 28, 28, 0.25);
  backdrop-filter: blur(10px);
  border: 1.5px solid rgba(255, 255, 255, 0.2);
  user-select: none;
  touch-action: none;
  z-index: 2;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    inset: 0;
    background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.25), transparent 50%);
    opacity: 0.8;
  }

  &::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(183, 28, 28, 0.4), rgba(211, 47, 47, 0.6));
    z-index: -1;
  }

  &.dragging {
    cursor: grabbing;
    z-index: 100;
    transform: scale(1.15);
    background: rgba(255, 255, 255, 0.2);
    box-shadow: 0 12px 40px rgba(183, 28, 28, 0.25), inset 0 0 40px rgba(183, 28, 28, 0.35);
    border-color: rgba(255, 255, 255, 0.3);

    &::after {
      background: linear-gradient(135deg, rgba(183, 28, 28, 0.5), rgba(211, 47, 47, 0.7));
    }

    .bubble-text {
      transform: scale(1.05);
    }
  }

  &:hover:not(.dragging) {
    transform: scale(1.1) translateY(-2px);
    background: rgba(255, 255, 255, 0.18);
    box-shadow: 0 10px 36px rgba(183, 28, 28, 0.2), inset 0 0 36px rgba(183, 28, 28, 0.3);
    border-color: rgba(255, 255, 255, 0.25);

    &::after {
      background: linear-gradient(135deg, rgba(183, 28, 28, 0.45), rgba(211, 47, 47, 0.65));
    }
  }

  &.selected {
    transform: scale(1.15);
    background: rgba(255, 255, 255, 0.22);
    box-shadow: 0 12px 40px rgba(183, 28, 28, 0.3), inset 0 0 40px rgba(183, 28, 28, 0.4);
    border-color: rgba(255, 255, 255, 0.35);
    z-index: 10;

    &::after {
      background: linear-gradient(135deg, rgba(183, 28, 28, 0.6), rgba(211, 47, 47, 0.8));
    }

    .bubble-text {
      transform: scale(1.05);
    }
  }
}

.bubble-text {
  color: white;
  font-size: 15px;
  font-weight: 600;
  text-align: center;
  padding: 12px;
  font-family: 'ZhuanTi', serif;
  max-width: 90%;
  word-break: break-word;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2), 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
  letter-spacing: 1px;
}

.location-box {
  width: 650px;
  height: 560px;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  position: relative;
}
.attraction-card-box{
  height: 560px;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width:1210px;
  background-color: #fff;
  position: relative;
  box-sizing: border-box;
  overflow-y: auto; /* 启用垂直滚动 */
}

.centered-text {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}
.city-select {
  position: absolute;
  top: 20px;
  left: 20px;
  width: 150px;
}

.city-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.image-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
}
.city-image,.wordcloud-image {
  width: 300px; /* 设置图片的宽度 */
  height: 200px; /* 设置图片的高度 */
  object-fit: cover; /* 保持图片的比例 */
  border-radius: 8px; /* 图片的圆角 */
  margin-bottom: 15px;
}
.wordcloud-image {
  object-fit: contain; /* 确保图片不裁剪 */
}

/* 滚动文本框样式 */
.description-box {
  max-height: 240px; /* 设置文本框的最大高度 */
  //font-family: 'ChillKaiShu',serif;
  overflow-y: auto; /* 启用垂直滚动 */
  padding: 10px;
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  margin-top: 10px;
  width: 90%;
}

.city-name-display {
  font-size: 18px;
  color: #333;
  margin-top: 100px;
}


.attractions-container {
  display: flex;
  flex-wrap: wrap; /* 允许换行 */
  gap: 15px; /* 卡片之间的间距 */
  justify-content: flex-start; /* 卡片左对齐 */
}

.attraction-card {
  background-image: url('@/assets/back/底纹.png');
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;

  margin-right: 22px;
  margin-left: 22px;
  margin-bottom: 15px;
  padding: 15px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 300px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.fancy-name {
  font-family: 'ZhuanTi', serif !important;
  font-size: 13px;
  color: #555;
}

.attraction-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.attraction-image {
  width: 100%;
  height: 180px;
  object-fit: cover;
  border-radius: 8px;
}

.attraction-details {
  margin-top: 10px;

  p {
    color: #2c3e50;
    font-family: 'HelveticaNeue',serif;
    font-size: 12px;
    line-height: 1.5;
    margin-top: 8px;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.attraction-details h3 {
  color: #d32f2f;
  font-family: 'HelveticaNeue',serif;
  font-size: 30px;
  margin: 0;
  font-weight: bold;
}

.attraction-details p {
  font-size: 14px;
  font-family: 'HelveticaNeue',serif;
  color: #555;
  margin-top: 8px;
}

.search-container {
  margin-top: 20px;
  width: 100%;
  max-width: 400px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-container input {
  flex: 1;
  padding: 10px;
  border: 1px solid #d32f2f;
  border-radius: 4px;
  font-size: 14px;
}

.search-container button {
  padding: 10px 20px;
  border: none;
  background-color: #d32f2f;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.3s ease;
}

.search-container button:hover {
  background-color: #b71c1c;
}

.detail-dialog {
  :deep(.el-dialog) {
    background-image: url('@/assets/back/底纹.png');
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
    position: fixed !important;
    top: 50% !important;
    left: 50% !important;
    transform: translate(-50%, -50%) !important;
    margin: 0 !important;
    width: 1200px !important;
    max-height: 90vh; /* 限制最大高度为视口高度的90% */
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  }

  :deep(.el-dialog__body) {
    padding: 0;
    height: calc(90vh - 40px); /* 减去一些边距 */
    overflow: hidden;
  }

  :deep(.el-dialog__header) {
    display: none;
  }

  :deep(.el-overlay) {
    display: flex;
    align-items: center;
    justify-content: center;
    overflow: hidden;  /* 防止遮罩层滚动 */
  }
}

/* 防止背景滚动 */
// :deep(.el-overlay-dialog) {
//   position: fixed;
//   top: 0;
//   right: 0;
//   bottom: 0;
//   left: 0;
//   overflow: hidden;
// }

.dialog-content {
  display: flex;
  height: 100%;
  width: 100%;
  overflow: hidden;
}

.left-section {
  flex: 0 0 40%;
  height: 100%;
  position: relative;
  background-color: black;
  overflow: hidden;
  margin-right: 18px;
  display: flex;
  align-items: center;
}

/* 修改图片包装器 */
.image-wrapper {
  width: 100%;
  height: 100%;  /* 稍微减小高度使图片看起来垂直居中 */
  overflow: hidden;
}

.detail-image {
  width: 500px;
  height: 580px;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.detail-image:hover {
  transform: scale(1.1);
}

.right-section {
  flex: 0 0 60%;
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: white;
  min-width: 0;
  border-left: 1px solid #eee;
}

.right-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: flex-start;  /* 标题靠左对齐 */
  align-items: center;
  background-color: white;

  h2 {
    margin: 0;
    font-size: 24px;
    color: #333;
    font-weight: bold;
  }
}

.right-content {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  scrollbar-width: thin;
  height: calc(90vh - 200px); /* 减去头部和底部的高度 */

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: #f1f1f1;
  }

  &::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 3px;
  }

  &::-webkit-scrollbar-thumb:hover {
    background: #555;
  }

  .info-content {
    max-width: 100%;
    
    .info-item {
      margin-bottom: 24px;

      .info-title h3 {
        position: sticky;
        top: 0;
        background-color: white;
        padding: 10px 0;
        margin: 0 0 12px 0;
        font-size: 18px;
        color: #333;
        padding-left: 10px;
        border-left: 4px solid #B71C1C;
        z-index: 1;
      }

      p {
        color: #666;
        line-height: 1.6;
        text-align: justify;
        word-wrap: break-word;
        margin: 0;
        padding: 0 10px;
      }
    }
  }
}

.right-footer {
  position: sticky;
  bottom: 0;
  padding: 16px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: white;
  width: 100%;
  z-index: 1;
}

.dialog-interaction-icons {
  display: flex;
  gap: 15px;
  margin-right: 40px;
}

.icon-wrapper {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 16px;
  transition: all 0.3s ease;

  &:hover {
    background-color: rgba(183, 28, 28, 0.1);
  }

  .icon {
    width: 20px;
    height: 20px;
    transition: transform 0.3s ease;
  }

  .icon.active {
    transform: scale(1.2);
  }

  span {
    color: #666;
    font-size: 14px;
  }
}

.analysis-btn {
  background-color: #B71C1C;
  border: none;
  padding: 10px 20px;
  font-size: 14px;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.analysis-btn:hover {
  background-color: #D32F2F;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(183, 28, 28, 0.2);
}

/* 右上角关闭按钮 */
.dialog-close-button {
  position: absolute;
  top: 16px;
  right: 16px;
  z-index: 10;
  cursor: pointer;
  background-color: rgba(183, 28, 28, 0.8);  /* 使用红色主题色 */
  border-radius: 50%;
  padding: 8px;
  transition: all 0.3s ease;

  .close-icon {
    font-size: 20px;
    color: #fff;
  }
}

.dialog-close-button:hover {
  background-color: #d32f2f;  /* 悬停时加深颜色 */
  transform: rotate(90deg);
}

/* 地理位置标题使用特殊字体 */
.location-title {
  text-align: center;
  font-family: 'ZhuanTi', serif !important; /* 使用纂体字体 */
  font-size: 25px;
}

/* 自定义模态框背景 */
:deep(.custom-modal) {
  background-color: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
}
</style>
