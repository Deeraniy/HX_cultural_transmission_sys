<template>
  <el-main>
    <div class="hunan-tourist-attractions">
      <div class="attraction-container">
        <!-- 上方的淡红色条 -->
        <div class="scroll-bar">
          <span class="scroll-bar-text">{{ $t('hu-xiang-xin-mei-ti-yi-shu-zuo-wei-hu-xiang-wen-hua-yu-xian-dai-ke-ji-de-jie-he-ti-zhan-xian-le-hu-nan-di-qu-zai-dang-dai-yi-shu-ling-yu-de-chuang-xin-yu-huo-li-ta-bu-jin-shi-hu-xiang-wen-hua-de-xin-biao-da-fang-shi-ye-shi-xian-dai-yi-shu-zai-di-fang-wen-hua-zhong-de-zhong-yao-shi-jian-sui-zhuo-ji-shu-de-bu-duan-jin-bu-he-yi-shu-xing-shi-de-duo-yuan-hua-hu-xiang-xin-mei-ti-yi-shu-de-wei-lai-chong-man-le-wu-xian-de-ke-neng-xing-bi-jiang-zai-quan-qiu-yi-shu-wu-tai-shang-zhan-ju-yi-xi-zhi-di') }}</span>
        </div>
        <!-- 图片轮播（垂直方向） -->
        <el-carousel height="400px" direction="vertical" :autoplay="false" v-model:active-index="currentIndex" @change="onCarouselChange" class="carousel-right">
          <el-carousel-item v-for="(item, index) in carouselData" :key="index">
            <div class="carousel-text-container" style="margin-left: 135px;margin-top: -10px;">
              <div class="carousel-text">
                <div class="s-title w">
                  <span>{{ item.name[locale] }}</span>
                </div>
              </div>
            </div>
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
      </div>
      <BookShelf :current-index="3" />
    </div>
  </el-main>
</template>


<script lang="ts" setup>
import {computed, nextTick, onMounted, ref, watch} from 'vue';

import $ from 'jquery'

import turn from '@/utils/turn'
import BookShelf from "@/components/FilmLiterature/Literature/BookShelf.vue";
import Video1 from "@/assets/Video1.jpg"
import Video2 from "@/assets/Video2.jpg"
import Video3 from "@/assets/Video3.jpg"
// 直接导入 JSON 文件
import bookData from '@/json/Book.json';
console.log(bookData.title)
import { useI18n } from 'vue-i18n';

const { locale } = useI18n(); // 获取当前语言
const currentIndex = ref(0);
const carouselData = [
  { 
    image: Video1,
    name: { zh: '再见爱人', en: 'Goodbye Lover' }
  },
  { 
    image: Video2,
    name: { zh: '声生不息', en: 'Sound and Life' }
  },
  { 
    image: Video3,
    name: { zh: '你好星期六', en: 'Hello Saturday' }
  }
];

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
  height: 490px;
  position: relative;
  display: flex; /* 使用 flex 布局 */
  flex-direction: row; /* 保证图片和文字并排显示 */

  background-repeat: no-repeat; /* 确保背景图片不重复 */
  background-size: cover; /* 背景图按比例缩放以覆盖整个容器 */
  background-position: center; /* 背景图片居中显示 */
  background-image: url('@/assets/VideoV.jpg');
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

.carousel-right {
  width: 1000px; /* 设置轮播组件的宽度 */
  margin-right: 20px; /* 与左侧内容的间距 */
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
  margin-left: 800px;
  width: 500px;
  height: auto;
}

</style>
