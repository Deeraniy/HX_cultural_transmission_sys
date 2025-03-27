<script setup>
import router from "@/router.js";

// 设置默认使用风格字体
document.documentElement.setAttribute('data-font-style', 'styled');
</script>

<template>
  <div id="app">
    <router-view/>
  </div>
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
  --font-family-base: 'HelveticaNeue2', serif;
  --font-family-styled: 'HelveticaNeue', serif;
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
</style>
