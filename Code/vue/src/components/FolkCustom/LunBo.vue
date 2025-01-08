<template>
  <div>
    <!-- Date and Weekday Display -->
    <div class="data-time">{{ currentDate }}</div>
    <div class="xingqi">{{ currentDay }}</div>

    <!-- Tabs -->
    <div class="s-second-header">
      <ul>
        <li
            v-for="(tab, index) in tabs"
            :key="index"
            :class="{ 'boder-line': activeTabIndex === index }"
            @click="selectTab(index)"
        >
          {{ tab }}
        </li>
      </ul>
    </div>

    <!-- Image Slider -->
    <div class="silder-block" @mouseenter="pauseSlider" @mouseleave="startSlider">
      <ul class="imgblock" :style="sliderStyle">
        <li v-for="(img, index) in images" :key="index" class="imglist">
          <img :src="img.src" alt="" />
        </li>
      </ul>
      <div class="dian">
        <div
            v-for="(dot, index) in images"
            :key="index"
            class="diandian"
            @mouseenter="jumpToImage(index)"
        >
          <img :src="dot === currentIndex ? 'img/icon/jianzhihong.png' : 'img/icon/jianzhibai.png'" />
        </div>
      </div>
    </div>

    <!-- List Block -->
    <div class="list-block">
      <h2>【全国】</h2>
      <div class="top">
        <ul>
          <li
              v-for="(item, index) in heritageCategories"
              :key="index"
              :class="{ jinse: activeCategory === item.title }"
              @click="selectCategory(item)"
          >
            {{ item.title }}
          </li>
        </ul>
      </div>
      <div class="bottom-list">
        <ul>
          <li v-for="(child, index) in activeCategoryData" :key="index" class="list-text">
            <span>{{ child.number }}</span>
            <span>{{ child.name }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

// Data
const currentDate = ref('')
const currentDay = ref('')
const activeTabIndex = ref(0)
const currentIndex = ref(0)
const activeCategory = ref({})
const activeCategoryData = ref([])

// Tab options
const tabs = ['国家级代表性项目', '国家及代表性传承人']

// Heritage categories
const heritageCategories = [
  {
    title: "国家级代表性项目",
    child: [
      { name: "民间文学", number: 231 },
      { name: "传统音乐", number: 401 },
      { name: "传统舞蹈", number: 324 },
      { name: "传统戏剧", number: 448 },
      { name: "曲艺", number: 425 },
      { name: "传统体育", number: 361 },
      { name: "传统美术", number: 193 },
      { name: "传统技艺", number: 507 },
      { name: "传统医药", number: 137 },
      { name: "民俗", number: 427 }
    ]
  },
  {
    title: "国家及代表性传承人",
    child: [
      { name: "民间文学", number: 123 },
      { name: "传统音乐", number: 380 },
      { name: "传统舞蹈", number: 298 },
      { name: "传统戏剧", number: 784 },
      { name: "曲艺", number: 207 },
      { name: "传统体育", number: 88 },
      { name: "传统美术", number: 378 },
      { name: "传统技艺", number: 518 },
      { name: "传统医药", number: 138 },
      { name: "民俗", number: 60 }
    ]
  }
]

// Images for the slider
const images = [
  { src: './img/lunbo/3.png' },
  { src: './img/lunbo/2.png' },
  { src: './img/lunbo/1.png' },
  { src: './img/lunbo/4.png' },
  { src: './img/lunbo/3.png' }
]

const sliderInterval = ref(null)

// Computed
const sliderStyle = computed(() => ({
  width: `${images.length * window.innerWidth}px`,
  transform: `translateX(-${currentIndex.value * window.innerWidth}px)`
}))

// Methods
const selectTab = (index) => {
  activeTabIndex.value = index
}

const startSlider = () => {
  sliderInterval.value = setInterval(() => {
    currentIndex.value = (currentIndex.value + 1) % images.length
  }, 3500)
}

const pauseSlider = () => {
  clearInterval(sliderInterval.value)
}

const jumpToImage = (index) => {
  currentIndex.value = index
}

const selectCategory = (item) => {
  activeCategory.value = item
  activeCategoryData.value = item.child
}

// Mounted lifecycle hook
onMounted(() => {
  const date = new Date()
  currentDate.value = date.toISOString().substring(0, date.toISOString().indexOf('T'))
  currentDay.value = `星期${'日一二三四五六'.charAt(date.getDay())}`
  startSlider()
})
</script>

<style scoped>
/* Add your styles here, ensuring the layout is similar to the original jQuery-based design */
</style>
