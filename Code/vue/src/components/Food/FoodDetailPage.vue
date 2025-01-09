<template>
  <div class="food-detail-page">
    <div class="header">
      <button @click="goBack" class="back-button">←</button>
      <h2>{{ food.name }}</h2>
    </div>
    <div class="food-info">
      <img :src="food.img" :alt="food.name" class="food-image" />
      <div class="food-description">
        <p>{{ food.description }}</p>
      </div>
    </div>
    <div class="sentiment-analysis">
      <h3>情感分析</h3>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';

// Import food items data
import food1 from '@/assets/foodImg/food1.jpg';
import food2 from '@/assets/foodImg/food2.jpg';
import food3 from '@/assets/foodImg/food3.jpg';
import food4 from '@/assets/foodImg/food4.jpg';
import food5 from '@/assets/foodImg/food5.jpg';
const route = useRoute();
const router = useRouter();
const tableData = [
  {
    word: '甜美',
    frequency: 120,
    sentiment: '正面'
  },
  {
    word: '糯米香',
    frequency: 110,
    sentiment: '正面'
  },
  {
    word: '外脆内软',
    frequency: 95,
    sentiment: '正面'
  },
  {
    word: '香甜',
    frequency: 130,
    sentiment: '正面'
  },
  {
    word: '油腻',
    frequency: 50,
    sentiment: '负面'
  },
  {
    word: '过于甜腻',
    frequency: 30,
    sentiment: '负面'
  },
  {
    word: '口感独特',
    frequency: 80,
    sentiment: '正面'
  }
]


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
  }];

// Find the selected food item by the foodName param
const food = computed(() => {
  return foodItems.find(item => item.name === route.params.foodName);
});

// Go back to the previous page
const goBack = () => {
  router.back();
};
</script>

<style scoped>
.food-detail-page {
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.back-button {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #000;
}

.food-info {
  display: flex;
  gap: 20px;
}

.food-image {
  width: 200px;
  height: 150px;
  object-fit: cover;
  border-radius: 8px;
}

.food-description {
  max-width: 600px;
}

.sentiment-analysis {
  margin-top: 30px;
  font-size: 18px;
  color: #555;
}
</style>
