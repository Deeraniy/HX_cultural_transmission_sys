<script setup>
import router from "@/router.js";
import { watch } from 'vue';
import { useRoute } from 'vue-router';
import BackgroundIntro from "@/components/Background/BackgroundIntro.vue";
import AboutUs from "@/components/About/AboutUs.vue";

const route = useRoute();

// 设置默认使用风格字体
document.documentElement.setAttribute('data-font-style', 'styled');

// 全局监听路由变化
watch(
  () => route.query,
  (newQuery, oldQuery) => {
    // 获取当前路由的组件名称或路径
    const currentPath = route.path;


    // 只监听 name, value, theme 这三个参数的变化
    const relevantOldQuery = {
      name: oldQuery?.name,
      value: oldQuery?.value,
      theme: oldQuery?.theme
    };

    const relevantNewQuery = {
      name: newQuery?.name,
      value: newQuery?.value,
      theme: newQuery?.theme
    };
    if(relevantNewQuery.name !== relevantOldQuery.name){
      // 只在这三个关键参数发生变化时刷新
      const hasRelevantChange = JSON.stringify(relevantNewQuery) !== JSON.stringify(relevantOldQuery);

      console.log('hasRelevantChange', hasRelevantChange);
      console.log('relevantNewQuery', relevantNewQuery);
      console.log('relevantOldQuery', relevantOldQuery);
    }

  },
  { deep: true }
);
</script>

<template>
  <div id="app">
    <router-view/>
  </div>
<!--  <background-intro/>-->
</template>

<style scoped>
#app{

}

header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>

<style>
/* 默认字体样式 */
:root {
  --font-family-base: '汇文明朝体', 'HelveticaNeue2', serif;
  --font-family-styled: '汇文明朝体', 'HelveticaNeue', serif;
}

/* 普通字体模式 */
[data-font-style="normal"] * {
  font-family: var(--font-family-base) !important;
}

/* 风格字体模式 */
[data-font-style="styled"] * {
  font-family: var(--font-family-styled) !important;
}

/* 允许特定元素保持自己的字体和大小 */
[data-font-style="styled"] [data-preserve-font],
[data-font-style="normal"] [data-preserve-font] {
  font-family: inherit !important;
  font-size: inherit !important;
}

/* 确保中文字符优先使用汇文明朝体 */
.chinese, [lang="zh"], [lang="zh-CN"] {
  font-family: '汇文明朝体', var(--font-family-styled) !important;
}
</style>
