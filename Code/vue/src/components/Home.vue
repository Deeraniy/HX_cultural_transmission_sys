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
.circle-container {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.circle {
  position: absolute;
  top: -120px; /* 从页面顶部进入 */
  border-radius: 50%;
  animation: slideDown 1s forwards;
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
