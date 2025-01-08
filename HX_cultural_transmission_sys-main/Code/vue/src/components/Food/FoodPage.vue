<template>
  <div class="food-section">
    <!-- Header -->
    <header class="header">
      <div class="logo">湘菜韵味</div>
      <span>The Essence of Hunan Cuisine</span>
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
        <el-menu
            default-active="0"
            class="el-menu-vertical-demo"
            @select="handleSelect"
            background-color="#ffffff"
            text-color="#333"
            active-text-color="var(--theme-color)"
        >
          <el-menu-item v-for="(item, index) in foodItems" :key="index" :index="index.toString()">
            <template #title>
              <router-link :to="`/food/detail/${item.name}`" class="menu-link">{{ item.name }}</router-link>
            </template>
          </el-menu-item>
        </el-menu>
      </aside>

      <!-- Main content -->
      <main class="content">
        <h2>湖南菜经典美食</h2>
        <!-- Filtered food items based on search query -->
        <el-card
            v-for="item in filteredFoodItems"
            :key="item.name"
            class="food-card"
            @click="goToFoodDetail(item.name)"
        >
          <div class="card-header">
            <img :src="item.img" :alt="item.name" class="food-image" />
          </div>
          <div class="card-content">
            <h3>{{ item.name }}</h3>
            <p>{{ item.description }}</p>
          </div>
        </el-card>
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

// Food items data
const foodItems = [
  {
    name: "糖油粑粑",
    img: food1,
    description: "糖油粑粑是一道湖南传统的甜点，外皮酥脆，内心软糯，香甜的糖浆包裹其中，口感独特，甜而不腻。每一口都能感受到浓郁的糯米香和糖浆的甜美，是一道深受欢迎的小吃。"
  },
  {
    name: "毛家红烧肉",
    img: food2,
    description: "毛家红烧肉是湖南省的传统经典菜肴，以猪肉为主料，采用独特的烹饪技法慢炖，猪肉酥软入味，色泽红亮。酱香浓郁，味道鲜美，入口即化。此菜深受毛泽东故乡人民的喜爱，成为湖南菜的代表之一。"
  },
  {
    name: "臭豆腐",
    img: food3,
    description: "臭豆腐是湖南街头小吃的代表之一，外脆内嫩，色泽金黄。它的独特之处在于其发酵的豆腐味道，虽然外面闻起来可能有些许“臭”，但吃上一口却香味扑鼻，味道醇厚。搭配上辣椒酱，更是让人欲罢不能。"
  },
  {
    name: "攸县香干",
    img: food4,
    description: "攸县香干是湖南省攸县的传统美食，选用本地优质黄豆制成豆腐，经过熏制后具有独特的香味。香干口感紧实，有嚼劲，通常与辣椒、蒜末、花生等配料一同炒制，色香味俱佳，是一道非常下饭的菜肴。"
  },
  {
    name: "辣椒炒肉",
    img: food5,
    description: "辣椒炒肉是湖南省的经典家常菜之一，选用猪肉作为主料，配以新鲜的辣椒和蒜末炒制而成。猪肉鲜嫩，辣椒脆爽，口感丰富。菜肴味道辛辣刺激，酱汁浓郁，辣味和肉香交织在一起，十分下饭"
  }
];

// Filter food items based on search query
const filteredFoodItems = computed(() => {
  return foodItems.filter(item =>
      item.name.toLowerCase().includes(searchQuery.value.toLowerCase())
  );
});

// Get the router instance to navigate
const router = useRouter();

// Click event handler for navigating to food detail
const goToFoodDetail = (foodName) => {
  router.push(`/food/detail/${foodName}`);
};

const handleSelect = (index) => {
  // 处理菜单选择事件
  console.log(`Selected: ${foodItems[index].name}`);
};
</script>

<style scoped>
/* 根主题色 */
*{
  --theme-color: #da251c; /* 主题色 红色 */
}

/* 整体布局 */
.food-section {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Header 样式 */
.header {
  background-color: var(--theme-color);
  color: #fff;
  padding: 20px;
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  position: relative;
}

.header .logo {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 10px;
}

.search-container {
  position: absolute;
  right: 20px;
  top: 20px;
}

.search-input {
  width: 200px;
}

/* 主体部分布局 */
.main-container {
  display: flex;
  flex: 1;
  margin-top: 20px;
  padding: 20px;
}

/* Sidebar 样式 */
.sidebar {
  width: 240px;
  background-color: #fff;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 20px;
}

.el-menu-vertical-demo {
  border-right: none;
}

.el-menu-item {
  background-color: #fff;
}

.el-menu-item:hover {
  background-color: #f0f0f0;
}

.menu-link {
  color: var(--theme-color);
  text-decoration: none;
  font-size: 18px;
}

.menu-link:hover {
  text-decoration: underline;
}

/* Main content 样式 */
.content {
  flex: 1;
  padding: 20px;
  background-color: #ffffff;
}

.content h2 {
  color: var(--theme-color);
  font-size: 28px;
  margin-bottom: 20px;
}

/* 每个美食项 */
.food-card {
  width: 100%;
  margin-bottom: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.card-header {
  display: flex;
  justify-content: left;
  align-items: center;
}

.food-image {
  width: 200px;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
}

.card-content {
  padding: 20px;
}

.card-content h3 {
  font-size: 22px;
  color: var(--theme-color);
  margin: 0;
  margin-bottom: 10px;
}

.card-content p {
  font-size: 16px;
  line-height: 1.5;
}
</style>
