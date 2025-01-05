<template>
  <el-main>
    <div class="hunan-tourist-attractions">
      <div class="attraction-container">
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
            <span>{{ carouselData[currentIndex]?.title }}</span>
          </div>
          <div class="p">{{ carouselData[currentIndex]?.description }}</div>
          <div class="ts nl2p">
            <p>主编：{{ carouselData[currentIndex]?.editor }}</p>
            <p>书号：{{ carouselData[currentIndex]?.isbn }}</p>
            <p>出版：{{ carouselData[currentIndex]?.publisher }}</p>
            <p>定价：{{ carouselData[currentIndex]?.price }}</p>
            <p>版次：{{ carouselData[currentIndex]?.edition }}</p>
            <p>印张：{{ carouselData[currentIndex]?.prints }}</p>
            <p>开本：{{ carouselData[currentIndex]?.format }}</p>
          </div>
        </div>
      </div>

      <BookShelf/>
    </div>


  </el-main>
</template>

<script lang="ts" setup>
import {computed, nextTick, onMounted, ref, watch} from 'vue';

import $ from 'jquery'

import turn from '@/utils/turn'
import BookShelf from "@/components/FilmLiterature/BookShelf.vue";
// Carousel 数据
const carouselData = ref([
  {
    title: '故宫日历·2025年·汉英对照',
    description: '2025年，乙巳年，生肖蛇，适逢故宫博物院建院一百周年。汉英对照版日历通过文物展示故宫百年来的发展历程。',
    image: 'https://img.dpm.org.cn/Uploads/image/2024/12/18/出版推荐448-546汉英日历-XHuSkowdJ260.png',
    editor: '陈丽华',
    isbn: '978-7-5134-1668-9',
    publisher: '故宫出版社',
    price: '96元',
    edition: '2024年11月第1版',
    prints: '16',
    format: '48开'
  },
  {
    title: '汉代玉器研究',
    description: '汉代是玉器发展史中的繁荣时代，玉器艺术进入高峰。',
    image: 'https://img.dpm.org.cn/Uploads/image/2024/12/18/出版推荐448-546汉代玉器研究-FXpuCWAOK260.png',
    editor: '徐琳',
    isbn: '978-7-5134-1614-6',
    publisher: '故宫出版社',
    price: '236元',
    edition: '2024年9月第1版',
    prints: '34',
    format: '16开'
  },
  {
    title: '清代大运彩瓷（全二册）',
    description: '清代大运瓷器是御窑厂每年烧制并送往清宫的基本任务。',
    image: 'https://img.dpm.org.cn/Uploads/image/2024/12/18/出版推荐448-546清代大运彩瓷-QWGTJeobg260.png',
    editor: '故宫博物院',
    isbn: '978-7-5134-1653-5',
    publisher: '故宫出版社',
    price: '880元',
    edition: '2024年8月第1版',
    prints: '66.5',
    format: '12开'
  }
]);
const imageArray = carouselData.value.map(item => item.image);
console.log(imageArray);

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
// 切换上一张
const prevSlide = () => {
  if (currentIndex.value > 0) {
    currentIndex.value -= 1;
  } else {
    currentIndex.value = carouselData.value.length - 1;
  }
};

// 切换下一张
const nextSlide = () => {
  if (currentIndex.value < carouselData.value.length - 1) {
    currentIndex.value += 1;
  } else {
    currentIndex.value = 0;
  }
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
  --el-main-padding:0;

}

.hunan-tourist-attractions {

  background-size: cover;
  background-repeat: no-repeat;
  background-position: center;
}
.attraction-container {
  display: flex;
  align-items: flex-start; /* 图片和文本在一行显示 */
  justify-content: space-between;
  width: 100%;
}

.hunan-tourist-attractions {
  display: flex;
  flex-direction: column;
  align-items: center;

  min-height: 100vh;
  padding: 10px;

}



.centered-text {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}



.fancy-name {
  font-family: 'ZhuanTi', serif; /* 使用纂体字体 */
  font-size: 13px; /* 根据需要调整字体大小 */
  color: #555; /* 设置字体颜色 */
}


.image-carousel {
  width: 500px;
  height: 500px; /* 允许容器根据内容自适应高度 */
  margin-right: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}


.location-box {
  font-family: 'HelveticaNeue', serif;
  margin-top: 20px;
  margin-left: 40px;
  margin-right: 20px;
  width: 650px;
  height: 320px; /* 设置固定高度 */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  background-color: #fff;
  overflow-y: auto; /* 内容超出时显示滚动条 */

  /* 设置右下角背景图片 */
  background-image: url('@/assets/水墨小人.png');
  background-position: right 10px bottom -10px; /* 向下偏移一点 */
  background-repeat: no-repeat;     /* 不重复显示背景 */
  background-size: 200px 250px;     /* 将背景图大小调整为 100px */
  //opacity: 0.3;
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
  color: #333;
}

.p {
  margin-left: 10px;
  font-size: 26px;
  color: #666;
  margin-top: 10px;
}

.ts {
  margin-left: 10px;
  font-size: 18px;
  color: #999;
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


/* 样式修改 */
.el-carousel {
  margin-left: 20px;
  width: 500px;
  height: auto;
}

</style>
