<template>
  <div class="circle-container">

    <div
        v-for="(circle, index) in circles"
        :key="index"
        class="circle"
        :style="{
        animationDelay: `${circle.delay}s`,
        width: circle.size + 'px',
        height: circle.size + 'px',
        left: circle.left + 'px',
        top: circle.top + 'px',
      }"
    >
      <img :src="circle.image" alt="circle" class="circle-image" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

// 预设的水平和垂直位置
const positions = [
  { left: -300, top: 200 },
  { left: 500, top: 100 },
  { left: 200, top: 100 },


  { left: 1000, top: 100 },
];

// 圆形数据
const circles = ref([
  { image: new URL('@/assets/circle1.png', import.meta.url).href, size: 800, delay: 0.2, left: 0, top: 0 },
  { image: new URL('@/assets/circle3.png', import.meta.url).href, size: 650, delay: 0.7, left: 0, top: 0 },
  { image: new URL('@/assets/circle2.png', import.meta.url).href, size: 500, delay: 0.5, left: 0, top: 0 },

  { image: new URL('@/assets/circle5.png', import.meta.url).href, size: 900, delay: 1.2, left: 0, top: 0 },
]);

// 打乱数组顺序的函数
function shuffleArray(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]]; // 交换元素
  }
}

// 在组件挂载后设置每个圆形的水平和垂直位置
onMounted(() => {
  // 打乱位置数组
  // 为每个圆形分配一个随机的位置
  circles.value.forEach((circle, index) => {
    circle.left = positions[index].left;
    circle.top = positions[index].top;  // 固定的竖直位置
  });
});
</script>

<style scoped>
@import '@/assets/font/font.css';
.circle-container {
  background-image: url("@/assets/img2.png");
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
  z-index: -11;
}
.main-title {
  font-family: 'HelveticaNeue', serif;
  position: absolute;
  top: 450px;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 8rem;
  font-weight: bold;
  color: #070608;
  text-align: center;
  z-index: 9999; /* 设置为最大值，确保在顶层 */
}
.circle {
  position: absolute;
  top: -120px; /* 从页面顶部进入 */
  border-radius: 50%;
  animation: slideDown 1s forwards;
  z-index: -10;
}
/* iframe 样式 */

.embedded-html {
  width: 100%;
  height: 100vh; /* 高度填满视口 */
  border: none;
  overflow: auto; /* 允许内部滚动 */
}
.circle-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@keyframes slideDown {
  to {
    transform: translateY(-50%);
  }
}
</style>
