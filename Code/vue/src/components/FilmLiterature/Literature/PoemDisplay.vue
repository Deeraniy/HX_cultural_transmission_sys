<template>
  <el-main>
    <div class="hunan-tourist-attractions">
      <div class="attraction-container" >
        <!-- 上方的淡红色条 -->
        <div class="scroll-bar">
          <span class="scroll-bar-text">{{ $t('hu-xiang-gu-dai-wen-xue-shi-zhong-guo-wen-xue-bao-ku-zhong-de-yi-ke-cui-can-ming-zhu-qi-lang-man-zhu-yi-qing-huai-jia-guo-qing-huai-yu-di-fang-te-se-zhi-jin-reng-zai-ying-xiang-zhuo-zhong-guo-wen-xue-de-fa-zhan-hu-xiang-wen-xue-bu-jin-shi-hu-nan-wen-hua-de-xiang-zheng-ye-wei-zhong-hua-wen-hua-de-duo-yang-xing-he-feng-fu-xing-zeng-tian-le-du-te-de-se-cai') }}</span>
        </div>

        <!-- 文字轮播（水平方向） -->
        <el-carousel height="300px" direction="horizontal" :autoplay="true" v-model:active-index="currentIndex" @change="onCarouselChange">
          <el-carousel-item v-for="(item, index) in carouselData" :key="index">
            <div :class="['carousel-text-container', { 'small-font': locale === 'en' }]"> <!-- 动态类绑定 -->
              <div class="carousel-text">
                <div class="s-title w">
                  <span>{{ item.name[locale] }}</span>
                </div>
                <div class="p">{{ item.introduction[locale] }}</div>
                <div class="ts nl2p">
                  <p>{{ $t('zuo-zhe-itemauthorlocale', [item.author[locale]]) }}</p>
                  <p>{{ $t('zhao-dai-itemdynastylocale', [item.dynasty[locale]]) }}</p>
                  <p>{{ $t('chuang-zuo-bei-jing-itembackgroundlocale', [item.background[locale]]) }}</p>
                </div>
              </div>
            </div>
          </el-carousel-item>

          <!-- 自定义上箭头 -->
          <template #prev-arrow>
            <div class="arrow prev">
              <i class="el-icon-arrow-left"></i>
            </div>
          </template>

          <!-- 自定义下箭头 -->
          <template #next-arrow>
            <div class="arrow next">
              <i class="el-icon-arrow-right"></i>
            </div>
          </template>
        </el-carousel>

      </div>
      <BookShelf :current-index="4" />
    </div>
  </el-main>
</template>

<script lang="ts" setup>
import { ref, nextTick, watch } from 'vue';
import BookShelf from "@/components/FilmLiterature/Literature/BookShelf.vue";
// 直接导入 JSON 文件
import poemData from '@/json/Poem.json';
import { useI18n } from 'vue-i18n';

const { locale } = useI18n(); // 获取当前语言
const carouselData = poemData;

const currentIndex = ref(0);

// 监听 currentIndex 的变化
watch(currentIndex, (newIndex) => {
  nextTick(() => {
    console.log("currentIndex updated to:", newIndex);
  });
});

// 轮播变化时手动更新
const onCarouselChange = (index: number) => {
  currentIndex.value = index;
  console.log("Carousel changed to index:", index);
};
</script>

<style scoped lang="scss">
@import '@/assets/font/font.css';

#app {
  height: 100vh;
  margin: 0;
}

.el-main {
  --el-main-padding: 0;
}

.hunan-tourist-attractions {
  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
  position: relative; /* 确保背景不被其他元素覆盖 */
}

.attraction-container {
  height: 400px;
  font-family: 'HelveticaNeue', serif;
  position: relative;
  display: flex; /* 使用 flex 布局 */
  flex-direction: row; /* 保证图片和文字并排显示 */
  width: 100%;
  //height: 100%; /* 保证容器占满屏幕 */
  background-image: url('@/assets/poem1.jpg');
}

.scroll-bar {
  width: 100%;
  height: 40px; /* 增加滚动条高度 */
  background-color: #B71C1C64; /* 淡红色 */
  position: absolute;
  top: 0; /* 确保它固定在容器顶部 */
  z-index: 10; /* 保证滚动条位于最上层 */
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
  font-size: 18px; /* 调整字体大小 */
  overflow: hidden; /* 超出部分隐藏 */
}

.scroll-bar-text {
  font-family: 'HelveticaNeue', serif;
  white-space: nowrap; /* 防止文本换行 */
  display: inline-block;
  padding-right: 100%; /* 保证文本宽度足够 */
  animation: scroll-text 30s linear infinite; /* 文字滚动动画 */
}

/* 滚动条的动画效果 */
@keyframes scroll-text {
  0% {
    transform: translateX(100%); /* 初始时，文本在右侧外面 */
  }
  100% {
    transform: translateX(-100%); /* 最终，文本滚动到左侧外面 */
  }
}

.carousel-text-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%; /* 保证容器填满整个轮播区域 */
}

.carousel-text {
  text-align: center;
  color: #fff;
}
/* 英文模式下，文字大小变小 */
.small-font .s-title {
  font-size: 30px;  /* 英文标题字体变小 */
}

.small-font .p {
  font-size: 28px;  /* 英文介绍文字变小 */
}

.small-font .ts {
  font-size: 20px;  /* 英文背景文字变小 */
}

.s-title {
  font-size: 40px;
  font-weight: bold;
  margin-top: 10px;
  margin-bottom: 10px;
}

.p {
  font-size: 34px;
  margin-bottom: 10px;
  margin-right: 40px;
  margin-left: 40px;
}

.ts {
  font-size: 25px;
}

/* 使用 :deep() 来深度修改 el-carousel 的水平指示器样式 */
.hunan-tourist-attractions :deep(.el-carousel__indicators--horizontal li button) {
  width: 10px;          /* 设置指示器的宽度 */
  height: 10px;         /* 设置指示器的高度 */
  border-radius: 50%;   /* 使按钮变圆 */
  background-color: #ccc; /* 设置默认颜色 */
  margin: 0 4px;        /* 上下间距 */
  transition: background-color 0.3s ease; /* 平滑过渡 */
}

/* 修改当前激活状态指示器的样式 */
.hunan-tourist-attractions :deep(.el-carousel__indicators--horizontal li.is-active button) {
  background-color: #b71c1c; /* 激活时的颜色 */
}

.el-carousel {
  margin-top: 60px;
  margin-bottom: 0px;
  width: 100%;
  height: auto;
}
</style>
