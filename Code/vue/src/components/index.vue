<template>
  <el-main>
    <div style="height: 100%">
      <!-- 轮播图 -->
      <el-carousel
          v-model:active-index="activeIndex"
          :autoplay="shouldAutoplay"
          :interval="3000"
          arrow="always"
          style="height: 100%; width: 100%; position: relative;"
      >
        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; position: relative;">
          <img src="@/assets/index-back3.jpg" alt="Image 3" style="width: 100%; height: 100%; object-fit: cover;" />
          <!-- 添加蒙版和文字 -->
          <div class="carousel-overlay">
            <span class="overlay-text">湖湘文化</span>
            <span class="overlay-text">数智传播网</span>
          </div>
        </div>
        <!-- 第一个视频项 -->
        <el-carousel-item>
          <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;">
            <video
                ref="videoElement"
                :src="videoUrl"
                width="100%"
                height="100%"

                autoplay
                muted
                @ended="onVideoEnded"
                style="object-fit: cover; width: 100%; height: 100%;"
            ></video>
          </div>
        </el-carousel-item>

        <!-- 后续图片项 -->
        <el-carousel-item>
          <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;">
            <img src="@/assets/index-back.jpg" alt="Image 1" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>
        </el-carousel-item>
        <el-carousel-item>
          <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;">
            <img src="@/assets/index-back2.png" alt="Image 2" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>
        </el-carousel-item>
        <el-carousel-item>
          <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0;">
            <img src="@/assets/index-back3.jpg" alt="Image 3" style="width: 100%; height: 100%; object-fit: cover;" />
          </div>
        </el-carousel-item>
      </el-carousel>
      <div class="iframe-section" style="max-height: 1440px">
        <iframe
            src="../../static/index.html"
            width="100%"
            frameborder="0"
            scrolling="no"
            sandbox="allow-scripts allow-popups allow-forms allow-same-origin allow-top-navigation"

        ></iframe>
      </div>

      <div class="block4" style="display: flex;">
        <div class="scrolllist">
          <ul style="display: flex; list-style-type: none; padding: 0; margin: 0;">
            <li class="sHoverItem" style="margin-right: 10px;">
              <a id="myLink" target="_self" href="/#/folkcustom">
                <div class="img" style="display: flex; justify-content: center; align-items: center; position: relative;">
                  <img src="@/assets/img/i1.jpg" />
                  <div class="mask m2"></div>
                  <div class="cont" style="position: absolute; text-align: center;">
                    <img alt="" title="" class="skin_common lazyload" src="@/assets/img/图书馆.png">
                    <p>非遗博物馆</p>
                  </div>
                </div>
              </a>
            </li>
            <li class="sHoverItem" style="margin-right: 10px;">
              <a target="_blank" href="/#/placeOfInterest">
                <div class="img" style="display: flex; justify-content: center; align-items: center; position: relative;">
                  <img src="@/assets/img/i2.jpg" />
                  <div class="mask m2"></div>
                  <div class="cont" style="position: absolute; text-align: center;">
                    <img alt="" title="" class="skin_common lazyload" src="@/assets/img/视听馆.png">
                    <p>风景区</p>
                  </div>
                </div>
              </a>
            </li>
            <li class="sHoverItem" style="margin-right: 10px;">
              <a target="_blank" href="/#/red">
                <div class="img" style="display: flex; justify-content: center; align-items: center; position: relative;">
                  <img src="@/assets/img/i3.jpg" />
                  <div class="mask m2"></div>
                  <div class="cont" style="position: absolute; text-align: center;">
                    <img alt="" title="" class="skin_common lazyload" src="@/assets/img/数字文库.png">
                    <p>红色文化走廊</p>
                  </div>
                </div>
              </a>
            </li>
            <li class="sHoverItem" style="margin-right: 10px;">
              <a id="bdclick_btn3" target="_blank" href="/#/filmLiterature">
                <div class="img" style="display: flex; justify-content: center; align-items: center; position: relative;">
                  <img src="@/assets/img/i4.jpg" />
                  <div class="mask m2"></div>
                  <div class="cont" style="position: absolute; text-align: center;">
                    <img alt="" title="" class="skin_common lazyload" src="@/assets/img/全景故宫.png">
                    <p>影视文学库</p>
                  </div>
                </div>
              </a>
            </li>
            <li class="sHoverItem" style="margin-right: 10px;">
              <a id="bdclick_btn4" target="_blank" href="/#/food">
                <div class="img" style="display: flex; justify-content: center; align-items: center; position: relative;">
                  <img src="@/assets/img/i5.jpg" />
                  <div class="mask m2"></div>
                  <div class="cont" style="position: absolute; text-align: center;">
                    <img alt="" title="" class="skin_common lazyload" src="@/assets/img/V故宫.png">
                    <p>美食街</p>
                  </div>
                </div>
              </a>
            </li>
          </ul>
        </div>
      </div>




    </div>
  </el-main>

</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import IndexMain from "@/components/IndexMain.vue";
// 使用 import 语法加载视频文件
import videoFile from '@/assets/湖南形象宣传片国际版《This is Hunan》.mp4';

const activeIndex = ref(0); // 当前轮播项的索引
const videoUrl = ref(videoFile); // 将视频路径赋值给变量
const shouldAutoplay = ref(false); // 控制是否自动播放轮播图
let carouselTimer = null; // 用于存储定时器
// 视频播放结束后的回调
// 视频播放结束后的处理
const onVideoEnded = () => {
  console.log('视频播放结束');
  shouldAutoplay.value = true; // 启用轮播
  activeIndex.value = 1; // 切换到第二项
  startCarousel(); // 开始轮播
};

// 开始轮播的函数
const startCarousel = () => {
  if (carouselTimer) clearInterval(carouselTimer);

  carouselTimer = setInterval(() => {
    if (activeIndex.value === 0) {
      // 如果回到视频项，停止轮播
      clearInterval(carouselTimer);
      shouldAutoplay.value = false;
      return;
    }
    activeIndex.value = (activeIndex.value + 1) % 4;
  }, 3000);
};

// 组件卸载前清理定时器
onBeforeUnmount(() => {
  if (carouselTimer) {
    clearInterval(carouselTimer);
  }
});
// 手动切换到下一个项
// 组件挂载时初始化
const iframeRef = ref(null);

// 动态设置 iframe 高度
onMounted(() => {
  shouldAutoplay.value = false;

  // 监听 iframe 加载完成
  if (iframeRef.value) {
    iframeRef.value.onload = () => {
      try {
        // 获取 iframe 内容的实际高度
        const height = iframeRef.value.contentWindow.document.documentElement.scrollHeight;
        iframeRef.value.style.height = `1800px`;
      } catch (e) {
        console.error('设置 iframe 高度失败:', e);
      }
    };
  }
});
</script>

<style scoped>
@import '@/assets/font/font.css';
.carousel-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5); /* 半透明黑色蒙版 */
  display: flex;
  flex-direction: column; /* 改为纵向排列 */
  justify-content: center;
  align-items: center;
  z-index: 2;
}

.overlay-text {
  font-family: 'HelveticaNeue', serif;
  color: white;
  font-size: 14rem;
  font-weight: bold;
  text-align: center;
  padding: 0px;
  line-height: 1.2; /* 控制行间距 */
  display: block; /* 确保每个文本块独占一行 */
  margin-top: -30px; /* 调整上边距，使两行文字更紧凑 */
}

/* 为第一行文字添加特殊样式 */
.overlay-text:first-child {
  margin-top: -250px; /* 保持原来的上边距 */
}

html, body {
  margin: 0;
  padding: 0;
  overflow: hidden !important; /* 强制禁止滚动 */
  height: 100% !important;
  width: 100% !important;
}

* {
  -ms-overflow-style: none;  /* IE 和 Edge */
  scrollbar-width: none;  /* Firefox */
}
.main-container {
  width: 100%;
  display: flex;
  overflow: hidden; /* 禁止滚动 */
  flex-direction: column;
}
/* 覆盖 element-plus 的默认样式 */

:deep(.el-main.el-main) {
  overflow: hidden !important;
  padding: 0 !important;
  height: 100% !important;
}

/* 或者使用属性选择器增加优先级 */
:deep([class*="el-main"]) {
  overflow: hidden !important;
  padding: 0 !important;
  height: 100% !important;
}

/* 如果还不行，可以尝试使用多重选择器 */
:deep(.el-container .el-main) {
  overflow: hidden !important;
  padding: 0 !important;
  height: 100% !important;
}

/* 隐藏滚动条 */
:deep(.el-main::-webkit-scrollbar) {
  width: 8px; /* 定义滚动条宽度 */
  height: 8px;
  background-color: transparent; /* 滚动条背景颜色 */
}

:deep(.el-main::-webkit-scrollbar-thumb) {
  background-color: transparent; /* 滚动条滑块颜色 */
  border-radius: 4px; /* 滚动条滑块圆角 */
}

:deep(.el-main::-webkit-scrollbar-thumb:hover) {
  background-color: rgba(0, 0, 0, 0.2); /* 鼠标悬停时滚动条滑块颜色 */
}
/* 确保轮播图的容器填满整个屏幕 */
.el-carousel {
  position: relative;
  width: 100%;
  height: 705px !important; /* 强制应用高度 */
  margin: 0 auto;
  overflow: hidden;
}

/* 使用 :deep 强制修改 el-carousel__container 的高度 */
:deep(.el-carousel__container) {
  height: 705px !important; /* 强制设置容器的高度 */
}

/* 每个轮播项的样式 */
.el-carousel-item {
  position: relative;
  width: 100%;
  height: 100%;
  overflow: hidden; /* 确保内容溢出时不会显示 */
}

/* 确保图片和视频填充并覆盖整个容器 */
video, img {
  object-fit: cover; /* 使内容填充容器并裁剪 */
  width: 100%;
  height: 100%;
}
video {
  object-fit: cover; /* 使视频填充容器并裁剪 */
  width: 100%;
  height: 100%;
  transform: scale(1.2); /* 稍微放大视频 */
  transform-origin: center center; /* 保持视频从中心放大 */
}

.iframe-section {
  width: 100%;
  height: 2000px; /* 或其他适当的高度 */
}

iframe {
  width: 100%;
  min-height: 100%; /* 至少保持一个视口高度 */
  border: none;
  overflow: hidden; /* 禁止滚动 */
}
html, body {
  margin: 0;
  padding: 0;
  overflow: hidden !important; /* 强制禁止滚动 */
  height: 100% !important;
  width: 100% !important;
}

/* 禁用滚动条 */
::-webkit-scrollbar {
  display: none;
}

* {
  -ms-overflow-style: none;  /* IE 和 Edge */
  scrollbar-width: none;  /* Firefox */
}
.cont{
  color: white;
  max-width: 100px;
  max-height: 100px;
}
.sHoverItem:hover .cont p {
  color: purple;
}

</style>
