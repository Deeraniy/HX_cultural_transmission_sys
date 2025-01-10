<template>
  <div class="food-section">
    <!-- Header -->
    <header class="header">
      <div class="search-container">
        <el-input
            v-model="searchQuery"
            placeholder="搜索美食..."
            class="search-input"
            prefix-icon="el-icon-search"
        />
      </div>
    </header>

    <div class="main-container">
      <!-- Sidebar -->
      <aside class="sidebar">
        <div class="food-block" v-for="(item, index) in paginatedFoodItems" :key="index">
          <el-card @click="goToFoodDetail(item.name)" class="food-card-sidebar">
            <div class="card-header">
              <img :src="item.img" :alt="item.name" class="food-image-sidebar" />
            </div>
            <div class="card-content">
              <h3>{{ item.name }}</h3>
            </div>
          </el-card>
        </div>
      </aside>

      <!-- Main content -->
      <main class="content">
        <h2 class="titleH">湖南菜经典美食</h2>
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
                  <img :src="item.img" :alt="item.name" class="food-image" />
                </div>
                <div class="card-content">
                  <h3>{{ item.name }}</h3>
                  <el-button @click.stop="goToFoodDetail(item.name)" size="small">查看详情</el-button>
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
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router'; // 导入 useRouter 来进行跳转
import food1 from '@/assets/foodImg/food1.jpg'
import food2 from '@/assets/foodImg/food2.jpg'
import food3 from '@/assets/foodImg/food3.jpg'
import food4 from '@/assets/foodImg/food4.jpg'
import food5 from '@/assets/foodImg/food5.jpg'

const searchQuery = ref('');
const rotationAngle = ref(0); // 旋转角度
const tiltAngle = ref(0); // 俯视仰视角度
const currentPage = ref(1); // 当前页码

// Food items data
const foodItems = [
  { name: "糖油粑粑", img: food1 },
  { name: "毛家红烧肉", img: food2 },
  { name: "臭豆腐", img: food3 },
  { name: "攸县香干", img: food4 },
  { name: "辣椒炒肉", img: food5 },
  { name: "糖油粑粑", img: food1 },
  { name: "毛家红烧肉", img: food2 },
  { name: "臭豆腐", img: food3 },
  { name: "攸县香干", img: food4 },
  { name: "辣椒炒肉", img: food5 }
];

// Filter food items
const filteredFoodItems = computed(() => {
  return foodItems.filter(item =>
      item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// Paginate food items
const paginatedFoodItems = computed(() => {
  const startIndex = (currentPage.value - 1) * 6;
  return filteredFoodItems.value.slice(startIndex, startIndex + 6);
});

// Get the router instance to navigate
const router = useRouter();

// Click event handler for navigating to food detail
const goToFoodDetail = (foodName) => {
  router.push(`/food/detail/${foodName}`);
};

// Function to rotate carousel
const rotateLeft = () => {
  rotationAngle.value -= 45;
};

const rotateRight = () => {
  rotationAngle.value += 45;
};

// Function to tilt carousel view (仰视/俯视)
const handlePageChange = (page) => {
  currentPage.value = page;
};

// Get the individual item style
const getItemStyle = (index) => {
  const angle = (360 / paginatedFoodItems.value.length) * index;
  const translateZ = 250; // Adjust distance from center for 3D effect
  return {
    transform: `rotateY(${angle}deg) translateZ(${translateZ}px)`
  };
};
</script>

<style scoped>
@import '@/assets/font/font.css';
/* 整体布局 */
.food-section {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
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
  position: absolute; /* 绝对定位 */
  right: 0; /* 放在最右边 */
  top: 220px; /* 距离顶部20px，调整可根据需求 */
  writing-mode: vertical-rl; /* 竖直从右到左 */
  white-space: nowrap; /* 防止文字换行 */
  margin: 0; /* 去除默认的上下边距 */
  font-family: 'HelveticaNeue', serif;
  margin-right: 150px;
}

/* 搜索框容器样式 */
.search-container {
  display: flex;

  justify-content: center; /* 水平居中 */
  align-items: center; /* 垂直居中 */
  position: absolute;
  top: 20px; /* 根据需要调整距离 */
  right: 20px;
  width: 100%; /* 让它撑满宽度 */
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
  margin-top: 20px;
  padding: 20px;
  height: calc(100vh - 140px); /* 高度撑满屏幕，减去 header 的高度 */
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
  height: 522px; /* 高度撑满父容器 */
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
  font-size: 28px;
  margin: 0;
}

/* Main content 样式 */
.content {
  background-image: url("@/assets/FoodF.png");
  flex: 1;

  padding-top:  80px;
  padding-bottom: 20px;
  background-color: #ffffff;
  height: 100%; /* 高度撑满父容器 */
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
  font-size: 30px;
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
  margin-top: 30px;
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
</style>
