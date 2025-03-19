<template>
      <!-- 主体内容 -->
      <Carousel/>
      <CultureIntroduction/>
      <FoodSection/>
</template>

<script setup>
import { onMounted, nextTick } from 'vue';
import Carousel from "@/components/Food/subcomponents/Carousel.vue";
import CultureIntroduction from "@/components/Food/subcomponents/CultureIntroduction.vue";
import FoodSection from "@/components/Food/subcomponents/FoodSection.vue";

// 在组件挂载时确保父组件顶栏样式正确
onMounted(() => {
  nextTick(() => {
    // 通知父组件刷新顶栏
    const event = new CustomEvent('refresh-header');
    window.dispatchEvent(event);
  });
});
</script>

<style scoped>

</style>
