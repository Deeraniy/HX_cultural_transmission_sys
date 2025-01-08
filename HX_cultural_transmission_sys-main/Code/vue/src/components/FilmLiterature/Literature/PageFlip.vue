<template>
  <div class="scene">
    <article class="book" @click="handlePageClick">
      <section
          v-for="(page, index) in pages"
          :key="index"
          :class="['page', { active: page.isActive, flipped: page.isFlipped }]"
      >
        <div class="front">
          <p><img :src="page.frontImage" alt="Front Image"></p>
        </div>
        <div class="back">
          <p><img :src="page.backImage" alt="Back Image"></p>
        </div>
      </section>
    </article>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const pages = ref([
  { frontImage: "https://placeimg.com/480/640/any?1", backImage: "https://placeimg.com/480/640/any?2", isActive: true, isFlipped: false },
  { frontImage: "https://placeimg.com/480/640/any?3", backImage: "https://placeimg.com/480/640/any?4", isActive: false, isFlipped: false },
  { frontImage: "https://placeimg.com/480/640/any?5", backImage: "https://placeimg.com/480/640/any?6", isActive: false, isFlipped: false },
  { frontImage: "https://placeimg.com/480/640/any?7", backImage: "https://placeimg.com/480/640/any?8", isActive: false, isFlipped: false },
  { frontImage: "https://placeimg.com/480/640/any?9", backImage: "https://placeimg.com/480/640/any?10", isActive: false, isFlipped: false }
]);

// 处理页面翻转
const handlePageClick = (event) => {
  const activePage = pages.value.find(page => page.isActive);

  if (activePage) {
    if (!activePage.isFlipped) {
      flipPageToBack(activePage);
    } else {
      flipPageToFront(activePage);
    }
  }
};

// 翻转到背面
const flipPageToBack = (page) => {
  page.isFlipped = true;
  page.isActive = false;

  const nextPage = pages.value[pages.value.indexOf(page) + 1];
  if (nextPage) {
    nextPage.isActive = true;
  }
};

// 翻转到正面
const flipPageToFront = (page) => {
  page.isFlipped = false;
  page.isActive = false;

  const prevPage = pages.value[pages.value.indexOf(page) - 1];
  if (prevPage) {
    prevPage.isActive = true;
  }
};
</script>

<style scoped>
html {
  height: 100%;
  overflow: hidden;
}
body {
  background: black;
  margin: 0;
  width: 100%;
  height: 100%;
}

.scene {
  width: 480px;
  height: 640px;
  margin: 16px auto;
  -webkit-perspective: 2000px;
  perspective: 2000px;
}

.book {
  position: relative;
  width: 100%;
  height: 100%;
  -webkit-transform-style: preserve-3d;
  transform-style: preserve-3d;
}

.page {
  cursor: pointer;
  position: absolute;
  color: black;
  width: 100%;
  height: 100%;
  -webkit-transition: 1.5s -webkit-transform;
  transition: 1.5s transform;
  -webkit-transform-style: preserve-3d;
  transform-style: preserve-3d;
  -webkit-transform-origin: left center;
  -ms-transform-origin: left center;
  transform-origin: left center;
}

.front,
.back {
  position: absolute;
  width: 100%;
  height: 100%;
  -webkit-box-sizing: border-box;
  -moz-box-sizing: border-box;
  box-sizing: border-box;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
  background: linear-gradient(to bottom right, #fff, #ccc);
}

.back {
  -webkit-transform: rotateY(180deg);
  transform: rotateY(180deg);
}

.page.active {
  z-index: 1;
}

.page.flipped {
  -webkit-transform: rotateY(-180deg);
  transform: rotateY(-180deg);
}

.page.flipped:last-of-type {
  z-index: 1;
}

p {
  margin: 0;
}
</style>
