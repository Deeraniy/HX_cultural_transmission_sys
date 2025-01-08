<template>
  <div class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <!-- 右上角关闭按钮 -->
      <button class="close-button" @click="closeModal">X</button>
      <div class="scene">
        <article class="book">
          <section
              v-for="(page, index) in pages"
              :key="index"
              :class="['page', { active: page.isActive, flipped: page.isFlipped }]">
            <div class="front" @click="handlePageClick(index, 'front')">
              <!-- 第一页展示封面，后续展示书名/描述 -->
              <div v-if="index === 0">
                <img :src="book.image_url" alt="Book Cover" class="book-cover" />
              </div>
              <div v-else>
                <p>{{ page.frontText }}</p>
              </div>
            </div>
            <div class="back" @click="handlePageClick(index, 'back')">
              <div v-if="index === 0">
                <h2 class="centered-title" style="position: absolute; top: 40%; left: 35%; transform: translate(-50%, -50%);">{{ page.title }}</h2>
                <button v-if="index === 0" class="jump-button" @click="analyze">情感分析</button>

              </div>
              <div v-else>
                <p>{{ page.backText }}</p>
              </div>
            </div>
          </section>
        </article>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';
import router from "@/router.js";

// 传入的 book 对象
const props = defineProps({
  book: Object
});

// 定义 emit 事件
const emit = defineEmits();

// 分割文本逻辑
const splitText = (text, maxLength) => {
  if (text.length <= maxLength) {
    return [text, ''];
  } else {
    const frontText = text.substring(0, maxLength);
    const backText = text.substring(maxLength);
    return [frontText, backText];
  }
};

// 初始化页面数据，第一页为封面，后续页为书名和描述
const pages = ref([
  {
    frontImage: props.book.image_url,
    backImage: 'https://placeimg.com/480/640/any?4',
    title: props.book.liter_name,
    frontText: '',
    backText: '',
    isActive: true,
    isFlipped: false
  }, // 封面
  {
    frontImage: '',
    backImage: 'https://placeimg.com/480/640/any?4',
    title: '',
    frontText: '',
    backText: '',
    isActive: false,
    isFlipped: false
  }  // 书名和描述
]);

// 在初始化时分割文本
const maxTextLength = 491; // 假设每页最多显示 150 个字符
const [frontText, backText] = splitText(props.book.text, maxTextLength);
pages.value[1].frontText = frontText;
pages.value[1].backText = backText;

// 触摸事件变量
let touchStartX = 0;
let touchEndX = 0;

// 处理页面翻转
const handlePageClick = (index, side) => {
  const activePage = pages.value.find(page => page.isActive);
  if (!activePage) return; // 如果没有活动页面，返回

  const currentPageIndex = pages.value.indexOf(activePage);
  const nextPage = pages.value[currentPageIndex + 1];
  const prevPage = pages.value[currentPageIndex - 1];

  if (side === 'front') {
    // 点击正面，翻到上一页
    if (!activePage.isFlipped) {
      flipPageToBack(activePage);
    } else {
      flipPageToFront(activePage);
    }
  } else if (side === 'back') {
    // 点击背面，翻到下一页
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
  page.isFlipped = false; // 修正翻转到正面时的状态
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

// 处理点击事件：判断点击位置
const handleClick = (event) => {
  const clickX = event.clientX; // 获取点击位置的X坐标
  const screenWidth = window.innerWidth; // 获取窗口的宽度
  const isLeftHalf = clickX < screenWidth / 2; // 判断是否在左半边

  if (isLeftHalf) {
    goToPrevPage(); // 左半边点击翻到上一页
  } else {
    goToNextPage(); // 右半边点击翻到下一页
  }
};

const analyze = () => {
  // 跳转到 PlaceDetail 页面
  router.push('/placeDetail'); // 直接使用路径进行跳转
};


// 翻到下一页
const goToNextPage = () => {
  const activePage = pages.value.find(page => page.isActive);
  if (!activePage) return;

  const currentPageIndex = pages.value.indexOf(activePage);
  const nextPage = pages.value[currentPageIndex + 1];

  if (nextPage) {
    nextPage.isActive = true;
    flipPageToBack(activePage);
  }
};

// 翻到上一页
const goToPrevPage = () => {
  const activePage = pages.value.find(page => page.isActive);
  if (!activePage) return;

  const currentPageIndex = pages.value.indexOf(activePage);
  const prevPage = pages.value[currentPageIndex - 1];

  if (prevPage) {
    prevPage.isActive = true;
    flipPageToFront(activePage); // 确保翻转回正面
  }
};
</script>

<style scoped>
@import '@/assets/font/font.css';
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
.centered-title{
  font-size: 60px;
  font-family: 'HelveticaNeue', serif;
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
.jump-button {
  position: absolute;
  bottom: 20px; /* 距离底部 20px */
  left: 50%; /* 水平居中 */
  transform: translateX(-50%); /* 精确居中 */
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
  z-index: 1000; /* 确保按钮在顶部 */
}

.jump-button:hover {
  background-color: #0056b3;
}

.jump-button:focus {
  outline: none;
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
  transition: 1.5s transform;
  transform-style: preserve-3d;
  transform-origin: left center;

}

.front,
.back {
  position: absolute;
  width: 100%;
  height: 100%;
  box-sizing: border-box;
  backface-visibility: hidden;
  background-color: #fff8f0; /* 书页背景色 */
  padding: 25px; /* 增加边距 */
  overflow: hidden; /* 防止内容溢出 */
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
  transform: rotateY(-180deg);
}

.page.flipped:last-of-type {
  z-index: 1;
}

.book-cover {
  width: 100%;
  height: auto;
  max-height: 100%;
}
.centered-title {
  font-size: 60px;
  font-family: 'HelveticaNeue', serif;
  writing-mode: vertical-rl; /* 竖排文本 */
  transform: rotate(180deg); /* 如果你想调整方向，可以旋转 */
}
</style>
