<template>
  <el-main>
    <div class="hunan-tourist-attractions">
      <div class="attraction-container">
        <!-- 上方的淡红色条 -->
        <div class="scroll-bar">
          <span class="scroll-bar-text">{{ $t('hu-xiang-wen-xue-yi-qi-feng-fu-de-wen-hua-nei-han-nong-yu-de-di-fang-feng-qing-he-xian-ming-de-jing-shen-zhui-qiu-cheng-wei-zhong-guo-wen-xue-de-zhong-yao-zu-cheng-bu-fen-ta-bu-jin-shi-hu-nan-ren-min-wen-hua-shen-fen-de-xiang-zheng-ye-shi-zhong-hua-wen-hua-duo-yang-xing-he-feng-fu-xing-de-ti-xian-hu-xiang-wen-xue-cheng-zai-zhuo-hu-xiang-wen-hua-de-you-jiu-li-shi-bing-ji-xu-ying-xiang-zhuo-dang-dai-zhong-guo-wen-xue-de-chuang-zuo-yu-fa-zhan') }}</span>
        </div>
        <!-- 图片轮播（垂直方向） -->
        <el-carousel height="400px" direction="vertical" :autoplay="false" v-model:active-index="currentIndex" @change="onCarouselChange">
          <el-carousel-item v-for="(item, index) in carouselData" :key="index">
            <div class="carousel-image-container">
              <img :src="item.image" alt="image" />
            </div>
          </el-carousel-item>
          <!-- 自定义上箭头 -->
          <template #prev-arrow>
            <div class="arrow prev">
              <i class="el-icon-arrow-up"></i>
            </div>
          </template>

          <!-- 自定义下箭头 -->
          <template #next-arrow>
            <div class="arrow next">
              <i class="el-icon-arrow-down"></i>
            </div>
          </template>
        </el-carousel>

        <!-- 右侧详情区域 -->
        <div class="location-box">
          <div class="s-title w">
            <span>{{ carouselData[currentIndex]?.title?.[locale] }}</span>
          </div>
          <div class="p">{{ carouselData[currentIndex]?.description[locale] }}</div>
          <div class="ts nl2p">
            <p>{{ $t('zhu-bian-carouseldatacurrentindexeditorlocale', [carouselData[currentIndex]?.editor?.[locale]]) }}</p>
            <p>{{ $t('shu-hao-carouseldatacurrentindexisbn', [carouselData[currentIndex]?.isbn]) }}</p>
            <p>{{ $t('chu-ban-carouseldatacurrentindexpublisherlocale', [carouselData[currentIndex]?.publisher[locale]]) }}</p>
            <p>{{ $t('ding-jia-carouseldatacurrentindexpricelocale', [carouselData[currentIndex]?.price[locale]]) }}</p>
            <p>{{ $t('ban-ci-carouseldatacurrentindexeditionlocale', [carouselData[currentIndex]?.edition[locale]]) }}</p>
            <p>{{ $t('yin-zhang-carouseldatacurrentindexprints', [carouselData[currentIndex]?.prints]) }}</p>
            <p>{{ $t('kai-ben-carouseldatacurrentindexformatlocale', [carouselData[currentIndex]?.format[locale]]) }}</p>
          </div>
        </div>

      </div>

      <BookShelf :current-index="1" />
    </div>
  </el-main>
</template>

<script lang="ts" setup>
import {computed, nextTick, onMounted, ref, watch} from 'vue';

import $ from 'jquery'

import turn from '@/utils/turn'
import BookShelf from "@/components/FilmLiterature/Literature/BookShelf.vue";
// 直接导入 JSON 文件
import bookData from '@/json/Book.json';
import { useI18n } from 'vue-i18n'; // 引入 vue-i18n
const { t, locale } = useI18n();  // 使用 vue-i18n 的 t 函数
console.log(locale.value)
console.log(bookData.title)
const carouselData = bookData

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

onMounted(() => {
  nextTick(() => {
    console.log("Mounted, currentIndex:", currentIndex.value);
  });
});
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
}

.attraction-container {
  height: 500px;
  position: relative;
  display: flex; /* 使用 flex 布局 */
  flex-direction: row; /* 保证图片和文字并排显示 */
  width: 100%;
  //height: 100%; /* 保证容器占满屏幕 */
  background-image: url('@/assets/BookB.png');
}

.attraction-container::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.2); /* 半透明白色，透明度可调 */
  z-index: -1; /* 确保覆盖层在背景图和文本下面 */
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
  animation: scroll-text 20s linear infinite; /* 文字滚动动画 */
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


.location-box {
  margin-top: 60px;
  font-family: 'HelveticaNeue', serif;
  margin-left: 40px;
  margin-right: 20px;
  width: 650px;
  height: 320px; /* 设置固定高度 */
  border-radius: 8px;

  /* 去掉背景色 */
  background-color: transparent; /* 完全透明的背景 */

  /* 去掉边框和阴影 */
  border: none; /* 去除边框 */
  box-shadow: none; /* 去除阴影 */

  /* 设置右下角背景图片 */
  //background-image: url('@/assets/水墨小人.png');
  background-position: right 10px bottom -10px; /* 向下偏移一点 */
  background-repeat: no-repeat; /* 不重复显示背景 */
  background-size: 200px 250px; /* 将背景图大小调整为 100px */

  /* 保证卡片的内容不受影响，保持完全不透明 */
  opacity: 1; /* 保证内容不透明 */
}

.carousel-image-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.carousel-image-container img {
  max-height: 100%;
  width: auto;
  object-fit: contain; /* 保证图片完整显示，避免裁剪 */
}

.pic img {
  width: 100%; /* 让图片填满容器的宽度 */
  height: 100%; /* 让图片填满容器的高度 */
  object-fit: cover; /* 保证图片不变形，填充整个容器 */
}

.s-title {
  margin-left: 10px;
  margin-top: 8px;
  font-size: 34px;
  font-weight: bold;
  color: #fff8f0;
}

.p {
  margin-left: 10px;
  font-size: 26px;
  color: #fff8f0;
  margin-top: 10px;
}

.ts {
  margin-left: 10px;
  font-size: 18px;
  color: #fff8f0;
}

/* 使用 :deep() 来深度修改 el-carousel 的垂直指示器样式 */
.hunan-tourist-attractions :deep(.el-carousel__indicators--vertical li button) {
  width: 10px;          /* 设置指示器的宽度 */
  height: 10px;         /* 设置指示器的高度 */
  border-radius: 50%;   /* 使按钮变圆 */
  background-color: #ccc; /* 设置默认颜色 */
  margin: 4px 0;        /* 上下间距 */
  transition: background-color 0.3s ease; /* 平滑过渡 */
}

/* 修改当前激活状态指示器的样式 */
.hunan-tourist-attractions :deep(.el-carousel__indicators--vertical li.is-active button) {
  background-color: #b71c1c; /* 激活时的颜色 */
}

.el-carousel {
  margin-top: 60px;
  margin-bottom: 20px;
  margin-left: 20px;
  width: 500px;
  height: auto;
}

</style>
