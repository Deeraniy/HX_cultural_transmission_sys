<script setup>
import TopNav from "@/components/Food/subcomponents/TopNav.vue";
import Footer from "@/components/Food/subcomponents/Footer.vue";
</script>
<template>
  <div class="app-layout">
    <header>
      <TopNav/>
    </header>
    <main class="content">
      <router-view></router-view>
    </main>
    <footer>
      <Footer/>
    </footer>
  </div>
</template>

<style scoped>
.app-layout {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 使布局至少占满整个视口高度 */

}

.content {
  flex: 1; /* 使主体内容占据剩余空间 */
  padding: 20px;
  background-color: #ffffff;
}
</style>
