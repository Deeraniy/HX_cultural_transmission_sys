<template>
  <div class="top">
    <div class="logo">
      <img src="@/assets/foodImg/logo2.jpg" alt="Logo" />
    </div>
    <div id="nav">
      <ul>
        <li v-for="(item, index) in navItems" :key="index">
          <!-- 使用 router-link 来实现导航 -->
          <router-link
              :to="item.link"
              class="nav-link"
              :class="{ 'active': activeLink === item.link }"
              @click="handleClick(item.link)"
          >
            {{ item.name }}
          </router-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const activeLink = ref(route.path);

const navItems = [
  { name: '首页', link: '/food' },
  { name: '传播效果分析', link: '/food/propagation' },
  { name: '美食专区', link: '/food/detail' },
];

const handleClick = (link) => {
  activeLink.value = link;
};
</script>


<style scoped>
.nav-link.active {
  color: #1e1f22; /* 点击后的字体颜色 */
}
.top {
  width: 100%;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
  background-color: #fff;
}

.logo {
  width: 210px;
  height: 100%;
  margin: auto;
}

.logo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

#nav {
  width: 655px;
  height: 50px;
  background: url("@/assets/foodImg/nav.png") no-repeat center center;
  background-size: cover;
  display: flex;
  align-items: center;
  margin: auto;
}

#nav ul {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: space-around;
  list-style: none;
  margin: 0;
  padding: 0;
}

#nav ul li {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.nav-link {
  font-family: "微软雅黑";
  font-size: 18px;
  color: #fff;
  text-decoration: none;
}

.nav-link:hover {
  color: #1e1f22;
}
</style>
