<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import banner1 from "@/assets/foodImg/banner1.png";
import banner2 from "@/assets/foodImg/banner2.jpg";
import banner3 from "@/assets/foodImg/banner3.jpg";
// 图片列表
const images = [
    banner1,
    banner2,
    banner3,
];

// 当前图片索引
const currentIndex = ref(0);
let timer = null;

// 切换到指定图片
const switchTo = (index) => {
  currentIndex.value = index;
};

// 切换到下一张图片
const nextImage = () => {
  currentIndex.value = (currentIndex.value + 1) % images.length;
};

// 切换到上一张图片
const prevImage = () => {
  currentIndex.value = (currentIndex.value - 1 + images.length) % images.length;
};

// 自动播放
const startAutoPlay = () => {
  timer = setInterval(nextImage, 3000); // 每3秒切换一次
};

// 停止自动播放
const stopAutoPlay = () => {
  clearInterval(timer);
};

// 组件挂载和卸载的生命周期
onMounted(() => {
  startAutoPlay();
});

onUnmounted(() => {
  stopAutoPlay();
});
</script>

<template>
  <div class="carousel" @mouseenter="stopAutoPlay" @mouseleave="startAutoPlay">
    <!-- 图片列表 -->
    <div class="carousel-inner" :style="{ transform: `translateX(-${currentIndex * 100}%)` }">
      <div class="carousel-item" v-for="(image, index) in images" :key="index">
        <img :src=image :alt="'Image ' + index" />
      </div>
    </div>

    <!-- 底部导航点 -->
    <div class="carousel-dots">
      <span
          v-for="(image, index) in images"
          :key="index"
          :class="{ active: index === currentIndex }"
          @click="switchTo(index)"
      ></span>
    </div>
    <!-- 左右箭头 -->
    <div class="carousel-arrows">
      <span class="arrow left" @click="prevImage">&lt;</span>
      <span class="arrow right" @click="nextImage">&gt;</span>
    </div>
  </div>

</template>

<style scoped>
.carousel {
  position: relative;
  width: 100%;

  height: 500px;
  margin: 0 auto;
  overflow: hidden;
}

.carousel-inner {
  display: flex;
  transition: transform 0.5s ease-in-out;
}

.carousel-item {
  flex: 0 0 100%;
  height: 100%;
}

.carousel-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.carousel-dots {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  gap: 10px;
}

.carousel-dots span {
  display: inline-block;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  background-color: #fff;
  opacity: 0.5;
  cursor: pointer;
}

.carousel-dots .active {
  background-color: red;
  opacity: 1;
}

.carousel-arrows {
  position: absolute;
  top: 50%;
  width: 100%;
  display: flex;
  justify-content: space-between;
  transform: translateY(-50%);
  pointer-events: none;
}

.arrow {
  pointer-events: all;
  font-size: 30px;
  color: #fff;
  background-color: rgba(0, 0, 0, 0.5);
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  user-select: none;
}
</style>
