<template>
  <div class="food-section">
    <!-- Header -->
    <div class="main-container">
      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="food-block" v-for="(item, index) in paginatedFoodItems" :key="index">
          <el-card @click="selectFoodItem(index)" class="food-card-sidebar">
            <div class="card-header">
              <img :src="item.img" :alt="getFoodDisplayName(item.name)" class="food-image-sidebar" />
            </div>
            <div class="card-content">
              <h3>{{ getFoodDisplayName(item.name) }}</h3>
              <div class="button-container">
                <el-button @click.stop="showFoodDetail(item)" size="small">{{ t('detail.place.viewDetail') }}</el-button>
                <el-button @click.stop="goToSentimentAnalysis(item.name)" size="small">{{ t('detail.place.sentimentAnalysis') }}</el-button>
              </div>
            </div>
          </el-card>
        </div>
      </aside>

      <!-- Main content -->
      <main class="content">
        <div class="search-container">
          <el-input
              v-model="searchQuery"
              :placeholder="t('detail.place.searchPlaceholder')"
              class="search-input"
              prefix-icon="el-icon-search"
          />
        </div>
        <h2 class="titleH">{{ t('detail.place.hunanCuisine') }}</h2>
        <!-- Carousel -->
        <div class="carousel-container">
          <div
              class="carousel"
              :style="{ transform: `rotateY(${rotationAngle}deg) rotateX(${tiltAngle}deg)` }"
          >
            <div
                class="carousel-item"
                v-for="(item, index) in paginatedFoodItems"
                :key="index"
                :style="getItemStyle(index)"
            >
              <el-card class="food-card" @click="rotateRight">
                <div class="card-header">
                  <img :src="item.img" :alt="getFoodDisplayName(item.name)" class="food-image" />
                </div>

                <div class="card-content">
                  <h3>{{ getFoodDisplayName(item.name) }}</h3>
                  <div class="button-container">
                    <el-button @click.stop="showFoodDetail(item)" size="small">{{ t('detail.place.viewDetail') }}</el-button>
                    <el-button @click.stop="sentimentAnalysis(item)" size="small">{{ t('detail.place.sentimentAnalysis') }}</el-button>
                  </div>
                </div>
              </el-card>
            </div>
          </div>
        </div>

        <!-- Control Buttons (Bottom) -->
        <div class="control-buttons">
          <el-pagination
              :current-page="currentPage"
              :page-size="8"
              :total="filteredFoodItems.length"
              @current-change="handlePageChange"
              layout="prev, pager, next"
          />
        </div>
      </main>
    </div>
  </div>
  <!-- Food Detail Dialog -->
  <el-dialog
      v-model="foodDetail.visible"
      :show-close="true"
      class="food-detail-dialog"
      width="600px"
  >
    <div class="food-detail-content">
      <div class="food-image-container">
        <img :src="foodDetail.item?.img" :alt="foodDetail.name" class="food-detail-image">
      </div>
      <div class="food-info">
        <h2>{{ foodDetail.name }}</h2>
        <div class="food-description">
          <p>{{ foodDetail.description }}</p>
        </div>
        <div class="food-actions">
          <div class="interaction-icons">
            <div class="icon-wrapper" @click="toggleLike">
              <img
                  :src="tagStatus.is_liked ? likeActiveIcon : likeIcon"
                  :class="['icon', { 'active': tagStatus.is_liked }]"
                  :alt="t('detail.place.like')"
              />
              <span>{{ tagStatus.total_likes || 0 }}</span>
            </div>
            <div class="icon-wrapper" @click="toggleFavorite">
              <img
                  :src="tagStatus.is_favorite ? favoriteActiveIcon : favoriteIcon"
                  :class="['icon', { 'active': tagStatus.is_favorite }]"
                  :alt="t('detail.place.favorite')"
              />
              <span>{{ t('detail.place.favorite') }}</span>
            </div>
          </div>
          <el-button
              type="primary"
              class="analysis-btn"
              @click="goToSentimentAnalysis(foodDetail.item?.name)"
          >
            {{ t('detail.place.sentimentAnalysis') }}
          </el-button>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue';
import { useRouter } from 'vue-router'; // 导入 useRouter 来进行跳转
import { useI18n } from 'vue-i18n';
import food1 from '@/assets/foodImg/food1.jpg'
import food2 from '@/assets/foodImg/food2.jpg'
import food3 from '@/assets/foodImg/food3.jpg'
import food4 from '@/assets/foodImg/food4.jpg'
import food5 from '@/assets/foodImg/food5.jpg'
import FoodAPI from '@/api/food';
import TagsAPI from '@/api/tags';
import UserAPI from '@/api/user'
import { useUserStore } from '@/stores/user';
import { ElMessage } from 'element-plus';
import cultureElements from '@/json/culture_elements_translated.json';
// 导入图标
import likeIcon from '@/assets/setting/赞.png'
import likeActiveIcon from '@/assets/setting/赞 (1).png'
import favoriteIcon from '@/assets/setting/收藏.png'
import favoriteActiveIcon from '@/assets/setting/收藏(1).png'

const { t, locale } = useI18n();

const searchQuery = ref('');
const rotationAngle = ref(0); // 旋转角度
const tiltAngle = ref(0); // 俯视仰视角度
const currentPage = ref(1); // 当前页码
const selectedIndex = ref(0);
import { reactive } from 'vue';


const userStore = useUserStore();
const router = useRouter();

// 标签状态
const tagStatus = ref({
  is_liked: false,
  is_favorite: false,
  total_likes: 0
});

// 获取用户ID
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

  // 如果都没有，返回 null
  console.warn('User ID is missing');
  return null;
};

// 初始化标签状态
const initializeTagStatus = async (foodId) => {
  try {
    const userId = getUserId();
    if (!userId) {
      console.warn('Cannot initialize tag status: User not logged in');
      // 未登录用户设置默认状态：未点赞、未收藏
      tagStatus.value = {
        is_liked: false,
        is_favorite: false,
        total_likes: 0
      };
      return;
    }

    console.log(`Initializing tag status with ID: ${foodId}`);
    const response = await TagsAPI.getTagByThemeAndOriginAPI('food', foodId);

    if (response.code === 200 && response.data) {
      const tagId = response.data.id;
      // 确保 userId 是数字类型
      const numericUserId = typeof userId === 'string' ? parseInt(userId, 10) : userId;
      const statusResponse = await TagsAPI.getTagStatusAPI(numericUserId, tagId);

      if (statusResponse.code === 200) {
        tagStatus.value = statusResponse.data;
      }
    }
  } catch (error) {
    console.error('Failed to initialize tag status:', error);
  }
};

// 点赞功能
const toggleLike = async () => {
  try {
    const userId = getUserId();
    if (!userId) {
      ElMessage.warning('请先登录后再点赞');
      return;
    }

    // 尝试从多个可能的来源获取 food_id
    const foodId = foodDetail.item?.food_id || foodDetail.item?.id || foodDetail.id;

    if (!foodId) {
      console.error('Food ID is missing, detail:', foodDetail);
      ElMessage.warning('无法获取食品ID，请重试');
      return;
    }

    console.log('Toggling like for food ID:', foodId);
    const response = await TagsAPI.getTagByThemeAndOriginAPI('food', foodId);
    if (response.code === 200 && response.data) {
      const tagId = response.data.id;

      // 确保 userId 是数字类型
      const numericUserId = typeof userId === 'string' ? parseInt(userId, 10) : userId;
      const likeResponse = await TagsAPI.toggleLikeAPI(numericUserId, tagId);

      if (likeResponse.code === 200) {
        tagStatus.value = {
          ...tagStatus.value,
          is_liked: likeResponse.data.is_liked,
          total_likes: likeResponse.data.total_likes
        };
      }
    }
  } catch (error) {
    console.error('点赞操作失败:', error);
  }
};

// 收藏功能
const toggleFavorite = async () => {
  try {
    const userId = getUserId();
    if (!userId) {
      ElMessage.warning('请先登录后再收藏');
      return;
    }

    // 尝试从多个可能的来源获取 food_id
    const foodId = foodDetail.item?.food_id || foodDetail.item?.id || foodDetail.id;

    if (!foodId) {
      console.error('Food ID is missing, detail:', foodDetail);
      ElMessage.warning('无法获取食品ID，请重试');
      return;
    }

    console.log('Toggling favorite for food ID:', foodId);
    const response = await TagsAPI.getTagByThemeAndOriginAPI('food', foodId);
    if (response.code === 200 && response.data) {
      const tagId = response.data.id;

      // 确保 userId 是数字类型
      const numericUserId = typeof userId === 'string' ? parseInt(userId, 10) : userId;
      const favoriteResponse = await TagsAPI.toggleFavoriteAPI(numericUserId, tagId);

      if (favoriteResponse.code === 200) {
        tagStatus.value.is_favorite = favoriteResponse.data.is_favorite;
      }
    }
  } catch (error) {
    console.error('收藏操作失败:', error);
  }
};

// 记录点击事件
const recordClick = async (foodId) => {
  try {
    const userId = getUserId();
    if (!userId) {
      console.log('未登录用户的点击不记录');
      return;
    }

    // 获取美食对应的标签
    const response = await TagsAPI.getTagByThemeAndOriginAPI('food', foodId);
    if (response.code === 200 && response.data) {
      const tagId = response.data.id;
      // 确保 userId 是数字类型
      const numericUserId = typeof userId === 'string' ? parseInt(userId, 10) : userId;
      // 使用 viewTagAPI 记录点击
      await TagsAPI.viewTagAPI(numericUserId, tagId);
      console.log(`记录用户 ${userId} 对美食 ${foodId} 的点击`);
    }
  } catch (error) {
    console.error('记录点击失败:', error);
  }
};

const addHistory = async (item) => {
  try {
    const userId = getUserId();
    if (!userId) {
      ElMessage.warning('请先登录以记录浏览历史');
      return;
    }
    const historyData = {
      uid: Number(userId), // 确保是数字类型
      type: "food", // 记录类型
      name: item.name, // 美食名称
      img_url: item.img, // 美食图片
      describe: item.description.substring(0, 50) || '美食描述', // 美食描述
    };
    
    // 调用API添加历史记录
    await UserAPI.AddUserHistory(historyData);
    console.log('浏览历史记录已添加:', item.name);
  
    // 记录点击事件
    await recordClick(item.food_id || item.id);
  } catch (error) {
    console.error('记录历史失败:', error);
  }
};

// 获取美食显示名称
const getFoodDisplayName = (name) => {
  const element = cultureElements.find(item => item.title === name);
  return locale.value === 'en' && element?.['title-en'] ? element['title-en'] : name;
};

// 获取美食描述
const getFoodDescription = (name) => {
  const element = cultureElements.find(item => item.title === name);
  return locale.value === 'en' && element?.['description-en'] ? element['description-en'] : element?.description || '';
};

// 修改显示食品详情的函数
const showFoodDetail = async (item) => {
  foodDetail.visible = true;
  foodDetail.name = getFoodDisplayName(item.name);
  foodDetail.description = getFoodDescription(item.name);
  foodDetail.img = item.img;
  foodDetail.item = item;
  foodDetail.id = item.food_id || item.id;
  addHistory(item)
  // 初始化标签状态
  await initializeTagStatus(foodDetail.id);
  // 记录点击
  await recordClick(foodDetail.id);
};

// 修改情感分析函数
const sentimentAnalysis = async (item) => {
  console.log('点击了情感分析按钮', item.name);
  // 记录点击
  await recordClick(item.food_id || item.id);

  router.push({
    path: '/detail',
    query: {
      name: item.name,
      value: 3,
      theme: 1
    }
  });
};

// 点击左侧菜品，更新右侧展示的菜品
const selectFoodItem = async (index) => {
  selectedIndex.value = index;
  const angle = (360 / paginatedFoodItems.value.length) * index;
  rotationAngle.value = angle; // 通过旋转角度更新 Carousel

  // 记录点击
  const item = paginatedFoodItems.value[index];
  if (item) {
    await recordClick(item.food_id || item.id);
  }
};

const foodDetail = reactive({
  visible: false,
  name: '',
  img: '',
  description: '',
  id: null, // 确保有 id 字段
});

// 关闭详情弹窗
const closeFoodDetail = () => {
  foodDetail.visible = false;
};

/*// Food items data with unique descriptions for each dish
const foodItems = [
  { name: "糖油粑粑", img: food1, description: "糖油粑粑是一种油炸甜点，外脆内软，甜美可口。" },
  { name: "毛家红烧肉", img: food2, description: "这道菜是湖南特色的红烧肉，色泽红亮，味道鲜美。" },
  { name: "臭豆腐", img: food3, description: "臭豆腐是湖南特色的街头小吃，外焦内嫩，臭味十足，令人上瘾。" },
  { name: "攸县香干", img: food4, description: "攸县香干有独特的风味，口感浓郁，富有烟熏味。" },
  { name: "辣椒炒肉", img: food5, description: "辣椒炒肉是一道麻辣可口的经典湘菜，味道香辣。" },
  { name: "糖油粑粑", img: food1, description: "糖油粑粑是一种油炸甜点，外脆内软，甜美可口。" },
  { name: "毛家红烧肉", img: food2, description: "这道菜是湖南特色的红烧肉，色泽红亮，味道鲜美。" },
  { name: "臭豆腐", img: food3, description: "臭豆腐是湖南特色的街头小吃，外焦内嫩，臭味十足，令人上瘾。" },
  { name: "攸县香干", img: food4, description: "攸县香干有独特的风味，口感浓郁，富有烟熏味。" },
  { name: "辣椒炒肉", img: food5, description: "辣椒炒肉是一道麻辣可口的经典湘菜，味道香辣。" }
];*/
const foodItems=ref([])
async function fetchFoodData() {
  try {
    const response = await FoodAPI.getFoodAPI();
    foodItems.value = response.data.map(item => ({
      id: item.food_id,
      name: item.food_name,
      img: item.image_url || '',
      description: item.description || ''
    }));
    console.log('Food data:', foodItems.value);
  } catch (error) {
    console.error('Error fetching food data:', error);
  }
}

onMounted(() => {
  fetchFoodData();
});

// Filter food items
const filteredFoodItems = computed(() => {
  if (!foodItems.value) return []; // 防止初始值为 null 时报错
  return foodItems.value.filter(item =>
      item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});


// Paginate food items
const paginatedFoodItems = computed(() => {
  const startIndex = (currentPage.value - 1) * 6;
  return filteredFoodItems.value.slice(startIndex, startIndex + 6);
});

// Click event handler for navigating to food detail
const goToSentimentAnalysis = (foodName) => {
  router.push({
    path: '/detail',
    query: {
      name: foodName,
      value: 3,
      theme: 1
    }
  });
};

// Function to rotate carousel
const rotateLeft = () => {
  rotationAngle.value += 45;
};

const rotateRight = () => {
  rotationAngle.value -= 45;
};

// Function to tilt carousel view (仰视/俯视)
const handlePageChange = (page) => {
  currentPage.value = page;
};

// Get the individual item style
const getItemStyle = (index) => {
  const angle = (360 / paginatedFoodItems.value.length) * index;
  const translateZ = 250; // Adjust distance from center for 3D effect
  // 根据选中的菜品，设置旋转角度
  if (selectedIndex.value === index) {
    return {
      transform: `rotateY(-${angle}deg) translateZ(${translateZ}px) scale(1.2)` // 选中的菜品放大显示
    };
  }
  return {
    transform: `rotateY(-${angle}deg) translateZ(${translateZ}px)`
  };
};

// 添加返回到美食主页的方法
const goToFoodHome = () => {
  router.push('/food/home');
};

</script>

<style scoped lang="scss">
/* 统一标题字体样式 */

.el-dialog__header {
  font-family: 'HelveticaNeue', serif  !important;;  /* 与其他部分保持一致的字体 */
  font-size: 24px ;  /* 标题大小 */
  font-weight: bold; /* 加粗 */
  color: #333 ; /* 字体颜色 */
  text-align: center; /* 让标题居中 */
}

/* 按钮样式 */
.el-button {
  font-family: 'HelveticaNeue', serif; /* 保持统一字体 */
  background-color: #da251c; /* 主题色 */
  color: white;
  border-radius: 20px; /* 圆角按钮 */

  transition: background-color 0.3s, color 0.3s;
  font-size: 12px; /* 按钮文字大小 */
}

/* 按钮悬浮和点击效果 */
.el-button:hover {
  background-color: #b81f17;
  border-color: #b81f17;
}

.el-button:active {
  background-color: #9e1914;
  border-color: #9e1914;
}

/* 控制按钮内的图标颜色 */
.el-button .el-icon {
  color: white;
}

/* 控制按钮区域 */
.control-buttons {
  margin-top: 30px;
  margin-left: 400px;
  text-align: center;
  background-color: transparent !important; /* 背景透明 */
}

.control-buttons :deep(.el-button) {
  background-color: transparent!important; /* 按钮背景透明 */
  color: #fff8f0; /* 默认文字颜色 */
  transition: color 0.3s ease, border-color 0.3s ease; /* 文字和边框颜色变化的过渡效果 */
}

/* 控制按钮点击时文字和箭头颜色变红 */
.control-buttons :deep(.el-button:active),
.control-buttons :deep(.el-pagination:active) {
  color: #da251c; /* 点击时文字颜色变红 */
  border-color: #da251c; /* 点击时边框颜色变红 */
}

/* 食品详情弹窗样式 */
.food-detail-dialog {
  text-align: center;
  font-family: 'HelveticaNeue', serif; /* 保持一致的字体 */
  padding: 20px;
}

.detail-image {
  width: 100%;
  max-width: 320px;
  margin: 0 auto 20px;
  display: block;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  border: 2px solid #f1f1f1; /* 为图片添加边框 */
}

/* 标题样式 */
.food-detail-dialog h2 {
  font-size: 20px;
  color: #333;
  margin-bottom: 10px;
  font-weight: bold;
}

/* 描述样式 */
.food-detail-dialog p {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 20px;
}

/* 自定义按钮样式 */
.dialog-footer .el-button {
  font-family: 'HelveticaNeue', serif;
  background-color: #da251c; /* 使用统一的主题色 */
  border-color: #da251c;
  color: #fff;
  padding: 10px 20px;
  border-radius: 20px; /* 弹窗按钮圆角 */
  transition: background-color 0.3s, color 0.3s;
}

.dialog-footer .el-button:hover {
  background-color: #b81f17; /* 按钮悬浮时变暗 */
  border-color: #b81f17;
}

.dialog-footer .el-button:active {
  background-color: #9e1914;
  border-color: #9e1914;
}

.button-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
.food-detail-dialog {
  text-align: center;
}

.detail-image {
  width: 100%;
  max-width: 300px;
  margin: 0 auto 20px;
  display: block;
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}
.food-detail-dialog h2 {
  margin: 10px 0;
  font-size: 24px;
  color: #333;
}

.food-detail-dialog p {
  font-size: 16px;
  color: #666;
  line-height: 1.5;
}

@import '@/assets/font/font.css';
/* 整体布局 */
.food-section {
  display: flex;
  flex-direction: column;
}

/* Header 样式 */
.header {
  font-family: 'HelveticaNeue', serif;
  color: #fff;
  text-align: center;
  font-size: 38px;
  font-weight: bold;
  position: relative; /* 让子元素可以使用绝对定位 */
  display: flex; /* 使用 flex 布局 */
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  height: 30px; /* 可以根据需要调整 */
}

.titleH {
  position: absolute;
  right: 0;
  top: 180px; /* 调整标题位置，上移40px */
  writing-mode: vertical-rl;
  white-space: nowrap;
  font-family: 'HelveticaNeue', serif;
  margin-right: 150px;
}

/* 英文状态下的标题位置调整 */
:root[lang="en"] .titleH {
  top: 150px; /* 英文状态下再上移30px */
}

/* 搜索框容器样式 */
.search-container {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  position: absolute;
margin-left: 390px;
  margin-top: -45px;
}

/* 搜索框样式 */
.search-input {
  width: 200px;
  font-family: 'HelveticaNeue', serif;
  margin: 0 auto; /* 自动调整左右外边距，实现居中 */
}

/* 主体部分布局 */
.main-container {
  display: flex;
  flex: 1;
  margin-top: 0px;
  padding: 20px;
}

/* Sidebar 样式 */
.sidebar {
  width: 240px;
  background-color: #fff;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  position: sticky;
  font-family: 'HelveticaNeue', serif;
  top: 20px;
  height: 630px; /* 高度撑满父容器 */
  overflow-y: auto; /* 超出部分滚动 */
}

.food-block {
  margin-bottom: 20px;
}

.food-card-sidebar {
  width: 100%;
  cursor: pointer;
}

.food-image-sidebar {
  width: 100%;
  height: 100px;
  object-fit: cover;
}

.food-card-sidebar .card-content {
  padding: 0px;
  text-align: center;
}

.food-card-sidebar h3 {
  font-size: 22px;
  margin: 5px;
}

/* Main content 样式 */
.content {
  background-image: url("@/assets/FoodF.png");
  flex: 1;

  padding-top:  80px;
  padding-bottom: 20px;
  background-color: #ffffff;
  height: 570px; /* 高度撑满父容器 */
  overflow-y: auto; /* 超出部分滚动 */
}

.content h2 {
  color: #fff8f0;
  font-size: 58px;
  margin-bottom: 20px;
  text-shadow: 3px 3px 5px rgba(0, 0, 0, 0.4); /* 添加阴影 */
}


/* Carousel 样式 */
.carousel-container {
  position: relative;
  margin-top: 50px;
  width: 90%;
  height: 400px;
  perspective: 1200px;
}

.carousel {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  position: absolute;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transition: transform 1s ease;
}

/* 每个卡片项 */
.carousel-item {
  position: absolute;
  width: 220px;
  height: 330px;
  font-family: 'HelveticaNeue', serif;
  font-size: 24px;
  transform-origin: center center;
  transition: transform 1s ease;
}

.food-card {
  width: 100%;
  height: 100%;
}

.food-card .card-header img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.food-card .card-content {
  padding: 0px;
  display: flex;
  flex-direction: column;
  justify-content: center; /* 垂直居中 */
  align-items: center; /* 水平居中 */
  height: 100%;
  text-align: center;
}

/* 控制按钮 */
.control-buttons {
  margin-top: 80px;
  margin-left:400px;
  text-align: center;
  background-color: transparent !important; /* 背景透明 */
}

/* 强制修改 .el-button 和 .el-pagination 的文字和箭头颜色 */
.control-buttons :deep(.el-button),
.control-buttons :deep(.el-pagination) {
  background-color: transparent!important; /* 按钮背景透明 */
  color: #fff8f0; /* 默认文字颜色 */
  transition: color 0.3s ease, border-color 0.3s ease; /* 文字和边框颜色变化的过渡效果 */
}

/* 控制按钮点击时文字和箭头颜色变红 */
.control-buttons :deep(.el-button:active),
.control-buttons :deep(.el-pagination:active) {
  color: #da251c; /* 点击时文字颜色变红 */
  border-color: #da251c; /* 点击时边框颜色变红 */
}

/* 控制按钮点击时图标颜色变红 */
.control-buttons :deep(.el-button:active .el-icon),
.control-buttons :deep(.el-pagination:active .el-icon) {
  color: #da251c; /* 点击时图标颜色变红 */
}


.el-button {
  margin: 0 10px;
}

.side-interaction-icons {
  position: absolute;
  right: -60px;
  top: 50%;
  transform: translateY(-50%);
  display: flex;
  flex-direction: column;
  gap: 20px;
  z-index: 100;
}

.icon-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 8px;
  border-radius: 8px;
  transition: transform 0.2s ease;
}

.icon-wrapper:hover {
  transform: scale(1.1);
}

.icon {
  width: 24px;
  height: 24px;
  opacity: 0.6;
  transition: opacity 0.3s ease;
}

.icon.active {
  opacity: 1;
}

.icon-wrapper span {
  font-size: 12px;
  color: #666;
  text-align: center;
}

/* 调整弹窗内容以适应右侧图标 */
.el-dialog {
  position: relative;
  margin-right: 60px !important;
}

/* 美食详情弹窗样式 */
.food-detail-dialog {
  :deep(.el-dialog) {
    border-radius: 12px;
    overflow: hidden;
  }

  :deep(.el-dialog__body) {
    padding: 0;
  }
}

.food-detail-content {
  .food-image-container {
    width: 100%;
    height: 400px;
    overflow: hidden;
    
    .food-detail-image {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transition: transform 0.3s ease;
      
      &:hover {
        transform: scale(1.05);
      }
    }
  }

  .food-info {
    padding: 24px;
    
    h2 {
      font-size: 24px;
      color: #333;
      margin: 0 0 16px 0;
      text-align: center;
    }

    .food-description {
      margin-bottom: 24px;
      
      p {
        color: #666;
        line-height: 1.6;
        text-align: justify;
        margin: 0;
      }
    }

    .food-actions {
      display: flex;
      justify-content: space-between;
      align-items: center;
      
      .interaction-icons {
        display: flex;
        gap: 16px;
      }

      .icon-wrapper {
        display: flex;
        align-items: center;
        gap: 4px;
        cursor: pointer;
        padding: 6px 12px;
        border-radius: 20px;
        transition: all 0.3s ease;

        &:hover {
          background-color: rgba(218, 37, 28, 0.1);
        }

        .icon {
          width: 20px;
          height: 20px;
          
          &.active {
            transform: scale(1.2);
          }
        }

        span {
          color: #666;
          font-size: 14px;
        }
      }

      .analysis-btn {
        background-color: #da251c;
        border: none;
        padding: 8px 20px;
        border-radius: 20px;
        
        &:hover {
          background-color: #b81f17;
        }
      }
    }
  }
}

/* 左侧卡片按钮组样式 */
.food-card-sidebar .button-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

/* 英文状态下左侧卡片按钮组位置调整 */
:root[lang="en"] .food-card-sidebar .button-container {
  margin-left: -20px;
  width: 90%;
  justify-content: flex-start;
}

/* 轮播卡片按钮组样式 */
.food-card .button-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

/* 英文状态下轮播卡片按钮组位置调整 */
:root[lang="en"] .food-card .button-container {
  margin-left: -40px;
  width: 95%;
  justify-content: flex-start;
  gap: 5px;
}

/* 英文状态下左侧卡片按钮样式 */
:root[lang="en"] .food-card-sidebar .el-button {
  font-size: 11px;
  padding: 8px 10px;
}

/* 英文状态下轮播卡片按钮样式 */
:root[lang="en"] .food-card .el-button {
  font-size: 10px;
  padding: 6px 8px;
}

/* 移除之前的通用按钮组样式 */
.button-container {
  display: flex;
  justify-content: space-between;
  width: 100%;
}
</style>
