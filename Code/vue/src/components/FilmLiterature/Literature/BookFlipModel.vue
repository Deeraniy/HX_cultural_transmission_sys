<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <!-- 右上角关闭按钮 -->
      <button class="close-button" @click="closeModal">X</button>
      <div class="scene">
        <article class="book" @click="handlePageClick">
          <section
              v-for="(page, index) in pages"
              :key="index"
              :class="['page', { active: page.isActive, flipped: page.isFlipped }]">
            <div class="front">
              <p><img :src="page.frontImage" alt="Front Image"></p>
            </div>
            <div class="back">
              <p><img :src="page.backImage" alt="Back Image"></p>
            </div>
          </section>
        </article>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';

// 传入的 book 对象
const props = defineProps({
  book: Object
});

// 定义 emit 事件
const emit = defineEmits();

// 页面数据
const pages = ref([
  { frontImage: 'https://c-ssl.dtstatic.com/uploads/blog/201502/08/20150208220613_WYYAQ.thumb.400_0.jpeg', backImage: 'https://th.bing.com/th/id/OIP.rj8jMjV8zZgtUmZuKNhYLwHaKx?rs=1&pid=ImgDetMain', isActive: true, isFlipped: false },
  { frontImage: 'https://placeimg.com/480/640/any?3', backImage: 'https://placeimg.com/480/640/any?4', isActive: false, isFlipped: false }
]);

// 处理页面翻转
const handlePageClick = () => {
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

// 关闭模态框
const closeModal = () => {
  emit('close');
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7); /* 更透明的背景 */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* 确保模态框在最上层 */
}

.modal-content {
  position: relative;
  background-color: transparent;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 90%;
  max-height: 80%;
}

.close-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: transparent;
  color: #fff;
  border: none;
  font-size: 24px;
  cursor: pointer;
  z-index: 100;
}

.scene {
  width: 400px; /* 减小宽度 */
  height: 540px; /* 减小高度 */
  margin: 16px auto;
  perspective: 1500px; /* 提高透视效果 */
}

.book {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
}

.page {
  cursor: pointer;
  position: absolute;
  color: black;
  width: 100%;
  height: 100%;
  transition: 1.5s transform cubic-bezier(0.25, 0.8, 0.25, 1); /* 更柔滑的过渡 */
  transform-style: preserve-3d;
  transform-origin: left center;
  box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3); /* 添加阴影增加立体感 */
}

.front,
.back {
  position: absolute;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  backface-visibility: hidden;
  background-color: #f8f8f8; /* 书页背景色 */
  overflow: hidden; /* 防止图片溢出 */
}

.front img,
.back img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover; /* 确保图片填充书页区域 */
}

.back {
  transform: rotateY(180deg);
}

.page.active {
  z-index: 1;
}

.page.flipped {
  transform: rotateY(-180deg) scale(0.98); /* 增加缩放效果 */
}

.page.flipped:last-of-type {
  z-index: 1;
}
</style>
